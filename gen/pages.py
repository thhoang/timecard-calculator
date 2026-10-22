"""Home, hub and trust pages."""
from .core import (Page, register, PAGES, BASE, SITE, CHECKED, CHECKED_LONG, REPO_ISSUES, faq_html, crumbs_html, ad, plain, table,
                   article_page, side_html, related_html, esc)
from .tools_a import S
from . import forms

TOOL_GROUPS = [
    ("Time cards and hours", [
        "/time-card-calculator/", "/bi-weekly-time-card-calculator/", "/semi-monthly-time-card-calculator/", "/hours-calculator/",
        "/timesheet/", "/time-duration-calculator/", "/lunch-break-calculator/", "/work-schedule-planner/"]),
    ("Overtime and pay", [
        "/overtime-calculator/", "/shift-differential-calculator/", "/paycheck-calculator/", "/hourly-to-salary/", "/salary-to-hourly/", "/pto-accrual-calculator/"]),
    ("Converters and rounding", [
        "/decimal-hours-converter/", "/minutes-to-decimal-chart/", "/time-rounding-calculator/", "/military-time-converter/"]),
]
GUIDES = ["/overtime-rules/", "/guides/exempt-vs-non-exempt/", "/guides/how-to-calculate-hours-worked-with-breaks/", "/guides/rounding-time-cards/",
          "/guides/how-to-fill-in-a-paper-time-card/", "/guides/bi-weekly-vs-semi-monthly-pay/", "/guides/how-to-read-a-timesheet/",
          "/guides/meal-and-rest-break-laws/", "/guides/time-card-mistakes-and-how-to-fix-them/", "/guides/tracking-hours-for-freelancers-and-contractors/"]


def tile(slug, tag=None):
    p = PAGES[slug]
    first = p.desc.split(". ")[0].rstrip(".") + "."
    return '<a class="tile" href="%s">%s<b>%s</b><span>%s</span></a>' % (slug, ('<span class="tag">%s</span>' % tag) if tag else "", esc(p.name), esc(first))


