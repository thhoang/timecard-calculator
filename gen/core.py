"""Shared building blocks: site constants, page registry, layout, schema, helpers."""
import html
import json
import re

BASE = "https://timecard-calculator.pages.dev"
SITE = "Time Card Calculator"
# The date the cited official sources were last read. Shown on pages and used for sitemap lastmod.
CHECKED = "2026-10-21"
CHECKED_LONG = "October 21, 2026"
REPO_ISSUES = "https://github.com/thhoang/timecard-calculator/issues"

# Official sources reused across pages: key -> (label, url)
SRC = {
    "dol23": ("U.S. Department of Labor, Fact Sheet #23: Overtime Pay Requirements of the FLSA", "https://www.dol.gov/agencies/whd/fact-sheets/23-flsa-overtime-pay"),
    "cfr516_2": ("29 CFR 516.2 - Employees subject to minimum wage or minimum wage and overtime provisions (required records)", "https://www.law.cornell.edu/cfr/text/29/516.2"),
    "cfr778_106": ("29 CFR 778.106 - Time of payment (overtime)", "https://www.law.cornell.edu/cfr/text/29/778.106"),
    "dol56a": ("U.S. Department of Labor, Fact Sheet #56A: Regular Rate of Pay under the FLSA", "https://www.dol.gov/agencies/whd/fact-sheets/56a-regular-rate"),
    "dol17a": ("U.S. Department of Labor, Fact Sheet #17A: Exemption for Executive, Administrative, Professional, and Computer Employees", "https://www.dol.gov/agencies/whd/fact-sheets/17a-overtime"),
    "cfr785_18": ("29 CFR 785.18 - Rest periods", "https://www.law.cornell.edu/cfr/text/29/785.18"),
    "cfr785_19": ("29 CFR 785.19 - Meal", "https://www.law.cornell.edu/cfr/text/29/785.19"),
    "cfr785_48": ("29 CFR 785.48 - Rounding practice (paragraph b)", "https://www.law.cornell.edu/cfr/text/29/785.48"),
    "dol_meal": ("U.S. Department of Labor, Wage and Hour Division: State meal period and rest break requirements (table, last revised January 1, 2023)", "https://www.dol.gov/agencies/whd/state/meal-breaks"),
    "dol_payday": ("U.S. Department of Labor, Wage and Hour Division: State payday requirements (table, last revised January 1, 2023)", "https://www.dol.gov/agencies/whd/state/payday"),
    "ca_ot": ("California Department of Industrial Relations (DLSE): Overtime", "https://www.dir.ca.gov/dlse/faq_overtime.htm"),
    "ak_ot": ("Alaska Department of Labor: Wage and Hour (AS 23.10.060, overtime)", "https://labor.alaska.gov/lss/forms/pam100.pdf"),
    "nv_ot": ("Nevada Office of the Labor Commissioner: Advisory Opinion AO-2025-05, daily or weekly overtime (NRS 608.018)", "https://labor.nv.gov/uploadedFiles/labornvgov/content/Employer/AO-2025-05%20Daily%20Overtime%20or%20Weekly%20Overtime.pdf"),
    "co_ot": ("Colorado Department of Labor and Employment: COMPS Order, Rule 4 (overtime)", "https://cdle.colorado.gov/sites/cdle/files/Adopted%20COMPS%20Order%20%2339%207%20CCR%201103-1%20%5Baccessible%5D.pdf"),
    "irs15": ("IRS Publication 15 (2026), Employer's Tax Guide", "https://www.irs.gov/publications/p15"),
    "irs15t": ("IRS Publication 15-T (2026), Federal Income Tax Withholding Methods", "https://www.irs.gov/publications/p15t"),
}

PAGES = {}          # slug -> Page
ORDER = []          # insertion order of slugs


class Page:
    def __init__(self, slug, title, desc, body, kind="static", crumbs=None, schema=None, in_sitemap=True,
                 name=None, lead_name=None):
        self.slug, self.title, self.desc, self.body = slug, title, desc, body
        self.kind, self.crumbs, self.schema, self.in_sitemap = kind, crumbs or [], schema or [], in_sitemap
        self.name = name or title
        self.related = []
        self.webpage_type = "WebPage"
        self.itemlist = []


