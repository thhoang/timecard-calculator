# Time Card Calculator

Free, fast, plain-HTML work-hours tools: weekly time card calculator with breaks
and overtime, hours-between-times calculator, printable weekly timesheet (save as
PDF), hourly-to-salary converter, and quick-answer pages for common shifts.

- No framework, no dependencies, no build step for the site itself
- `generate.py` writes the static site into `public/` (run: `python3 generate.py`)
- All calculators run client-side; entries stay in the visitor's browser
- Deployed as static files on Cloudflare Pages

## Structure
- `generate.py` - page generator (all HTML lives here as templates)
- `assets/style.css`, `assets/tools.js` - shared styles and calculator logic
- `public/` - generated static site (upload this to hosting)
