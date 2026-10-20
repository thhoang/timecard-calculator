#!/usr/bin/env python3
"""Generate the static site for Time Card Calculator.
Plain HTML output, no build dependencies. Run: python3 generate.py
Output lands in ./public/ (upload that folder to any static host)."""
import os, shutil, json, datetime

BASE = "https://timecard-calculator.pages.dev"
SITE = "Time Card Calculator"
TAGLINE = "Free time card, work hours and timesheet tools"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")
TODAY = datetime.date.today().isoformat()

NAV = [
    ("/", "Time Card"),
    ("/hours-calculator/", "Hours Calculator"),
    ("/timesheet/", "Timesheet PDF"),
    ("/hourly-to-salary/", "Hourly to Salary"),
    ("/overtime-rules/", "Overtime Rules"),
]

def nav_html(active):
    return "\n".join(
        '<a href="{href}"{cls}>{label}</a>'.format(
            href=h, label=l, cls=' class="active"' if h == active else "")
        for h, l in NAV)

def layout(slug, title, desc, body, active="/", schema=None, canonical=None):
    canon = canonical or (BASE + slug)
    schema_html = ""
    if schema:
        schema_html = '<script type="application/ld+json">' + json.dumps(schema, separators=(",", ":")) + "</script>"
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canon}">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><circle cx='50' cy='50' r='45' fill='%230b5fff'/><path d='M50 25v25l18 10' stroke='white' stroke-width='8' fill='none' stroke-linecap='round'/></svg>">
<link rel="stylesheet" href="/assets/style.css">
{schema_html}
</head>
<body>
<header class="site-header"><div class="container">
<a class="brand" href="/">Time Card <span>Calculator</span></a>
<nav class="site-nav" aria-label="Main">
{nav}
</nav>
</div></header>
<main><div class="container">
{body}
</div></main>
<footer class="site-footer"><div class="container">
<nav aria-label="Footer">
<a href="/about/">About</a>
<a href="/privacy/">Privacy</a>
<a href="/contact/">Contact</a>
<a href="/hours/">Shift hours index</a>
</nav>
<div class="copyright">&copy; <span id="year">2026</span> {site}. Free tools, no sign-up. Results are estimates, not payroll advice.</div>
</div></footer>
<script src="/assets/tools.js"></script>
</body>
</html>
""".format(title=title, desc=desc, canon=canon, nav=nav_html(active), body=body, site=SITE, schema_html=schema_html)

def faq_schema(qa):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qa]}

def webapp_schema(name, desc, slug):
    return {"@context": "https://schema.org", "@type": "WebApplication", "name": name,
            "url": BASE + slug, "applicationCategory": "BusinessApplication",
            "operatingSystem": "Any", "browserRequirements": "Requires JavaScript",
            "description": desc, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}

AD = '<div class="ad-slot" data-ad-slot="reserved"><!-- reserved ad slot: paste AdSense unit here after approval --></div>'

def faq_html(qa):
    return "\n".join("<details><summary>{}</summary><p>{}</p></details>".format(q, a) for q, a in qa)

# ---------------------------------------------------------------- index
def page_index():
    rows = "\n".join(
        '<tr><th scope="row">{d}</th>'
        '<td><input class="in" type="text" inputmode="numeric" placeholder="8:00" aria-label="{d} clock in"></td>'
        '<td><input class="out" type="text" inputmode="numeric" placeholder="17:00" aria-label="{d} clock out"></td>'
        '<td><input class="brk" type="number" min="0" step="5" placeholder="30" aria-label="{d} break minutes"></td>'
        '<td class="day-total" aria-live="polite"></td></tr>'.format(d=d)
        for d in ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])
    qa = [
        ("How do I calculate my work hours for the week?",
         "Enter your clock-in and clock-out times for each day, plus unpaid break minutes. The calculator subtracts breaks, adds up the week, and splits regular and overtime hours using the rule you choose."),
        ("What overtime rule should I use?",
         "Most US workers use the federal rule: overtime starts after 40 hours in a workweek, paid at 1.5 times the regular rate. California, Alaska, Nevada and Colorado also have daily overtime rules - pick 'Daily 8h + weekly 40h' if your state has a daily threshold. Check our overtime rules guide for details."),
        ("Does it work for night shifts?",
         "Yes. If your clock-out time is earlier than your clock-in time, the shift counts as running past midnight into the next day."),
        ("Is my timesheet stored anywhere?",
         "Only in your own browser (local storage). Nothing is sent to a server, and clearing your browser data removes it. Use the Print button to save a PDF copy."),
    ]
    body = """
