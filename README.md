# Time Card Calculator

Free, fast, client-side work-hours tools plus plain-English guides, generated as a static site
(no framework, no runtime dependencies). 121 pages: 18 calculators, 10 guides, shift-hour /
hours-per-year / hourly-to-annual / decimal-chart quick-answer pages, trust pages, sitemap and robots.

- Every calculator runs in the browser; nothing a visitor types is sent anywhere.
- Rules (overtime, breaks, tax withholding) are stated only where an official source (U.S. DOL, IRS,
  state labor agency) is linked on the page, with a "last checked" date. Open questions are in `NOTES.md`.
- Ads: empty, fixed-height `<aside class="ad-slot">` containers below the fold. No ad or analytics code.
- Hosted as static files (Cloudflare Pages). Output folder: `public/`.

## Build and preview
```
python generate.py            # regenerates public/ (Python 3, standard library only)
cd public
python -m http.server 8000    # then open http://localhost:8000
```
(On Windows PowerShell run the commands on separate lines; do not chain them with `&&`.)

## Tests (all free, no installs)
```
node tests/test_calc.js       # calculator math vs hand-worked examples (104 assertions)
python tests/check_links.py   # internal links, #anchors, canonicals, sitemap, orphan pages
python tests/sanity.py        # titles/descriptions unique, JSON-LD, no blocking/external scripts,
                              #   no images, no ad code, ad slots below the calculator, word counts
python tests/ui_smoke.py      # drives 20 calculator cases in headless Edge/Chrome (skips if none installed)
```

## Layout
| Path | Purpose |
| --- | --- |
| `generate.py` | entry point: builds all pages, sitemap, robots.txt, `_headers` |
| `gen/core.py` | layout, JSON-LD, breadcrumbs, ad slots, source links (`SRC`), `BASE` URL, `CHECKED` date |
| `gen/forms.py` | calculator markup (ids are wired up in `assets/tools.js`) |
| `gen/tools_a.py`, `gen/tools_b.py` | calculator pages and their long explanations |
| `gen/extras.py`, `gen/extras2.py` | additional explanatory sections appended by slug |
| `gen/guides.py` | the guides |
| `gen/programmatic.py` | data-driven page families (shifts, hours per year, hourly rates, decimal charts) |
| `gen/pages.py` | home, hubs, About / Contact / Privacy / Disclaimer / Editorial policy / 404 |
| `assets/calc.js` | pure calculation functions (also run by node in the tests) |
| `assets/tools.js` | DOM wiring for each calculator; `assets/style.css` styles |
| `public/` | generated site (committed so it can be uploaded as-is) |

## Maintaining
- **Update the date** after re-checking sources: change `CHECKED` / `CHECKED_LONG` in `gen/core.py`.
- **Tax tables** (`TAX2026` in `assets/calc.js`, `_SINGLE` in `gen/programmatic.py`, text in `gen/tools_b.py`)
  must be updated every year from IRS Publication 15-T and Publication 15.
- **Domain:** if the site moves from `timecard-calculator.pages.dev`, change `BASE` in `gen/core.py`.
- **Adding a calculator:** add markup in `gen/forms.py`, logic in `assets/calc.js` (+ a test) and an init
  function in `assets/tools.js`, then a page in `gen/tools_*.py` with `tool_page(...)`.
