#!/usr/bin/env python3
"""Sanity checks on the generated site (run after generate.py): performance, SEO, schema, ads, content depth.
Run: python tests/sanity.py   (exit code 1 on any failure)"""
import json
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "public"))
MAX_HTML = 150 * 1024
MAX_ASSET_TOTAL = 120 * 1024


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = self.desc = self.canon = None
        self.h1 = 0
        self.scripts, self.ld, self.imgs, self.styles = [], [], 0, []
        self._in = None
        self._buf = ""
        self.stack, self.text_in_prose, self.ads, self.tools_seen, self.ad_before_tool = [], [], 0, False, False
        self.noindex = False
        self.words = 0
        self.prose_depth = 0
        self.ad_depth = 0
        self.ad_text = ""
        self.skip = 0
        self.faq_items = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = a.get("class", "") or ""
        if tag == "title":
            self._in = "title"
        if tag == "meta" and a.get("name") == "description":
            self.desc = a.get("content")
        if tag == "meta" and a.get("name") == "robots" and "noindex" in (a.get("content") or ""):
            self.noindex = True
        if tag == "link" and a.get("rel") == "canonical":
            self.canon = a.get("href")
        if tag == "link" and a.get("rel") == "stylesheet":
            self.styles.append(a.get("href"))
        if tag == "h1":
            self.h1 += 1
        if tag == "img":
            self.imgs += 1
        if tag == "script":
            if a.get("type") == "application/ld+json":
                self._in = "ld"
                self._buf = ""
            else:
                self.scripts.append(a)
        if tag == "section" and "data-tool" in a:
            self.tools_seen = True
        if tag == "aside" and "ad-slot" in cls:
            self.ads += 1
            self.ad_depth += 1
            if "data-tool" not in a and not self.tools_seen and self._is_tool:
                self.ad_before_tool = True
        elif self.ad_depth and tag not in ("br",):
            self.ad_depth += 1
        if tag == "details":
            self.faq_items += 1
        if tag in ("script", "style", "nav", "header", "footer"):
            self.skip += 1
        if ("prose" in cls.split()) or tag == "article":
            self.prose_depth += 1 if self.prose_depth == 0 else 0
            if self.prose_depth == 0:
                self.prose_depth = 1

    _is_tool = False

    def handle_endtag(self, tag):
        if tag in ("title",) or (tag == "script" and self._in == "ld"):
            if self._in == "ld":
                self.ld.append(self._buf)
            self._in = None
        if self.ad_depth:
            self.ad_depth -= 1
        if tag in ("script", "style", "nav", "header", "footer"):
            self.skip = max(0, self.skip - 1)

    def handle_data(self, data):
        if self._in == "title":
            self.title = (self.title or "") + data
        elif self._in == "ld":
            self._buf += data
        if self.ad_depth:
            self.ad_text += data
        if not self.skip:
            self.words += len(data.split())

    def handle_comment(self, data):
        pass


def walk():
    for dp, _, fs in os.walk(ROOT):
        for fn in fs:
            if fn.endswith(".html"):
                full = os.path.join(dp, fn)
                rel = os.path.relpath(full, ROOT).replace("\\", "/")
                url = "/" + rel[:-len("index.html")] if rel.endswith("index.html") else "/" + rel
                yield url, full


def types_of(graph):
    out = set()
    for n in graph:
        t = n.get("@type")
        out.update(t if isinstance(t, list) else [t])
    return out


