"""Data-driven page families. Every page gets its own computed numbers, worked example, prose and FAQ."""
from .core import (article_page, table, example, faq_html, Page, register, ad, crumbs_html, related_html, side_html,
                   sources_html, BASE, plain, CHECKED, CHECKED_LONG, SRC)
from .tools_a import S
import json

SRC["dol_minwage"] = ("U.S. Department of Labor: Minimum Wage (federal minimum wage $7.25 per hour effective July 24, 2009)", "https://www.dol.gov/agencies/whd/minimum-wage")

FED_MIN = 7.25


def m0(x):
    return "${:,.0f}".format(x)


def m2(x):
    return "${:,.2f}".format(x)


def g(x, d=2):
    s = ("%." + str(d) + "f") % x
    return s.rstrip("0").rstrip(".") if "." in s else s


def ampm(h24):
    return "%d%s" % (h24 % 12 or 12, "am" if h24 < 12 else "pm")


def hm(h):
    """decimal hours -> h:mm"""
    t = int(round(h * 60))
    return "%d:%02d" % (t // 60, t % 60)


def week_pay(hours, rate):
    """Federal weekly overtime on one workweek."""
    reg = min(hours, 40.0)
    ot = max(0.0, hours - 40.0)
    return reg, ot, reg * rate + ot * rate * 1.5


# ---- paycheck estimate port of assets/calc.js (single filer, IRS Pub 15-T 2026, standard Step 1 only)
_SINGLE = [(0, 0, 0, 0), (7500, 0, .10, 7500), (19900, 1240, .12, 19900), (57900, 5800, .22, 57900),
           (113200, 17966, .24, 113200), (209275, 41024, .32, 209275), (263725, 58448, .35, 263725),
           (648100, 192979.25, .37, 648100)]


def est_net_biweekly(gross_period, periods=26):
    adj = max(0.0, gross_period * periods - 8600)
    row = _SINGLE[0]
    for r in _SINGLE:
        if adj >= r[0]:
            row = r
    fed = max(0.0, row[1] + (adj - row[3]) * row[2]) / periods
    ss = min(gross_period * periods, 184500) / periods * 0.062
    med = gross_period * 0.0145
    return gross_period - fed - ss - med, fed, ss, med


# =============================================================== shift hour pages
START_TXT = {
    6: "A 6 am start is the early shift: it is common in places that open before the rest of the town, such as bakeries, warehouses, construction sites and hospital morning handovers.",
    7: "A 7 am start fits workplaces that want the day running by mid-morning, such as schools, clinics, trades and distribution centres, and it gets you ahead of the commute.",
    8: "An 8 am start is the most familiar clock-in time: offices, shops, factories and public services all use it, so schedules built around it are easy to coordinate.",
    9: "A 9 am start is the classic office opening hour. It avoids the earliest commute and lines up with school and childcare drop-offs.",
    10: "A 10 am start is a late-morning shift, typical for retail, restaurants, salons and anywhere customers do not arrive until later in the day.",
}
END_TXT = {
    14: "Finishing at 2 pm leaves the whole afternoon free, which is why early shifts that end here suit second jobs, studying or school pick-ups.",
    15: "A 3 pm finish is a half-way point between a short and a full day and lines up with the end of the school day.",
    16: "Ending at 4 pm gets you out ahead of the rush hour while still covering a solid working day.",
    17: "Finishing at 5 pm is the traditional close of the working day, and most office timetables are built to end here.",
    18: "A 6 pm finish extends coverage into the evening, useful for customer-facing teams and anyone who needs overlap with another time zone.",
    19: "Working until 7 pm is a long day that often goes with retail close-downs, restaurants and client work, so overtime is worth checking.",
    20: "An 8 pm finish makes for a very long day, typically a closing shift or a stretch with on-site demands; the paid-hours and overtime figures below matter.",
}
LEN_TXT = {
    4: "Four hours is a half shift. Shifts this short usually do not include an unpaid meal, so the clock-to-clock figure and the paid figure are normally the same.",
    5: "Five hours is just short of the point where many employers begin scheduling a meal break, so the paid time is often the whole span.",
    6: "Six hours is a short shift; whether a meal is unpaid or paid depends on the employer and the state, so check your own schedule.",
    7: "Seven hours is a long half-day; a 30-minute unpaid meal makes this a 6.5-hour paid shift.",
    8: "Eight hours clock to clock is a standard working day only if there is no unpaid meal; with a meal the paid time is shorter.",
    9: "Nine hours clock to clock is the standard full day: with a one-hour unpaid lunch it is exactly eight paid hours, and with a 30-minute lunch it is eight and a half.",
    10: "Ten hours is the length of a four-day-week shift: four of them make a 40-hour week if the meal is an hour, or 38 if it is 30 minutes.",
    11: "Eleven hours is a long shift; five days of it is well over 40 hours even after an unpaid meal, so weekly overtime is likely.",
    12: "Twelve hours is the length of a typical long-rotation shift. Three of them is roughly a full-time week, and a fourth pushes the total into overtime.",
    13: "Thirteen hours is an extended shift. Check whether your state counts hours past 12 in a day differently (the overtime calculator covers California and Colorado).",
    14: "Fourteen hours is an extreme day. Check the overtime and double-time rules for your state before relying on the weekly totals.",
}


def shift_pages(shifts):
    for start, end in shifts:
        s, e = ampm(start), ampm(end)
        slug = "/hours/%s-to-%s/" % (s, e)
        gross = end - start
        meal = 0.5 if gross >= 6 else 0.0
        net = gross - meal
        n5, n6 = net * 5, net * 6
        reg5, ot5, _ = week_pay(n5, 20)
        reg6, ot6, _ = week_pay(n6, 20)
        days_to_40 = 40.0 / net
        clock24 = "%02d:00 to %02d:00" % (start, end)
        # break table
        brk_rows = []
        for b in (0, 15, 30, 45, 60):
            nb = gross - b / 60.0
            brk_rows.append(["No break" if b == 0 else "%d minutes" % b, g(nb) + " h (%s)" % hm(nb), g(nb * 5) + " h"])
        # pay table
        pay_rows = []
        for r in (15, 20, 25, 30):
            d = net * r
            _, _, w5 = week_pay(n5, r)
            pay_rows.append([m2(r) + "/h", m2(d), m2(w5), m2(w5 * 2)])
        # scenario table
        sc = []
        for label, days in (("4 days a week", 4), ("5 days a week", 5), ("6 days a week", 6), ("7 days a week", 7)):
            h = net * days
            rg, ot, pay20 = week_pay(h, 20)
            _, _, pay25 = week_pay(h, 25)
            sc.append([label, g(h) + " h", g(rg) + " h", g(ot) + " h" if ot else "none", m2(pay20), m2(pay25)])
        if ot5 > 0:
            ot_sentence = ("Five paid days add up to %s hours, so %s hours are overtime under the federal weekly rule (over 40 hours in a workweek)." % (g(n5), g(ot5)))
        else:
            ot_sentence = ("Five paid days add up to %s hours, which is %s hours short of 40, so there is no weekly overtime under the federal rule. A sixth day brings the week to %s hours%s." % (
                g(n5), g(40 - n5), g(n6), (", which is %s hours of overtime" % g(ot6)) if ot6 > 0 else ", still within 40 hours"))
        ex_net = net
        ex_rate = 18.5 + (start - 6) * 1.25 + (end - 14) * 0.5
        ex_rate = round(ex_rate * 4) / 4.0
        d_pay = ex_net * ex_rate
        w_reg, w_ot, w_pay = week_pay(n5, ex_rate)
        bi_pay = w_pay * 2
        example_html = example("%s to %s at %s an hour" % (s, e, m2(ex_rate)), (
            "<p>A worker clocks in at %s and out at %s. Clock to clock that is %s hours (%s). %s</p>"
            "<p><b>Daily pay:</b> %s paid hours &times; %s = <b>%s</b>.</p>"
            "<p><b>Weekly (5 shifts):</b> %s hours%s = <b>%s</b>.</p>"
            "<p><b>Bi-weekly (10 shifts):</b> two workweeks of %s hours each = <b>%s</b> gross, before taxes.</p>") % (
            s, e, g(gross), hm(gross),
            ("A %s-minute unpaid meal brings paid time to %s hours." % (int(meal * 60), g(net)) if meal else "No unpaid meal is assumed on a shift this short."),
            g(net), m2(ex_rate), m2(d_pay),
            g(n5), (" (%s regular + %s overtime at %s)" % (g(w_reg), g(w_ot), m2(ex_rate * 1.5)) if w_ot else ""), m2(w_pay),
            g(n5), m2(bi_pay)))
        faq = [
            ("Is %s to %s %s hours?" % (s, e, g(gross)),
             "Yes. %s to %s (%s) is %s hours clock to clock. With a 30-minute unpaid lunch the paid time is %s hours, and with a one-hour lunch it is %s hours." % (s, e, clock24, g(gross), g(gross - 0.5), g(gross - 1))),
            ("How many hours a week is %s to %s, Monday to Friday?" % (s, e),
             "Five days is %s hours clock to clock, or %s paid hours with a 30-minute unpaid lunch. Two weeks (ten shifts) is %s hours clock to clock." % (g(gross * 5), g(( gross - 0.5) * 5), g(gross * 10))),
            ("How much do you earn working %s to %s at $20 an hour?" % (s, e),
             "Assuming %s, one shift pays %s gross and a five-day week pays %s before taxes%s." % (
                 ("a 30-minute unpaid meal" if meal else "no unpaid meal"), m2(net * 20), m2(week_pay(n5, 20)[2]),
                 (", including %s of overtime premium" % m2(ot5 * 10)) if ot5 else "")),
            ("Does %s to %s lead to overtime?" % (s, e),
             ("Working this shift five days a week gives %s paid hours, which is over 40, so the extra %s hours are overtime under the federal weekly rule. Some states also count hours over a daily limit; see the overtime calculator." % (g(n5), g(ot5))) if ot5 else
             ("Not on a five-day week: %s paid hours is under 40. You would need about %s shifts of this length in one workweek to reach 40 hours, and any hours beyond that are overtime under the federal rule." % (g(n5), g(days_to_40, 1)))),
            ("Is the lunch break included in %s to %s?" % (s, e),
             "Usually it is not: an unpaid meal in which you are completely relieved of duty comes out of the span. Short paid rest breaks stay in. See the guide on calculating hours worked with breaks."),
        ]
        prev_end = end - 1 if end - 1 > start else None
        nxt_end = end + 1 if end + 1 <= 20 else None
        sib = []
        for a, b in ((start, prev_end), (start, nxt_end), (start - 1, end), (start + 1, end)):
            if b is not None and 5 < a < b and (a, b) != (start, end) and (a, b) in SHIFT_SET:
                sib.append('<a href="/hours/%s-to-%s/">%s to %s</a>' % (ampm(a), ampm(b), ampm(a), ampm(b)))
        body_sections = [
            S("The answer for %s to %s" % (s, e), (
                '<div class="answer-box"><div class="big">%s hours</div><div>%s to %s (%s) is %s hours clock to clock. With a 30-minute unpaid lunch that is <b>%s hours</b>; with a one-hour lunch, <b>%s hours</b>.</div></div>' % (
                    g(gross), s, e, clock24, g(gross), g(gross - 0.5), g(gross - 1)) +
                "<p>%s %s %s</p>" % (START_TXT[start], END_TXT[end], LEN_TXT[gross]))),
            S("Weekly and bi-weekly totals", table(
                ["Schedule", "Clock-to-clock hours", "Paid hours (%s)" % ("30-min meal" if meal else "no meal")],
                [["1 shift", g(gross), g(net)], ["5 shifts (1 week)", g(gross * 5), g(n5)], ["10 shifts (bi-weekly)", g(gross * 10), g(net * 10)],
                 ["~21.7 shifts (average month)", g(gross * 5 * 52 / 12), g(n5 * 52 / 12)], ["260 shifts (a year)", g(gross * 260), g(net * 260)]]) +
                "<p>%s</p>" % ot_sentence),
            S("Worked example", example_html),
            S("Pay at several hourly rates", table(["Hourly rate", "One shift", "Five shifts (week)", "Ten shifts (bi-weekly)"], pay_rows) +
              "<p>Weekly and bi-weekly figures apply overtime at 1.5 times the rate for paid hours over 40 in each workweek (the federal rule) and are gross pay before taxes. Different rate? Use the <a href=\"/hourly-to-salary/\">hourly to salary calculator</a>.</p>"),
            S("Overtime scenarios for this shift", table(["Days per week", "Paid hours", "Regular", "Overtime (1.5x)", "Gross at $20", "Gross at $25"], sc) +
              "<p>In states with daily overtime (for example California after 8 hours in a day, or Colorado after 12), a %s-hour shift may already include daily overtime. Test your numbers in the <a href=\"/overtime-calculator/\">overtime calculator</a>.</p>" % g(gross)),
            S("%s to %s with different break lengths" % (s, e), table(["Unpaid break", "Paid hours per day", "Per week (5 days)"], brk_rows)),
            S("Check your own times", "<p>If your clock-in is not exactly %s or you work part of the day on the other side of midnight, use the <a href=\"/hours-calculator/?in=%s&amp;out=%s&amp;brk=%d\">hours calculator</a> pre-filled with this shift, the <a href=\"/time-card-calculator/\">time card calculator</a> for a full week, or the <a href=\"/lunch-break-calculator/\">lunch break calculator</a> to see what the meal costs.</p>" % (s, s, e, int(meal * 60))),
            "<h2>Nearby shifts</h2><p>%s</p>" % " &middot; ".join(sib),
        ]
        title = "%s to %s Is How Many Hours? %s h (%s h With Lunch) - Weekly Totals" % (s.upper(), e.upper(), g(gross), g(gross - 0.5))
        desc = "%s to %s is %s hours clock to clock, %s with a 30-minute lunch. Weekly (%s h) and bi-weekly totals, pay at $15 to $30 an hour and overtime scenarios." % (s, e, g(gross), g(gross - 0.5), g(n5))
        pg = article_page(slug, "%s to %s hours" % (s, e), title, desc, "%s to %s Is How Many Hours?" % (s, e),
                          "Clock-to-clock hours, paid hours after lunch, weekly and bi-weekly totals, pay at several hourly rates and overtime scenarios for a %s to %s shift." % (s, e),
                          body_sections, faq, sources=["dol23"], source_note="Overtime figures use the federal weekly rule from the Department of Labor fact sheet.",
                          related=["/hours-calculator/", "/time-card-calculator/", "/lunch-break-calculator/", "/overtime-calculator/", "/hours/"],
                          crumbs=[("/", "Home"), ("/hours/", "Shift hours"), (slug, "%s to %s" % (s, e))], kind="prog")


SHIFT_SET = set()


def hours_index(shifts):
    by_start = {}
    for a, b in shifts:
        by_start.setdefault(a, []).append(b)
    secs = ""
    for a in sorted(by_start):
        chips = "".join('<a class="chip" href="/hours/%s-to-%s/">%s to %s <small>(%s h)</small></a>' % (ampm(a), ampm(b), ampm(a), ampm(b), g(b - a)) for b in by_start[a])
        secs += "<h2>Shifts starting at %s</h2><div class=\"chips\">%s</div>" % (ampm(a), chips)
    sections = [
        "<p>&ldquo;What time is that in hours?&rdquo; is the question behind a lot of schedule searches. Each page below answers it for one shift and goes further: clock-to-clock hours, paid hours after lunch, weekly and bi-weekly totals, pay at several hourly rates, overtime scenarios and a break table. Pick your start time, then your finish time. For a time not listed, use the <a href=\"/hours-calculator/\">hours calculator</a>.</p>",
        secs,
        S("How to use these pages", "<ul><li>Clock-to-clock hours are simply end minus start. Paid hours subtract an unpaid meal.</li><li>Weekly totals assume five identical shifts. Bi-weekly totals are two workweeks, with overtime figured separately in each.</li><li>Overtime figures use the federal weekly rule (over 40 hours in the workweek), as described by the U.S. Department of Labor. State rules may differ; see the <a href=\"/overtime-rules/\">overtime rules guide</a>.</li></ul>"),
    ]
    article_page("/hours/", "Shift Hours Index", "Shift Hours Index - How Many Hours Between Common Start and End Times",
                 "How many hours are between common shift times: 8am to 5pm, 9am to 5pm, 7am to 3pm and more, with paid hours, weekly and bi-weekly totals and overtime scenarios.",
                 "Shift Hours Index: How Many Hours Is Your Shift?", "Thirty-five common start and finish times, each answered with paid hours, weekly totals, pay and overtime.",
                 sections, [("What is the most common shift length?", "Eight paid hours is the familiar full-time day: nine hours clock to clock with a one-hour unpaid lunch, or eight and a half hours with a 30-minute lunch."),
                            ("How do I convert a shift to hours?", "Subtract the start time from the end time (add 12 hours to PM times), then subtract any unpaid meal."),
                            ("What if my shift crosses midnight?", "Use the hours calculator, which handles overnight shifts."), ("Which overtime rule do these pages use?", "The federal weekly rule: hours over 40 in a workweek are paid at 1.5 times the regular rate, as described by the U.S. Department of Labor.")],
                 related=["/hours-calculator/", "/time-card-calculator/", "/lunch-break-calculator/", "/overtime-calculator/"],
                 crumbs=[("/", "Home"), ("/hours/", "Shift hours")], kind="hub", ad_ok=True)


# =============================================================== hours per year
HPW = [10, 15, 20, 24, 25, 30, 32, 35, 36, 37.5, 40, 44, 45, 48, 50, 60]
HPW_NOTE = {
    10: "Ten hours a week is a small side job: two five-hour shifts or one long day.",
    15: "Fifteen hours is the kind of schedule a student or someone with a second job works: three five-hour shifts.",
    20: "Twenty hours is the classic half-time week: four five-hour days or five four-hour days.",
    24: "Twenty-four hours is three eight-hour days, a common compressed part-time schedule.",
    25: "Twenty-five hours a week is five five-hour days, a typical school-hours schedule.",
    30: "Thirty hours is three-quarters of a full-time week: six hours a day for five days, or an eight-hour day shaved off a four-day week.",
    32: "Thirty-two hours is four eight-hour days, the pattern behind the four-day work week.",
    35: "Thirty-five hours is seven hours a day for five days, often seen in jobs with a longer unpaid lunch.",
    36: "Thirty-six hours is three twelve-hour shifts, the pattern used in many round-the-clock roles.",
    37.5: "Thirty-seven and a half hours is five 7.5-hour days, which is how an 8-hour clock-to-clock day looks after a 30-minute unpaid lunch.",
    40: "Forty hours is the standard full-time week and the line at which federal weekly overtime begins.",
    44: "Forty-four hours is a 40-hour week with an extra four hours, perhaps a half-day Saturday.",
    45: "Forty-five hours is nine hours a day for five days: a one-hour paid-or-unpaid lunch decides whether it is 40 or 45.",
    48: "Forty-eight hours is six eight-hour days, or four twelve-hour shifts.",
    50: "Fifty hours is ten hours a day for five days: a very common long week in trades and management.",
    60: "Sixty hours is a long week: five twelve-hour days, or six ten-hour days.",
}


def hpw_pages():
    for h in HPW:
        label = ("%g" % h)
        slug = "/hours-per-year/%s-hours-a-week/" % label.replace(".", "-")
        yearly = h * 52
        monthly = yearly / 12
        biweekly = h * 2
        d5, d4, d3 = h / 5, h / 4, h / 3
        reg, ot, _ = week_pay(h, 1)
        pct = h / 40 * 100
        rates = (15, 20, 25, 30)
        pay_rows = []
        for r in rates:
            _, _, w = week_pay(h, r)
            pay_rows.append([m2(r) + "/h", m2(w), m2(w * 52), m2(w * 50)])
        unpaid_rows = []
        for w in (0, 2, 4):
            unpaid_rows.append(["%d unpaid week%s" % (w, "" if w == 1 else "s") if w else "Paid all 52 weeks", g(h * (52 - w), 1) + " h", g(h * (52 - w) / 12, 1) + " h"])
        if ot > 0:
            ot_text = ("Over 40 hours a week, federal overtime applies to non-exempt employees: %s regular hours plus %s overtime hours each week. At $20 an hour that is %s a week instead of %s at straight time, a premium of %s a week or %s over 52 weeks." % (
                g(reg), g(ot), m2(week_pay(h, 20)[2]), m2(h * 20), m2(ot * 10), m2(ot * 10 * 52)))
        else:
            ot_text = ("At %s hours a week there is no federal overtime. You would need %s more hour%s in a workweek to reach 40; any hours beyond that are overtime for non-exempt employees." % (g(h), g(40 - h), "" if 40 - h == 1 else "s"))
        band = ("part-time" if h < 35 else "full-time" if h <= 40 else "above full-time")
        title = "%s Hours a Week Is How Many Hours a Year? (%s Hours)" % (label, "{:,.0f}".format(yearly) if yearly == int(yearly) else "{:,.1f}".format(yearly))
        desc = "%s hours a week is %s hours a year (52 weeks), %s hours a month and %s hours bi-weekly. Pay at $15-$30 an hour, unpaid-week adjustments and overtime." % (
            label, "{:,.0f}".format(yearly) if yearly == int(yearly) else "{:,.1f}".format(yearly), g(monthly, 1), g(biweekly, 1))
        sections = [
            S("The answer", '<div class="answer-box"><div class="big">%s hours a year</div><div>%s hours &times; 52 weeks = %s. That is <b>%s hours a month</b> on average and <b>%s hours every two weeks</b>.</div></div><p>%s This schedule is %s%% of a 40-hour week and counts as %s work.</p>' % (
                "{:,.1f}".format(yearly).rstrip("0").rstrip("."), label, "{:,.1f}".format(yearly).rstrip("0").rstrip("."), g(monthly, 1), g(biweekly, 1), HPW_NOTE[h], g(pct, 1), band)),
            S("How the hours break down", table(
                ["Measure", "Hours"],
                [["Per week", label], ["Per bi-weekly period", g(biweekly, 2)], ["Per semi-monthly period (average)", g(yearly / 24, 2)], ["Per month (average)", g(monthly, 2)], ["Per quarter", g(yearly / 4, 1)], ["Per year (52 weeks)", g(yearly, 1)]]) +
              "<p>Spread over a 5-day week that is %s hours a day; over a 4-day week %s hours a day; over 3 days %s hours a day.</p>" % (g(d5), g(d4), g(d3))),
            S("Worked example", example("%s hours a week at $20 an hour" % label, (
                "<p>Weekly gross = %s%s = <b>%s</b>. Annual = %s &times; 52 = <b>%s</b>. Two unpaid weeks would remove %s, leaving %s.</p>") % (
                (g(h) + " h &times; $20") if ot == 0 else (g(reg) + " h &times; $20 + " + g(ot) + " h &times; $30"), "", m2(week_pay(h, 20)[2]),
                m2(week_pay(h, 20)[2]), m2(week_pay(h, 20)[2] * 52), m2(week_pay(h, 20)[2] * 2), m2(week_pay(h, 20)[2] * 50)))),
            S("Pay at common hourly rates", table(["Hourly rate", "Weekly", "52 weeks", "50 weeks (2 unpaid)"], pay_rows) + "<p>All figures are gross, before taxes%s.</p>" % (", and include federal overtime pay for hours above 40 in each week" if ot else "")),
            S("If you have unpaid time off", table(["Scenario", "Hours per year", "Hours per month"], unpaid_rows)),
            S("Overtime", "<p>%s See <a href=\"/overtime-calculator/\">overtime rules and the calculator</a> for state differences.</p>" % ot_text),
        ]
        faq = [
            ("How many hours a year is %s hours a week?" % label, "%s hours a week &times; 52 weeks = %s hours a year, before subtracting any unpaid time off." % (label, g(yearly, 1))),
            ("How many hours a month is %s hours a week?" % label, "About %s hours: %s &times; 52 &divide; 12." % (g(monthly, 1), label)),
            ("What is %s hours a week per day?" % label, "%s hours a day over five days, or %s hours over four days." % (g(d5), g(d4))),
            ("Is %s hours a week full time?" % label, "There is no single federal definition in the sources we cite; employers define it for benefits. A 40-hour week is the standard comparison and %s hours is %s%% of that." % (label, g(pct, 1))),
            ("Do I get overtime at %s hours a week?" % label, "Under the federal rule, non-exempt employees receive overtime for hours over 40 in a workweek. %s" % ("At %s hours that is %s hours of overtime per week." % (label, g(ot)) if ot else "At %s hours there is none." % label)),
        ]
        prev_next = []
        idx = HPW.index(h)
        for j in (idx - 1, idx + 1):
            if 0 <= j < len(HPW):
                prev_next.append("/hours-per-year/%s-hours-a-week/" % ("%g" % HPW[j]).replace(".", "-"))
        article_page(slug, "%s hours a week" % label, title, desc, "%s Hours a Week: Hours Per Year, Month and Pay Period" % label,
                     "How many hours %s a week adds up to over a month and a year, what it pays at common hourly rates and when overtime starts." % label,
                     sections, faq, sources=["dol23"], related=prev_next + ["/hours-per-year/", "/hourly-to-salary/", "/overtime-calculator/", "/time-card-calculator/"],
                     crumbs=[("/", "Home"), ("/hours-per-year/", "Hours per year"), (slug, "%s hours a week" % label)], kind="prog")


def hpw_index():
    rows = [['<a href="/hours-per-year/%s-hours-a-week/">%s hours a week</a>' % (("%g" % h).replace(".", "-"), "%g" % h), "{:,.1f}".format(h * 52).rstrip("0").rstrip("."), g(h * 52 / 12, 1), g(h * 2, 1)] for h in HPW]
    sections = [
        "<p>How many hours do you work in a year? Multiply the weekly hours by 52. These pages go further for each common schedule: hours per month and bi-weekly period, per-day splits, pay at common hourly rates, unpaid-week adjustments and overtime.</p>",
        table(["Hours a week", "Hours a year", "Hours a month", "Hours bi-weekly"], rows),
        S("How to calculate yearly hours", '<div class="formula">hours per year = hours per week &times; weeks worked per year</div><p>Full-time at 40 hours is 2,080 hours; subtract unpaid weeks from 52 first if you have them. Hourly pay times yearly hours is your gross annual pay; the <a href="/hourly-to-salary/">hourly to salary calculator</a> does it for you.</p>'),
    ]
    article_page("/hours-per-year/", "Hours Per Year Index", "Hours Per Year - How Many Hours a Year at 10 to 60 Hours a Week",
                 "Hours per year for any weekly schedule: 20, 30, 32, 35, 37.5, 40, 45, 50 hours a week and more, with monthly and bi-weekly hours.",
                 "Hours Per Year by Weekly Schedule", "Pick a weekly schedule to see its hours per year, month and pay period.", sections,
                 [("How many hours in a year at 40 hours a week?", "2,080 hours: 40 &times; 52."), ("How many working hours are in a month?", "About 173.3 for a 40-hour week: 2,080 &divide; 12."), ("Do unpaid weeks change the total?", "Yes. Subtract the unpaid weeks from 52 before multiplying.")],
                 related=["/hourly-to-salary/", "/hours/", "/time-card-calculator/"], crumbs=[("/", "Home"), ("/hours-per-year/", "Hours per year")], kind="hub")


# =============================================================== hourly to annual
RATES = [12, 13, 14, 15, 16, 17, 18, 19, 20, 22, 25, 28, 30, 35, 40, 45, 50]


def rate_pages():
    for r in RATES:
        slug = "/hourly-to-annual/%d-dollars-an-hour/" % r
        annual = r * 2080
        net, fed, ss, med = est_net_biweekly(annual / 26)
        part = [(20, "20 hours"), (30, "30 hours"), (32, "32 hours"), (35, "35 hours"), (40, "40 hours")]
        part_rows = [[lab, m0(r * hh * 52), m0(r * hh * 52 / 12), m0(r * hh * 2)] for hh, lab in part]
        ot45 = week_pay(45, r)[2]
        ot50 = week_pay(50, r)[2]
        raise1 = 2080
        hours_for_1000 = 1000.0 / r
        mult = r / FED_MIN
        note_h = {12: 35, 13: 28, 14: 24, 15: 32, 16: 36, 17: 30, 18: 25, 19: 33, 20: 37.5, 22: 29, 25: 38, 28: 31, 30: 34, 35: 26, 40: 22, 45: 27, 50: 23}[r]
        sections = [
            S("The answer", '<div class="answer-box"><div class="big">%s a year</div><div>$%d an hour &times; 40 hours &times; 52 weeks = <b>%s</b> gross, full time, before taxes. That is %s a month, %s every two weeks, and %s a week.</div></div>' % (
                m0(annual), r, m0(annual), m2(annual / 12), m2(annual / 26), m2(r * 40))),
            S("Pay by period at $%d an hour (40 hours a week)" % r, table(["Period", "Gross pay"], [
                ["Hourly", m2(r)], ["Daily (8 hours)", m2(r * 8)], ["Weekly", m2(r * 40)], ["Bi-weekly (26 checks)", m2(annual / 26)], ["Semi-monthly (24 checks)", m2(annual / 24)], ["Monthly", m2(annual / 12)], ["Annual", m0(annual)]])),
            S("Worked example: what a real schedule pays", example("$%d an hour at %s hours a week" % (r, "%g" % note_h), (
                "<p>%s hours &times; $%d = %s a week. Over 52 weeks that is <b>%s</b>, or %s a month on average. With two unpaid weeks off, it falls to %s.</p>") % (
                "%g" % note_h, r, m2(note_h * r), m0(note_h * r * 52), m2(note_h * r * 52 / 12), m0(note_h * r * 50)))),
            S("Part-time and full-time at $%d" % r, table(["Hours a week", "Annual", "Monthly", "Bi-weekly"], part_rows, hl=4)),
            S("Overtime at $%d an hour" % r, "<p>For a non-exempt employee under the federal weekly rule, hours over 40 are paid at 1.5 times the rate, or <b>%s</b> an hour. A 45-hour week pays %s (40 &times; $%d + 5 &times; %s), which is %s more than straight time. A 50-hour week pays %s. Annualised over 52 weeks, a regular 45-hour week at $%d an hour is %s. State daily-overtime rules can add more; use the <a href=\"/overtime-calculator/\">overtime calculator</a>.</p>" % (
                m2(r * 1.5), m2(ot45), r, m2(r * 1.5), m2(ot45 - 45 * r), m2(ot50), r, m0(ot45 * 52))),
            S("Estimated take-home pay at $%d an hour" % r, "<p>Our <a href=\"/paycheck-calculator/\">paycheck estimator</a> (federal tax only, single filer, no deductions, IRS 2026 Publication 15-T percentage method) estimates a bi-weekly check of about <b>%s</b> from %s gross: roughly %s federal income tax withholding, %s Social Security and %s Medicare. State and local taxes, a different W-4 and benefit deductions will change the result. This is an estimate, not a payslip.</p>" % (
                m2(net), m2(annual / 26), m2(fed), m2(ss), m2(med))),
            S("Putting $%d in context" % r, "<ul><li>$%d is %s times the federal minimum wage of $7.25 per hour (U.S. Department of Labor). Your state or city minimum may be higher.</li><li>A $1 raise from $%d adds %s a year at full time, a %s%% increase.</li><li>You earn $%s per minute and need about %s hours of work to gross $1,000.</li></ul>" % (
                r, g(mult, 2), r, m0(raise1), g(100.0 / r, 1), g(r / 60.0, 3), g(hours_for_1000, 1))),
        ]
        faq = [
            ("How much is $%d an hour a year?" % r, "$%d &times; 40 hours &times; 52 weeks = %s a year gross, full time." % (r, m0(annual))),
            ("How much is $%d an hour a month?" % r, "About %s a month before taxes: %s &divide; 12." % (m2(annual / 12), m0(annual))),
            ("How much is $%d an hour bi-weekly?" % r, "%s per check: $%d &times; 80 hours." % (m2(r * 80), r)),
            ("How much is $%d an hour after taxes?" % r, "A federal-only estimate for a single filer is about %s per bi-weekly check (see the paycheck estimator); your real figure depends on your state, W-4 and deductions." % m2(net)),
            ("What is $%d an hour with overtime?" % r, "Overtime hours are paid at %s an hour for non-exempt employees under the federal weekly rule. A 45-hour week pays %s." % (m2(r * 1.5), m2(ot45))),
        ]
        idx = RATES.index(r)
        rel = []
        for j in (idx - 1, idx + 1):
            if 0 <= j < len(RATES):
                rel.append("/hourly-to-annual/%d-dollars-an-hour/" % RATES[j])
        article_page(slug, "$%d an hour" % r, "$%d an Hour Is How Much a Year? %s Full Time (After Tax Estimate)" % (r, m0(annual)),
                     "$%d an hour is %s a year full time: %s a month, %s bi-weekly. Part-time totals, overtime pay, estimated take-home and a $1-raise comparison." % (r, m0(annual), m0(annual / 12), m0(annual / 26)),
                     "$%d an Hour Is How Much a Year?" % r,
                     "Annual, monthly, bi-weekly and weekly pay at $%d an hour, with part-time schedules, overtime and an estimated take-home figure." % r,
                     sections, faq, sources=["dol23", "dol_minwage", "irs15t"], source_note="Take-home figures are estimates from the IRS 2026 percentage method.",
                     related=rel + ["/hourly-to-annual/", "/hourly-to-salary/", "/salary-to-hourly/", "/paycheck-calculator/"],
                     crumbs=[("/", "Home"), ("/hourly-to-annual/", "Hourly to annual"), (slug, "$%d an hour" % r)], kind="prog")


def rate_index():
    rows = [['<a href="/hourly-to-annual/%d-dollars-an-hour/">$%d an hour</a>' % (r, r), m0(r * 2080), m0(r * 2080 / 12), m0(r * 80), m0(r * 40)] for r in RATES]
    sections = [
        "<p>Full-time pay is hourly rate &times; 2,080 (40 hours &times; 52 weeks). Choose a rate for the detail: monthly, bi-weekly and weekly pay, part-time schedules, overtime and an estimated take-home figure.</p>",
        table(["Hourly rate", "Annual (full time)", "Monthly", "Bi-weekly", "Weekly"], rows),
        S("Quick rule of thumb", '<p>Double the hourly rate and add three zeros for a fast annual estimate: $20 an hour &rarr; about $40,000 (exactly $41,600). For a precise result including unpaid weeks, use the <a href="/hourly-to-salary/">hourly to salary calculator</a>.</p>'),
    ]
    article_page("/hourly-to-annual/", "Hourly to Annual Pay Tables", "Hourly Rate to Annual Salary - $12 to $50 an Hour Pay Tables",
                 "Convert hourly rates to annual salary: tables and detail pages for $12, $15, $20, $25, $30, $40, $50 an hour with monthly, bi-weekly and weekly pay.",
                 "Hourly Rate to Annual Salary Tables", "See what every common hourly rate pays per year, month, bi-weekly check and week.",
                 sections, [("How do I convert hourly to annual?", "Multiply by 2,080 for a full-time year (40 hours &times; 52 weeks)."), ("What is $20 an hour per year?", "$41,600 full time."), ("Are these gross or net amounts?", "Gross, before taxes. Use the paycheck estimator for an estimate of take-home pay.")],
                 related=["/hourly-to-salary/", "/salary-to-hourly/", "/paycheck-calculator/"], crumbs=[("/", "Home"), ("/hourly-to-annual/", "Hourly to annual")], kind="hub")


# =============================================================== hh:mm to decimal charts
DEC_MIN = {1: 10, 2: 15, 3: 20, 4: 25, 5: 30, 6: 35, 7: 40, 8: 45, 9: 50, 10: 55, 11: 5, 12: 12}
DEC_NOTE = {
    1: "One hour is the building block: every minute you add is the decimal part of the hour.",
    2: "Two hours is a short task or a brief overtime stretch.",
    3: "Three hours often shows up as a short shift or a block of overtime on the end of a day.",
    4: "Four hours is a half-day shift, the length of many part-time and school-hours jobs.",
    5: "Five hours is a long part-time shift and the point where many break rules start to matter.",
    6: "Six hours is a short full day of work after an unpaid break is deducted.",
    7: "Seven hours is a common paid day in jobs with a 7.5-hour schedule or a one-hour unpaid lunch on a shorter shift.",
    8: "Eight hours is the standard paid workday, the figure behind the 40-hour week.",
    9: "Nine hours is a long day or an 8-hour day plus an hour of overtime.",
    10: "Ten hours is the shift length of a four-day, 40-hour week.",
    11: "Eleven hours is a long shift where daily overtime may apply in some states.",
    12: "Twelve hours is a long-rotation shift, and the point where double time can begin in California.",
}


def decimal_pages():
    for h in range(1, 13):
        slug = "/decimal-hours/%d-hours-chart/" % h
        m = DEC_MIN[h]
        ex_dec = h + m / 60.0
        rows = []
        for mm in range(0, 60, 5):
            d = h + mm / 60.0
            rows.append(["%d:%02d" % (h, mm), "%.4f" % d, "%.2f" % d, m2(round(d, 2) * 15), m2(round(d, 2) * 20), m2(round(d, 2) * 25)])
        full = [["%d:%02d" % (h, mm), "%.2f" % (h + mm / 60.0)] for mm in range(60)]
        quarters = [full[i:i + 15] for i in range(0, 60, 15)]
        fulltxt = "".join("<h3>%d:%02d to %d:%02d</h3>%s" % (h, i * 15, h, i * 15 + 14, table(["hh:mm", "Decimal"], q, num_from=1)) for i, q in enumerate(quarters))
        five = ex_dec * 5
        sections = [
            S("%d hours and minutes as decimals" % h, "<p>%s To convert %d hours and any number of minutes, add the minutes &divide; 60 to %d. The table below does it in 5-minute steps and shows the pay at $15, $20 and $25 an hour.</p>" % (DEC_NOTE[h], h, h) + table(
                ["Time", "Decimal (4 places)", "Decimal (2 places)", "Pay at $15", "Pay at $20", "Pay at $25"], rows)),
            S("Worked example: %d:%02d" % (h, m), example("%d hours %d minutes" % (h, m), (
                "<p>%d minutes &divide; 60 = %s, so %d:%02d = %d + %s = <b>%s hours</b> (rounded to two places: %.2f).</p>"
                "<p>Pay at $18.00 an hour: %s &times; $18 = <b>%s</b>. Five days of %d:%02d = %s decimal hours (%s) = %s.</p>") % (
                m, g(m / 60.0, 4), h, m, h, g(m / 60.0, 4), g(ex_dec, 4), ex_dec, g(ex_dec, 2), m2(round(ex_dec, 2) * 18), h, m, g(five, 2), hm(five), m2(round(five, 2) * 18)))),
            S("Going the other way", "<p>To turn a decimal like %s back into hours and minutes, keep the whole hours (%d) and multiply the decimal part by 60: 0.%s &times; 60 = %s minutes. Use the <a href=\"/decimal-hours-converter/\">decimal hours converter</a> for any value.</p>" % (
                g(ex_dec, 2), h, ("%.2f" % ex_dec).split(".")[1], g(round(ex_dec, 2) % 1 * 60, 1))),
            S("Every minute from %d:00 to %d:59" % (h, h), fulltxt),
        ]
        faq = [
            ("What is %d:%02d in decimal hours?" % (h, m), "%s hours: %d + %d/60." % (g(ex_dec, 2), h, m)),
            ("What is %d hours 30 minutes in decimal?" % h, "%d.5 hours." % h),
            ("What is %d hours 15 minutes in decimal?" % h, "%d.25 hours." % h),
            ("What is %d hours 45 minutes in decimal?" % h, "%d.75 hours." % h),
            ("Why does my time card show %d.50 instead of %d:50?" % (h, h), "Because the decimal .50 is half an hour (30 minutes). %d:50 equals %s decimal hours." % (h, g(h + 50 / 60.0, 2))),
        ]
        nxt = []
        for j in (h - 1, h + 1):
            if 1 <= j <= 12:
                nxt.append("/decimal-hours/%d-hours-chart/" % j)
        article_page(slug, "%d hours decimal chart" % h, "%d Hours in Decimal: hh:mm to Decimal Chart for %d:00-%d:59" % (h, h, h),
                     "Convert %d hours and any minutes to decimal hours: full %d:00 to %d:59 chart, pay at $15-$25 an hour and a worked example for %d:%02d." % (h, h, h, h, m),
                     "%d Hours and Minutes to Decimal Chart" % h,
                     "Every time from %d:00 to %d:59 as decimal hours, with pay at common rates." % (h, h), sections, faq,
                     related=nxt + ["/decimal-hours/", "/decimal-hours-converter/", "/minutes-to-decimal-chart/", "/time-card-calculator/"],
                     crumbs=[("/", "Home"), ("/decimal-hours/", "Decimal hours charts"), (slug, "%d hours" % h)], kind="prog")


def decimal_index():
    lis = "".join('<a class="chip" href="/decimal-hours/%d-hours-chart/">%d hours</a>' % (h, h) for h in range(1, 13))
    sections = [
        "<p>Payroll multiplies decimal hours by a rate, but time cards show hours and minutes. Each chart below lists every minute for a given number of hours with the decimal value, plus pay at several rates. For minutes only (0-59) use the <a href=\"/minutes-to-decimal-chart/\">minutes to decimal chart</a>.</p>",
        '<div class="chips">%s</div>' % lis,
        S("The one-line formula", '<div class="formula">decimal = hours + minutes &divide; 60</div><p>15 minutes = 0.25, 30 = 0.50, 45 = 0.75. All other minutes are repeating or rounded decimals.</p>'),
    ]
    article_page("/decimal-hours/", "Decimal Hours Charts", "Hours and Minutes to Decimal Charts - 1 to 12 Hours",
                 "hh:mm to decimal hours charts for 1 to 12 hours: every minute converted, with pay at $15, $20 and $25 an hour.",
                 "Hours and Minutes to Decimal Charts", "Choose the number of hours, then read the decimal for any minute.", sections,
                 [("What is 7:30 in decimal?", "7.5 hours."), ("How do I convert minutes to decimal?", "Divide by 60."), ("What is 15 minutes in decimal hours?", "0.25 hours.")],
                 related=["/decimal-hours-converter/", "/minutes-to-decimal-chart/", "/time-duration-calculator/"], crumbs=[("/", "Home"), ("/decimal-hours/", "Decimal hours charts")], kind="hub")


def build():
    shifts = [(a, b) for a in range(6, 11) for b in range(14, 21) if b > a]
    SHIFT_SET.update(shifts)
    shift_pages(shifts)
    hours_index(shifts)
    hpw_pages()
    hpw_index()
    rate_pages()
    rate_index()
    decimal_pages()
    decimal_index()
    return shifts
