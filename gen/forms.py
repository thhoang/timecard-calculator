"""HTML for the interactive calculators. Element ids follow '<prefix>-<name>' and are wired up in assets/tools.js."""
from .core import inp, sel, check, result_block

RULE_OPTS = [
    ("federal", "Federal (FLSA): over 40 hours in the workweek", True),
    ("ca", "California: daily 8 h / 12 h, weekly 40 h, 7th day"),
    ("ak", "Alaska: over 8 h a day and over 40 h a week"),
    ("nv_low", "Nevada, pay under 1.5x state minimum wage: daily 8 h + weekly 40 h"),
    ("nv_high", "Nevada, pay at or above 1.5x state minimum wage: weekly 40 h"),
    ("co", "Colorado: over 12 h a day and over 40 h a week"),
    ("none", "No overtime (just total the hours)"),
]
WEEKDAYS = [(1, "Monday", True), (2, "Tuesday"), (3, "Wednesday"), (4, "Thursday"), (5, "Friday"), (6, "Saturday"), (0, "Sunday")]


def tool_card(tool, p, title, sub, inner, attrs="", buttons_extra=""):
    res = result_block(p)
    if buttons_extra:
        res = res.replace('<button type="button" class="ghost" data-reset>', buttons_extra + '<button type="button" class="ghost" data-reset>')
    return ('<section class="tool" data-tool="%s" data-p="%s" %s aria-labelledby="%s-title"><h2 class="tool-title" id="%s-title">%s</h2>'
            '<p class="tool-sub">%s</p><p class="print-only"><b>%s</b> &middot; <span data-today></span></p>%s%s</section>') % (
        tool, p, attrs, p, p, title, sub, title, inner, res)


def timecard(period="weekly", locked=False, title="Time card calculator", sub="Enter clock-in and clock-out times for each day. Totals, overtime and pay update as you type.", extra_fields=True):
    periods = [("weekly", "Weekly (7 days)"), ("biweekly", "Bi-weekly (14 days)"), ("semimonthly1", "Semi-monthly: 1st to 15th"),
               ("semimonthly2", "Semi-monthly: 16th to end of month"), ("monthly", "Monthly (calendar month)")]
    if locked:
        periods = periods[:1]
    popts = [(v, t, v == period) for v, t in periods]
    top = ('<div class="grid3">' + sel("tc-period", "Pay period type", popts) +
           '<div class="field"><label for="tc-start" id="tc-start-label">Pay period starts</label><input id="tc-start" type="date"></div>' +
           sel("tc-wk", "Workweek starts on", WEEKDAYS, hint="Overtime is counted per workweek") + "</div>")
    ident = ""
    if extra_fields:
        ident = '<div class="grid2 no-print">' + inp("tc-name", "Employee name (optional)", placeholder="Jane Doe", autocomplete="off") + inp("tc-company", "Company (optional)", placeholder="Acme Inc", autocomplete="off") + "</div>"
    table = ('<p class="print-only" id="tc-pp"></p><div class="table-wrap"><table class="tc-table"><thead><tr><th scope="col">Date</th><th scope="col">Clock in</th>'
             '<th scope="col">Clock out</th><th scope="col">Break (min)</th><th scope="col" class="num">Hours</th></tr></thead><tbody id="tc-body"></tbody></table></div>')
    bottom = ('<div class="grid2 no-print">' + sel("tc-rule", "Overtime rule", RULE_OPTS) +
              sel("tc-round", "Round each punch to", [("0", "No rounding", True), ("5", "Nearest 5 min"), ("6", "Nearest 6 min (1/10 h)"), ("15", "Nearest 15 min (7-minute rule)")]) +
              inp("tc-rate", "Hourly rate (optional)", "number", min="0", step="0.01", placeholder="18.50") +
              inp("tc-prior", "Hours already worked earlier this workweek", "text", hint="Only if your period starts mid-week, e.g. 12 or 12:30", placeholder="0") + "</div>")
    fill = '<button type="button" class="secondary no-print" data-fill>Fill an example week</button>'
    return tool_card("timecard", "tc", title, sub, top + ident + table + bottom, attrs='data-period="%s"%s' % (period, " data-locked" if locked else ""), buttons_extra=fill)


