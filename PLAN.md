# PLAN - expanding Time Card Calculator

Branch: `feature/expand-timecard-tools` (never commit/push to `main`).

## What existed (Step 1 summary)
- 53 tracked files: `generate.py` (one 570-line file with every page as inline strings),
  `assets/style.css` (4.7 KB, single 760px column), `assets/tools.js` (time card, hours-between,
  hourly-to-salary), `public/` (generated: home = weekly time card, hours calculator, timesheet,
  hourly-to-salary, one short overtime page, 35 "8am to 5pm" shift pages, about/privacy/contact,
  sitemap, robots, 404).
- Weaknesses: thin pages (shift pages are one table + 3 FAQs, no worked example), no step-by-step
  breakdown, no guides, no breadcrumbs, no BreadcrumbList schema, no disclaimer / editorial pages,
  contact page invents an e-mail address, ad slot is `display:none` when empty (no reserved height),
  overtime page cites no source for state rules, no tests.

## Architecture
- `generate.py` stays the entry point and now only orchestrates. HTML/content lives in `gen/`:
  `core.py` (layout, schema, breadcrumbs, ad slots, sources footer), `tools.py` (calculator pages),
  `guides.py`, `programmatic.py`, `pages.py` (home, hubs, trust pages).
- `assets/calc.js` = pure math (unit-tested with node), `assets/tools.js` = DOM wiring,
  `assets/style.css` = redesigned styles. Scripts are `defer`red; no images; no third-party code.
- `tests/`: `test_calc.js` (hand-worked examples), `check_links.py` (internal links/anchors/canonicals),
  `sanity.py` (page weight, blocking scripts, titles/descriptions unique, ad-slot rules).

## Pages
Calculators (18): time card (weekly/bi-weekly/semi-monthly/monthly engine, 3 entry URLs),
hours between two times (dates + overnight), overtime pay (federal + CA/AK/NV/CO presets, double time,
bonus in regular rate), time duration add/subtract, decimal hours <-> hh:mm, minutes-to-decimal chart,
paycheck estimator (IRS Pub 15-T 2026 percentage method, FICA), hourly -> salary, salary -> hourly,
PTO accrual, lunch / unpaid break deduction, shift differential, work schedule / shift planner,
military (24-hour) time converter, time rounding (5/6/15 min, DOL 7-minute rule), printable timesheet.

Guides (9, 800-1500 words, worked examples, FAQ, sources): overtime rules by state, exempt vs
non-exempt, hours worked with breaks, rounding time cards legally, filling in a paper time card,
bi-weekly vs semi-monthly pay, how to read a timesheet, meal & rest break laws by state (cited only),
time card mistakes and fixes, tracking hours for freelancers/contractors.

Programmatic (each with own worked example and prose, not number swaps):
- `/hours/<a>-to-<b>/` x35 upgraded (weekly/biweekly totals, pay at several rates, overtime scenarios)
- `/hours-per-year/<n>-hours-a-week/` (16 pages)
- `/hourly-to-annual/<n>-dollars-an-hour/` (17 pages)
- `/decimal-hours/<h>-hours-chart/` hh:mm -> decimal tables (12 pages)
- hub/index pages for each family.

Trust/SEO: About, Contact, Privacy, Disclaimer, Editorial policy, breadcrumbs, related-links blocks,
JSON-LD (WebApplication, FAQPage, BreadcrumbList, Article for guides), canonical, unique title+description,
sitemap.xml + robots.txt regenerated. Pages that state a rule carry a Sources box with link + "last checked".

Ads: empty `<aside class="ad-slot">` with fixed min-height, placed only after the calculator/first
content section; no ad script anywhere.

## Rules followed
Only free code, no .env/secrets, no deploy, no wrangler. Facts only from dol.gov / irs.gov / state
labor departments; anything not confirmed is left out and listed in NOTES.md.