<h1>Free Time Card Calculator with Breaks &amp; Overtime</h1>
<p>Add your clock-in and clock-out times for the week. The calculator totals your hours,
subtracts unpaid breaks, and splits regular and overtime pay. Everything runs in your browser -
no sign-up, nothing uploaded.</p>
<div class="card" id="timecard-app">
  <div class="grid3 no-print">
    <div class="field"><label for="emp-name">Name (optional)</label><input id="emp-name" type="text" placeholder="Jane Doe"></div>
    <div class="field"><label for="emp-company">Company (optional)</label><input id="emp-company" type="text" placeholder="Acme Inc"></div>
    <div class="field"><label for="week-start">Week starting</label><input id="week-start" type="date"></div>
  </div>
  <p class="print-only">Time card - <span id="pp-name"></span></p>
  <div class="table-wrap"><table>
    <thead><tr><th>Day</th><th>Clock in</th><th>Clock out</th><th>Break (min)</th><th>Hours</th></tr></thead>
    <tbody id="tc-body">""" + rows + """</tbody>
  </table></div>
  <div class="grid3 no-print">
    <div class="field"><label for="ot-rule">Overtime rule</label>
      <select id="ot-rule">
        <option value="weekly40">Weekly: over 40 h (federal)</option>
        <option value="daily8">Daily 8 h + weekly 40 h (CA-style)</option>
        <option value="none">No overtime</option>
      </select></div>
    <div class="field"><label for="round">Round each day to</label>
      <select id="round">
        <option value="0">No rounding</option>
        <option value="5">Nearest 5 min</option>
        <option value="10">Nearest 10 min</option>
        <option value="15">Nearest 15 min</option>
      </select></div>
    <div class="field"><label for="ot-mult">Overtime multiplier</label>
      <select id="ot-mult">
        <option value="1.5">1.5x (time and a half)</option>
        <option value="2">2x (double time)</option>
      </select></div>
  </div>
  <div class="field no-print" style="max-width:220px"><label for="rate">Hourly rate (optional, for pay)</label>
    <input id="rate" type="number" min="0" step="0.01" placeholder="18.50"></div>
  <div class="results" aria-live="polite">
    <div class="row"><span>Total hours</span><b id="r-total">0:00</b></div>
    <div class="row"><span>Regular hours</span><b id="r-regular">0:00</b></div>
    <div class="row"><span>Overtime hours</span><b id="r-ot">0:00</b></div>
    <div class="row grand" id="r-pay-row" style="display:none"><span>Estimated pay</span><b id="r-pay"></b></div>
    <p><small id="r-pay-note"></small></p>
  </div>
  <div class="btn-row no-print">
    <button id="tc-print" type="button">Print / save as PDF</button>
    <button id="tc-clear" type="button" class="ghost">Clear week</button>
  </div>