def main():
    fails = []
    titles, descs = {}, {}
    n = 0
    for url, full in walk():
        n += 1
        raw = open(full, encoding="utf-8").read()
        size = len(raw.encode("utf-8"))
        if size > MAX_HTML:
            fails.append("%s: HTML is %d KB (limit %d)" % (url, size // 1024, MAX_HTML // 1024))
        ids = re.findall(r'\sid="([^"]+)"', raw)
        dup = sorted({i for i in ids if ids.count(i) > 1})
        if dup:
            fails.append("%s: duplicate ids %s" % (url, dup))
        p = P()
        p._is_tool = 'data-tool="' in raw
        p.feed(raw)
        t = (p.title or "").strip()
        if not (15 <= len(t) <= 75):
            fails.append("%s: title length %d (%r)" % (url, len(t), t))
        titles.setdefault(t, []).append(url)
        d = p.desc or ""
        if not (70 <= len(d) <= 175):
            fails.append("%s: meta description length %d" % (url, len(d)))
        descs.setdefault(d, []).append(url)
        if p.h1 != 1:
            fails.append("%s: %d h1 tags" % (url, p.h1))
        if p.imgs:
            fails.append("%s: has <img> (page should stay image-free)" % url)
        for s in p.scripts:
            if not s.get("src"):
                fails.append("%s: inline script found" % url)
            elif "defer" not in s:
                fails.append("%s: blocking script %s" % (url, s.get("src")))
            elif s["src"].startswith("http"):
                fails.append("%s: external script %s" % (url, s["src"]))
        for s in p.styles:
            if s.startswith("http"):
                fails.append("%s: external stylesheet" % url)
        if re.search(r"adsbygoogle|googlesyndication|pagead|doubleclick|gtag\(|googletagmanager", raw):
            fails.append("%s: contains ad/analytics script code" % url)
        if p.ad_before_tool:
            fails.append("%s: ad slot placed above the calculator" % url)
        if p.ad_text.strip() and p.ad_text.strip() != "Advertisement":
            pass  # ad slots only contain a comment and the CSS label
        # schema
        if not p.ld:
            fails.append("%s: no JSON-LD" % url)
        for blob in p.ld:
            try:
                data = json.loads(blob)
            except ValueError as e:
                fails.append("%s: invalid JSON-LD (%s)" % (url, e))
                continue
            ty = types_of(data["@graph"])
            if url != "/404.html" and "WebPage" not in ty and not ty & {"AboutPage", "ContactPage", "CollectionPage"}:
                fails.append("%s: no WebPage-type node" % url)
            if url != "/" and url != "/404.html" and "BreadcrumbList" not in ty:
                fails.append("%s: no BreadcrumbList" % url)
            if 'data-tool="' in raw and url != "/" and not {"WebApplication", "FAQPage"} <= ty:
                fails.append("%s: tool page missing WebApplication/FAQPage" % url)
        # content depth
        if url.startswith("/guides/") and url != "/guides/" or url == "/overtime-rules/":
            m = re.search(r'<article class="prose">(.*?)</article>', raw, re.S)
            body = re.sub(r"<[^>]+>", " ", m.group(1)) if m else ""
            wc = len(body.split())
            if wc < 800:
                fails.append("%s: guide article only %d words (min 800)" % (url, wc))
            if p.faq_items < 3:
                fails.append("%s: fewer than 3 FAQ items" % url)
        if 'data-tool="' in raw and url != "/":
            m = re.search(r'<div class="below-tool prose">(.*?)</div><section class="faq"', raw, re.S)
            body = re.sub(r"<[^>]+>", " ", m.group(1)) if m else ""
            wc = len(body.split())
            if wc < 600:
                fails.append("%s: tool explanation only %d words (min 600)" % (url, wc))
            if "class=\"example\"" not in raw:
                fails.append("%s: no worked example" % url)
            if "data-print" not in raw:
                fails.append("%s: no print button" % url)
            if 'id="' not in raw or "-steps" not in raw:
                fails.append("%s: no step-by-step breakdown container" % url)
        if p.faq_items < 3 and url not in ("/404.html",) and not re.match(r"^/(about|editorial-policy|disclaimer|privacy|contact)/$", url):
            fails.append("%s: fewer than 3 FAQ items" % url)
    for k, v in titles.items():
        if len(v) > 1:
            fails.append("duplicate title %r on %s" % (k, v))
    for k, v in descs.items():
        if len(v) > 1:
            fails.append("duplicate meta description on %s" % v)
    total = 0
    for fn in os.listdir(os.path.join(ROOT, "assets")):
        total += os.path.getsize(os.path.join(ROOT, "assets", fn))
    if total > MAX_ASSET_TOTAL:
        fails.append("assets total %d KB (limit %d KB)" % (total // 1024, MAX_ASSET_TOTAL // 1024))
    robots = open(os.path.join(ROOT, "robots.txt")).read()
    if "Sitemap:" not in robots:
        fails.append("robots.txt lacks Sitemap")
    for f in fails:
        print("FAIL", f)
    print("checked %d pages; assets %d KB; %d failures" % (n, total // 1024, len(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