def register(page):
    if page.slug in PAGES:
        raise ValueError("duplicate slug " + page.slug)
    PAGES[page.slug] = page
    ORDER.append(page.slug)
    return page


def esc(s):
    return html.escape(s, quote=True)


def plain(s):
    """Strip tags for JSON-LD text."""
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s))).strip()


# ---------------------------------------------------------------- navigation
NAV = [
    ("/calculators/", "Calculators"),
    ("/guides/", "Guides"),
    ("/hours/", "Shift Hours"),
    ("/hourly-to-annual/", "Pay Tables"),
    ("/about/", "About"),
]


def nav_html(slug):
    out = []
    for href, label in NAV:
        active = slug.startswith(href) or (href == "/calculators/" and PAGES.get(slug) is not None and PAGES[slug].kind == "tool")
        out.append('<a href="%s"%s>%s</a>' % (href, ' class="active"' if active else "", label))
    return "\n".join(out)


FOOT_TOOLS = [("/time-card-calculator/", "Time card calculator"), ("/overtime-calculator/", "Overtime calculator"),
              ("/hours-calculator/", "Hours calculator"), ("/paycheck-calculator/", "Paycheck estimator"),
              ("/hourly-to-salary/", "Hourly to salary"), ("/timesheet/", "Printable timesheet")]
FOOT_GUIDES = [("/overtime-rules/", "Overtime rules by state"), ("/guides/exempt-vs-non-exempt/", "Exempt vs non-exempt"),
               ("/guides/meal-and-rest-break-laws/", "Meal and rest breaks"), ("/guides/rounding-time-cards/", "Rounding time cards"),
               ("/guides/bi-weekly-vs-semi-monthly-pay/", "Bi-weekly vs semi-monthly")]
FOOT_SITE = [("/about/", "About"), ("/editorial-policy/", "Editorial policy"), ("/disclaimer/", "Disclaimer"),
             ("/privacy/", "Privacy"), ("/contact/", "Contact")]


def _ul(items):
    return "<ul>" + "".join('<li><a href="%s">%s</a></li>' % i for i in items) + "</ul>"


# ---------------------------------------------------------------- blocks
def ad(slot_id, short=False):
    return ('<aside class="ad-slot%s" data-ad-slot="%s" aria-label="Advertisement" role="complementary">'
            '<!-- EMPTY AD SLOT %s: fixed height reserved, no ad code installed. Add the ad unit here after approval. -->'
            '</aside>') % (" ad-short" if short else "", slot_id, slot_id)


def faq_html(qa):
    return '<section class="faq" aria-labelledby="faq-h"><h2 id="faq-h">Frequently asked questions</h2>' + "\n".join(
        "<details><summary>%s</summary><p>%s</p></details>" % (q, a) for q, a in qa) + "</section>"


def sources_html(keys, extra=None, note=None):
    items = [SRC[k] for k in keys] + list(extra or [])
    if not items:
        return ""
    lis = "".join('<li><a href="%s" rel="noopener">%s</a></li>' % (u, esc(l)) for l, u in items)
    return ('<section class="sources" aria-labelledby="src-h"><h2 id="src-h">Sources and last checked</h2><ul>%s</ul>'
            '<p class="updated">Last checked: <time datetime="%s">%s</time>. %s'
            'Rules change; confirm with the linked agency before relying on a figure. This is general information, not legal or payroll advice - see our <a href="/disclaimer/">disclaimer</a>.</p></section>'
            ) % (lis, CHECKED, CHECKED_LONG, (note + " ") if note else "")


def related_html(slugs, title="Related tools and guides"):
    tiles = []
    for s in slugs:
        p = PAGES.get(s)
        if p:
            tiles.append('<a class="tile" href="%s"><b>%s</b><span>%s</span></a>' % (s, esc(p.name), esc(p.desc.split(". ")[0].rstrip(".") + ".")))
    if not tiles:
        return ""
    return '<section class="related"><h2>%s</h2><div class="card-grid">%s</div></section>' % (title, "".join(tiles))