def hours_between(prefix_title="Hours between two times", dates=True, small=False):
    d1 = inp("hb-sdate", "Start date (optional)", "date") if dates else ""
    d2 = inp("hb-edate", "End date (optional)", "date") if dates else ""
    inner = ('<div class="grid2">' + d1 + inp("hb-stime", "Start time", "text", placeholder="8:00 am", autocomplete="off") + d2 +
             inp("hb-etime", "End time", "text", placeholder="5:00 pm", autocomplete="off") + "</div>" +
             '<div class="grid3">' + inp("hb-break", "Unpaid break (minutes)", "number", min="0", step="5", placeholder="30") +
             (inp("hb-days", "Days per week", "number", min="1", max="7", step="1", value="5") + inp("hb-rate", "Hourly rate (optional)", "number", min="0", step="0.01", placeholder="20") if not small else "") + "</div>")
    return tool_card("hb", "hb", prefix_title, "Type times the way you say them: 8, 8am, 8:30, 5:15 pm, 17:15 or 1715.", inner)


def overtime():
    days = "".join(inp("ot-d%d" % i, "Day %d" % (i + 1), "text", placeholder="0", autocomplete="off", inputmode="decimal") for i in range(7))
    presets = [("federal", "Federal (FLSA) - over 40 h a week", True), ("ca", "California - daily 8 h / 12 h, 7th day, weekly 40 h"), ("ak", "Alaska - over 8 h a day and 40 h a week"),
               ("nv_low", "Nevada - pay under 1.5x state minimum (daily 8 h + weekly 40 h)"), ("nv_high", "Nevada - pay at or above 1.5x state minimum (weekly 40 h)"),
               ("co", "Colorado - over 12 h a day and 40 h a week"), ("custom", "Custom rule")]
    inner = ('<div class="grid3">' + sel("ot-preset", "Overtime rule", presets) + inp("ot-rate", "Regular hourly rate ($)", "number", min="0", step="0.01", placeholder="20") +
             sel("ot-wk", "Workweek starts on", WEEKDAYS, hint="Matters for California's 7th-day rule") + "</div>"
             '<fieldset><legend>Hours worked each day (8, 8.5 or 8:30)</legend><div class="grid4">' + days + "</div></fieldset>"
             '<div class="grid2">' + inp("ot-bonus", "Non-discretionary bonus this week ($, optional)", "number", min="0", step="0.01", placeholder="0",
                                         hint="Production, shift or attendance bonuses count toward the regular rate") + "</div>"
             '<fieldset class="custom-only" hidden><legend>Custom rule</legend><div class="grid3">' +
             inp("ot-cd", "Daily overtime after (hours)", "number", min="0", step="0.25", placeholder="8") + inp("ot-cdt", "Daily double time after (hours)", "number", min="0", step="0.25", placeholder="12") +
             inp("ot-cw", "Weekly overtime after (hours)", "number", min="0", step="0.25", placeholder="40", value="40") + inp("ot-cm1", "Overtime multiplier", "number", min="1", step="0.25", value="1.5") +
             inp("ot-cm2", "Double-time multiplier", "number", min="1", step="0.25", value="2") + "</div></fieldset>")
    return tool_card("ot", "ot", "Overtime pay calculator", "Pick a rule, enter hours for each day of the workweek and your rate.", inner)


