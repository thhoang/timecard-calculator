#!/usr/bin/env python3
"""Internal link checker for the generated site in ./public.
Checks: every internal href/src resolves to a file, #fragments exist, canonicals match the page URL, every sitemap
URL exists, every indexable page is in the sitemap, no orphan pages (each page is linked from at least one other page).
Run: python tests/check_links.py   (exit code 1 on any problem)"""
import os
import re
import sys
from html.parser import HTMLParser
from urllib.parse import urlsplit

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "public")
ROOT = os.path.abspath(ROOT)
BASE = "https://timecard-calculator.pages.dev"


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.ids, self.canonical = [], set(), None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag in ("link",) and a.get("rel") == "canonical":
            self.canonical = a.get("href")
        if tag == "link" and a.get("rel") == "stylesheet":
            self.links.append(a["href"])
        if tag == "script" and a.get("src"):
            self.links.append(a["src"])


def url_to_file(path):
    path = path.split("?")[0]
    f = os.path.join(ROOT, path.lstrip("/"))
    if path.endswith("/"):
        return os.path.join(f, "index.html")
    if os.path.isfile(f):
        return f
    return None


def main():
    pages = {}
    for dp, _, fs in os.walk(ROOT):
        for fn in fs:
            if fn.endswith(".html"):
                full = os.path.join(dp, fn)
                rel = os.path.relpath(full, ROOT).replace("\\", "/")
                url = "/" + rel[:-len("index.html")] if rel.endswith("index.html") else "/" + rel
                p = P()
                p.feed(open(full, encoding="utf-8").read())
                pages[url] = p
    errors, inbound = [], {u: 0 for u in pages}
    for url, p in pages.items():
        want = BASE + url
        if p.canonical != want:
            errors.append("%s: canonical %s != %s" % (url, p.canonical, want))
        for h in p.links:
            if h.startswith(("mailto:", "tel:", "data:", "javascript:")):
                continue
            sp = urlsplit(h)
            if sp.scheme in ("http", "https"):
                if h.startswith(BASE):
                    sp = urlsplit(h[len(BASE):])
                else:
                    continue
            path = sp.path or url
            if not path.startswith("/"):
                errors.append("%s: relative link %s (use root-relative)" % (url, h))
                continue
            f = url_to_file(path)
            if not f or not os.path.isfile(f):
                errors.append("%s: broken link %s" % (url, h))
                continue
            target = "/" + os.path.relpath(f, ROOT).replace("\\", "/")
            target = target[:-len("index.html")] if target.endswith("index.html") else target
            if target != url and target in inbound:
                inbound[target] += 1
            if sp.fragment and f.endswith(".html"):
                tp = pages.get(target)
                if tp is not None and sp.fragment not in tp.ids:
                    errors.append("%s: missing anchor #%s in %s" % (url, sp.fragment, target))
    sm = open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()
    locs = re.findall(r"<loc>([^<]+)</loc>", sm)
    for loc in locs:
        u = loc[len(BASE):]
        if u not in pages:
            errors.append("sitemap lists missing page %s" % u)
    for u in pages:
        if u != "/404.html" and BASE + u not in locs:
            errors.append("page not in sitemap: %s" % u)
    for u, n in inbound.items():
        if u != "/404.html" and n == 0:
            errors.append("orphan page (no inbound links): %s" % u)
    for e in errors:
        print("ERROR", e)
    print("checked %d pages, %d problems" % (len(pages), len(errors)))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