def side_html(slugs):
    lis = ""
    for s in slugs:
        p = PAGES.get(s)
        if p:
            lis += '<li><a href="%s">%s</a></li>' % (s, esc(p.name))
    box = ""
    if lis:
        box = '<div class="side-box"><h2>Related</h2><ul>%s</ul></div>' % lis
    box += ('<div class="side-box"><h2>Private by design</h2><p style="margin:0;font-size:.92rem">Everything on this page is calculated '
            'in your browser. Nothing you type is sent to us.</p></div>')
    return '<aside class="side no-print" aria-label="Related pages">%s</aside>' % box


def crumbs_html(trail):
    """trail: list of (href, label); last item is the current page (no link needed)."""
    lis = []
    for i, (h, l) in enumerate(trail):
        if i == len(trail) - 1:
            lis.append('<li aria-current="page">%s</li>' % esc(l))
        else:
            lis.append('<li><a href="%s">%s</a></li>' % (h, esc(l)))
    return '<nav class="crumbs no-print" aria-label="Breadcrumb"><ol>%s</ol></nav>' % "".join(lis)


# ---------------------------------------------------------------- form helpers
def inp(id_, label, typ="text", hint="", cls="", **attrs):
    a = "".join(' %s="%s"' % (k.replace("_", "-"), esc(str(v))) for k, v in attrs.items())
    h = '<div class="hint">%s</div>' % hint if hint else ""
    return '<div class="field %s"><label for="%s">%s</label><input id="%s" type="%s"%s>%s</div>' % (cls, id_, label, id_, typ, a, h)


def sel(id_, label, options, hint="", cls=""):
    """options: list of (value, text) or (value, text, selected)"""
    o = "".join('<option value="%s"%s>%s</option>' % (x[0], " selected" if len(x) > 2 and x[2] else "", x[1]) for x in options)
    h = '<div class="hint">%s</div>' % hint if hint else ""
    return '<div class="field %s"><label for="%s">%s</label><select id="%s">%s</select>%s</div>' % (cls, id_, label, id_, o, h)


def check(id_, label, checked=False):
    return '<div class="field"><label class="check"><input id="%s" type="checkbox"%s> <span>%s</span></label></div>' % (id_, " checked" if checked else "", label)


def result_block(prefix, title="Result"):
    """Standard result area: hero answer, stats, step-by-step breakdown, buttons."""
    return ('<div class="answer-box" id="%(p)s-answer" aria-live="polite" hidden>'
            '<div class="big" id="%(p)s-big"></div><div id="%(p)s-sub"></div></div>'
            '<p class="empty-state" id="%(p)s-empty">Enter your numbers above and the result appears here.</p>'
            '<div id="%(p)s-extra"></div>'
            '<div class="breakdown" id="%(p)s-bd" hidden><h3>How this was calculated</h3><ol class="steps" id="%(p)s-steps"></ol></div>'
            '<div class="btn-row no-print"><button type="button" data-print>Print this result</button>'
            '<button type="button" class="ghost" data-reset>Reset</button></div>') % {"p": prefix}