def duration():
    rows = ""
    for i in range(6):
        rows += ('<div class="grid3" style="grid-template-columns:110px 1fr"><div class="field"><label for="du-s%d">Action</label><select id="du-s%d"><option value="+">Add</option><option value="-"%s>Subtract</option></select></div>' % (i, i, "")
                 + inp("du-v%d" % i, "Time %d" % (i + 1), "text", placeholder="1:30 or 1h 30m" if i == 0 else "", autocomplete="off") + "</div>")
    a = tool_card("duration", "du", "Add and subtract hours and minutes", "Enter durations like 1:30, 2h 15m, 45m or 1.5. The first line is your starting amount.", rows)
    b = tool_card("timeplus", "tp", "Add or subtract time from a clock time", "What time is it 7 hours 45 minutes after 10:15 pm?",
                  '<div class="grid3">' + inp("tp-time", "Clock time", "text", placeholder="10:15 pm", autocomplete="off") +
                  sel("tp-op", "Action", [("+", "Add", True), ("-", "Subtract")]) + inp("tp-dur", "Duration", "text", placeholder="7:45", autocomplete="off") + "</div>")
    return a, b


def decimal_tools():
    a = tool_card("hm2dec", "hd", "Hours and minutes to decimal hours", "Turn 7 hours 45 minutes into 7.75 for payroll.",
                  '<div class="grid2">' + inp("hd-h", "Hours", "number", min="0", step="1", placeholder="7") + inp("hd-m", "Minutes", "number", min="0", step="1", placeholder="45") + "</div>")
    b = tool_card("dec2hm", "dh", "Decimal hours to hours and minutes", "Turn 7.75 back into 7:45.",
                  inp("dh-v", "Decimal hours", "text", placeholder="7.75", inputmode="decimal", autocomplete="off"))
    return a, b


def minutes_tool():
    return tool_card("mins", "mc", "Minutes to decimal hours", "Convert any number of minutes - 45, 410 or 1,275 - to decimal hours.",
                     inp("mc-v", "Minutes", "number", min="0", step="1", placeholder="410"))


def paycheck():
    inner = ('<div class="grid3">' + sel("pc-mode", "Start from", [("hourly", "Hourly rate and hours", True), ("gross", "Gross pay per period")]) +
             sel("pc-freq", "Pay frequency", [("52", "Weekly"), ("26", "Bi-weekly", True), ("24", "Semi-monthly"), ("12", "Monthly")]) +
             sel("pc-status", "Federal filing status (W-4)", [("single", "Single or married filing separately", True), ("married", "Married filing jointly")]) + "</div>"
             '<div class="grid3 hourly-only">' + inp("pc-rate", "Hourly rate ($)", "number", min="0", step="0.01", placeholder="22") + inp("pc-reg", "Regular hours per week", "number", min="0", step="0.5", value="40") +
             inp("pc-ot", "Overtime hours per week", "number", min="0", step="0.5", value="0") + "</div>"
             '<div class="grid3 gross-only" hidden>' + inp("pc-gross", "Gross pay per period ($)", "number", min="0", step="0.01", placeholder="2000") + "</div>"
             '<fieldset><legend>Deductions per pay period (optional)</legend><div class="grid4">' +
             inp("pc-sec125", "Health/cafeteria plan, pre-tax ($)", "number", min="0", step="0.01", placeholder="0") + inp("pc-k401", "401(k) or similar, pre-tax ($)", "number", min="0", step="0.01", placeholder="0") +
             inp("pc-state", "State/local income tax (% of wages)", "number", min="0", step="0.1", placeholder="0", hint="Your own estimate") + inp("pc-other", "Other withholding ($)", "number", min="0", step="0.01", placeholder="0") + "</div></fieldset>")
    return tool_card("pc", "pc", "Paycheck estimator (gross to net)", "A simple estimate of take-home pay using IRS 2026 federal withholding tables.", inner)


def hourly_salary(mode):
    if mode == "h2s":
        main = inp("hs-v", "Hourly rate ($)", "number", min="0", step="0.01", placeholder="25")
        t, s = "Hourly to salary calculator", "See what an hourly wage adds up to per year, month, pay period and day."
    else:
        main = inp("hs-v", "Annual salary ($)", "number", min="0", step="100", placeholder="62000")
        t, s = "Salary to hourly calculator", "Find the hourly rate behind a yearly salary, using your real weekly hours."
    inner = ('<div class="grid3">' + main + inp("hs-hpw", "Hours per week", "number", min="1", max="100", step="0.5", value="40") +
             inp("hs-off", "Unpaid weeks off per year", "number", min="0", max="51", step="1", value="0", hint="0 = paid all 52 weeks") + "</div>")
    return tool_card("hs", "hs", t, s, inner, attrs='data-mode="%s"' % mode)