</div>
""" + AD + """
<h2>How to use this time card calculator</h2>
<ul class="tight">
<li>Type times the way you think of them: <code>8</code>, <code>8am</code>, <code>8:30</code> or <code>17:30</code> all work.</li>
<li>Enter unpaid breaks in minutes (a 30-minute lunch = <code>30</code>).</li>
<li>Night shift past midnight? Enter the actual times - the calculator handles the date change.</li>
<li>Add your hourly rate to see estimated pay with overtime at time-and-a-half or double time.</li>
<li>Print or save the filled time card as a PDF for your records or your manager.</li>
</ul>
<h2>Common questions</h2>
""" + faq_html(qa) + """
<h2>More free work-hours tools</h2>
<ul>
<li><a href="/hours-calculator/">Hours calculator</a> - hours between any two times, with breaks.</li>
<li><a href="/timesheet/">Printable weekly timesheet</a> - fill in and print a clean timesheet PDF.</li>
<li><a href="/hourly-to-salary/">Hourly to salary converter</a> - see what your rate adds up to per year.</li>
<li><a href="/hours/">Shift hours index</a> - quick answers like "8am to 5pm is how many hours".</li>
</ul>
"""
    schema = {"@context": "https://schema.org", "@graph": [
        webapp_schema("Time Card Calculator", "Free weekly time card calculator with breaks and overtime. Totals work hours and estimates pay in the browser.", "/"),
        faq_schema(qa)]}
    return layout("/", "Time Card Calculator - Free Weekly Work Hours & Overtime",
        "Free time card calculator: enter clock in/out times and breaks, get total hours, regular and overtime split, and estimated pay. Print or save as PDF. No sign-up.",
        body, active="/", schema=schema)

# ---------------------------------------------------------------- hours calculator
def page_hours():
    qa = [
        ("How do you calculate hours between two times?",
         "Subtract the start time from the end time. If the end is earlier than the start (a night shift), add 24 hours first. Then subtract any unpaid break."),
        ("Is 8am to 5pm 8 or 9 hours?",
         "It is 9 hours clock to clock. If you take an unpaid one-hour lunch, you work 8 paid hours."),
        ("Can I use this for night shifts?",
         "Yes. A shift from 10pm to 6am is counted as 8 hours - the calculator assumes the end is the next morning when the end time is earlier than the start."),
    ]
    body = """
<h1>Hours Calculator - Hours Between Two Times</h1>
<p>Enter a start and end time to get the hours between them, with an optional unpaid break.
Perfect for "how many hours did I work?" questions.</p>
<div class="card" id="hb-app">
  <div class="grid3">
    <div class="field"><label for="hb-in">Start time</label><input id="hb-in" type="text" inputmode="numeric" placeholder="8:00 am"></div>
    <div class="field"><label for="hb-out">End time</label><input id="hb-out" type="text" inputmode="numeric" placeholder="5:00 pm"></div>
    <div class="field"><label for="hb-break">Unpaid break (min)</label><input id="hb-break" type="number" min="0" step="5" placeholder="30"></div>
  </div>
  <div class="answer-box" id="hb-result" style="display:none">
    <div class="big"><span id="hb-hm"></span></div>
    <div>= <b id="hb-dec"></b> (<span id="hb-gross"></span>)</div>
    <div class="muted" id="hb-week"></div>
  </div>
</div>
""" + AD + """
<h2>Tips</h2>
<ul class="tight">
<li>Accepts <code>9</code>, <code>9am</code>, <code>9:30</code>, <code>21:30</code> - whatever is natural to you.</li>
<li>End time earlier than start time means the shift runs past midnight.</li>
<li>Looking for a whole week? Use the <a href="/">time card calculator</a> instead.</li>
<li>Common shifts answered instantly: <a href="/hours/">see the shift hours index</a>.</li>
</ul>
<h2>Common questions</h2>
""" + faq_html(qa)
    schema = {"@context": "https://schema.org", "@graph": [
        webapp_schema("Hours Calculator", "Calculate hours between two times with an optional unpaid break.", "/hours-calculator/"),
        faq_schema(qa)]}
    return layout("/hours-calculator/", "Hours Calculator - Hours Between Two Times (With Break)",
        "Calculate hours between a start and end time, minus an unpaid break. Handles overnight shifts. Shows hours:minutes and decimal hours.",
        body, active="/hours-calculator/", schema=schema)

# ---------------------------------------------------------------- printable timesheet
def page_timesheet():
    qa = [
        ("Can I save this timesheet as a PDF?",
         "Yes. Fill it in, press Print / save as PDF, and choose 'Save as PDF' as the printer in your browser. You get a clean one-page timesheet."),
        ("Is this timesheet accepted by employers?",
         "It has the standard fields (name, week, daily in/out, breaks, totals, signature lines). Most small businesses accept a printed timesheet like this, but check what your employer or payroll provider requires."),
    ]
    body = """
