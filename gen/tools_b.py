"""Calculator pages, part B: decimals, pay, PTO, breaks, differentials, schedules, military time, rounding."""
from .core import tool_page, table, example
from . import forms
from .tools_a import S


def minute_chart_rows(step=5):
    return [["%d min" % m, "%.4f" % (m / 60.0), "%.2f" % (m / 60.0)] for m in range(0, 60, step)]


def build():
    # ------------------------------------------------------------------ decimal hours converter
    a, b = forms.decimal_tools()
    tool_page(
        "/decimal-hours-converter/", "Decimal Hours Converter",
        "Decimal Hours Converter - hh:mm to Decimal and Decimal to hh:mm",
        "Convert hours and minutes to decimal hours (7:45 = 7.75) and decimal hours back to hh:mm. Includes a conversion table and the exact formula for payroll.",
        "Decimal Hours Converter: hh:mm to Decimal and Back",
        "Payroll software usually wants 7.75 where your time card says 7:45. These two converters translate in both directions and show the working, and the tables below cover the common values.",
        a + b,
        [
            S("The two formulas", """
<div class="formula">decimal hours = hours + (minutes &divide; 60)</div>
<div class="formula">minutes = (decimal part of the hours) &times; 60</div>
<p>Example, hh:mm to decimal: 7 hours 45 minutes. 45 &divide; 60 = 0.75, so the decimal is 7 + 0.75 = <b>7.75</b>.</p>
<p>Example, decimal to hh:mm: 7.75 hours. The whole number is 7 hours; 0.75 &times; 60 = 45 minutes, so <b>7:45</b>.</p>"""),
            S("Worked examples with awkward minutes", example("8 hours 20 minutes", "<p>20 &divide; 60 = 0.3333&hellip;, so 8:20 is 8.3333&hellip; hours. Rounded to two places that is <b>8.33</b>. At $24.00/hour the exact pay is 8.3333 &times; $24 = $200.00, while 8.33 &times; $24 = $199.92. The 8-cent difference is why some payroll systems keep three or four decimal places.</p>") +
              example("6 hours 10 minutes", "<p>10 &divide; 60 = 0.1667, so 6:10 is 6.17 hours (rounded). Going back: 0.17 &times; 60 = 10.2 minutes, which rounds to 10, so 6.17 converts back to 6:10.</p>") +
              example("Decimal to time: 37.4 hours", "<p>0.4 &times; 60 = 24 minutes, so 37.4 hours is <b>37:24</b>, not 37:40. This is the mistake people make most often when they read the decimal part as minutes.</p>")),
            S("Quarter-hour and common conversions", table(
                ["Minutes", "Decimal hours", "Rounded (2 places)"], minute_chart_rows(5)) +
              '<p>The quarter-hour marks are the ones to memorise: 15 minutes = 0.25, 30 minutes = 0.50, 45 minutes = 0.75. The full 1-to-59 minute chart is on the <a href="/minutes-to-decimal-chart/">minutes to decimal chart</a>, and the <a href="/decimal-hours/">hours chart index</a> has a table for every hour from 1 to 12.</p>'),
            S("Why a time card is converted to decimals", """
<p>Pay is hours multiplied by rate. Multiplying 7:45 by $18.00 is awkward; 7.75 &times; $18.00 = $139.50 is simple. Payroll systems, invoices and spreadsheets store decimals for that reason. Time clocks that round to the nearest 6 minutes use tenths of an hour (6 minutes = 0.1), which makes every entry an exact one-decimal number. See <a href="/time-rounding-calculator/">rounding</a> for how that works.</p>"""),
        ],
        [("How do you convert minutes to decimal hours?", "Divide the minutes by 60. 45 minutes is 45 &divide; 60 = 0.75 hours."),
         ("How do I convert 7:45 to a decimal?", "7 + 45/60 = 7.75."),
         ("What is 8.5 hours in hours and minutes?", "8 hours and 30 minutes: 0.5 &times; 60 = 30."),
         ("Why is 0.30 hours not 30 minutes?", "Because the decimal is a fraction of an hour. 0.30 hours is 0.30 &times; 60 = 18 minutes. 30 minutes is 0.50 hours."),
         ("How many decimal places should I use?", "Follow your payroll system. Two places is common; for exact pay keep more places until the final rounding.")],
        related=["/minutes-to-decimal-chart/", "/time-duration-calculator/", "/time-rounding-calculator/", "/decimal-hours/", "/time-card-calculator/"],
    )

    # ------------------------------------------------------------------ minutes to decimal chart
    chart_rows = []
    for m in range(0, 60):
        chart_rows.append(["%d" % m, "%.3f" % (m / 60.0), "%.2f" % (m / 60.0)])
    quarters = [chart_rows[i:i + 15] for i in range(0, 60, 15)]
    big_chart = ""
    for qi, q in enumerate(quarters):
        big_chart += "<h3>%d to %d minutes</h3>" % (qi * 15, qi * 15 + 14) + table(["Minutes", "Decimal hours (3 places)", "Rounded (2 places)"], q)
    tool_page(
        "/minutes-to-decimal-chart/", "Minutes to Decimal Chart",
        "Minutes to Decimal Chart - 1 to 59 Minutes in Decimal Hours",
        "Minutes to decimal hours chart for payroll: every minute from 0 to 59 converted to a decimal, plus a calculator for any number of minutes.",
        "Minutes to Decimal Chart (0-59 Minutes)",
        "Look up any minute value from 0 to 59, or convert a longer total such as 410 minutes. The chart gives three decimal places for exact pay and the two-place figure most payroll forms use.",
        forms.minutes_tool(),
        [
            S("How to use the chart", """
<p>Find the minutes on the time card in the left column and read the decimal across. For 7 hours 37 minutes, take the 37-minute value (0.617 or 0.62 rounded) and add it to 7 for 7.62 hours. If you have a long list of minutes rather than hours and minutes, convert the total with the calculator above: 410 minutes is 410 &divide; 60 = 6.83 hours, or 6:50.</p>
<div class="formula">decimal hours = minutes &divide; 60</div>"""),
            S("Worked example: a week of minutes", example("Five shifts of minutes, $17.50 an hour", """
<p>An employee has these paid minutes: 485, 492, 510, 478, 465. The total is 2,430 minutes. 2,430 &divide; 60 = <b>40.5 hours</b> (40:30). Federal overtime starts after 40 hours in a workweek, so 0.5 hour is overtime. Pay = 40 &times; $17.50 + 0.5 &times; $26.25 = $700.00 + $13.13 = <b>$713.13</b> (rounded to the cent).</p>""")),
            S("Full minutes chart", big_chart),
            S("Tenth-of-an-hour (6-minute) shortcut", """
<p>Some time clocks record time in tenths of an hour. Each 6 minutes is 0.1, so 12 minutes is 0.2, 18 is 0.3, 30 is 0.5, 42 is 0.7, 54 is 0.9. Because 6 does not divide into every minute value, punches are usually rounded to the nearest 6 minutes first. The rounding page explains the effect.</p>"""),
        ],
        [("What is 30 minutes in decimal?", "0.5 hours."),
         ("What is 15 minutes in decimal?", "0.25 hours."),
         ("What is 45 minutes as a decimal?", "0.75 hours."),
         ("How do I convert 410 minutes to hours?", "410 &divide; 60 = 6.8333 hours, which is 6 hours and 50 minutes."),
         ("Why do some charts show 0.02 for 1 minute and some show 0.017?", "1 &divide; 60 is 0.016667. Rounded to two places that is 0.02; to three places it is 0.017. Use more places when the totals are large or you need exact pay.")],
        related=["/decimal-hours-converter/", "/time-duration-calculator/", "/decimal-hours/", "/time-rounding-calculator/"],
    )

    # ------------------------------------------------------------------ paycheck estimator
    tool_page(
        "/paycheck-calculator/", "Paycheck Estimator",
        "Paycheck Estimator - Gross to Net Pay (2026 Federal, Simple)",
        "Simple paycheck estimator: turn hourly pay or gross wages into estimated take-home pay using 2026 IRS federal withholding tables, Social Security and Medicare.",
        "Paycheck Estimator: Gross Pay to Take-Home Pay",
        "A simple estimate, clearly not a payslip. It subtracts federal income tax withholding (IRS Publication 15-T, 2026 percentage method), Social Security and Medicare from your gross pay, plus pre-tax deductions and a state percentage you choose.",
        forms.paycheck(),
        [
            S("What this estimator includes - and what it leaves out", """
<table class="plain" style="width:auto"><tbody>
<tr><td><b>Included</b></td><td>Federal income tax withholding per the IRS 2026 percentage method (standard Step 1 only), Social Security 6.2% up to the $184,500 wage base, Medicare 1.45%, pre-tax health and retirement deductions, an optional state/local percentage you enter, and any other flat withholding.</td></tr>
<tr><td><b>Not included</b></td><td>W-4 Step 2 (multiple jobs), Step 3 credits, Step 4 adjustments, state and local tax tables, post-tax deductions such as garnishments, tips, bonuses taxed as supplemental wages, additional Medicare tax for high earners, and anything specific to your employer.</td></tr>
</tbody></table>
<p>It is therefore a ballpark. If you need your real number, check your last pay stub and Form W-4, or ask your payroll department.</p>"""),
            S("How the estimate is built", """
<ol>
<li><b>Gross pay per period.</b> For hourly pay: weekly gross &times; 52 &divide; pay periods. Overtime hours are paid at 1.5 times your rate.</li>
<li><b>Taxable wages.</b> Gross pay minus the pre-tax deductions you enter. Health or cafeteria-plan deductions reduce income tax and Social Security/Medicare wages; 401(k)-type deferrals reduce income-tax wages only.</li>
<li><b>Annualise.</b> Multiply by the number of pay periods, then subtract the Pub 15-T standard amount ($8,600 for single, $12,900 for married filing jointly) to get the adjusted annual wage.</li>
<li><b>Apply the IRS rate table.</b> The 2026 schedule for single filers starts at 0% up to $7,500, then 10% to $19,900, 12% to $57,900, 22% to $113,200, 24% to $209,275, and so on. Married filing jointly starts 0% up to $19,300, then 10% to $44,100, 12% to $120,100, and so on.</li>
<li><b>Divide by the pay periods</b> to get withholding for one paycheck.</li>
<li><b>Add Social Security and Medicare</b> and subtract everything from gross.</li>
</ol>"""),
            S("Worked example: $2,000 bi-weekly, single", example("Hand calculation", """
<p>Gross $2,000 &times; 26 = $52,000 a year. Subtract $8,600: adjusted annual wage $43,400. The single schedule's 12% row starts at $19,900 with a base of $1,240, so tax = $1,240 + 12% &times; ($43,400 &minus; $19,900) = $1,240 + $2,820 = $4,060 a year. Divided by 26 = <b>$156.15</b> per paycheck.</p>
<p>Social Security: $2,000 &times; 6.2% = <b>$124.00</b>. Medicare: $2,000 &times; 1.45% = <b>$29.00</b>.</p>
<p>Estimated take-home = $2,000.00 &minus; $156.15 &minus; $124.00 &minus; $29.00 = <b>$1,690.85</b> (before any state or local tax).</p>""")),
            S("Reading the result", """
<p>The estimator shows take-home as a percentage of gross for your own inputs. Use the annual column to see how a raise would change the year, and compare it with the <a href="/hourly-to-salary/">hourly to salary converter</a> to see gross income at your rate.</p>"""),
        ],
        [("How accurate is this paycheck estimator?", "It is an estimate. Federal figures follow the IRS 2026 Publication 15-T percentage method for a W-4 with no credits or adjustments. Your employer's payroll system, state taxes and deductions will change the real amount."),
         ("Why does it ask for a state percentage?", "State and local income tax systems differ widely and change often. Instead of guessing, we let you enter your own estimated percentage; leave it at 0 to see federal only."),
         ("What is the Social Security wage base?", "For 2026 the IRS lists the Social Security wage base limit as $184,500 in Publication 15. Social Security tax stops on wages above that amount in the year. Medicare tax has no limit."),
         ("Does overtime change my withholding?", "Overtime raises gross pay for the period, and because withholding is estimated by annualising that period's pay, a big overtime week can look like a high-income year to the formula. Over the full year, tax is settled when you file your return."),
         ("Is this calculator for salaried workers too?", "Yes. Choose Gross pay per period and type the salary divided by the number of pay periods.")],
        sources=["irs15", "irs15t"],
        source_note="Tax figures are for 2026 and will change; the page's tables must be updated each year (see NOTES.md in the repository).",
        related=["/hourly-to-salary/", "/overtime-calculator/", "/salary-to-hourly/", "/guides/bi-weekly-vs-semi-monthly-pay/"],
    )

    # ------------------------------------------------------------------ hourly to salary
    rates = [15, 18, 20, 25, 30, 40]
    rows = [["$%d" % r, "${:,.0f}".format(r * 40), "${:,.0f}".format(r * 40 * 2), "${:,.0f}".format(r * 2080 / 12), "${:,.0f}".format(r * 2080)] for r in rates]
    tool_page(
        "/hourly-to-salary/", "Hourly to Salary Calculator",
        "Hourly to Salary Calculator - Yearly, Monthly & Bi-Weekly Pay",
        "Hourly to salary calculator: convert an hourly wage to annual, monthly, bi-weekly, semi-monthly, weekly and daily pay, with hours per week and unpaid weeks off.",
        "Hourly to Salary Calculator",
        "Multiply your hourly wage by the hours you really work and the weeks you are paid. Change hours per week or add unpaid weeks off for part-time, seasonal or school-year work.",
        forms.hourly_salary("h2s"),
        [
            S("The formula", """
<div class="formula">annual pay = hourly rate &times; hours per week &times; paid weeks per year</div>
<p>A full-time year is usually counted as 40 &times; 52 = 2,080 hours. That is the figure behind most &ldquo;hourly to salary&rdquo; rules of thumb: <b>double the hourly rate and add three zeros</b> gets you within a few percent ($20/hour is about $41,600). Everything is gross pay, before taxes and deductions.</p>
<p>Monthly pay is annual &divide; 12, bi-weekly is annual &divide; 26 and semi-monthly is annual &divide; 24. Weekly and daily are shown for a normal 5-day week.</p>"""),
            S("Worked examples", example("$20 an hour, full time", "<p>$20 &times; 40 &times; 52 = <b>$41,600</b>. Monthly: $41,600 &divide; 12 = $3,466.67. Bi-weekly check: $41,600 &divide; 26 = $1,600.00. Semi-monthly check: $41,600 &divide; 24 = $1,733.33.</p>") +
              example("$20 an hour with two unpaid weeks off", "<p>Paid weeks = 52 &minus; 2 = 50. $20 &times; 40 &times; 50 = <b>$40,000</b>, which is $1,600 less than the full-year figure. Enter 2 in the unpaid weeks box to check your own year.</p>") +
              example("$18.50 an hour, 32 hours a week", "<p>$18.50 &times; 32 &times; 52 = <b>$30,784</b>. Part-time hours cut annual income proportionally, but benefits or eligibility rules can also depend on hours.</p>") +
              example("Overtime is not included", "<p>The calculator assumes straight time. A worker at $20 an hour regularly working 45 hours earns about 5 &times; $10 extra each week in overtime premium (5 hours at the extra half rate), or $2,600 a year more, if they are non-exempt under the federal rule. Use the <a href=\"/overtime-calculator/\">overtime calculator</a> for that.</p>")),
            S("Quick table at 40 hours a week, 52 weeks", table(["Hourly", "Weekly", "Bi-weekly", "Monthly", "Annual"], rows, hl=2) +
              '<p>See any rate in detail: <a href="/hourly-to-annual/">hourly rate to annual salary pages</a> for $12 to $50 an hour.</p>'),
            S("Hourly versus salary: what changes", """
<p>An hourly worker is paid for hours worked, and non-exempt hourly employees receive overtime pay over 40 hours in a workweek. A salaried employee is paid a fixed amount per pay period; whether overtime is owed depends on whether the job is exempt, not on the pay method. Our <a href="/guides/exempt-vs-non-exempt/">exempt vs non-exempt guide</a> explains the difference. To go the other way, use the <a href="/salary-to-hourly/">salary to hourly calculator</a>.</p>"""),
        ],
        [("How do you convert hourly pay to an annual salary?", "Multiply the hourly rate by hours per week and by paid weeks per year. At 40 hours and 52 weeks, $20 an hour is $41,600."),
         ("How many working hours are in a year?", "2,080 for a standard full-time year (40 hours x 52 weeks), before subtracting unpaid time off."),
         ("Is $25 an hour a good salary?", "$25 an hour at 40 hours a week is $52,000 a year, or $2,000 per bi-weekly check, before taxes. Whether that is good depends on where you live and your costs."),
         ("Does this include taxes?", "No. These are gross figures. Use the paycheck estimator to estimate take-home pay."),
         ("Should I use 52 weeks or fewer?", "Use 52 if you are paid every week of the year, including paid vacation and holidays. Use fewer if you have unpaid time off, such as school-year or seasonal work.")],
        related=["/salary-to-hourly/", "/hourly-to-annual/", "/paycheck-calculator/", "/overtime-calculator/", "/pto-accrual-calculator/"],
    )

    # ------------------------------------------------------------------ salary to hourly
    sal = [30000, 40000, 50000, 60000, 75000, 100000]
    srows = [["${:,.0f}".format(s), "${:.2f}".format(s / 2080.0), "${:,.0f}".format(s / 26), "${:,.0f}".format(s / 24), "${:,.0f}".format(s / 12)] for s in sal]
    tool_page(
        "/salary-to-hourly/", "Salary to Hourly Calculator",
        "Salary to Hourly Calculator - Annual Salary to Hourly Wage",
        "Salary to hourly calculator: divide an annual salary by the hours you really work. Includes hours per week, unpaid weeks off, and bi-weekly and monthly pay.",
        "Salary to Hourly Calculator",
        "A salary hides how many hours it takes to earn it. Enter the salary and your real weekly hours to see the hourly rate, and discover how a 50-hour week changes it.",
        forms.hourly_salary("s2h"),
        [
            S("The formula", """
<div class="formula">hourly rate = annual salary &divide; (hours per week &times; paid weeks per year)</div>
<p>For a standard full-time year, divide by 2,080 (40 &times; 52). A $52,000 salary is exactly $25.00 an hour. The shortcut: <b>take off three zeros and halve it</b> (52,000 &rarr; 52 &rarr; 26, close to $25).</p>"""),
            S("Worked examples", example("$62,000 salary, 40 hours", "<p>$62,000 &divide; 2,080 = <b>$29.81</b> per hour (29.8077 before rounding).</p>") +
              example("Same $62,000, but a 50-hour week", "<p>Hours per year = 50 &times; 52 = 2,600. $62,000 &divide; 2,600 = <b>$23.85</b>. Working ten extra hours a week lowers the effective hourly pay by about $5.96, which is why the true hours matter when you compare job offers.</p>") +
              example("$60,000 with two unpaid weeks", "<p>Paid weeks = 50, so $60,000 &divide; (40 &times; 50) = <b>$30.00</b> per hour.</p>")),
            S("Quick table (40 hours, 52 weeks)", table(["Salary", "Hourly", "Bi-weekly check", "Semi-monthly check", "Monthly"], srows)),
            S("Things that make the hourly figure misleading", """
<ul>
<li><b>Unpaid overtime.</b> If you are an exempt salaried employee you may work more than 40 hours without extra pay. If you are non-exempt, you are owed overtime. See <a href="/guides/exempt-vs-non-exempt/">exempt vs non-exempt</a>.</li>
<li><b>Benefits.</b> Health insurance, retirement matching and paid leave are not in the salary figure.</li>
<li><b>Taxes.</b> Everything here is gross. Use the <a href="/paycheck-calculator/">paycheck estimator</a> for take-home pay.</li>
</ul>"""),
        ],
        [("How do I convert salary to an hourly rate?", "Divide the annual salary by the number of hours you work in a year, usually 2,080 for full time."),
         ("What is $50,000 a year per hour?", "$50,000 &divide; 2,080 = $24.04 per hour at 40 hours a week."),
         ("What is $100,000 a year per hour?", "$100,000 &divide; 2,080 = $48.08 per hour."),
         ("Why is my effective hourly rate lower than the calculator says?", "Because you work more hours than 40. Enter your real weekly hours."),
         ("Should paid vacation reduce the hours?", "No. Paid time off is part of the salary, so keep 52 paid weeks. Only reduce weeks for unpaid time.")],
        related=["/hourly-to-salary/", "/hourly-to-annual/", "/paycheck-calculator/", "/guides/bi-weekly-vs-semi-monthly-pay/"],
    )

    # ------------------------------------------------------------------ PTO accrual
    tool_page(
        "/pto-accrual-calculator/", "PTO Accrual Calculator",
        "PTO Accrual Calculator - Vacation Hours Per Pay Period & Balance",
        "PTO accrual calculator: find how many vacation hours you earn per pay period or per hour worked, project your balance and see the effect of a PTO cap.",
        "PTO and Vacation Accrual Calculator",
        "Employers grant paid time off in different ways: a number of hours each pay period, days per year or one hour for every so many hours worked. Enter yours to see what you earn and what your balance will be.",
        forms.pto(),
        [
            S("Three common accrual methods", """
<ol>
<li><b>Hours per pay period.</b> The handbook says, for example, 3.08 hours bi-weekly. Annual PTO = hours &times; number of pay periods.</li>
<li><b>Days per year.</b> 15 days &times; 8 hours = 120 hours a year, divided across your pay periods.</li>
<li><b>Hours worked.</b> &ldquo;1 hour for every 30 hours worked&rdquo; means a full-time employee at 2,080 hours earns 2,080 &divide; 30 = 69.3 hours a year. Part-time staff earn proportionally less.</li>
</ol>
<p>Your employer's policy decides the method, the waiting period, whether PTO can roll over and whether it is paid out when you leave. The Department of Labor says the FLSA does not require payment for time not worked, such as vacations, sick leave or holidays, and leaves those benefits to employers and employees to decide. State laws vary on payout and sick leave, so check your state's labor department.</p>"""),
            S("Worked examples", example("15 days a year, paid bi-weekly", "<p>15 &times; 8 = 120 hours a year. &divide; 26 pay periods = <b>4.62 hours</b> per paycheck. After 13 pay periods (about 6 months) the balance is 60 hours, if none is used.</p>") +
              example("Same 120 hours, semi-monthly", "<p>120 &divide; 24 = <b>5.00 hours</b> per paycheck. The yearly total is identical; only the size of each accrual changes.</p>") +
              example("A balance cap", "<p>Accrual of 4 hours per bi-weekly period with an 80-hour cap and no PTO used reaches the cap after 20 pay periods. For the remaining 6 periods of a 26-period year, 24 hours of accrual are lost to the cap. Use the cap box above to see how much you would lose and plan time off before you hit it.</p>")),
            S("Planning tips", """
<ul>
<li>Check how your employer treats the accrual at the moment you hit the cap: some stop accruing, some pay out.</li>
<li>Use the planned PTO box to see the balance after you take trips during the year.</li>
<li>If your PTO is a lump sum on January 1 rather than accrued, enter it as the starting balance and set accrual to 0.</li>
<li>Combine this with the <a href="/work-schedule-planner/">work schedule planner</a> to map days off.</li>
</ul>"""),
        ],
        [("How do I calculate PTO accrual per pay period?", "Divide annual PTO hours by the number of pay periods. 120 hours a year over 26 bi-weekly periods is 4.62 hours each."),
         ("How much PTO is 15 days?", "At 8 hours a day, 15 days is 120 hours."),
         ("Do part-time employees accrue PTO?", "Only if the employer's policy provides it. Accrual based on hours worked automatically scales with hours."),
         ("Are employers required to provide PTO?", "The Department of Labor says the FLSA does not require payment for time not worked, such as vacations, sick leave or holidays. State or local laws may add requirements, so check your state labor department."),
         ("What is a PTO cap?", "A limit on the balance you can hold. Once reached, accrual stops until you use time.")],
        related=["/hourly-to-salary/", "/work-schedule-planner/", "/time-card-calculator/", "/guides/bi-weekly-vs-semi-monthly-pay/"],
        extra_sources=[("U.S. Department of Labor, Vacation Leave", "https://www.dol.gov/general/topic/workhours/vacation_leave")],
    )

    # ------------------------------------------------------------------ lunch break calculator
    tool_page(
        "/lunch-break-calculator/", "Lunch Break Calculator",
        "Lunch Break Calculator - Paid Hours After an Unpaid Meal Break",
        "Lunch break calculator: subtract an unpaid meal break from your shift to see paid hours, auto-deduct rules, weekly totals and what the break costs in pay.",
        "Lunch and Unpaid Break Calculator",
        "Enter clock-in and clock-out times and the length of the unpaid meal. See your paid hours per day and week, whether an automatic deduction applies and how much the break costs you.",
        forms.lunch(),
        [
            S("Which breaks are paid and which are not", """
<p>Federal regulations separate two kinds of breaks. A <b>bona fide meal period</b> is not work time: 29 CFR 785.19 says the employee must be completely relieved from duty for the purposes of eating regular meals, and that ordinarily 30 minutes or more is long enough. A <b>rest period</b> is different: 29 CFR 785.18 describes rest periods of short duration, running from 5 minutes to about 20 minutes, which are common in industry, usually paid and counted as hours worked.</p>
<p>So subtract the lunch only if you are really off duty. If you eat at your desk, answer the phone or stay on call, the time is generally hours worked and should be paid. The federal rules set minimums; states can require more. The DOL's state table lists, for example, a 30-minute meal period after 5 hours in California and Colorado, and after 8 continuous hours in Nevada; read our <a href="/guides/meal-and-rest-break-laws/">meal and rest break guide</a>.</p>"""),
            S("Worked examples", example("8:00 am to 5:00 pm with a 30-minute lunch", "<p>Clock to clock: 9:00. Minus 30 minutes = <b>8:30</b> paid (8.50 hours). Five days = 42:30, so 2:30 of weekly overtime under the federal rule. At $18.00 an hour the lunch deduction costs 0.5 &times; $18 &times; 5 = $45 a week compared with paying the full 9 hours.</p>") +
              example("The same shift with a one-hour lunch", "<p>9:00 &minus; 1:00 = <b>8:00</b>. Five days = exactly 40:00, so no overtime. Lengthening an unpaid lunch lowers paid hours, so it matters at the overtime line.</p>") +
              example("Automatic meal deduction", "<p>Some timekeeping systems deduct 30 minutes automatically when a shift is longer than 6 hours. For a 6:00 am to 12:00 pm shift (exactly 6 hours) nothing is deducted; for 6:00 am to 12:30 pm, 30 minutes comes off, leaving 6:00 paid. If you did work through the meal, ask for a correction (see <a href=\"/guides/time-card-mistakes-and-how-to-fix-them/\">time card mistakes</a>).</p>")),
            S("What to check on your own time card", """
<ul>
<li>Is the unpaid meal shown on the card the length you actually took?</li>
<li>Were you completely relieved of duty during it?</li>
<li>Are short rest breaks (5-20 minutes) left inside your paid time?</li>
<li>Does an automatic deduction apply on days you worked through lunch?</li>
</ul>"""),
        ],
        [("Are lunch breaks paid?", "A bona fide meal period where you are completely relieved of duty is not paid work time under federal rules. Short rest breaks of about 5 to 20 minutes are generally paid. State law and your employer's policy may differ."),
         ("Does federal law require a lunch break?", "Federal regulations (29 CFR 785.19) explain when a meal period counts as unpaid, but the Department of Labor publishes meal and rest break requirements as a state-by-state table. Several states do require meal periods and some require rest breaks; see our meal and rest break guide."),
         ("What if I work through lunch?", "That time is generally hours worked and should be paid. Tell your supervisor and have the time card corrected."),
         ("How long should an unpaid lunch be?", "Federal regulations say 30 minutes or more is ordinarily long enough for a bona fide meal period. Shorter periods may have to be paid depending on the circumstances."),
         ("Does a longer lunch reduce overtime?", "Yes. Unpaid time does not count as hours worked, so a longer unpaid lunch lowers weekly hours.")],
        sources=["cfr785_18", "cfr785_19", "dol_meal"],
        related=["/guides/how-to-calculate-hours-worked-with-breaks/", "/guides/meal-and-rest-break-laws/", "/time-card-calculator/", "/hours-calculator/"],
    )

    # ------------------------------------------------------------------ shift differential
    tool_page(
        "/shift-differential-calculator/", "Shift Differential Calculator",
        "Shift Differential Calculator - Night Shift & Evening Pay",
        "Shift differential calculator: add a night, evening or weekend premium to your hourly rate. See hours in the differential window, pay per shift and weekly pay with overtime.",
        "Shift Differential and Night Pay Calculator",
        "Night shifts often pay a little extra, either a flat amount per hour or a percentage. Enter your shift, the hours the differential covers and the amount, and see exactly how many hours qualify and what you earn.",
        forms.shiftdiff(),
        [
            S("What a shift differential is", """
<p>A shift differential is extra pay per hour for working undesirable hours - nights, evenings, weekends or holidays. It is set by your employer, union contract or policy, so check yours. The window and amount are therefore inputs here, pre-filled with an example (10:00 pm to 6:00 am), not rules.</p>
<p>The calculator counts only the minutes of your shift that overlap the window, even when the window or the shift crosses midnight. Hours outside the window earn the base rate. The unpaid break is taken from the hours outside the window first, which is the assumption most favorable to the employee; if your policy treats the break differently the number will vary slightly.</p>"""),
            S("Worked example", example("$20 base, $2 flat differential, 6:00 pm to 3:00 am, 30-minute break", """
<ul>
<li>Clock to clock: 9:00; minus the 30-minute break = 8:30 paid (8.5 hours).</li>
<li>Window 10:00 pm to 6:00 am overlaps the shift from 10 pm to 3 am = 5 hours.</li>
<li>Base pay: 8.5 &times; $20 = $170.00. Differential: 5 &times; $2 = $10.00. One shift = <b>$180.00</b>, an effective $21.18 per hour.</li>
<li>Five shifts: 42.5 hours. Straight-time pay = $900.00. The differential is part of the regular rate, so the weighted regular rate is $900 &divide; 42.5 = $21.18 and the overtime premium is 2.5 hours &times; 0.5 &times; $21.18 = $26.47. Weekly total = <b>$926.47</b>.</li>
</ul>""")),
            S("Percent vs flat differentials", """
<p>A 10% differential on a $20 base is $2.00 an hour, the same as a flat $2. They diverge when your base rate changes: after a raise to $25 the percent version becomes $2.50 while the flat version stays $2. The calculator accepts either.</p>
<p>For overtime, the Department of Labor says the regular rate includes all remuneration for employment except the payments the law specifically lets employers exclude; shift differentials are not among the exclusions in the DOL's list. That is why the weekly figure above uses a blended regular rate. Your employer's payroll should do the same.</p>"""),
            S("Related checks", """
<ul>
<li>Check how many hours a night shift is with the <a href="/hours-calculator/">hours calculator</a>.</li>
<li>Compare overtime rules in your state with the <a href="/overtime-calculator/">overtime calculator</a>.</li>
<li>Estimate your net pay with the <a href="/paycheck-calculator/">paycheck estimator</a>.</li>
</ul>"""),
        ],
        [("What is a shift differential?", "Extra pay added to your hourly rate for working less desirable hours, such as nights or weekends."),
         ("Is night shift pay required by law?", "Night-shift premiums are normally set by an employer policy or a union contract. Check your offer letter, contract and state labor department for anything required where you work."),
         ("Does shift differential count toward overtime?", "The DOL says the regular rate includes all remuneration for employment except specific exclusions, and shift differentials are not on that exclusion list, so overtime generally is based on a rate that includes them."),
         ("Can the differential window cross midnight?", "Yes. A window like 10:00 pm to 6:00 am is handled correctly."),
         ("How do I calculate a percentage differential?", "Multiply the base rate by the percentage. 10% of $20 is $2.00.")],
        sources=["dol56a", "dol23"],
        related=["/overtime-calculator/", "/hours-calculator/", "/paycheck-calculator/", "/time-card-calculator/"],
    )

    # ------------------------------------------------------------------ work schedule planner
    tool_page(
        "/work-schedule-planner/", "Work Schedule Planner",
        "Work Schedule Planner - Shift Patterns (4-on-3-off, 2-2-3) & Weekly Hours",
        "Work schedule and shift planner: lay out 5-2, 4-3, 3-4, 2-2-3 and custom shift patterns on a calendar and see hours per week, averages and 40-hour overtime flags.",
        "Work Schedule and Shift Planner",
        "Plan a repeating shift pattern before you accept it. Pick the rotation, the shift times and the start date, and see a week-by-week calendar with hours and overtime flags.",
        forms.planner(),
        [
            S("Common shift patterns", table(
                ["Pattern", "Cycle", "Shift length that fits", "Average hours / week"],
                [["5 on, 2 off", "7 days", "8-8.5 h", "40-42.5"], ["4 on, 3 off", "7 days", "10 h", "40"], ["3 on, 4 off", "7 days", "12 h", "36"],
                 ["2-2-3 (Pitman)", "14 days, 7 shifts", "12 h", "42"], ["4 on, 4 off", "8 days", "12 h", "42"], ["7 on, 7 off", "14 days", "12 h", "42"]], num_from=9) +
              "<p>Averages are shift length multiplied by shifts per cycle, divided by weeks in the cycle (for example 7 twelve-hour shifts per 14 days is 84 hours per two weeks, or 42 per week).</p>"),
            S("How to read the calendar", """
<ul>
<li>Each row is a Monday-to-Sunday week. A bold time means a shift starts that day; &ldquo;off&rdquo; means no shift.</li>
<li>The right-hand column adds up paid hours: shift length minus the unpaid break, times the shifts that week.</li>
<li>Rows highlighted in green pass 40 hours. Under the federal weekly rule, hours above 40 in the workweek earn overtime (see <a href="/overtime-calculator/">overtime calculator</a>). Your employer's workweek definition and state rules may differ.</li>
</ul>"""),
            S("Worked example: the 2-2-3 rotation with 12-hour shifts", example("Why 42 hours on average hides 60-hour weeks", """
<p>The 2-2-3 rotation repeats every 14 days with 7 shifts: 2 on, 2 off, 3 on, then 2 off, 2 on, 3 off. Over two weeks that is 7 &times; 12 = 84 hours, an average of 42 a week. But the weeks alternate. In one week you may work 5 shifts (60 hours) and in the other 2 shifts (24 hours). Under the federal weekly rule, the 60-hour week contains 20 overtime hours even though the average looks close to 40 - overtime is not averaged across weeks. Whether your employer uses a different arrangement is something to ask before accepting the schedule.</p>""")),
            S("Tips for choosing a schedule", """
<ul>
<li>Compare average hours <i>and</i> the biggest week in the plan.</li>
<li>Use the unpaid break box to see paid hours, not just hours at work.</li>
<li>Add an hourly rate to preview straight-time and overtime-premium pay for the weeks shown.</li>
<li>Pair with the <a href="/pto-accrual-calculator/">PTO calculator</a> to plan days off.</li>
</ul>"""),
        ],
        [("What is a 4 on 3 off schedule?", "Four consecutive working days followed by three days off, repeating each week. With 10-hour shifts it totals 40 hours a week."),
         ("What is a 2-2-3 schedule?", "A 14-day rotation: work 2 days, off 2, work 3, off 2, work 2, off 3. Each person works 7 of every 14 days."),
         ("Do 12-hour shifts mean overtime?", "Under the federal rule overtime is based on more than 40 hours in the workweek. A week with four 12-hour shifts is 48 hours. State daily rules may add more."),
         ("Can I plan a custom pattern?", "Yes. Choose Custom and set the number of days on and days off."),
         ("Does this save my schedule?", "No. Nothing leaves your browser and nothing is stored; print the result to keep it.")],
        sources=["dol23"],
        related=["/overtime-calculator/", "/time-card-calculator/", "/pto-accrual-calculator/", "/lunch-break-calculator/"],
    )

    # ------------------------------------------------------------------ military time
    a, b = forms.military()
    hours_rows = []
    for h in range(24):
        h12 = h % 12 or 12
        ap = "AM" if h < 12 else "PM"
        label = {0: " (midnight)", 12: " (noon)"}.get(h, "")
        hours_rows.append(["%02d:00" % h, "%02d00" % h, "%d:00 %s%s" % (h12, ap, label)])
    tool_page(
        "/military-time-converter/", "Military Time Converter",
        "Military Time Converter - 24-Hour to 12-Hour Time (With Chart)",
        "Military time converter: change 12-hour AM/PM time to 24-hour military time and back. Includes a full 24-hour chart and a calculator for hours between two military times.",
        "Military (24-Hour) Time Converter",
        "Type 5:30 pm and get 17:30 (1730 hours), or type 0600 and get 6:00 AM. A second calculator finds how many hours lie between two 24-hour times, which is how many shift schedules are written.",
        a + b,
        [
            S("Converting by hand", """
<ol>
<li><b>12-hour to 24-hour:</b> AM hours are unchanged, except 12 AM which is 00. PM hours add 12, except 12 PM which stays 12. So 3:15 PM is 15:15 and 12:40 AM is 00:40.</li>
<li><b>24-hour to 12-hour:</b> 00 becomes 12 AM, 01-11 are AM, 12 is 12 PM, and 13-23 subtract 12 and are PM. So 21:05 is 9:05 PM.</li>
<li>Military style writes four digits and no colon: 0905, 2105 &ldquo;hours&rdquo;.</li>
</ol>"""),
            S("24-hour time chart", table(["24-hour", "Military", "12-hour"], hours_rows, num_from=9)),
            S("Worked examples", example("A military-time shift", "<p>0700 to 1530. 15:30 &minus; 07:00 = 8 hours 30 minutes. With a 30-minute unpaid meal that is <b>8:00</b> paid.</p>") +
              example("Crossing midnight", "<p>2200 to 0600. 06:00 is earlier than 22:00 so add 24 hours: 30:00 &minus; 22:00 = 8 hours. A 2200-0600 shift is 8 hours long.</p>") +
              example("Reading a schedule", "<p>A schedule reading &ldquo;Tue 1400-2230&rdquo; means Tuesday 2:00 PM to 10:30 PM, 8 hours 30 minutes before break.</p>")),
            S("Where 24-hour time is used", """
<p>Many hospitals, emergency services, the armed forces, airlines, transportation and manufacturing plants schedule in 24-hour time because it removes AM/PM mistakes. Time clocks in those settings often display 24-hour times, so converting is a routine skill for time card checking. Use the <a href="/time-card-calculator/">time card calculator</a>, which accepts 24-hour entries directly (type 1730 or 17:30).</p>"""),
        ],
        [("What is 1700 in standard time?", "5:00 PM."),
         ("What is 0000 in military time?", "Midnight, 12:00 AM, the start of the day."),
         ("How do you read 1345?", "Thirteen forty-five hours, or 1:45 PM."),
         ("How do you convert 6:30 PM to military time?", "Add 12 to the hour: 18:30, or 1830 hours."),
         ("Is 2400 a valid time?", "Some systems write 2400 for the end of the day, but most use 0000 for midnight. This converter treats 24:00 as 00:00.")],
        related=["/hours-calculator/", "/time-duration-calculator/", "/time-card-calculator/", "/work-schedule-planner/"],
    )

    # ------------------------------------------------------------------ rounding
    tool_page(
        "/time-rounding-calculator/", "Time Rounding Calculator",
        "Time Rounding Calculator - 5, 6 & 15 Minute Rounding (7-Minute Rule)",
        "Time rounding calculator: see how rounding punches to 5, 6 or 15 minutes (the 7-minute rule) changes a shift, with a rounding chart and a plain-English look at federal rules.",
        "Time Rounding Calculator: 5, 6 and 15 Minutes (7-Minute Rule)",
        "Enter your actual clock-in and clock-out and choose how the time clock rounds. See the rounded punches, the difference in minutes and what it could mean over a year.",
        forms.rounding(),
        [
            S("The 7-minute rule in plain English", """
<p>When time is rounded to the nearest quarter hour (15 minutes), a punch up to 7 minutes past a quarter mark is rounded <i>down</i> and one 8 minutes or more past is rounded <i>up</i>. That is what people call the &ldquo;7-minute rule&rdquo; or &ldquo;8-minute rule&rdquo;. Federal regulation 29 CFR 785.48(b) does not use that name; it recognises the practice of recording starting and stopping time to the nearest 5 minutes, or to the nearest one-tenth or quarter of an hour, and accepts it for enforcement purposes where it does not result, over a period of time, in failure to compensate employees properly.</p>""" + table(
                ["Minutes past the hour (punch)", "Rounds to", "Direction"],
                [["0 - 7", ":00", "down (or no change)"], ["8 - 22", ":15", "8-14 up, 15 none, 16-22 down"], ["23 - 37", ":30", "23-29 up, 30 none, 31-37 down"], ["38 - 52", ":45", "38-44 up, 45 none, 46-52 down"], ["53 - 59", "next :00", "up"]], num_from=9)),
            S("Rounding to 5 and 6 minutes", """
<ul>
<li><b>5 minutes:</b> 1-2 minutes past a mark round down, 3-4 round up (so 8:03 &rarr; 8:05, 8:02 &rarr; 8:00).</li>
<li><b>6 minutes (tenth of an hour):</b> 1-2 down, 3-5 up (8:03 &rarr; 8:06). Each rounded value is an exact tenth of an hour, which is why some payroll systems like it.</li>
<li><b>Always up / always down:</b> the calculator also shows these so you can see how one-sided rounding differs. Rounding that always favors the employer is the situation regulators and courts examine most closely.</li>
</ul>"""),
            S("Worked examples", example("A shift that loses time", "<p>Actual: in 8:08 am, out 5:07 pm, 30-minute break. Clock-in: 8 minutes past 8:00, so it rounds <i>up</i> to 8:15. Clock-out: 7 minutes past 5:00, so it rounds <i>down</i> to 5:00. Rounded time = 8:15 to 5:00 = 8:45, minus 30 = <b>8:15</b>. Actual = 8:59 &minus; 30 = 8:29. Difference: <b>-14 minutes</b>, worth $4.20 at $18.00 an hour.</p>") +
              example("A shift that gains time", "<p>Actual: in 7:52 am, out 5:08 pm. Clock-in is 7 minutes past 7:45, so it rounds down to 7:45; clock-out is 8 minutes past 5:00, so it rounds up to 5:15. Rounded = 7:45 to 5:15 = 9:30 versus actual 9:16, which is 14 minutes more. Rounding averages out only when punches fall on both sides of the marks across many shifts.</p>")),
            S("What to do if you think rounding is costing you", """
<ol>
<li>Keep your own record of actual punches for a few weeks (the <a href="/time-card-calculator/">time card calculator</a> lets you compare rounded and unrounded totals).</li>
<li>Compare the total with your pay stub.</li>
<li>Ask payroll to explain the rounding policy in writing.</li>
<li>If you still have concerns, contact your state labor department or the U.S. Department of Labor's Wage and Hour Division. Our <a href="/guides/rounding-time-cards/">rounding guide</a> covers the details.</li>
</ol>"""),
        ],
        [("What is the 7-minute rule for time clocks?", "A common method of rounding to the nearest 15 minutes: 1 to 7 minutes round down and 8 to 14 minutes round up. Federal regulations accept rounding to the nearest 5 minutes, tenth or quarter hour only if it does not result, over time, in failure to compensate employees properly."),
         ("Is rounding time cards legal?", "Federal regulation 29 CFR 785.48(b) accepts rounding that averages out over time. Practices that consistently favor the employer can be unlawful, and some states have stricter rules. See our guide."),
         ("What is the 8-minute rule?", "The same quarter-hour rule described from the other direction: 8 minutes or more past a quarter mark rounds up."),
         ("How does 6-minute rounding work?", "Time is recorded in tenths of an hour (6 minutes each). Minutes 1-2 round down and 3-5 round up."),
         ("Should I round start and end times or total hours?", "The federal regulation talks about recording starting and stopping time. Rounding the punches, as this calculator does, is the standard application.")],
        sources=["cfr785_48"],
        related=["/guides/rounding-time-cards/", "/decimal-hours-converter/", "/time-card-calculator/", "/minutes-to-decimal-chart/"],
    )