def home():
    qa = [
        ("How do I calculate my work hours?", "Subtract your clock-in time from your clock-out time and subtract any unpaid break. Our time card calculator does this for every day in a week, bi-weekly or semi-monthly period, and shows each step."),
        ("Is my data private?", "Yes. Every calculator runs in your browser. The times and rates you enter are not sent to any server. A time card you fill in is saved only in your own browser's local storage, and you can clear it with the Reset button."),
        ("Are these calculators free?", "Yes, with no sign-up. The site is built to be supported by advertising later, but the tools will stay free."),
        ("Where do your overtime and break rules come from?", "From the U.S. Department of Labor, the IRS and state labor departments. Each page that states a rule links to its source and shows the date we last checked it. Where we could not confirm a rule from an official source, we left it out."),
        ("Can I use this to run payroll?", "No. These are calculators for estimates and for checking your own numbers. Payroll has legal requirements this site does not cover. See the disclaimer."),
    ]
    quick = forms.hours_between("Quick answer: hours between two times", dates=False, small=True)
    hero = ('<section class="hero"><h1>Work hours, time cards and overtime - worked out step by step</h1>'
            '<p>Free calculators for time cards, overtime, pay and schedules, with every step shown and plain-English guides based on official US sources. No sign-up, nothing uploaded.</p>'
            '<div class="pill-row"><a class="pill" href="/time-card-calculator/">Time card calculator</a><a class="pill" href="/overtime-calculator/">Overtime calculator</a>'
            '<a class="pill" href="/hours-calculator/">Hours calculator</a><a class="pill" href="/paycheck-calculator/">Paycheck estimator</a><a class="pill" href="/timesheet/">Printable timesheet</a></div>'
            '<div class="trust-row"><span>Runs in your browser</span><span>Sources and check dates on every rule</span><span>Print or save as PDF</span></div></section>')
    groups = ""
    for title, slugs in TOOL_GROUPS:
        groups += '<div class="section-title"><h2>%s</h2></div><div class="card-grid">%s</div>' % (title, "".join(tile(s) for s in slugs))
    gtiles = "".join(tile(s, "Guide") for s in GUIDES[:6])
    quick_ans = ('<div class="section-title"><h2>Quick answers</h2></div><div class="chips">'
                 '<a class="chip" href="/hours/8am-to-5pm/">8am to 5pm is how many hours?</a><a class="chip" href="/hours/9am-to-5pm/">9am to 5pm</a><a class="chip" href="/hours/7am-to-3pm/">7am to 3pm</a>'
                 '<a class="chip" href="/hours-per-year/40-hours-a-week/">40 hours a week in a year</a><a class="chip" href="/hourly-to-annual/20-dollars-an-hour/">$20 an hour is how much a year</a>'
                 '<a class="chip" href="/hourly-to-annual/15-dollars-an-hour/">$15 an hour a year</a><a class="chip" href="/decimal-hours/8-hours-chart/">8 hours in decimal</a><a class="chip" href="/hours/">All shift hours</a></div>')
    why = S("Why this site is different", """
<p>Most time card calculators give a number and nothing else. Here you can see <i>how</i> the number was reached: each calculator lists the steps (minutes between times, unpaid breaks, regular versus overtime hours, pay) so you can check it against a pay stub, learn the method, or spot a mistake.</p>
<ul>
<li><b>Real-life inputs.</b> Overnight shifts, date-crossing spans, unpaid meals, bi-weekly and semi-monthly pay periods, workweek start days, bonuses in the regular rate, state overtime presets.</li>
<li><b>Worked examples and long explanations</b> under every tool, written in plain English.</li>
<li><b>Sources, not guesses.</b> Overtime, break and tax rules link to the U.S. Department of Labor, the IRS or the state agency, with the date we last checked. See our <a href="/editorial-policy/">editorial policy</a>.</li>
<li><b>Printable.</b> Every result can be printed or saved as a PDF without menus or ads.</li>
<li><b>Private.</b> Calculations happen on your device.</li>
</ul>""")
    how = S("How to get an accurate result", """
<ol>
<li>Use the actual times you worked, not the scheduled ones.</li>
<li>Enter only <i>unpaid</i> meal breaks; paid rest breaks stay inside your hours.</li>
<li>Choose the overtime rule for the state where you work and the workweek start day your employer uses.</li>
<li>Compare the answer with your pay stub. If they differ, read <a href="/guides/time-card-mistakes-and-how-to-fix-them/">time card mistakes and how to fix them</a>.</li>
</ol>""")
    body = ('{hero}<div class="layout"><div class="main-col">{quick}{groups}{ad1}{quick_ans}<div class="section-title"><h2>Guides</h2><a href="/guides/">All guides</a></div><div class="card-grid">{g}</div>'
            '<div class="prose">{why}{how}</div>{faq}{ad2}</div>{side}</div>').format(
        hero=hero, quick=quick, groups=groups, ad1=ad("home-1"), quick_ans=quick_ans, g=gtiles, why=why, how=how, faq=faq_html(qa), ad2=ad("home-2", short=True),
        side=side_html([]).replace('<div class="side-box"><h2>Related</h2><ul></ul></div>', ""))
    schema = [
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": plain(q), "acceptedAnswer": {"@type": "Answer", "text": plain(a)}} for q, a in qa]},
    ]
    pg = register(Page("/", "Time Card Calculator - Free Work Hours, Overtime & Pay Calculators",
                       "Free time card, overtime, hours and paycheck calculators with step-by-step results, worked examples and plain-English guides based on US Department of Labor sources.",
                       body, "home", [], schema, name="Home"))
    pg.related = []