<h1>Printable Weekly Timesheet Generator</h1>
<p>Fill in the fields below, then print or save a clean timesheet as PDF. The printed version
drops the buttons and menus - just the timesheet, totals and signature lines.</p>
<div class="card" id="ts-app">
  <div id="timecard-app">
  <p class="print-only">Weekly timesheet - <span id="pp-name"></span></p>
  <div class="grid3 no-print">
    <div class="field"><label for="emp-name">Employee name</label><input id="emp-name" type="text" placeholder="Jane Doe"></div>
    <div class="field"><label for="emp-company">Company</label><input id="emp-company" type="text" placeholder="Acme Inc"></div>
    <div class="field"><label for="week-start" id="ts-week-label">Week starting</label><input id="week-start" type="date"></div>
  </div>
  <div class="table-wrap"><table>
    <thead><tr><th>Day</th><th>Clock in</th><th>Clock out</th><th>Break (min)</th><th>Hours</th></tr></thead>
    <tbody id="tc-body">""" + "\n".join(
        '<tr><th scope="row">{d}</th>'
        '<td><input class="in" type="text" placeholder="8:00" aria-label="{d} in"></td>'
        '<td><input class="out" type="text" placeholder="17:00" aria-label="{d} out"></td>'
        '<td><input class="brk" type="number" min="0" step="5" placeholder="30" aria-label="{d} break"></td>'
        '<td class="day-total"></td></tr>'.format(d=d)
        for d in ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]) + """</tbody>
  </table></div>
  <div class="grid3 no-print">
    <div class="field"><label for="ot-rule">Overtime rule</label>
      <select id="ot-rule">
        <option value="weekly40">Weekly: over 40 h (federal)</option>
        <option value="daily8">Daily 8 h + weekly 40 h (CA-style)</option>
        <option value="none">No overtime</option>
      </select></div>
    <div class="field"><label for="round">Round each day to</label>
      <select id="round"><option value="0">No rounding</option><option value="5">5 min</option><option value="10">10 min</option><option value="15">15 min</option></select></div>
    <div class="field"><label for="rate">Hourly rate (optional)</label><input id="rate" type="number" min="0" step="0.01" placeholder="18.50"></div>
  </div>
  <input id="ot-mult" type="hidden" value="1.5">
  <div class="results" aria-live="polite">
    <div class="row"><span>Total hours</span><b id="r-total">0:00</b></div>
    <div class="row"><span>Regular hours</span><b id="r-regular">0:00</b></div>
    <div class="row"><span>Overtime hours</span><b id="r-ot">0:00</b></div>
    <div class="row grand" id="r-pay-row" style="display:none"><span>Estimated pay</span><b id="r-pay"></b></div>
    <p><small id="r-pay-note"></small></p>
  </div>
  </div>
  <div class="print-only">
    <p>Employee signature: ________________________&nbsp;&nbsp;&nbsp;Date: ____________</p>
    <p>Supervisor signature: ______________________&nbsp;&nbsp;&nbsp;Date: ____________</p>
  </div>
  <div class="btn-row no-print">
    <button id="tc-print" type="button">Print / save as PDF</button>
    <button id="tc-clear" type="button" class="ghost">Clear</button>
  </div>
