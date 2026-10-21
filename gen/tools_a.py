"""Calculator pages, part A: time cards, hours between times, overtime, durations."""
from .core import tool_page, table, example, SRC
from . import forms


def S(h2, body, id_=None):
    return '<h2%s>%s</h2>%s' % (' id="%s"' % id_ if id_ else "", h2, body)


def build():
    # ------------------------------------------------------------------ weekly time card
    tool_page(
        "/time-card-calculator/", "Time Card Calculator",
        "Time Card Calculator - Free Weekly Hours, Breaks & Overtime",
        "Free time card calculator for weekly, bi-weekly and semi-monthly pay periods. Add clock in/out times and breaks, see regular, overtime and gross pay, then print it.",
        "Time Card Calculator with Breaks and Overtime",
        "Enter when you clocked in and out each day. The calculator subtracts unpaid breaks, adds up the pay period, applies an overtime rule per workweek and shows every step. It runs in your browser, so nothing you type is uploaded.",
        forms.timecard("weekly"),
        [
            S("How to use this time card calculator", """
<ol>
<li><b>Choose the pay period.</b> Weekly is the default. Switch to bi-weekly, semi-monthly or monthly and the rows change to the real calendar dates, so you can enter two weeks or a whole month.</li>
<li><b>Set the day your workweek starts.</b> Employers pick a fixed 7-day workweek (it does not have to be Monday to Sunday), and overtime is counted inside that week only.</li>
<li><b>Type your times.</b> <code>8</code>, <code>8am</code>, <code>8:30</code>, <code>5:15 pm</code>, <code>17:15</code> and <code>1715</code> all work. If the clock-out is earlier than the clock-in, the shift is treated as an overnight shift that ends the next day.</li>
<li><b>Enter unpaid break minutes.</b> Only unpaid meal periods go here. Short paid rest breaks stay inside your hours.</li>
<li><b>Pick an overtime rule and, if you like, add your hourly rate.</b> The result shows regular hours, overtime hours and gross pay, with a step-by-step explanation underneath.</li>
</ol>
<p>Press <b>Print this result</b> to print or save a PDF of the filled-in card and the calculation. Your entries are kept in this browser (local storage) so they are still there when you come back; press <b>Reset</b> to wipe them.</p>"""),
            S("A worked example", example("One week, five shifts, $18 an hour", """
<p>A warehouse employee enters the week below and chooses the federal rule (overtime after 40 hours in the workweek).</p>""" + table(
                ["Day", "In", "Out", "Break", "Hours worked"],
                [["Monday", "8:00 am", "5:00 pm", "30 min", "8:30"], ["Tuesday", "8:00 am", "5:30 pm", "30 min", "9:00"], ["Wednesday", "7:30 am", "6:00 pm", "60 min", "9:30"],
                 ["Thursday", "8:00 am", "5:00 pm", "30 min", "8:30"], ["Friday", "8:00 am", "4:00 pm", "30 min", "7:30"], ["Week total", "", "", "", "43:00"]], num_from=4) + """
<p><b>Step 1.</b> Each day is clock-out minus clock-in minus the unpaid break. Tuesday: 8:00 am to 5:30 pm is 9 hours 30 minutes, minus 30 minutes = 9:00.</p>
<p><b>Step 2.</b> Add the days: 8:30 + 9:00 + 9:30 + 8:30 + 7:30 = 43:00 (43.00 decimal hours).</p>
<p><b>Step 3.</b> Under the federal weekly rule the first 40 hours are regular and the remaining 3 hours are overtime.</p>
<p><b>Step 4.</b> Pay = 40 &times; $18.00 + 3 &times; ($18.00 &times; 1.5) = $720.00 + $81.00 = <b>$801.00</b> gross, before taxes.</p>""")),
            S("What the overtime rule options mean", """
<p>The default is the federal Fair Labor Standards Act rule: non-exempt employees must be paid at least one and one-half times their regular rate for hours over 40 in a workweek, and the workweek is a fixed, repeating period of 168 hours (seven consecutive 24-hour periods). Federal law does not average hours over two or more weeks, and it does not require daily overtime by itself.</p>
<p>A few states add their own thresholds, which is why the selector includes California, Alaska, Nevada and Colorado. Each one is explained, with its official source, on our <a href="/overtime-rules/">overtime rules by state</a> page and applied in detail in the <a href="/overtime-calculator/">overtime pay calculator</a>. If your state is not listed, the federal option is the usual starting point, but check with your state labor department because many states have rules of their own.</p>"""),
            S("Rounding punches", """
<p>The <b>Round each punch</b> option rounds the clock-in and clock-out times to the nearest 5, 6 or 15 minutes before hours are totalled. The 15-minute option uses the common &ldquo;7-minute rule&rdquo;: a punch 1 to 7 minutes past a quarter-hour mark rounds down and 8 to 14 minutes rounds up. Federal regulations (29 CFR 785.48(b)) accept rounding practices only when they do not result, over a period of time, in failure to compensate employees properly. Read our <a href="/guides/rounding-time-cards/">guide to rounding time cards</a> and try the <a href="/time-rounding-calculator/">rounding calculator</a> to see what it does to your own shifts.</p>"""),
            S("Tips for an accurate time card", """
<ul>
<li>Record the real punch times, not the scheduled ones. Estimates are the most common source of disputes.</li>
<li>Fix errors the same day. See <a href="/guides/time-card-mistakes-and-how-to-fix-them/">time card mistakes and how to fix them</a>.</li>
<li>If a shift runs past midnight, enter the true times and let the calculator carry the date change.</li>
<li>Need to hand the result to payroll as decimal hours? Use the <a href="/decimal-hours-converter/">decimal hours converter</a>.</li>
<li>Working a longer pay period? Use the <a href="/bi-weekly-time-card-calculator/">bi-weekly</a> or <a href="/semi-monthly-time-card-calculator/">semi-monthly</a> versions.</li>
</ul>"""),
        ],
        [("How do I calculate my hours for the week?", "For each day subtract the clock-in time from the clock-out time, then subtract any unpaid break. Add the daily totals. This calculator does those steps and shows them, including the decimal version of your total (for example 43:00 is 43.00 hours)."),
         ("Does the calculator handle overnight shifts?", "Yes. If the clock-out is earlier than the clock-in, the shift is counted as ending the next day. A 10:00 pm to 6:00 am shift is 8 hours before any break."),
         ("Is overtime figured per day or per week?", "Federal law measures overtime per workweek (over 40 hours). Some states, including California, Alaska, Nevada (for lower-paid workers) and Colorado, also have daily thresholds. Choose the rule that matches your state in the overtime rule menu."),
         ("Where is my time card saved?", "Only in your own browser's local storage on this device. Nothing is sent to a server. Clearing your browser data, or pressing Reset, deletes it."),
         ("Can I print or save the time card as a PDF?", "Yes. Press Print this result and choose Save as PDF as the destination in your browser's print dialog. Menus, ads and explanations are hidden on the printout."),
         ("Is this payroll advice?", "No. It is a calculator for estimates. Your employer's payroll system, your state's rules and your agreements decide what you are actually paid. See our disclaimer.")],
        sources=["dol23", "cfr785_48"],
        related=["/bi-weekly-time-card-calculator/", "/semi-monthly-time-card-calculator/", "/overtime-calculator/", "/timesheet/", "/hours-calculator/", "/guides/how-to-read-a-timesheet/"],
    )

    # ------------------------------------------------------------------ bi-weekly time card
    tool_page(
        "/bi-weekly-time-card-calculator/", "Bi-Weekly Time Card Calculator",
        "Bi-Weekly Time Card Calculator - 2 Weeks of Hours & Overtime",
        "Bi-weekly time card calculator: enter two weeks of clock in/out times, see overtime figured separately for each workweek, total hours and gross pay for the 14-day pay period.",
        "Bi-Weekly Time Card Calculator (2 Weeks)",
        "Built for employees paid every two weeks (26 pay periods a year). It lists the 14 real dates, figures overtime one workweek at a time and shows the total for the whole pay period.",
        forms.timecard("biweekly", title="Bi-weekly time card", sub="Fourteen days, two workweeks, one pay period."),
        [
            S("Why a bi-weekly pay period needs a different calculation", """
<p>A bi-weekly pay period is 14 days, but overtime does not work on 14 days. Under the federal rule each workweek stands alone: a 50-hour week followed by a 30-hour week contains 10 hours of overtime, even though the two weeks average exactly 40. The U.S. Department of Labor states that averaging of hours over two or more weeks is not permitted. A calculator that only adds up 80 hours and checks whether the total is over 80 will under-report overtime.</p>
<p>This tool splits the 14 days into workweeks that start on the day you choose and applies the overtime rule inside each one. The table beneath the result shows the split so you can compare it with your pay stub.</p>"""),
            S("Worked example: two weeks that look average", example("Week 1: 42:30. Week 2: 38:00. Rate $22.00.", """
<p>Total for the period: 42:30 + 38:00 = <b>80:30</b>.</p>
<ul>
<li><b>Week 1:</b> 40:00 regular + 2:30 overtime = 40 &times; $22.00 + 2.5 &times; $33.00 = $880.00 + $82.50 = $962.50.</li>
<li><b>Week 2:</b> 38:00, all regular = 38 &times; $22.00 = $836.00.</li>
<li><b>Period gross:</b> $962.50 + $836.00 = <b>$1,798.50</b>.</li>
</ul>
<p>If someone wrongly averaged the two weeks, 80.5 hours would show only 0.5 hours over 80 and underpay the 2.5 overtime hours in week 1.</p>""")),
            S("How to fill in the two weeks", """
<ol>
<li>Pick the first day of your pay period as the start date. Your employer's calendar or last pay stub shows it.</li>
<li>Set the workweek start day. If you do not know it, ask payroll; it is often Sunday or Monday.</li>
<li>Enter in and out times for every day you worked. Leave days off blank.</li>
<li>Add the unpaid meal break in minutes.</li>
<li>Check the per-workweek table: each row should match the weekly totals on your timesheet.</li>
</ol>"""),
            S("Bi-weekly pay in numbers", """
<p>Bi-weekly means 26 paychecks a year, and in some months a bi-weekly employee receives three paychecks. That is different from semi-monthly pay, which is 24 paychecks on fixed dates such as the 15th and the last day. The <a href="/guides/bi-weekly-vs-semi-monthly-pay/">bi-weekly vs semi-monthly guide</a> compares the two, and the <a href="/hourly-to-salary/">hourly to salary calculator</a> shows the gross amount of one bi-weekly check for any hourly rate.</p>
<p>For a quick sense of scale at 40 hours a week: $15/hour is $1,200 per bi-weekly check, $20/hour is $1,600 and $25/hour is $2,000, all before taxes.</p>"""),
        ],
        [("How do I calculate bi-weekly hours?", "Total the hours for each of the two workweeks, then add the weeks together. Figure overtime separately inside each workweek, not on the combined total."),
         ("Is overtime calculated on 80 hours in a bi-weekly pay period?", "Not under the federal Fair Labor Standards Act. Overtime is measured per workweek (over 40 hours) and the Department of Labor says averaging hours over two or more weeks is not permitted."),
         ("What if my pay period starts in the middle of a workweek?", "Use the box labelled Hours already worked earlier this workweek. Those hours count toward the 40-hour limit for the first workweek shown."),
         ("How many bi-weekly pay periods are in a year?", "26, because 52 weeks divided by 2 is 26. Some calendar years contain 27 paydays depending on where the first payday falls."),
         ("Can I print the bi-weekly time card?", "Yes. Use Print this result and pick Save as PDF, or print it directly.")],
        sources=["dol23"],
        related=["/time-card-calculator/", "/semi-monthly-time-card-calculator/", "/guides/bi-weekly-vs-semi-monthly-pay/", "/overtime-calculator/", "/hourly-to-salary/"],
    )

    # ------------------------------------------------------------------ semi-monthly time card
    tool_page(
        "/semi-monthly-time-card-calculator/", "Semi-Monthly Time Card Calculator",
        "Semi-Monthly Time Card Calculator - 1st-15th and 16th-End",
        "Semi-monthly time card calculator for pay periods that run the 1st to the 15th and the 16th to month end. Handles workweeks that straddle two pay periods.",
        "Semi-Monthly Time Card Calculator (1st-15th / 16th-End)",
        "Semi-monthly pay means 24 paychecks a year on fixed dates, so pay periods are 13 to 16 days long and workweeks often straddle two of them. This calculator shows the actual calendar dates and lets you carry hours across the boundary.",
        forms.timecard("semimonthly1", title="Semi-monthly time card", sub="Choose the 1st-15th or the 16th-to-month-end period, then pick any date in the month."),
        [
            S("How semi-monthly periods work", """
<p>Semi-monthly pay periods follow the calendar, not the 7-day workweek. The first period is the 1st through the 15th. The second is the 16th through the last day of the month, which is 13 days in a non-leap February and up to 16 days in a 31-day month. That is why the number of weekdays in a period changes: March 2026 has 10 weekdays from the 1st to the 15th but 12 from the 16th to the 31st (the tool shows the exact dates).</p>
<p>The workweek, however, is still seven days. When a workweek begins in one period and ends in the next, overtime for that week depends on all of its hours. If you are completing the second period, enter the hours you worked earlier in that same workweek in <b>Hours already worked earlier this workweek</b>, and the calculator counts them toward the 40-hour threshold.</p>"""),
            S("Worked example: a workweek that straddles the 15th", example("January 2026, workweek starting Monday", """
<p>Monday January 12 to Thursday January 15 an employee works four 10-hour days (40 hours), all in the first period (1st-15th). On Friday January 16, the first day of the second period, they work 8 more hours.</p>
<ul>
<li>The workweek (Jan 12-18) totals 48 hours, so under the federal weekly rule 8 hours are overtime.</li>
<li>When filling in the 16th-to-month-end card, type <code>40</code> in the box for hours already worked earlier this workweek. The calculator then shows the 8 hours on Friday as overtime.</li>
<li>At $24.00/hour those 8 hours earn 8 &times; $36.00 = $288.00 instead of $192.00 at straight time.</li>
</ul>
<p>Under 29 CFR 778.106, overtime pay is due on the regular payday for the pay period in which the workweek ends. This workweek ends Sunday January 18, in the second period, so that is the paycheck that should include the overtime for all 8 hours. Ask your payroll department how it handles the straddling week.</p>""")),
            S("Semi-monthly vs bi-weekly in one paragraph", """
<p>Bi-weekly checks arrive every other week (26 a year) and always cover exactly two workweeks. Semi-monthly checks arrive twice a month (24 a year) and each one covers roughly half a month. A salaried employee gets the same amount each time (annual salary &divide; 24), but an hourly employee's check varies with how many working days fall in the period. See the <a href="/guides/bi-weekly-vs-semi-monthly-pay/">full comparison</a>.</p>"""),
            S("Checking your entries", """
<ul>
<li>Switch the pay period selector between <b>1st to 15th</b> and <b>16th to end of month</b>; the rows rebuild for the month of the date you chose.</li>
<li>Use the <b>Monthly</b> option if your employer pays once a month.</li>
<li>Compare the total with your timesheet. If you are off by a few minutes, check whether rounding is applied by your employer. See <a href="/guides/rounding-time-cards/">rounding time cards</a>.</li>
</ul>"""),
        ],
        [("How many days are in a semi-monthly pay period?", "The first period is always 15 days (1st to 15th). The second is 13 to 16 days depending on the month's length."),
         ("How many pay periods are in a year if I am paid semi-monthly?", "24: two for each of the 12 months."),
         ("What if a workweek spans two pay periods?", "Overtime is based on the whole workweek. Enter the hours already worked earlier in the week in the 'Hours already worked' box so the second period is calculated correctly."),
         ("Do I get the same check every semi-monthly period?", "A salaried employee does. An hourly employee's check changes with the hours worked in each period."),
         ("Is semi-monthly pay legal everywhere?", "Pay frequency is set by state law. The U.S. Department of Labor publishes a state-by-state payday table; for example it lists semi-monthly pay as an option in Nevada and Alaska. Check your state labor department for your own rules.")],
        sources=["dol23", "cfr778_106", "dol_payday"],
        related=["/time-card-calculator/", "/bi-weekly-time-card-calculator/", "/guides/bi-weekly-vs-semi-monthly-pay/", "/salary-to-hourly/", "/overtime-calculator/"],
    )

    # ------------------------------------------------------------------ printable timesheet
    tool_page(
        "/timesheet/", "Printable Weekly Timesheet",
        "Printable Weekly Timesheet - Fill In Online and Save as PDF",
        "Free printable weekly timesheet: type clock in/out times and breaks, get totals and overtime, then print or save a PDF with signature lines. No sign-up.",
        "Printable Weekly Timesheet",
        "Fill in the week on screen and print a clean timesheet with your name, company, daily hours, totals and signature lines. The buttons, menus and ads drop off the printed page.",
        forms.timecard("weekly", locked=True, title="Weekly timesheet", sub="Fill in the week, then print or save as PDF. Signature lines are added to the printout.").replace(
            '<div class="btn-row no-print">', '<div class="print-only"><p>Employee signature: ____________________________ Date: ____________</p><p>Supervisor signature: ___________________________ Date: ____________</p></div><div class="btn-row no-print">', 1),
        [
            S("How to print or save the timesheet as a PDF", """
<ol>
<li>Type your name, company and the first day of the week.</li>
<li>Enter clock-in and clock-out times and unpaid breaks for each day you worked.</li>
<li>Press <b>Print this result</b>.</li>
<li>In the print dialog choose <b>Save as PDF</b> as the destination (Chrome, Edge) or <b>PDF</b> &rarr; <b>Save as PDF</b> (Safari, macOS) to create a file you can e-mail. Choose your printer to print on paper.</li>
</ol>
<p>The printout contains the filled table, your totals, the calculation steps and two signature lines. Menus, buttons and advertising are hidden so it stays a one-page document.</p>"""),
            S("What a good timesheet contains", """
<p>The federal recordkeeping regulation for covered employees (29 CFR 516.2) requires employers to keep, among other items, the time of day and day of week on which the employee's workweek begins, the hours worked on each workday and the total hours worked each workweek. This timesheet records the date, time in, time out, unpaid break and daily total, and it prints the week-start date so the workweek is clear. Pay rate and pay amounts are usually kept by your employer's payroll system.</p>
<p>For a walkthrough of each column and how to double-check the arithmetic by hand, read <a href="/guides/how-to-read-a-timesheet/">how to read a timesheet</a>, or learn how to <a href="/guides/how-to-fill-in-a-paper-time-card/">fill in a paper time card</a> if your workplace still uses cards.</p>"""),
            S("Example of a completed week", example("Part-time retail schedule", """
<p>Monday 9:00 am to 2:00 pm (no break) = 5:00; Wednesday 12:00 pm to 8:30 pm with a 30-minute break = 8:00; Saturday 10:00 am to 4:00 pm with a 30-minute break = 5:30. Total = 5:00 + 8:00 + 5:30 = <b>18:30</b> (18.50 hours). At $16.00/hour that is $296.00 gross for the week.</p>""")),
            S("Using the timesheet for different jobs", """
<ul>
<li><b>Employees:</b> keep your own copy to check your pay stub against.</li>
<li><b>Freelancers and contractors:</b> a signed timesheet attached to an invoice shows exactly what you billed. See <a href="/guides/tracking-hours-for-freelancers-and-contractors/">tracking hours for freelancers</a>.</li>
<li><b>Small business owners:</b> collect one per employee each week; your payroll provider or accountant tells you what records to keep.</li>
</ul>"""),
        ],
        [("Can I save this timesheet as a PDF?", "Yes. Press Print this result, then choose Save as PDF as the printer in the print dialog."),
         ("Will my employer accept this timesheet?", "It has the standard fields: name, week, daily in/out, breaks, totals and signature lines. Many small employers accept a printed timesheet like this, but confirm with your employer or payroll provider."),
         ("Is the data stored anywhere?", "Only in your own browser's local storage. Press Reset to remove it."),
         ("Does the timesheet include overtime?", "Yes. Choose the overtime rule for your state; the totals show regular and overtime hours."),
         ("Can I print more than one week?", "Fill one week, print it, then press Reset and start the next week. For two weeks on one card use the bi-weekly time card.")],
        sources=["dol23", "cfr516_2"],
        related=["/time-card-calculator/", "/guides/how-to-read-a-timesheet/", "/guides/how-to-fill-in-a-paper-time-card/", "/bi-weekly-time-card-calculator/"],
    )

    # ------------------------------------------------------------------ hours calculator
    tool_page(
        "/hours-calculator/", "Hours Calculator",
        "Hours Calculator - Hours Between Two Times & Dates (Overnight OK)",
        "Hours calculator: find the hours and minutes between two times or two dates. Handles overnight shifts, multi-day spans, unpaid breaks and gives decimal hours.",
        "Hours Calculator - Hours Between Two Times or Dates",
        "How many hours between 8:00 am and 5:00 pm? Between 10:00 pm Friday and 6:00 am Monday? Enter the start and end, add an unpaid break and get hours:minutes, decimal hours and the working-out.",
        forms.hours_between(),
        [
            S("How the hours calculator works", """
<div class="formula">hours = end time &minus; start time &minus; unpaid break</div>
<p>Everything is converted to minutes after midnight, subtracted, and converted back. When you leave the dates blank and the end time is not after the start time, the calculator assumes the shift ends the next day (an overnight shift). When you fill in the start and end <b>dates</b>, it uses them exactly, so a span of several days works: from 6:00 pm Friday to 6:00 am Monday is 60 hours.</p>
<p>Pick a break length and the tool subtracts it from the clock-to-clock time. Two extra fields scale the answer: <b>days per week</b> shows a weekly total, and an <b>hourly rate</b> shows pay for the shift.</p>"""),
            S("Worked examples", example("1. A day shift", "<p>8:00 am to 5:00 pm with a 60-minute lunch. Clock to clock: 9:00. Minus 60 minutes = <b>8:00</b> (8.00 hours).</p>") +
              example("2. An overnight shift", "<p>10:00 pm to 6:30 am with a 30-minute break. 10:00 pm to 6:30 am is 8:30. Minus 30 minutes = <b>8:00</b>. No dates needed: the end time is earlier than the start, so the calculator adds the next day.</p>") +
              example("3. Crossing several days", "<p>Start Friday 6:00 pm, end Monday 6:00 am. Friday 6 pm &rarr; Saturday 6 pm is 24 h, &rarr; Sunday 6 pm is 48 h, &rarr; Monday 6 am is 60 h. Total <b>60:00</b> (60.00 hours), useful for on-call weekends.</p>")),
            S("Hours between two times: the manual method", """
<ol>
<li>Write both times in 24-hour form (5:00 pm is 17:00).</li>
<li>Subtract the minutes first. If the end minutes are smaller than the start minutes, borrow one hour (60 minutes).</li>
<li>Subtract the hours.</li>
<li>If the result is negative, the end time is on the next day: add 24 hours.</li>
<li>Subtract unpaid breaks.</li>
</ol>
<p>Example: 7:45 am to 4:20 pm. In 24-hour form 7:45 and 16:20. Minutes: 20 &minus; 45 is negative, so borrow: 80 &minus; 45 = 35 and the hour becomes 15. Hours: 15 &minus; 7 = 8. Answer 8 hours 35 minutes (8.58 decimal hours).</p>"""),
            S("Daylight saving time", """
<p>Dates are treated as plain calendar days. If a shift spans the night the clocks change, the real elapsed time is one hour shorter or longer than the clock-based result. If you are paid for actual hours worked, adjust by one hour or ask payroll how that night is handled.</p>"""),
            S("Related quick answers", """
<p>Looking for a common shift? Our <a href="/hours/">shift hours index</a> answers questions like <a href="/hours/8am-to-5pm/">8am to 5pm is how many hours</a> with weekly totals, pay at several rates and overtime scenarios.</p>"""),
        ],
        [("How do you calculate hours between two times?", "Subtract the start from the end. If the end is earlier than the start the shift passes midnight, so add 24 hours. Then subtract unpaid breaks. The calculator shows each step."),
         ("Is 8am to 5pm 8 or 9 hours?", "It is 9 hours clock to clock. With an unpaid one-hour lunch the paid time is 8 hours, and with a 30-minute lunch it is 8.5 hours."),
         ("How do I calculate hours across midnight?", "Enter the real start and end times. If the end time is earlier than the start time, the calculator treats the end as the next day. 10 pm to 6 am is 8 hours."),
         ("Can it calculate more than 24 hours?", "Yes: enter the start and end dates. The span can be as long as you need."),
         ("What is the decimal hours result for?", "Payroll systems usually multiply decimal hours by the hourly rate. 7 hours 45 minutes is 7.75 decimal hours. Use the decimal hours converter for conversions without a start and end time.")],
        sources=[],
        related=["/time-card-calculator/", "/time-duration-calculator/", "/decimal-hours-converter/", "/lunch-break-calculator/", "/hours/", "/military-time-converter/"],
    )

    # ------------------------------------------------------------------ overtime calculator
    tool_page(
        "/overtime-calculator/", "Overtime Pay Calculator",
        "Overtime Pay Calculator - Weekly, Daily & Double Time (CA, AK, NV, CO)",
        "Overtime pay calculator with federal weekly overtime and state presets for California, Alaska, Nevada and Colorado: daily overtime, double time, bonuses in the regular rate.",
        "Overtime Pay Calculator: Weekly, Daily and Double Time",
        "Enter the hours you worked on each day of the workweek, pick the overtime rule that applies to you and see regular hours, overtime hours, double-time hours and gross pay, with every step shown.",
        forms.overtime(),
        [
            S("How overtime is calculated", """
<p>The federal Fair Labor Standards Act (FLSA) requires covered, non-exempt employees to be paid at least one and one-half times their regular rate for hours worked over 40 in a workweek. The workweek is a fixed, regularly recurring period of 168 hours, seven consecutive 24-hour periods. It can start on any day and need not match the calendar week.</p>
<div class="formula">overtime pay = overtime hours &times; regular rate &times; 1.5</div>
<p>The <b>regular rate</b> is not always the base hourly wage. The Department of Labor explains that it includes all remuneration for employment, with specific exclusions. A non-discretionary bonus, such as a production or attendance bonus promised in advance, is added to the week's straight-time earnings and divided by total hours to get the regular rate that overtime is based on. Use the bonus box above to see the effect. Discretionary bonuses, expense reimbursements and pay for leave are examples the DOL lists as excludable.</p>"""),
            S("State presets and what they do", """
<p>The presets implement these rules, each linked to an official source below:</p>""" + table(
                ["Preset", "Daily rule", "Weekly rule", "Source"],
                [["Federal", "None", "1.5x over 40 h", "U.S. DOL Fact Sheet 23"],
                 ["California", "1.5x over 8 h; 2x over 12 h; on the 7th consecutive workday of the workweek, 1.5x for the first 8 h and 2x after 8 h", "1.5x over 40 h (hours not already overtime)", "CA Dept. of Industrial Relations (DLSE)"],
                 ["Alaska", "1.5x over 8 h", "1.5x over 40 h; daily overtime hours are not counted twice", "AK Dept. of Labor, AS 23.10.060"],
                 ["Nevada (pay under 1.5x state minimum)", "1.5x over 8 h in a 24-hour period", "1.5x over 40 h", "NV Labor Commissioner, NRS 608.018"],
                 ["Nevada (pay at or above 1.5x state minimum)", "None", "1.5x over 40 h", "NV Labor Commissioner, NRS 608.018"],
                 ["Colorado", "1.5x over 12 h in a workday (the 12 consecutive hours rule is not modeled)", "1.5x over 40 h", "CO Dept. of Labor and Employment, COMPS Order"]], num_from=9) +
              """<p>Not every worker is covered: exemptions, industry-specific orders, collective bargaining agreements and alternative workweek schedules can change the result. The calculator applies the general rule only. The <a href="/overtime-rules/">overtime rules by state guide</a> explains each rule in detail.</p>"""),
            S("Worked examples", example("Federal: 47 hours at $20.00", """
<p>Mon 9, Tue 10, Wed 8, Thu 11, Fri 9 = 47 hours. The first 40 are regular and 7 are overtime. Pay = 40 &times; $20 + 7 &times; $30 = $800 + $210 = <b>$1,010.00</b>.</p>""") +
              example("California: a 13-hour day at $24.00", """
<p>Mon 13, Tue 10, Wed 8, Thu 8, Fri 8 = 47 hours. Monday: 8 regular, 4 at 1.5x (hours 9-12), 1 at 2x (hour 13). Tuesday: 8 regular, 2 at 1.5x. Wednesday to Friday: 8 each, regular. Totals: 40 regular, 6 overtime, 1 double time. Pay = 40 &times; $24 + 6 &times; $36 + 1 &times; $48 = $960 + $216 + $48 = <b>$1,224.00</b>. Under the plain federal rule the same week would pay $1,212.00 (40 regular + 7 overtime).</p>""") +
              example("Colorado: four 12-hour days at $30.00", """
<p>4 &times; 12 = 48 hours. No day passes 12 hours, so there is no daily overtime, but the weekly total is 8 hours over 40. Pay = 40 &times; $30 + 8 &times; $45 = $1,200 + $360 = <b>$1,560.00</b>.</p>""") +
              example("Bonus in the regular rate: 45 hours at $20.00 plus a $90 production bonus", """
<p>Straight-time earnings = 45 &times; $20 + $90 = $990. Regular rate = $990 &divide; 45 = $22.00. Overtime premium = 5 hours &times; 0.5 &times; $22.00 = $55. Total = $990 + $55 = <b>$1,045.00</b>, which is $55 more than the $990 you would have with straight time alone.</p>""")),
            S("Using the calculator correctly", """
<ul>
<li>Enter hours for the <b>workweek</b> your employer uses, starting with day 1. Pick the start day so the 7th-day rule lines up.</li>
<li>Count hours worked, not hours scheduled. Unpaid meal periods are not hours worked; see <a href="/guides/how-to-calculate-hours-worked-with-breaks/">calculating hours with breaks</a>.</li>
<li>Exempt employees (many salaried executive, administrative and professional roles) are not owed overtime under the FLSA. Read <a href="/guides/exempt-vs-non-exempt/">exempt vs non-exempt</a> before assuming you qualify either way.</li>
<li>For a whole pay period of dated hours use the <a href="/time-card-calculator/">time card calculator</a>.</li>
</ul>"""),
        ],
        [("How do I calculate overtime pay?", "Multiply your regular hourly rate by 1.5 and by the number of overtime hours, then add that to your regular pay for the first 40 hours. If you earned a non-discretionary bonus, include it when working out the regular rate."),
         ("Is overtime based on 40 hours a week or 8 hours a day?", "Federal law uses 40 hours in a workweek. California, Alaska, Colorado (12 hours) and, for lower-paid workers, Nevada also have daily thresholds. Use the matching preset."),
         ("What is double time?", "Double time means 2 times the regular rate. Federal law does not require it. California requires it for hours over 12 in a workday and for hours over 8 on the 7th consecutive day of a workweek, according to the state's Department of Industrial Relations."),
         ("Do paid holidays and vacation count toward the 40 hours?", "Federal overtime is based on hours actually worked, and the Department of Labor lists pay for periods when no work is performed (vacation, holidays, sick leave) among payments that may be left out of the regular rate. Your employer's policy, a union contract or your state may count paid leave toward overtime, so ask payroll. Enter only hours actually worked in this calculator."),
         ("Are salaried employees entitled to overtime?", "Only if they are non-exempt. Being paid a salary does not by itself make an employee exempt. See our exempt vs non-exempt guide."),
         ("Does the calculator work for pay periods longer than one week?", "Use the time card calculator for bi-weekly or semi-monthly periods; it applies overtime to each workweek.")],
        sources=["dol23", "dol56a", "ca_ot", "ak_ot", "nv_ot", "co_ot"],
        source_note="Daily-overtime figures for California, Alaska, Nevada and Colorado come from the linked state agency pages.",
        related=["/overtime-rules/", "/time-card-calculator/", "/guides/exempt-vs-non-exempt/", "/paycheck-calculator/", "/shift-differential-calculator/"],
    )

    # ------------------------------------------------------------------ time duration calculator
    a, b = forms.duration()
    tool_page(
        "/time-duration-calculator/", "Time Duration Calculator",
        "Time Duration Calculator - Add & Subtract Hours and Minutes",
        "Add and subtract hours and minutes, or add a duration to a clock time. Enter 1:30, 2h 15m or 1.5 and get hours:minutes, decimal hours and total minutes.",
        "Time Duration Calculator: Add and Subtract Hours and Minutes",
        "Totalling several tasks, taking a break off a shift or finding what time it will be in 7 hours 45 minutes. Two calculators on this page do the arithmetic that hours and minutes make awkward, because there are 60 minutes in an hour, not 100.",
        a + b,
        [
            S("Why hours and minutes are hard to add by hand", """
<p>Decimal arithmetic assumes ten of something makes the next unit, but minutes roll over at 60. Adding 1:45 and 2:30 as if they were decimals gives 3.75, but the correct answer is 4:15. The reliable manual method is to convert everything to minutes, add or subtract, then convert back.</p>
<div class="formula">total minutes = hours &times; 60 + minutes &nbsp;&nbsp; | &nbsp;&nbsp; hours = total minutes &divide; 60 (whole part), minutes = remainder</div>"""),
            S("Worked examples", example("Adding task times", "<p>Start with 3:45, add 2:30, add 1:15. In minutes: 225 + 150 + 75 = 450 minutes = 7 hours 30 minutes = <b>7:30</b> (7.50 decimal hours).</p>") +
              example("Subtracting a break", "<p>A 9:15 shift minus a 0:45 unpaid break: 555 &minus; 45 = 510 minutes = <b>8:30</b>.</p>") +
              example("What time will it be?", "<p>10:15 pm plus 7 hours 45 minutes: 22:15 + 7:45 = 30:00. Subtract 24 hours: 6:00, which is <b>6:00 am the next day</b>.</p>") +
              example("Going backwards", "<p>What time did a 6.5-hour job that finished at 2:10 pm start? 14:10 minus 6:30 = <b>7:40 am</b>.</p>")),
            S("Accepted formats", """
<table class="plain" style="width:auto"><tbody>
<tr><td><code>1:30</code></td><td>1 hour 30 minutes</td></tr>
<tr><td><code>1h 30m</code> or <code>1 hr 30 min</code></td><td>1 hour 30 minutes</td></tr>
<tr><td><code>45m</code></td><td>45 minutes</td></tr>
<tr><td><code>1.5</code></td><td>1.5 hours (1 hour 30 minutes)</td></tr>
<tr><td><code>2h</code></td><td>2 hours</td></tr>
</tbody></table>
<p>Results show hours:minutes, decimal hours, total minutes and, over 24 hours, days plus hours. Decimal hours are what most payroll tools want; the <a href="/decimal-hours-converter/">decimal hours converter</a> explains the conversion in depth.</p>"""),
            S("When to use which tool", """
<ul>
<li>One shift with a start and end time: <a href="/hours-calculator/">hours calculator</a>.</li>
<li>A whole week or pay period: <a href="/time-card-calculator/">time card calculator</a>.</li>
<li>Many separate durations to total: the first calculator on this page.</li>
</ul>"""),
        ],
        [("How do I add hours and minutes?", "Convert to minutes, add, and convert back: 2:45 + 1:30 is 165 + 90 = 255 minutes = 4:15. Or let the calculator do it."),
         ("How do I subtract time?", "Convert to minutes and subtract. 5:10 minus 1:40 is 310 &minus; 100 = 210 minutes = 3:30."),
         ("What is 1.5 hours in hours and minutes?", "1 hour 30 minutes. The decimal .5 is half of 60 minutes."),
         ("Can the result be negative?", "Yes. If you subtract more than you started with, the answer shows a minus sign, for example -0:30."),
         ("Does it work for time past 24 hours?", "Yes. Totals over 24 hours are shown in hours and also as days plus hours.")],
        related=["/hours-calculator/", "/decimal-hours-converter/", "/minutes-to-decimal-chart/", "/time-card-calculator/"],
    )
