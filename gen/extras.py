"""Additional explanatory sections appended to calculator pages and guides (keyed by slug)."""


def S(h2, body):
    return "<h2>%s</h2>%s" % (h2, body)


def box(title, inner):
    return '<div class="example"><h3>%s</h3>%s</div>' % (title, inner)


def tbl(headers, rows):
    th = "".join("<th>%s</th>" % h for h in headers)
    tr = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % c for c in r) for r in rows)
    return '<div class="table-wrap"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % (th, tr)


EXTRA = {}

# ------------------------------------------------------------------ calculator pages
EXTRA["/bi-weekly-time-card-calculator/"] = [
    S("Reading the per-workweek table", """
<p>Under the result you will see one row per workweek and a total row. Check three things against your pay stub. First, each week's <b>total</b> should match the hours on your timesheet for that week. Second, the <b>regular</b> column is capped at 40:00 under the federal rule, so a week with 45 hours shows 40:00 regular and 5:00 overtime. Third, the <b>period total</b> is the sum of the weeks, not a re-run of the rule on the combined hours. If your stub shows fewer overtime hours than this table, the most likely cause is that your employer averaged the two weeks, which the Department of Labor says is not permitted, or that your workweek begins on a different day than the one you selected.</p>"""),
    S("Choosing the right workweek start day", """
<p>Your employer sets the workweek, and it can start on any day and hour. The easiest way to find it is on a pay stub or timesheet header that says &ldquo;week ending&rdquo;: if the week ends Saturday, it starts Sunday. If you pick the wrong day, a long Monday-to-Friday run might be split across two workweeks and the overtime split changes. Example: 10 hours each on Thursday, Friday, Saturday, Sunday and Monday is 50 hours in one 7-day window, but with a Monday start it is 40 hours in one workweek (Thursday to Sunday) and 10 in the next, so no overtime. That is why the start day matters.</p>"""),
]
EXTRA["/semi-monthly-time-card-calculator/"] = [
    S("A quick way to estimate a semi-monthly check", """
<p>For an hourly employee, count the working days in the period and multiply by the paid hours per day and the hourly rate. For example, March 1-15, 2026 contains 10 weekdays, so 10 &times; 8 hours = 80 hours; March 16-31 contains 12 weekdays, so 12 &times; 8 = 96 hours. At $22.00 an hour the two checks are $1,760 and $2,112 before taxes, even though the monthly total of 176 hours is simply 22 working days. Salaried employees do not see this swing because their check is annual salary &divide; 24.</p>
<p>Enter your actual hours above and the per-workweek table will show whether any of those hours cross the 40-hour line.</p>"""),
]
EXTRA["/timesheet/"] = [
    S("A printable template for real-world situations", """
<table class="plain" style="width:auto"><tbody>
<tr><td><b>Split shifts</b></td><td>Enter the full span (first clock-in to last clock-out) and put the gap in the break box. A 7:00 am to 11:00 am shift plus 3:00 pm to 6:00 pm is 11 hours clock to clock; enter a break of 240 minutes to get 7:00.</td></tr>
<tr><td><b>Overnight work</b></td><td>Enter the real times. 10:00 pm to 6:30 am is counted as 8 hours 30 minutes on the day it started.</td></tr>
<tr><td><b>Unpaid lunch</b></td><td>Enter the minutes; the printed total excludes them.</td></tr>
<tr><td><b>Days off</b></td><td>Leave the row blank. It prints as an empty line.</td></tr>
</tbody></table>
<p>Tip: if you need two weeks on one sheet, use the <a href="/bi-weekly-time-card-calculator/">bi-weekly time card</a>, which prints 14 dated rows.</p>"""),
    S("Keeping signed copies", """
<p>Print two copies if you want to keep one: one for the employer, one for yourself. Photograph signed pages and store them somewhere you can find later. If your employer has a required form, use this printout as your private cross-check and compare totals every period.</p>"""),
]
EXTRA["/hours-calculator/"] = [
    S("Typical results to sanity-check against", tbl(
        ["Start", "End", "Break", "Net hours"],
        [["9:00 am", "5:00 pm", "30 min", "7:30"], ["9:00 am", "5:00 pm", "60 min", "7:00"], ["7:00 am", "3:30 pm", "30 min", "8:00"], ["6:00 pm", "2:30 am", "30 min", "8:00"], ["11:00 pm", "7:00 am", "0", "8:00"], ["12:00 pm", "8:45 pm", "45 min", "8:00"]]) + """
<p>If your result is very different from the ballpark you expected, check the AM/PM on both times or whether the end falls on the next day.</p>"""),
]
EXTRA["/decimal-hours-converter/"] = [
    S("Common mistakes when converting", """
<ul>
<li><b>Reading the decimal as minutes.</b> 7.30 hours is 7 hours 18 minutes, not 7:30.</li>
<li><b>Truncating instead of rounding.</b> 8:50 is 8.8333&hellip;; cutting it to 8.83 loses a fraction of a minute, while 8.8 loses 2 minutes.</li>
<li><b>Rounding too early.</b> Convert every day to decimals with several places, add them, and round the total once. Rounding each day to two places can drift by a minute or two over a week.</li>
<li><b>Mixing formats on one card.</b> A column of 7:45, 8.25 and 7:30 is a recipe for a wrong total.</li>
</ul>"""),
    S("Example: why rounding order matters", box("Five days of 8:20", """
<p>Each 8:20 is 8.3333 hours. Five days: 41.6667 hours = 41.67 hours, or 41:40. If every day is rounded first to 8.33, five days is 41.65 hours, which is 41:39. A one-minute difference per week is small, but it is also a shortfall over a year of 52 weeks of 52 minutes.</p>""")),
]
EXTRA["/minutes-to-decimal-chart/"] = [
    S("Converting a long list of minutes", """
<p>When a system records durations as minutes (phone logs, delivery apps, project trackers), it is easier to add the minutes first and divide once. Example: 95, 140, 75 and 120 minutes total 430 minutes; 430 &divide; 60 = 7.17 hours, or 7:10. The same list converted line by line and rounded to two places (1.58 + 2.33 + 1.25 + 2.00) gives 7.16, one hundredth less, because of the rounding of each line.</p>"""),
]
EXTRA["/hourly-to-salary/"] = [
    S("Beyond the base salary", """
<p>An hourly wage is only part of what a job pays. When you compare an hourly job with a salaried one, line up the extras: employer health insurance contributions, retirement matching, paid holidays and vacation, bonuses and overtime. Paid time off matters especially for the calculation above: if you are paid for vacation and holidays, use 52 weeks; if you work seasonally or are paid only for hours on the clock, enter your unpaid weeks. A person earning $22 an hour who is paid for 52 weeks makes $45,760, but the same person on a 10-month school-year schedule with 10 paid weeks fewer makes $22 &times; 40 &times; 42 = $36,960 unless the employer spreads pay over 12 months.</p>"""),
]
EXTRA["/salary-to-hourly/"] = [
    S("Using the result to compare offers", """
<p>Suppose you are comparing two offers for the same 45-hour week. Offer A is a $58,000 salary: $58,000 &divide; (45 &times; 52 = 2,340 hours) = $24.79 an hour. Offer B is $26 an hour with overtime for non-exempt staff: 40 &times; $26 + 5 &times; $39 = $1,235 a week, or $64,220 over 52 weeks. For the same hours, B pays about $6,220 more, and its hourly rate is higher on every hour worked. Looking only at the headline salary would not show that. This is the comparison the calculator makes easy.</p>"""),
    S("Salary history, raises and the hourly rate", """
<p>A 3% raise on $62,000 is $1,860, which adds $0.89 an hour at 2,080 hours. If your hours grow at the same time, the effective gain can disappear. Enter your real weekly hours each time you compare.</p>
<p>For related conversions, see the <a href="/hourly-to-annual/">hourly rate to annual salary tables</a>, which list common rates from $12 to $50, and the <a href="/guides/bi-weekly-vs-semi-monthly-pay/">pay period guide</a> for how a salary becomes checks.</p>"""),
]
EXTRA["/pto-accrual-calculator/"] = [
    S("Frequently used accrual rates", tbl(
        ["Policy", "Hours per year", "Per bi-weekly period", "Per semi-monthly period"],
        [["10 days (8 h)", "80", "3.08", "3.33"], ["15 days (8 h)", "120", "4.62", "5.00"], ["20 days (8 h)", "160", "6.15", "6.67"], ["25 days (8 h)", "200", "7.69", "8.33"]]) + """
<p>These are straight arithmetic: annual hours divided by 26 or 24. Your employer's handbook states the actual rate. Some employers accrue by hours worked, which gives different amounts for part-time employees: for example 1 hour for every 30 hours worked gives a 20-hour-a-week employee about 34.7 hours a year.</p>"""),
    S("Accrual vs front-loaded PTO", """
<p><b>Accrual</b> means you earn PTO gradually as you work: the balance builds up each pay period. <b>Front-loaded</b> means you receive the full annual amount at the beginning of the year (or on your anniversary). With accrual, a new employee may have little PTO available in the first months; with front-loading, the full amount is available immediately, and policies for unused time and for leaving the company usually differ. Whatever the type, use the starting balance and cap boxes to model your own year.</p>"""),
]
EXTRA["/lunch-break-calculator/"] = [
    S("How a meal deduction can move you into overtime", """
<p>A weekly total of exactly 40 hours has no overtime, and one extra 15 minutes does. Because unpaid meals reduce hours worked, a 30-minute difference per day matters: five days of 8:30 paid is 42:30, which includes 2:30 of overtime, while five days of 8:00 paid is 40:00 with none. Use the calculator for each pattern, then multiply the daily paid time by days.</p>""" + tbl(
        ["Clock-to-clock", "Unpaid meal", "Paid / day", "Paid / 5 days", "Overtime (federal)"],
        [["9:00", "0:30", "8:30", "42:30", "2:30"], ["9:00", "1:00", "8:00", "40:00", "none"], ["8:30", "0:30", "8:00", "40:00", "none"], ["9:30", "0:30", "9:00", "45:00", "5:00"], ["10:00", "0:30", "9:30", "47:30", "7:30"]])),
    S("Automatic deduction systems", """
<p>Many timekeeping systems deduct a set meal period automatically. That is convenient but only accurate if the meal is actually taken and the employee is relieved of duty. If an automatic deduction is applied on a day you worked through the meal or were interrupted, ask for a correction. Keep a note of the date and what happened so you can show it when you ask.</p>"""),
]
EXTRA["/shift-differential-calculator/"] = [
    S("Common ways differentials are structured", """
<ul>
<li><b>Flat amount per hour for hours in a window</b> (the example above): $2.00 for each hour between 10 pm and 6 am.</li>
<li><b>Percentage of base pay</b>: 10% on evenings, 15% on nights.</li>
<li><b>Whole-shift differential</b>: if most of the shift falls in the window the whole shift gets the premium. This calculator counts only the hours inside the window; for a whole-shift rule, set the window to cover the whole shift.</li>
<li><b>Weekend or holiday premium</b>: handled the same way by changing the window.</li>
</ul>
<p>Because these vary by employer and contract, read your offer letter or policy and enter the numbers it states.</p>"""),
    S("Estimating the yearly value", box("A $2.00 night differential", """
<p>Five shifts a week with 5 differential hours each is 25 hours &times; $2.00 = $50.00 a week, or $2,600 over 52 weeks (before any overtime effect). A 10% differential on a $20 base rate is the same $2.00, but it grows with raises.</p>""")),
]
EXTRA["/time-duration-calculator/"] = [
    S("Hours and minutes in everyday tasks", """
<p>Adding durations comes up more often than people expect: totalling a week of project tasks, adding travel time to a meeting, working out how long a flight and layover take, subtracting a lunch from a shift or checking how much overtime you did across several days. The principle is the same in each case: turn every duration into minutes, add or subtract, and turn the result back into hours and minutes.</p>
<p>Example, travel plan: a 2 hour 50 minute drive, a 45-minute stop, and a 1 hour 35 minute ferry add to 170 + 45 + 95 = 310 minutes = 5 hours 10 minutes. If you leave at 7:20 am, the second calculator on this page shows an arrival at 12:30 pm.</p>"""),
    S("Time arithmetic cheat sheet", tbl(
        ["Minutes", "As hours:minutes", "Decimal hours"],
        [["15", "0:15", "0.25"], ["30", "0:30", "0.50"], ["45", "0:45", "0.75"], ["90", "1:30", "1.50"], ["105", "1:45", "1.75"], ["150", "2:30", "2.50"], ["480", "8:00", "8.00"], ["525", "8:45", "8.75"]]) + """
<p>Need many more conversions? The <a href="/minutes-to-decimal-chart/">minutes to decimal chart</a> has every value from 0 to 59.</p>"""),
]
EXTRA["/military-time-converter/"] = [
    S("Writing and saying military time", """
<p>In 24-hour notation the day runs from 0000 (midnight) to 2359. Four digits are written without a colon: the first two are hours, the last two are minutes. 0600 is six o'clock in the morning, 1200 is noon, 1800 is six in the evening and 2359 is one minute before midnight. In speech, times are commonly said digit-pair by pair: 0830 is &ldquo;oh-eight-thirty&rdquo;, 1700 is &ldquo;seventeen hundred&rdquo;. The convention differs a little between organisations, so follow your workplace's style.</p>"""),
    S("Using 24-hour time on a time card", """
<p>Time clocks, rosters and shift schedules in hospitals, factories, airlines and public safety services are often in 24-hour time. Our calculators accept it directly: type <code>1730</code> or <code>17:30</code> and it is read as 5:30 pm. For a shift that crosses midnight, enter the real end time (for example 0630 after a 2200 start). The <a href="/time-card-calculator/">time card calculator</a> then counts the shift as ending the next day.</p>
<p>A common mistake is to subtract military times as if they were decimals: 1530 minus 0700 is not 830 minutes. Convert to hours and minutes first: 15:30 minus 07:00 is 8 hours 30 minutes.</p>"""),
]
EXTRA["/paycheck-calculator/"] = [
    S("Why take-home pay changes from check to check", """
<p>Gross pay for hourly employees moves with hours and overtime, so withholding moves as well. Because the federal percentage method annualises each paycheck, an unusually large check (a big overtime week, a bonus) is withheld as if you earned that much all year. That does not mean you owe tax at that rate; any over-withholding is settled when you file. Likewise, 401(k) deferrals reduce your income tax withholding but not Social Security or Medicare wages, while many health-plan premiums reduce both.</p>"""),
    S("Ways to check the estimate", """
<ol>
<li>Enter your actual gross pay per period from a recent pay stub in the &ldquo;Gross pay per period&rdquo; mode.</li>
<li>Match the filing status on your Form W-4 (Step 1(c)).</li>
<li>Enter any pre-tax deductions from the stub.</li>
<li>Compare federal withholding, Social Security (6.2%) and Medicare (1.45%) lines. Social Security and Medicare should match closely; federal income tax will differ if your W-4 has Steps 2-4 filled in.</li>
</ol>"""),
]
EXTRA["/work-schedule-planner/"] = [
    S("Questions to ask before accepting a rotating schedule", """
<ul>
<li>What day does the workweek start, and what time? It decides where weeks are cut and which hours are overtime.</li>
<li>Is the unpaid break a fixed length, and is it actually uninterrupted?</li>
<li>How are shifts that cross midnight assigned to a workweek?</li>
<li>Does the employer count paid leave toward the 40 hours? (Policies differ.)</li>
<li>How much notice is given of schedule changes, and how are swaps handled?</li>
</ul>"""),
    S("Reading average hours carefully", """
<p>An average of 42 hours does not mean you work 42 every week. With a rotation that alternates 60-hour and 24-hour weeks, the 60-hour weeks are the ones that earn overtime under the federal weekly rule, and the 24-hour weeks do not offset them. That is why the planner shows each week separately. Use the weekly table to compare options and to check your pay stub for the high-hour weeks.</p>"""),
]
EXTRA["/time-rounding-calculator/"] = [
    S("A week of rounded punches", tbl(
        ["Day", "Actual in / out", "Rounded in / out (15 min)", "Actual paid", "Rounded paid"],
        [["Mon", "7:58 / 4:32", "8:00 / 4:30", "8:04", "8:00"], ["Tue", "8:09 / 4:36", "8:15 / 4:30", "7:57", "7:45"], ["Wed", "7:51 / 4:44", "7:45 / 4:45", "8:23", "8:30"], ["Thu", "8:03 / 5:12", "8:00 / 5:15", "8:39", "8:45"], ["Fri", "8:00 / 4:25", "8:00 / 4:30", "7:55", "8:00"]]) + """
<p>Totals: actual 40:58 versus rounded 41:00. In this particular week rounding favored the employee by two minutes; a different set of punches would not. The test is how it behaves over many weeks (a 30-minute meal is deducted from each day in every column).</p>"""),
]
EXTRA["/overtime-calculator/"] = [
    S("Overtime and the pay stub", """
<p>A stub that shows overtime should list overtime hours and the overtime rate separately. If it lists total hours at one rate, compare it with the totals above: your straight-time pay is hours &times; rate, and the premium is overtime hours &times; 0.5 &times; rate. Federal recordkeeping rules (29 CFR 516.2) require employers to keep the regular hourly rate for any workweek in which overtime is due, total straight-time earnings and total premium pay for overtime, so those numbers should be available from payroll if you ask.</p>"""),
]