</div>
""" + AD + """
<h2>Tips for a clean printout</h2>
<ul class="tight">
<li>Use your browser's print dialog and pick "Save as PDF" to email the timesheet.</li>
<li>The header, buttons and this text disappear on the printed copy - only the timesheet prints.</li>
<li>Your entries stay in this browser, so you can come back and adjust before printing.</li>
</ul>
<h2>Common questions</h2>
""" + faq_html(qa)
    schema = {"@context": "https://schema.org", "@graph": [
        webapp_schema("Printable Weekly Timesheet", "Fill in a weekly timesheet online and print or save it as a PDF, with totals and signature lines.", "/timesheet/"),
        faq_schema(qa)]}
    return layout("/timesheet/", "Printable Weekly Timesheet - Fill In & Save as PDF",
        "Free printable weekly timesheet: enter clock times and breaks, get totals, then print or save as PDF. Signature lines included. No sign-up.",
        body, active="/timesheet/", schema=schema)

# ---------------------------------------------------------------- hourly to salary
def page_salary():
    qa = [
        ("How do you convert hourly pay to an annual salary?",
         "Multiply your hourly rate by the hours you work per week, then by the weeks you work per year. At 40 hours and 52 weeks, $20/hour is $41,600 per year before taxes."),
        ("Is $25 an hour a good salary?",
         "$25/hour at 40 hours a week is about $52,000 a year before taxes - roughly $4,333 a month or $1,000 a week. Whether that is 'good' depends on your location and household costs."),
        ("Does this include taxes?",
         "No. These are gross (before tax) numbers. Your take-home pay depends on your state, filing status and benefits deductions."),
    ]
    body = """
<h1>Hourly to Salary Converter</h1>
<p>See what an hourly rate adds up to per year, month, week and day. Adjust hours per week
and weeks per year for part-time or seasonal work.</p>
<div class="card" id="hs-app">
  <div class="grid3">
    <div class="field"><label for="hs-hourly">Hourly rate ($)</label><input id="hs-hourly" type="number" min="0" step="0.01" placeholder="20"></div>
    <div class="field"><label for="hs-hpw">Hours per week</label><input id="hs-hpw" type="number" min="1" max="80" step="1" value="40"></div>
    <div class="field"><label for="hs-wpy">Weeks per year</label><input id="hs-wpy" type="number" min="1" max="52" step="1" value="52"></div>
  </div>
  <div class="answer-box" id="hs-result" style="display:none">
    <div class="big" id="hs-annual"></div>
    <div><span id="hs-monthly"></span> &middot; <span id="hs-weekly"></span> &middot; <span id="hs-daily"></span></div>
    <div class="muted">Gross pay before taxes and deductions.</div>
  </div>
</div>
""" + AD + """
<h2>Quick reference: common hourly rates at 40 h/week</h2>
<div class="table-wrap"><table>
<thead><tr><th>Hourly</th><th>Weekly</th><th>Monthly</th><th>Yearly</th></tr></thead>
<tbody>
""" + "\n".join("<tr><td>${r:.2f}</td><td>${w:,.0f}</td><td>${m:,.0f}</td><td>${y:,.0f}</td></tr>".format(
        r=r, w=r*40, m=r*40*52/12, y=r*40*52)
        for r in [15, 17, 18.50, 20, 22, 25, 28, 30, 35, 40, 50]) + """
</tbody></table></div>
<h2>Common questions</h2>
""" + faq_html(qa)
    schema = {"@context": "https://schema.org", "@graph": [
        webapp_schema("Hourly to Salary Converter", "Convert an hourly wage to annual, monthly, weekly and daily pay.", "/hourly-to-salary/"),
        faq_schema(qa)]}
    return layout("/hourly-to-salary/", "Hourly to Salary Converter - What Your Rate Pays Per Year",
        "Convert hourly pay to yearly salary: enter your rate, hours per week and weeks per year. See annual, monthly, weekly and daily gross pay.",
        body, active="/hourly-to-salary/", schema=schema)

# ---------------------------------------------------------------- overtime rules guide
def page_overtime():
    body = """
