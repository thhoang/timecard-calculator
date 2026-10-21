#!/usr/bin/env python3
"""Generate the static site for Time Card Calculator into ./public/ (plain HTML, no dependencies).

Run:  python generate.py
Content lives in the gen/ package:
  gen/core.py          layout, schema, helpers, source links
  gen/forms.py         calculator markup (ids are wired up in assets/tools.js)
  gen/tools_a.py, tools_b.py   calculator pages and their long explanations
  gen/guides.py        guides
  gen/programmatic.py  shift-hour, hours-per-year, hourly-to-annual and decimal-chart pages
  gen/pages.py         home, hubs, trust pages
"""
import os
import shutil

from gen import core, tools_a, tools_b, guides, programmatic, pages, extras2  # noqa: F401 (extras2 registers more sections on import)

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "public")

# hub page -> URL prefix whose child pages it lists in its ItemList schema
HUB_PREFIX = {"/hours/": "/hours/", "/hours-per-year/": "/hours-per-year/", "/hourly-to-annual/": "/hourly-to-annual/", "/decimal-hours/": "/decimal-hours/"}


def build_pages():
    tools_a.build()
    tools_b.build()
    guides.build()
    programmatic.build()
    pages.home()
    pages.calculators_hub()
    pages.guides_hub()
    pages.trust_pages()
    pages.not_found()
    for hub, prefix in HUB_PREFIX.items():
        core.PAGES[hub].itemlist = [(core.PAGES[s].name, s) for s in core.ORDER if s.startswith(prefix) and s != hub]
        core.PAGES[hub].webpage_type = "CollectionPage"


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def main():
    os.makedirs(OUT, exist_ok=True)
    for name in os.listdir(OUT):  # clear contents but keep the folder (a dev server may be running in it)
        full = os.path.join(OUT, name)
        shutil.rmtree(full) if os.path.isdir(full) else os.remove(full)
    build_pages()
    for slug in core.ORDER:
        pg = core.PAGES[slug]
        rel = "404.html" if slug == "/404.html" else slug.strip("/") + "/index.html" if slug != "/" else "index.html"
        write(os.path.join(OUT, rel), core.layout(pg))
    urls = [s for s in core.ORDER if core.PAGES[s].in_sitemap]
    prio = {"home": "1.0", "tool": "0.9", "hub": "0.7", "guide": "0.8", "prog": "0.5", "static": "0.3"}
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sm.append("<url><loc>%s%s</loc><lastmod>%s</lastmod><priority>%s</priority></url>" % (core.BASE, u, core.CHECKED, prio.get(core.PAGES[u].kind, "0.5")))
    sm.append("</urlset>")
    write(os.path.join(OUT, "sitemap.xml"), "\n".join(sm) + "\n")
    write(os.path.join(OUT, "robots.txt"), "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % core.BASE)
    shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(OUT, "assets"))
    # Cloudflare Pages reads this file for response headers (static config, no secrets).
    write(os.path.join(OUT, "_headers"), "/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n  X-Frame-Options: SAMEORIGIN\n\n"
          "/assets/*\n  Cache-Control: public, max-age=3600, must-revalidate\n")
    print("built %d pages (%d in sitemap) into public/" % (len(core.ORDER), len(urls)))


if __name__ == "__main__":
    main()