# ------------------------------------------------------------------ guides
EXTRA["/guides/bi-weekly-vs-semi-monthly-pay/"] = [
    S("Which months have three bi-weekly paychecks?", """
<p>Because 26 checks do not divide evenly into 12 months, two months of the year contain three bi-weekly paydays. If the first payday of 2026 is Friday, January 2 and checks follow every 14 days, the paydays are Jan 2, 16, 30; Feb 13, 27; Mar 13, 27; Apr 10, 24; May 8, 22; Jun 5, 19; Jul 3, 17, 31; Aug 14, 28; Sep 11, 25; Oct 9, 23; Nov 6, 20; Dec 4, 18. That is 26 paydays with three in January and July. Which months get three depends on the first payday of the year, and in some years the calendar produces 27 paydays.</p>"""),
    S("Budgeting with each schedule", box("$60,000 a year", """
<p>On bi-weekly pay, the average monthly gross is $60,000 &divide; 12 = $5,000, but a normal month brings two checks of $2,307.69 = $4,615.38 and a three-check month brings $6,923.07. Many people budget on two checks a month and treat the extra check as savings or a debt payment. On semi-monthly pay every month brings two checks of $2,500.00 = $5,000.00 exactly.</p>""")),
    S("Questions to ask your employer", """
<ul>
<li>What are the exact pay period start and end dates, and how many days after the period ends is payday?</li>
<li>What day does the workweek begin (this decides overtime)?</li>
<li>What happens when payday falls on a weekend or holiday?</li>
<li>Is the first paycheck partial, and how is it calculated?</li>
<li>If the pay schedule changes, how will it be communicated and how will the transition check be computed?</li>
</ul>"""),
]
EXTRA["/guides/exempt-vs-non-exempt/"] = [
    S("Common misconceptions", """
<ul>
<li><b>&ldquo;I'm salaried, so I can't get overtime.&rdquo;</b> Not necessarily. The salary basis is one test among several, and the duties test matters too.</li>
<li><b>&ldquo;My title says manager.&rdquo;</b> Duties decide, not titles.</li>
<li><b>&ldquo;I signed an agreement that I'm exempt.&rdquo;</b> An agreement does not by itself make an employee exempt if the legal tests are not met.</li>
<li><b>&ldquo;Everyone who is paid hourly gets overtime.&rdquo;</b> Most do, but some jobs and industries have specific exemptions in federal or state law; check the sources.</li>
</ul>"""),
    S("The effective hourly rate of an exempt job", box("$65,000 salary, different weeks", """
<p>At 40 hours a week (2,080 hours), $65,000 is $31.25 an hour. At 50 hours a week (2,600 hours) it is $25.00 an hour. At 55 hours (2,860 hours) it is $22.73 an hour. If you are exempt, overtime is not owed, but tracking your hours with the <a href="/time-card-calculator/">time card calculator</a> shows what each extra hour is really worth to you.</p>""")),
    S("What employers should do", """
<p>Classification is the employer's responsibility. Review each role against the Department of Labor's fact sheet, document the duties performed, keep records for non-exempt staff as required by 29 CFR 516.2, and look at state law, which can be stricter than the federal rule. When in doubt, ask the Wage and Hour Division or a qualified employment professional.</p>"""),
]
EXTRA["/guides/how-to-calculate-hours-worked-with-breaks/"] = [
    S("Split shifts and multiple punches", box("In at 7:00, out at 11:30; in at 12:00, out at 4:00", """
<p>Add the two blocks: 4:30 + 4:00 = <b>8:30</b>. The 30 minutes between 11:30 and 12:00 is not part of either block, so you do not subtract it again. If your system records only the first clock-in and last clock-out (7:00 to 4:00 = 9:00), subtract the unpaid gap (30 minutes) to get the same 8:30.</p>""")),
    S("Overnight shifts with a meal", box("10:00 pm to 6:30 am with a 30-minute meal", """
<p>10:00 pm to 6:30 am is 8:30 clock to clock; minus 30 minutes = <b>8:00</b>. Enter the true times rather than splitting the shift at midnight; the <a href="/hours-calculator/">hours calculator</a> handles the date change for you.</p>""")),
    S("Quick reference: paid hours by shift and meal length", tbl(
        ["Clock to clock", "No meal", "30 min", "45 min", "60 min"],
        [["6:00", "6:00", "5:30", "5:15", "5:00"], ["8:00", "8:00", "7:30", "7:15", "7:00"], ["8:30", "8:30", "8:00", "7:45", "7:30"], ["9:00", "9:00", "8:30", "8:15", "8:00"], ["10:00", "10:00", "9:30", "9:15", "9:00"], ["12:00", "12:00", "11:30", "11:15", "11:00"]]) + """
<p>Keep paid rest breaks inside your hours; only subtract meal periods that meet the federal definition of a bona fide meal period.</p>"""),
]
EXTRA["/guides/how-to-fill-in-a-paper-time-card/"] = [
    S("Overnight and split shifts on a paper card", """
<p>Most paper cards have one In/Out pair per day. For an overnight shift, write the day you started and the real clock-out time, then note &ldquo;+1&rdquo; or &ldquo;next day&rdquo; beside the out time so the person totalling the card does not treat it as a negative. For a split shift, use a second In/Out pair or write both blocks on one line and total them. A shift of 10:00 pm to 6:30 am with a 30-minute meal is 8:00 paid; a split of 7:00-11:30 and 12:00-4:00 is 4:30 + 4:00 = 8:30.</p>"""),
    S("Totalling the week two ways", """
<p>Total in minutes and in hours-and-minutes and check they agree. Hours and minutes: add the minutes column first (carry 60 minutes into an hour), then the hours. Minutes: multiply each day's hours by 60, add, then divide by 60. Example for the week above, 36:53: (36 &times; 60) + 53 = 2,213 minutes; 2,213 &divide; 60 = 36.88 hours. If the two methods disagree, find the difference by redoing the days one at a time.</p>"""),
    S("Time clocks that stamp the card", """
<p>Mechanical clocks print the time on the card and may print in 24-hour or decimal formats, so read the clock's manual first. Stamps can be crooked or faint; if one is unreadable, write the correct time beside it, initial it and ask your supervisor to initial it as well. If your workplace has switched to a digital system, keep the same habits: check your total at the end of each week and keep your own record.</p>"""),
    S("When to move from paper to a calculator", """
<p>A paper card works fine for a handful of employees. It struggles once you have overtime thresholds, bi-weekly or semi-monthly pay periods, rounding rules or several pay rates. The <a href="/time-card-calculator/">time card calculator</a> can be used alongside paper cards as a cross-check: enter the same times and compare totals.</p>"""),
]
EXTRA["/guides/how-to-read-a-timesheet/"] = [
    S("Common pay codes you may see", tbl(
        ["Code", "Usually means", "Worth checking"],
        [["REG", "Regular hours at the base rate", "Capped at 40 per workweek for federal overtime"], ["OT / OT1", "Overtime hours at 1.5x", "Hours over 40 in the workweek (or the state daily threshold)"], ["DT / OT2", "Double time hours", "Only in states or contracts that require it"], ["PTO / VAC", "Paid time off", "Paid, but not hours worked"], ["HOL", "Paid holiday", "Rate and whether it counts toward overtime"], ["SICK", "Paid sick leave", "Accrual balance"]]) + """
<p>Codes vary by employer and payroll system; your payroll department can supply the legend.</p>"""),
    S("Reading a bi-weekly timesheet", """
<p>A bi-weekly sheet has 14 days and two workweek totals. Check each week against 40 hours separately, because overtime is figured weekly. A sheet that shows only a 14-day total with overtime computed on 80 hours is not following the federal workweek rule. Mismatches between the sheet and the stub usually come from one of five places: a missed punch, a meal deduction, rounding, the wrong workweek boundary or an overtime rate not applied.</p>"""),
    S("Hours-only and project timesheets", """
<p>Some timesheets list only hours per day (no clock times) or hours per project. These are fine for pay if hours are accurate, but without times they are harder to audit. If you can, keep a private note of your actual start and end times, particularly for days when you leave early, work through a break or start before the scheduled time.</p>"""),
]
EXTRA["/guides/meal-and-rest-break-laws/"] = [
    S("How to check your own state", """
<ol>
<li>Open the Department of Labor's state table and find your state's row. It links to the state agency.</li>
<li>On the state agency page, look for a topic named meal periods, rest breaks or hours of work. Note the length, when the break must be given and who is covered.</li>
<li>Check whether your industry or occupation has a separate wage order or exemption.</li>
<li>Check your employer handbook, union contract or offer letter; they can provide more than the minimum.</li>
<li>If you are not sure, ask your state labor department. They answer these questions.</li>
</ol>"""),
    S("Example: a 12-hour shift where a second meal period is listed", box("12-hour shift in California", """
<p>The DOL table lists a second 30-minute meal period for shifts over 10 hours in California, subject to waiver rules. If both meal periods are unpaid and taken, 12 hours clock to clock becomes <b>11:00</b> paid (12:00 minus 1:00). If only one 30-minute meal is taken, paid time is 11:30. The calculator's <a href="/lunch-break-calculator/">lunch break tool</a> lets you test either pattern.</p>""")),
    S("Why break rules and pay rules are different", """
<p>Break laws (whether you get a break and when) come mostly from state law. Pay rules (whether the break is paid and whether it counts toward overtime) come from federal regulations plus state law and employer policy. Consequently, an employer can comply with one and not the other. For example, a state may require a 30-minute meal period, while the federal regulations decide whether a given meal period is a bona fide, unpaid one (complete relief from duty).</p>"""),
]
EXTRA["/guides/rounding-time-cards/"] = [
    S("A full week of examples", tbl(
        ["Day", "Actual in / out", "Rounded (15 min)", "Actual paid (30 min meal)", "Rounded paid"],
        [["Mon", "7:58 / 4:32", "8:00 / 4:30", "8:04", "8:00"], ["Tue", "8:09 / 4:36", "8:15 / 4:30", "7:57", "7:45"], ["Wed", "7:51 / 4:44", "7:45 / 4:45", "8:23", "8:30"], ["Thu", "8:03 / 5:12", "8:00 / 5:15", "8:39", "8:45"], ["Fri", "8:00 / 4:25", "8:00 / 4:30", "7:55", "8:00"]]) + """
<p>This week: actual 40:58; rounded 41:00. Individual days move up or down, but the total is within two minutes. This is what a neutral rounding policy looks like. If every row of a real week went the same way, you would need to question the policy.</p>"""),
    S("Alternatives to rounding", """
<ul>
<li><b>Pay to the minute.</b> Modern systems calculate exact minutes; it is simple to explain.</li>
<li><b>Grace periods with exact pay.</b> Allow a short window for attendance policy without changing pay.</li>
<li><b>Rounding in tenths.</b> Round to 6 minutes so each entry is a one-decimal number, if the policy is neutral.</li>
</ul>"""),
]
EXTRA["/guides/time-card-mistakes-and-how-to-fix-them/"] = [
    S("A simple correction request you can copy", """
<div class="formula">Subject: Time card correction - [date]<br>Hello [name], on [date] I clocked in at [time] and out at [time] with a [length] unpaid meal. The card shows [what it shows]. The correct paid time is [hours:minutes]. Please correct it before the [date] payroll cutoff. Thank you.</div>
<p>Keep a copy. If the correction is declined, ask for the reason in writing.</p>"""),
    S("Special cases that cause errors", """
<ul>
<li><b>Overnight shifts</b> assigned to the wrong day, which can move hours into the wrong workweek.</li>
<li><b>Transfers between departments or pay rates</b> during one shift, where each block needs its own rate.</li>
<li><b>Holidays</b> where the premium is applied to the wrong hours.</li>
<li><b>Daylight saving time changes</b>, when a night shift is an hour longer or shorter than the clock shows.</li>
<li><b>Edits by a supervisor</b> after you signed the card.</li>
</ul>"""),
    S("For managers: a correction log", """
<p>Keep a record of every change: the date, the original entry, the corrected entry, who requested it, who approved it and why. A log makes payroll audits simple and protects both employee and employer. Corrections should be made the same pay period when possible.</p>"""),
]
EXTRA["/guides/tracking-hours-for-freelancers-and-contractors/"] = [
    S("Set your hourly rate from an income goal", box("Target: $80,000 a year", """
<p>Not all of your working hours are billable. If you can bill 1,200 hours a year (about 23 a week over 52 weeks), the rate needed is $80,000 &divide; 1,200 = <b>$66.67 an hour</b> before business costs and taxes. Billing 1,500 hours lowers that to $53.33. Tracking your actual billable hours for a few months replaces guesswork with data.</p>""")),
    S("Learn what fixed-price projects really pay", box("$2,400 project, 48 hours", """
<p>You quote a fixed fee of $2,400. When you track the work it takes 48 hours, so the effective rate is $2,400 &divide; 48 = <b>$50 an hour</b>. If you had estimated 30 hours at $80 an hour, the project took 18 hours longer than planned and paid $30 an hour less. Tracking time on fixed-fee work shows which projects are worth repeating.</p>""")),
    S("A simple log template", tbl(
        ["Date", "Client", "Task", "Start", "End", "Hours", "Billable?"],
        [["Mar 2", "Acme", "Wireframes", "9:00", "11:30", "2:30", "Yes"], ["Mar 2", "-", "Invoicing", "11:30", "12:00", "0:30", "No"], ["Mar 3", "Acme", "Revisions", "1:00", "3:45", "2:45", "Yes"]]) + """
<p>A spreadsheet with these columns is enough. Add a totals row per client per week, convert minutes to decimals with the <a href="/decimal-hours-converter/">decimal hours converter</a>, and attach the log to your invoice.</p>"""),
]