def pto():
    inner = ('<div class="grid3">' + sel("pto-method", "How does your employer give PTO?", [("perperiod", "Hours per pay period", True), ("days", "Days per year"), ("ratio", "1 hour per N hours worked")]) +
             sel("pto-freq", "Pay frequency", [("52", "Weekly"), ("26", "Bi-weekly", True), ("24", "Semi-monthly"), ("12", "Monthly")]) +
             inp("pto-hpw", "Hours worked per week", "number", min="0", step="0.5", value="40") + "</div>"
             '<div class="grid3"><div data-m="perperiod">' + inp("pto-pp", "PTO hours per pay period", "number", min="0", step="0.01", placeholder="3.08") + "</div>"
             '<div data-m="days" hidden>' + inp("pto-days", "PTO days per year", "number", min="0", step="0.5", placeholder="15") + "</div>"
             '<div data-m="days" hidden>' + inp("pto-hday", "Hours in a PTO day", "number", min="1", step="0.5", value="8") + "</div>"
             '<div data-m="ratio" hidden>' + inp("pto-ratio", "1 hour of PTO per ___ hours worked", "number", min="1", step="1", placeholder="30") + "</div></div>"
             '<div class="grid4">' + inp("pto-start", "Starting balance (hours)", "number", min="0", step="0.5", value="0") + inp("pto-cap", "Balance cap (hours, optional)", "number", min="0", step="1", placeholder="120") +
             inp("pto-used", "PTO you plan to use per year (hours)", "number", min="0", step="1", value="0") + inp("pto-n", "Pay periods to project", "number", min="1", max="104", step="1", value="26") + "</div>")
    return tool_card("pto", "pto", "PTO accrual calculator", "Work out how much paid time off you earn and what your balance will be.", inner)


def lunch():
    inner = ('<div class="grid3">' + inp("lb-in", "Clock in", "text", placeholder="8:00 am", autocomplete="off") + inp("lb-out", "Clock out", "text", placeholder="5:00 pm", autocomplete="off") +
             inp("lb-meal", "Unpaid meal break (min)", "number", min="0", step="5", value="30") + "</div>"
             '<div class="grid4">' + inp("lb-thr", "Auto-deduct only if shift is over (hours, optional)", "number", min="0", step="0.5", placeholder="6") +
             inp("lb-rn", "Paid rest breaks per shift", "number", min="0", step="1", value="2") + inp("lb-rm", "Minutes per rest break", "number", min="0", step="1", value="10") +
             inp("lb-days", "Days per week", "number", min="1", max="7", value="5") + "</div>"
             '<div class="grid3">' + inp("lb-rate", "Hourly rate (optional)", "number", min="0", step="0.01", placeholder="18") + "</div>")
    return tool_card("lb", "lb", "Lunch and unpaid break calculator", "See paid hours after an unpaid meal break, and what the break costs per week.", inner)


def shiftdiff():
    inner = ('<div class="grid3">' + inp("sd-rate", "Base hourly rate ($)", "number", min="0", step="0.01", placeholder="20") +
             sel("sd-type", "Differential type", [("flat", "Dollars per hour", True), ("pct", "Percent of base rate")]) + inp("sd-diff", "Differential amount", "number", min="0", step="0.01", placeholder="2") + "</div>"
             '<div class="grid2">' + inp("sd-in", "Shift starts", "text", placeholder="6:00 pm", autocomplete="off") + inp("sd-out", "Shift ends", "text", placeholder="3:00 am", autocomplete="off") + "</div>"
             '<fieldset><legend>When does the differential apply? (check your policy)</legend><div class="grid2">' +
             inp("sd-ws", "Differential window starts", "text", value="10:00 pm", autocomplete="off") + inp("sd-we", "Differential window ends", "text", value="6:00 am", autocomplete="off") + "</div></fieldset>"
             '<div class="grid2">' + inp("sd-break", "Unpaid break (minutes)", "number", min="0", step="5", value="30") + inp("sd-days", "Shifts per week", "number", min="1", max="7", value="5") + "</div>")
    return tool_card("sd", "sd", "Shift differential and night pay calculator", "Add night, evening or weekend premium pay to your hourly rate.", inner)