# ---------------------------------------------------------------- layout
def layout(page):
    page.body = page.body.replace("{{RELATED}}", related_html(page.related)).replace("{{SIDE}}", side_html(page.related))
    canon = BASE + page.slug if page.slug != "/404.html" else BASE + "/404.html"
    graph = [
        {"@type": "WebSite", "@id": BASE + "/#website", "url": BASE + "/", "name": SITE, "inLanguage": "en-US",
         "description": "Free time card, work hours, overtime and pay calculators", "publisher": {"@id": BASE + "/#org"}},
        {"@type": "Organization", "@id": BASE + "/#org", "name": SITE, "url": BASE + "/"},
    ] + list(page.schema)
    wp = {"@type": page.webpage_type, "@id": canon + "#webpage", "url": canon, "name": page.title, "description": page.desc,
          "inLanguage": "en-US", "dateModified": CHECKED, "isPartOf": {"@id": BASE + "/#website"}}
    if page.crumbs and len(page.crumbs) > 1:
        wp["breadcrumb"] = {"@id": canon + "#breadcrumb"}
    graph.append(wp)
    if page.itemlist:
        graph.append({"@type": "ItemList", "name": page.name, "numberOfItems": len(page.itemlist),
                      "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "url": BASE + u} for i, (n, u) in enumerate(page.itemlist)]})
    if page.crumbs and len(page.crumbs) > 1:
        graph.append({"@type": "BreadcrumbList", "@id": canon + "#breadcrumb", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": l, "item": BASE + h}
            for i, (h, l) in enumerate(page.crumbs)]})
    schema_html = ""
    if graph:
        schema_html = '<script type="application/ld+json">%s</script>' % json.dumps(
            {"@context": "https://schema.org", "@graph": graph}, separators=(",", ":"), ensure_ascii=False).replace("</", "<\\/")
    robots = '' if page.in_sitemap else '<meta name="robots" content="noindex">'
    return """<!DOCTYPE html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
{robots}
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{site}">
<meta property="og:locale" content="en_US">
<meta property="og:url" content="{canon}">
<meta name="twitter:card" content="summary">
<meta name="theme-color" content="#0c1b33">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><circle cx='50' cy='50' r='45' fill='%230a58d6'/><path d='M50 25v25l18 10' stroke='white' stroke-width='8' fill='none' stroke-linecap='round'/></svg>">
<link rel="stylesheet" href="/assets/style.css">
{schema_html}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header"><div class="container">
<a class="brand" href="/"><span class="brand-mark" aria-hidden="true"></span>Time Card <span>Calculator</span></a>
<nav class="site-nav" aria-label="Main">
{nav}
</nav>
</div></header>
<main id="main"><div class="container">
{body}
</div></main>
<footer class="site-footer"><div class="container">
<div class="foot-grid">
<div><h2>{site}</h2><p style="margin:0">Free, private work-hours calculators and plain-English guides. Results are estimates, not legal or payroll advice.</p></div>
<div><h2>Calculators</h2>{ft}</div>
<div><h2>Guides</h2>{fg}</div>
<div><h2>Site</h2>{fs}</div>
</div>
<div class="copyright">&copy; 2026 {site}. Calculators run in your browser; your entries are not sent anywhere. Official-source rules were last checked {checked}.</div>
</div></footer>
{scripts}
</body>
</html>
""".format(title=esc(page.title), desc=esc(page.desc), canon=canon, robots=robots, schema_html=schema_html,
           nav=nav_html(page.slug), body=page.body, site=SITE, ft=_ul(FOOT_TOOLS), fg=_ul(FOOT_GUIDES),
           fs=_ul(FOOT_SITE), checked=CHECKED_LONG,
           og_type="article" if page.kind in ("guide", "prog") else "website",
           scripts=('<script src="/assets/calc.js" defer></script>\n<script src="/assets/tools.js" defer></script>' if 'data-tool="' in page.body else ""))


# ---------------------------------------------------------------- page templates
def tool_page(slug, name, title, desc, h1, lead, tool, sections, qa, sources=(), related=(), crumbs=None,
              app_name=None, extra_sources=None, source_note=None):
    """Calculator page. sections: list of HTML strings (the long explanation). Ad slot goes after the 2nd section."""
    from .extras import EXTRA
    sections = list(sections) + EXTRA.get(slug, [])
    trail = crumbs or [("/", "Home"), ("/calculators/", "Calculators"), (slug, name)]
    parts = []
    for i, s in enumerate(sections):
        parts.append(s)
        if i == 1:
            parts.append(ad("in-content-1"))
    if len(sections) < 2:
        parts.append(ad("in-content-1"))
    body = ('{crumbs}<div class="page-head"><h1>{h1}</h1><p class="lead">{lead}</p></div>'
            '<div class="layout"><div class="main-col">{tool}<div class="below-tool prose">{article}</div>'
            '{faq}{src}{ad2}{rel}</div>{side}</div>').format(
        crumbs=crumbs_html(trail), h1=h1, lead=lead, tool=tool, article="\n".join(parts), faq=faq_html(qa),
        src=sources_html(sources, extra_sources, source_note), ad2=ad("in-content-2", short=True),
        rel="{{RELATED}}", side="{{SIDE}}")
    schema = [
        {"@type": "WebApplication", "name": app_name or name, "url": BASE + slug, "applicationCategory": "BusinessApplication",
         "operatingSystem": "Any", "browserRequirements": "Requires JavaScript", "description": desc,
         "inLanguage": "en-US", "isAccessibleForFree": True, "publisher": {"@id": BASE + "/#org"},
         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": plain(q), "acceptedAnswer": {"@type": "Answer", "text": plain(a)}} for q, a in qa]},
    ]
    pg = register(Page(slug, title, desc, body, "tool", trail, schema, name=name))
    pg.related = list(related)
    return pg


def article_page(slug, name, title, desc, h1, lead, sections, qa, sources=(), related=(), crumbs=None, kind="guide",
                 extra_sources=None, source_note=None, schema_type="Article", ad_ok=True):
    from .extras import EXTRA
    sections = list(sections) + EXTRA.get(slug, [])
    trail = crumbs or [("/", "Home"), ("/guides/", "Guides"), (slug, name)]
    parts = []
    for i, s in enumerate(sections):
        parts.append(s)
        if i == 1 and ad_ok:
            parts.append(ad("in-content-1"))
    body = ('{crumbs}<div class="page-head"><h1>{h1}</h1><p class="article-meta">Updated <time datetime="{c}">{cl}</time> &middot; {ml} &middot; <a href="/editorial-policy/">How we write</a></p>'
            '<p class="lead">{lead}</p></div><div class="layout"><div class="main-col"><article class="prose">{article}</article>'
            '{faq}{src}{ad2}{rel}</div>{side}</div>').format(
        crumbs=crumbs_html(trail), h1=h1, c=CHECKED, cl=CHECKED_LONG, ml={"guide": "Plain-English guide", "prog": "Quick-answer page", "hub": "Index"}.get(kind, "Guide"), lead=lead, article="\n".join(parts), faq=faq_html(qa) if qa else "",
        src=sources_html(sources, extra_sources, source_note), ad2=ad("in-content-2", short=True) if ad_ok else "",
        rel="{{RELATED}}", side="{{SIDE}}")
    schema = []
    if kind not in ("static", "hub"):
        schema.append({"@type": schema_type, "headline": plain(h1), "description": desc, "url": BASE + slug,
                       "dateModified": CHECKED, "datePublished": CHECKED, "inLanguage": "en-US",
                       "author": {"@id": BASE + "/#org"}, "publisher": {"@id": BASE + "/#org"},
                       "mainEntityOfPage": {"@id": BASE + slug + "#webpage"}})
    if qa:
        schema.append({"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": plain(q), "acceptedAnswer": {"@type": "Answer", "text": plain(a)}} for q, a in qa]})
    pg = register(Page(slug, title, desc, body, kind, trail, schema, name=name))
    pg.related = list(related)
    return pg


def table(headers, rows, cls="", num_from=1, hl=None):
    """headers: list[str]; rows: list[list[str]]; numeric columns right-aligned from index num_from."""
    th = "".join('<th scope="col"%s>%s</th>' % (' class="num"' if i >= num_from else "", h) for i, h in enumerate(headers))
    out = []
    for ri, r in enumerate(rows):
        tds = "".join(
            ('<th scope="row">%s</th>' % c) if i == 0 else ('<td%s>%s</td>' % (' class="num"' if i >= num_from else "", c))
            for i, c in enumerate(r))
        out.append('<tr%s>%s</tr>' % (' class="hl"' if hl is not None and ri == hl else "", tds))
    return '<div class="table-wrap"><table class="%s"><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % (cls, th, "".join(out))


def example(title, inner):
    return '<div class="example"><h3>%s</h3>%s</div>' % (title, inner)


def money(n, d=2):
    return "${:,.{d}f}".format(n, d=d)


def dec(x, d=2):
    s = ("%." + str(d) + "f") % x
    s = s.rstrip("0").rstrip(".") if "." in s else s
    return s