<h1>Overtime Rules: Federal 40-Hour Rule and State Daily Overtime</h1>
<p>This guide explains the overtime rules the <a href="/">time card calculator</a> can apply,
in plain language. It is general information, not legal advice - when in doubt, check your
state labor department.</p>
<h2>The federal baseline (FLSA)</h2>
<p>Under the Fair Labor Standards Act, non-exempt employees earn overtime at
<b>1.5 times their regular rate</b> for all hours worked over <b>40 in a workweek</b>.
A workweek is any fixed 7-day period your employer sets - it does not have to start on Monday.
Federal law has <b>no daily overtime</b>: working a 10-hour day is not overtime unless the week
goes past 40 hours.</p>
<h2>States with daily overtime rules</h2>
<div class="table-wrap"><table>
<thead><tr><th>State</th><th>Daily overtime rule</th></tr></thead>
<tbody>
<tr><td>California</td><td>1.5x over 8 h/day; 2x over 12 h/day; 1.5x for the first 8 h on the 7th consecutive workday in a workweek, 2x beyond 8 h that day.</td></tr>
<tr><td>Alaska</td><td>1.5x over 8 h/day (employers with 4+ employees), plus the 40 h weekly rule.</td></tr>
<tr><td>Nevada</td><td>1.5x over 8 h/day for employees paid less than 1.5x the state minimum wage; higher-paid staff follow the 40 h weekly rule.</td></tr>
<tr><td>Colorado</td><td>1.5x over 12 h/day, plus the 40 h weekly rule.</td></tr>
<tr><td>Oregon</td><td>Daily overtime (over 10 h) applies to mill, factory and manufacturing workers only.</td></tr>
</tbody></table></div>
<p>Everywhere else, the federal 40-hour weekly rule is the only rule for most workers.
A few states (like Minnesota) set the weekly line at 48 hours instead of 40 for some employers.</p>
<h2>Which rule should I pick in the calculator?</h2>
<ul class="tight">
<li><b>Weekly: over 40 h</b> - correct for most US workers in most states.</li>
<li><b>Daily 8 h + weekly 40 h</b> - closest fit for California and Alaska-style rules. Daily overtime hours are not double-counted toward the weekly threshold.</li>
<li><b>No overtime</b> - for salaried/exempt tracking, or when you only need total hours.</li>
</ul>
<h2>Who is "non-exempt"?</h2>
<p>Most hourly workers are non-exempt and get overtime. Exempt employees (many salaried
executive, administrative, professional and computer roles above a salary threshold) do not.
Job title alone does not decide - duties and pay level do. The
<a href="https://www.dol.gov/agencies/whd/overtime" rel="noopener">US Department of Labor overtime page</a>
has the current salary thresholds.</p>
""" + AD
    return layout("/overtime-rules/", "Overtime Rules by State: 40-Hour Week & Daily Overtime Explained",
        "Federal overtime starts after 40 hours a week at 1.5x pay. California, Alaska, Nevada and Colorado add daily overtime. Plain-language guide with a state table.",
        body, active="/overtime-rules/")

# ---------------------------------------------------------------- programmatic shift pages
def fmt_ampm(h24):
    ap = "am" if h24 < 12 else "pm"
    h = h24 % 12 or 12
    return "%d%s" % (h, ap)

def shift_page(start, end):
    s, e = fmt_ampm(start), fmt_ampm(end)
    slug = "/hours/%s-to-%s/" % (s, e)
    gross = end - start
    net30 = gross - 0.5
    net60 = gross - 1
    breaks = [(0, gross), (15, gross - 0.25), (30, gross - 0.5), (45, gross - 0.75), (60, gross - 1)]
    def dec(h): return ("%g" % round(h, 2))
    table_rows = "\n".join(
        "<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (
            ("%d minutes" % b) if b else "No break", dec(n) + " hours", dec(n * 5) + " hours")
        for b, n in breaks)
    qa = [
        ("Is %s to %s %s hours?" % (s, e, dec(gross)),
         "Yes, %s to %s is %s hours clock to clock. Your paid working time is less if you take an unpaid break - with a 30-minute lunch it is %s hours." % (s, e, dec(gross), dec(net30))),
        ("How many hours a week is %s to %s, Monday to Friday?" % (s, e),
         "Five days of %s to %s is %s hours clock to clock, or %s paid hours with a 30-minute unpaid lunch each day." % (s, e, dec(gross * 5), dec(net30 * 5))),
        ("Is lunch included in %s to %s?" % (s, e),
         "Usually not. In most US workplaces an unpaid meal break (commonly 30 or 60 minutes) comes out of the span, so %s to %s with a one-hour lunch is %s paid hours. Paid rest breaks do count as work time." % (s, e, dec(net60))),
    ]
    prev_end = end - 1 if end - 1 > start else None
    next_end = end + 1 if end + 1 <= 20 else None
    siblings = []
    if prev_end: siblings.append('<a href="/hours/%s-to-%s/">%s to %s</a>' % (s, fmt_ampm(prev_end), s, fmt_ampm(prev_end)))
    if next_end: siblings.append('<a href="/hours/%s-to-%s/">%s to %s</a>' % (s, fmt_ampm(next_end), s, fmt_ampm(next_end)))
    for st in (start - 1, start + 1):
        if 5 <= st < end and st != start:
            siblings.append('<a href="/hours/%s-to-%s/">%s to %s</a>' % (fmt_ampm(st), e, fmt_ampm(st), e))
    body = """