def calculators_hub():
    groups = ""
    for title, slugs in TOOL_GROUPS:
        groups += "<h2>%s</h2><div class=\"card-grid\">%s</div>" % (title, "".join(tile(s) for s in slugs))
    sections = ["<p>Every calculator runs in your browser, shows its steps, links to a worked example and an explanation of the rules, and can be printed. Pick the one that matches your question.</p>", groups,
                S("Which calculator should I use?", """
<ul>
<li><b>I want my week or pay period totalled:</b> <a href="/time-card-calculator/">time card calculator</a> (or the <a href="/bi-weekly-time-card-calculator/">bi-weekly</a> and <a href="/semi-monthly-time-card-calculator/">semi-monthly</a> versions).</li>
<li><b>I want to know how long one shift is:</b> <a href="/hours-calculator/">hours calculator</a>.</li>
<li><b>I think I am owed overtime:</b> <a href="/overtime-calculator/">overtime calculator</a>.</li>
<li><b>My payroll wants decimals:</b> <a href="/decimal-hours-converter/">decimal hours converter</a>.</li>
<li><b>I want to compare job offers:</b> <a href="/hourly-to-salary/">hourly to salary</a>, <a href="/salary-to-hourly/">salary to hourly</a> and the <a href="/paycheck-calculator/">paycheck estimator</a>.</li>
</ul>""")]
    pg = article_page("/calculators/", "All Calculators", "All Time Card and Work Hours Calculators - Free, Step-by-Step",
                      "Every time card, hours, overtime, pay and schedule calculator in one place: time cards, overtime, hours between times, PTO, paycheck, rounding and more.",
                      "All Calculators", "Eighteen free tools for tracking, totalling and checking work hours.", sections,
                      [("Are the calculators free?", "Yes, and there is no sign-up."), ("Do you save what I type?", "Time cards are kept in your browser only. Nothing is sent to us."), ("Can I print a result?", "Yes. Every calculator has a Print this result button; choose Save as PDF in the print dialog to keep a copy.")],
                      related=["/time-card-calculator/", "/overtime-calculator/", "/guides/"], crumbs=[("/", "Home"), ("/calculators/", "Calculators")], kind="hub")
    pg.itemlist = [(PAGES[s].name, s) for _, slugs in TOOL_GROUPS for s in slugs]
    pg.webpage_type = "CollectionPage"


def guides_hub():
    sections = ["<p>Plain-English guides with worked examples and links to official sources. Each one states the date we last checked those sources.</p>",
                '<div class="card-grid">%s</div>' % "".join(tile(s, "Guide") for s in GUIDES),
                S("How we write these guides", "<p>Rules are stated only where we can link to the U.S. Department of Labor, the IRS or a state labor department. Everything else is arithmetic you can check yourself. Read the <a href=\"/editorial-policy/\">editorial policy</a>.</p>")]
    pg = article_page("/guides/", "Guides", "Guides: Overtime, Breaks, Rounding, Timesheets & Pay Periods",
                      "Plain-English guides to overtime rules, exempt vs non-exempt, breaks, rounding time cards, timesheets and pay periods, with worked examples and official sources.",
                      "Guides", "How overtime, breaks, rounding and pay periods work, in plain English.", sections,
                      [("Are these guides legal advice?", "No. They are general information with links to official sources. See the disclaimer."), ("How current are the rules?", "Each guide shows the date its official sources were last checked, and links to them so you can confirm the current rule."), ("Can I suggest a topic?", "Yes. Use the contact page to suggest a guide or report an error.")],
                      related=["/calculators/", "/overtime-calculator/"], crumbs=[("/", "Home"), ("/guides/", "Guides")], kind="hub")
    pg.itemlist = [(PAGES[s].name, s) for s in GUIDES]
    pg.webpage_type = "CollectionPage"