def planner():
    pats = [("5-2", "5 on, 2 off (Mon-Fri style)", True), ("4-3", "4 on, 3 off (four 10s)"), ("3-4", "3 on, 4 off (three 12s)"), ("6-1", "6 on, 1 off"),
            ("223", "2-2-3 rotation (Pitman, 14-day cycle)"), ("4-4", "4 on, 4 off"), ("7-7", "7 on, 7 off"), ("2-2", "2 on, 2 off"), ("custom", "Custom: N on, M off")]
    inner = ('<div class="grid3">' + sel("sp-pattern", "Schedule pattern", pats) + '<div class="field"><label for="sp-start">First shift date</label><input id="sp-start" type="date"></div>' +
             inp("sp-weeks", "Weeks to show", "number", min="1", max="12", value="4") + "</div>"
             '<div class="grid3 custom-only" hidden>' + inp("sp-on", "Days on", "number", min="1", max="14", value="4") + inp("sp-offd", "Days off", "number", min="0", max="14", value="3") + "</div>"
             '<div class="grid4">' + inp("sp-in", "Shift starts", "text", value="7:00 am", autocomplete="off") + inp("sp-out", "Shift ends", "text", value="5:30 pm", autocomplete="off") +
             inp("sp-break", "Unpaid break (min)", "number", min="0", step="5", value="30") + inp("sp-rate", "Hourly rate (optional)", "number", min="0", step="0.01", placeholder="24") + "</div>")
    return tool_card("sp", "sp", "Work schedule and shift planner", "Lay out a repeating shift pattern on a calendar and see the hours in every week.", inner)


def military():
    a = tool_card("mt", "mt", "12-hour and 24-hour (military) time converter", "Type a time in either format - it converts to the other.",
                  inp("mt-v", "Time", "text", placeholder="5:30 pm or 1730", autocomplete="off"))
    b = tool_card("mh", "mh", "Hours between two military times", "Find the length of a shift written in 24-hour time.",
                  '<div class="grid2">' + inp("mh-a", "Start (24-hour)", "text", placeholder="0700", autocomplete="off") + inp("mh-b", "End (24-hour)", "text", placeholder="1530", autocomplete="off") + "</div>")
    return a, b


def rounding():
    inner = ('<div class="grid2">' + inp("rd-in", "Actual clock in", "text", placeholder="8:06 am", autocomplete="off") + inp("rd-out", "Actual clock out", "text", placeholder="5:07 pm", autocomplete="off") + "</div>"
             '<div class="grid4">' + sel("rd-step", "Round to", [("5", "5 minutes"), ("6", "6 minutes (tenth of an hour)"), ("15", "15 minutes (quarter hour)", True)]) +
             sel("rd-mode", "Method", [("nearest", "Nearest (7-minute rule at 15)", True), ("up", "Always up"), ("down", "Always down")]) +
             inp("rd-break", "Unpaid break (min)", "number", min="0", step="5", value="30") + inp("rd-rate", "Hourly rate (optional)", "number", min="0", step="0.01", placeholder="18") + "</div>"
             '<div class="grid3">' + inp("rd-days", "Shifts per week", "number", min="1", max="7", value="5") + "</div>")
    return tool_card("rd", "rd", "Time rounding calculator", "See how 5-, 6- and 15-minute rounding changes a shift and your pay.", inner)