<h1>%s to %s Is How Many Hours?</h1>
<div class="answer-box">
<div class="big">%s hours</div>
<div>%s to %s is %s hours clock to clock (%s:00 to %s:00).</div>
<div>With a 30-minute unpaid lunch: <b>%s working hours</b>.</div>
</div>
<p>Need the exact math for your own times, breaks or overnight shifts?
Use the <a href="/hours-calculator/?in=%sam&amp;out=%spm">hours calculator</a>.</p>
<h2>%s to %s with different break lengths</h2>
<div class="table-wrap"><table>
<thead><tr><th>Unpaid break</th><th>Paid hours per day</th><th>Per week (5 days)</th></tr></thead>
<tbody>%s</tbody></table></div>
<h2>Common questions</h2>
%s
<h2>Nearby shifts</h2>
<p>%s</p>
""" % (s, e, dec(gross), s, e, dec(gross), start, end, dec(net30),
       start, end - 12 if end > 12 else end, s, e, table_rows, faq_html(qa), " &middot; ".join(siblings))
    title = "%s to %s Is How Many Hours? (%s h, or %s h With Lunch)" % (s.upper(), e.upper(), dec(gross), dec(net30))
    desc = "%s to %s is %s hours clock to clock, or %s working hours with a 30-minute lunch. Weekly totals and break table inside." % (s, e, dec(gross), dec(net30))
    return slug, layout(slug, title, desc, body, active="", schema=faq_schema(qa))

def page_hours_index(shifts):
    items = "\n".join('<li><a href="{slug}">{s} to {e} is how many hours?</a></li>'.format(
        slug="/hours/%s-to-%s/" % (fmt_ampm(a), fmt_ampm(b)), s=fmt_ampm(a), e=fmt_ampm(b))
        for a, b in shifts)
    body = """
<h1>Shift Hours Index - Quick Answers</h1>
<p>"9 to 5" is the famous one, but shifts start and end all over the clock. Pick yours for an
instant answer with break and weekly totals, or use the
<a href="/hours-calculator/">hours calculator</a> for any times.</p>
<ul class="list-plain">
%s
</ul>
""" % items
    return layout("/hours/", "Shift Hours Index - How Many Hours Between Common Shift Times",
        "Quick answers to how many hours are between common shift times: 8am to 5pm, 9am to 5pm, 7am to 3pm and more, with break and weekly totals.",
        body, active="/hours-calculator/")

# ---------------------------------------------------------------- static pages
def page_about():
    body = """
<h1>About</h1>
<p>%s is a small, free tool site for people who track work hours: shift workers, freelancers,
and small business owners who need a quick, honest time card.</p>
<p>The tools run entirely in your browser. There are no accounts, nothing to install, and your
timesheet data never leaves your device.</p>
<h2>What we build</h2>
<ul class="tight">
<li>A weekly time card calculator with breaks, overtime rules and pay estimates.</li>
<li>An hours-between-times calculator for quick answers.</li>
<li>A printable weekly timesheet you can save as a PDF.</li>
<li>An hourly-to-salary converter.</li>
</ul>
<p>The site is supported by advertising, which keeps the tools free.</p>
""" % SITE
    return layout("/about/", "About - " + SITE,
        "About Time Card Calculator: free, private, browser-based work-hours tools.", body, active="")

def page_privacy():
    body = """