def trust_pages():
    pg = article_page("/about/", "About", "About Time Card Calculator - Free Work Hours Tools",
                      "About Time Card Calculator: free, private, step-by-step work hours, overtime and pay calculators built on official US sources.",
                      "About Time Card Calculator", "A small, independent set of free tools for people who track work hours.", [
                          S("What this site is", """
<p>%s is a collection of calculators and plain-English guides for shift workers, hourly employees, freelancers and small-business owners who need to total hours, check overtime or understand a timesheet. The tools run entirely in your browser, with no account, no sign-up and no data upload.</p>
<p>Many hour calculators give one number. We show the working, because the working is what lets you check a pay stub, catch a mistake or learn the method.</p>""" % SITE),
                          S("What we do not do", """
<ul>
<li>We do not give legal, tax or payroll advice. See the <a href="/disclaimer/">disclaimer</a>.</li>
<li>We do not state a rule unless we can link to an official source. See the <a href="/editorial-policy/">editorial policy</a>.</li>
<li>We do not collect or sell your timesheet data. See the <a href="/privacy/">privacy policy</a>.</li>
</ul>"""),
                          S("What's here", """
<p>Browse the <a href="/calculators/">calculators</a>, the <a href="/guides/">guides</a>, and the quick-answer pages for <a href="/hours/">shift hours</a>, <a href="/hours-per-year/">hours per year</a>, <a href="/hourly-to-annual/">hourly-to-annual pay</a> and <a href="/decimal-hours/">decimal hour charts</a>.</p>
<p>The site is intended to be supported by advertising so the tools can stay free.</p>"""),
                          S("Corrections", """<p>If you find a mistake, tell us through the <a href="/contact/">contact page</a>. We correct errors and note material changes in the page's &ldquo;last checked&rdquo; date.</p>"""),
                      ], [], related=["/editorial-policy/", "/calculators/", "/guides/"], crumbs=[("/", "Home"), ("/about/", "About")], kind="static", ad_ok=False)
    pg.webpage_type = "AboutPage"

    pg = article_page("/editorial-policy/", "Editorial Policy", "Editorial Policy - How We Research and Check Our Content",
                      "How Time Card Calculator researches, sources, tests and corrects its calculators and guides: official sources only, last-checked dates and tested math.",
                      "Editorial Policy", "How the calculators are built and how the guides are checked.", [
                          S("Sources", """
<p>Statements about wage-and-hour rules, break requirements and tax withholding must come from the U.S. Department of Labor, the Internal Revenue Service, the Code of Federal Regulations, or a state labor agency. Each page that states a rule links the source at the bottom and shows the date we last checked it. If we cannot confirm a rule from an official source, we leave it out rather than guess.</p>"""),
                          S("Calculators", """
<p>Calculator logic is plain JavaScript that runs in the browser. The math is covered by an automated test script that checks results against hand-worked examples (overtime splits, pay, rounding, pay periods, withholding). Worked examples on the pages are calculated with the same formulas, and the page text shows every step so readers can verify them.</p>"""),
                          S("What we label as estimates", """
<p>Take-home pay, state overtime presets and any figure that depends on facts we cannot know (your W-4, your employer's policies, your state's industry rules) are estimates and labelled as such. Tax figures are for a stated tax year and are reviewed each year.</p>"""),
                          S("Updates and corrections", """
<p>Rules change. We re-check cited sources periodically and update the &ldquo;last checked&rdquo; date when we do. If you spot an error, use the <a href="/contact/">contact page</a>; we correct confirmed errors promptly.</p>"""),
                          S("Advertising", """<p>The site is intended to be supported by advertising. Advertising will not influence what the guides say, and ad slots are kept away from the calculators' inputs and results.</p>"""),
                          S("Not advice", """<p>Everything here is general information. Read the <a href="/disclaimer/">disclaimer</a>.</p>"""),
                      ], [], related=["/about/", "/disclaimer/", "/guides/"], crumbs=[("/", "Home"), ("/editorial-policy/", "Editorial policy")], kind="static", ad_ok=False)

    pg = article_page("/disclaimer/", "Disclaimer", "Disclaimer - Not Legal, Tax or Payroll Advice",
                      "Disclaimer: Time Card Calculator provides general information and estimates only. It is not legal, tax or payroll advice.",
                      "Disclaimer", "Please read this before relying on any result.", [
                          S("Not legal, tax or payroll advice", """
<p>The calculators, guides and examples on this site are for general information and estimation. They are <b>not legal advice, not tax advice and not payroll advice</b>, and they do not create any professional relationship. Wage-and-hour, tax and payroll rules depend on your job, your employer, your state and city, any union or contract, and the facts of your situation.</p>"""),
                          S("Estimates, not payslips", """
<p>Results, including overtime splits and take-home pay, are estimates. Your employer's payroll system, your Form W-4, your state's rules and other deductions determine what you are actually paid. Always compare with your pay stub and confirm with your employer, payroll provider, state labor department or a qualified professional.</p>"""),
                          S("Rules change", """
<p>We link to official sources and show the date we last checked them, but laws, regulations, tax tables and agency guidance change. Use the linked sources to confirm the current rule before relying on it.</p>"""),
                          S("No warranty", """<p>The site and its calculators are provided &ldquo;as is&rdquo; without warranties of any kind. To the extent permitted by law, we are not liable for decisions made using the results.</p>"""),
                          S("Related", """<p>See our <a href="/editorial-policy/">editorial policy</a> for how we source and test content and our <a href="/privacy/">privacy policy</a> for how data is handled.</p>"""),
                      ], [], related=["/editorial-policy/", "/privacy/", "/about/"], crumbs=[("/", "Home"), ("/disclaimer/", "Disclaimer")], kind="static", ad_ok=False)

    pg = article_page("/privacy/", "Privacy Policy", "Privacy Policy - Time Card Calculator",
                      "Privacy policy: calculators run in your browser, entries stay on your device, no accounts. How local storage and any future advertising are handled.",
                      "Privacy Policy", "Last updated %s." % CHECKED_LONG, [
                          S("Your timesheet and calculator data", """
<p>Everything you type into a calculator is processed in your browser. It is not sent to our servers. The time card and timesheet remember what you entered by saving it in your browser's local storage on your own device, so it is still there when you return. Use the Reset button, or clear your browser's site data, to delete it. We cannot see or recover it.</p>"""),
                          S("Accounts and personal information", """<p>There are no accounts and no sign-up. We do not ask for your name, email or payment details. If you type a name or company into the printable timesheet, it stays on your device and appears only on the page you print.</p>"""),
                          S("Cookies, analytics and advertising", """
<p>At the time of this update the site sets no cookies of its own, runs no analytics and shows no advertising. The site is intended to be supported by advertising in the future. If we add third-party advertising or analytics (for example Google AdSense), those services may use cookies or similar technologies to serve and measure ads, and we will update this policy before they are enabled and describe the choices available to you. Google explains how to manage personalised ads at <a href="https://adssettings.google.com/" rel="noopener">adssettings.google.com</a>.</p>"""),
                          S("Hosting logs", """<p>The site is served as static files by a hosting provider, which may keep standard server logs (such as IP address, requested page and time) for security and operations. We do not use those logs to identify visitors.</p>"""),
                          S("Children", """<p>The site is a general-audience tool and is not directed to children under 13.</p>"""),
                          S("Contact", """<p>Questions about this policy? Use the <a href="/contact/">contact page</a>.</p>"""),
                      ], [], related=["/disclaimer/", "/about/"], crumbs=[("/", "Home"), ("/privacy/", "Privacy policy")], kind="static", ad_ok=False)

    pg = article_page("/contact/", "Contact", "Contact - Time Card Calculator",
                      "Contact Time Card Calculator to report a calculator bug, suggest a new tool or flag an error in a guide.",
                      "Contact", "Report a bug, suggest a tool or flag a correction.", [
                          S("How to reach us", """
<p>The easiest way is to open an issue on the project's public repository: <a href="%s" rel="noopener">%s</a>. Please include the page address, what you entered, what you expected and what you got.</p>
<p>Please do <b>not</b> post personal pay records or employer details: the calculators run locally, so we never see your numbers and you do not need to share them to report a problem.</p>""" % (REPO_ISSUES, REPO_ISSUES)),
                          S("What we can help with", """
<ul><li>A calculator that gives a wrong or confusing result</li><li>A rule on a guide that looks out of date, with a link to the official source</li><li>A tool you would like to see</li></ul>
<p>We cannot give individual legal, tax or payroll advice. For wage-and-hour questions about your own job, contact your state labor department or the U.S. Department of Labor's Wage and Hour Division.</p>"""),
                      ], [], related=["/about/", "/disclaimer/"], crumbs=[("/", "Home"), ("/contact/", "Contact")], kind="static", ad_ok=False)
    pg.webpage_type = "ContactPage"


def not_found():
    body = ('<div class="page-head"><h1>Page not found</h1><p class="lead">That page does not exist. Try one of the popular tools:</p></div>'
            '<div class="card-grid">%s</div>' % "".join(tile(s) for s in ["/time-card-calculator/", "/hours-calculator/", "/overtime-calculator/", "/timesheet/"]))
    register(Page("/404.html", "Page not found - " + SITE, "The page you were looking for does not exist. Try one of the popular time card and work hours calculators.", body, "static", [], [], in_sitemap=False, name="Not found"))