<h1>Privacy Policy</h1>
<p><small>Last updated: %s</small></p>
<p>%s is designed to collect as little as possible.</p>
<h2>Your timesheet data</h2>
<p>Times you enter are stored only in your own browser's local storage so the form keeps your
entries between visits. This data is never sent to our servers - the calculators run entirely
on your device. Clearing your browser data deletes it.</p>
<h2>Cookies and advertising</h2>
<p>We plan to show ads through third-party networks such as Google AdSense. If enabled, those
networks may use cookies or similar technologies to serve ads based on your visits. You can
control personalized advertising in your
<a href="https://adssettings.google.com/" rel="noopener">Google ad settings</a>.</p>
<h2>Analytics</h2>
<p>If we add privacy-friendly analytics, it will count page visits in aggregate. We do not build
individual profiles.</p>
<h2>Contact</h2>
<p>Questions about this policy? See the <a href="/contact/">contact page</a>.</p>
""" % (TODAY, SITE)
    return layout("/privacy/", "Privacy Policy - " + SITE,
        "Privacy policy: timesheet data stays in your browser, no accounts, minimal data collection.", body, active="")

def page_contact():
    body = """
<h1>Contact</h1>
<p>Found a bug in a calculator, want a new tool, or spotted an error in a guide? We would like
to hear it.</p>
<p>Email: <b>hello@timecard-calculator.pages.dev</b></p>
<p>Please do not send timesheets with personal employee data - remember the tools run locally,
so we never see what you type, and you do not need to send it to us.</p>
"""
    return layout("/contact/", "Contact - " + SITE,
        "Contact the Time Card Calculator team about bugs, tool requests or corrections.", body, active="")

def page_404():
    body = """
<h1>Page not found</h1>
<p>That page does not exist. Try one of the tools:</p>
<ul>
<li><a href="/">Time card calculator</a></li>
<li><a href="/hours-calculator/">Hours calculator</a></li>
<li><a href="/timesheet/">Printable timesheet</a></li>
<li><a href="/hours/">Shift hours index</a></li>
</ul>
"""
    return layout("/404.html", "Page not found - " + SITE, "Page not found.", body, active="", canonical=BASE + "/404.html")

# ---------------------------------------------------------------- build
def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    pages = {
        "index.html": page_index(),
        "hours-calculator/index.html": page_hours(),
        "timesheet/index.html": page_timesheet(),
        "hourly-to-salary/index.html": page_salary(),
        "overtime-rules/index.html": page_overtime(),
        "about/index.html": page_about(),
        "privacy/index.html": page_privacy(),
        "contact/index.html": page_contact(),
        "404.html": page_404(),
    }
    shifts = [(a, b) for a in range(6, 11) for b in range(14, 21) if b > a]
    for a, b in shifts:
        slug, html = shift_page(a, b)
        pages[slug.strip("/") + "/index.html"] = html
    pages["hours/index.html"] = page_hours_index(shifts)
    for rel, html in pages.items():
        path = os.path.join(OUT, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(html)
    # sitemap
    urls = ["/", "/hours-calculator/", "/timesheet/", "/hourly-to-salary/", "/overtime-rules/",
            "/hours/", "/about/", "/privacy/", "/contact/"]
    urls += ["/hours/%s-to-%s/" % (fmt_ampm(a), fmt_ampm(b)) for a, b in shifts]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sm.append("<url><loc>%s%s</loc><lastmod>%s</lastmod></url>" % (BASE, u, TODAY))
    sm.append("</urlset>")
    with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
        f.write("\n".join(sm))
    with open(os.path.join(OUT, "robots.txt"), "w") as f:
        f.write("User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % BASE)
    shutil.copytree(os.path.join(os.path.dirname(OUT), "assets"), os.path.join(OUT, "assets"))
    print("built %d pages + sitemap (%d urls) into public/" % (len(pages), len(urls)))

if __name__ == "__main__":
    main()
