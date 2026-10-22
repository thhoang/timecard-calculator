"""More explanatory sections (second batch), appended to the lists in extras.EXTRA."""
from .extras import EXTRA, S, box, tbl


def add(slug, *sections):
    EXTRA.setdefault(slug, []).extend(sections)


# ---------------------------------------------------------------- calculators
add("/decimal-hours-converter/", S("Where decimal hours show up", """
<p>You meet decimal hours in payroll exports, invoices, project trackers, spreadsheets and union pay schedules. A spreadsheet stores a duration as a fraction of a day, so 6:00 is 0.25 in a time-formatted cell; multiply by 24 to get decimal hours (0.25 &times; 24 = 6.00). If you copy a time like 7:45 into a spreadsheet and multiply it by the hourly rate directly, the answer will be wrong unless you first multiply the time by 24. The converters above avoid that trap by working in plain hours and minutes.</p>
<p>Rule of thumb for checking: if the minutes are under 30, the decimal should be under .50; if you see 7.45 where you expected 7:45, the decimal is wrong, because 7:45 is 7.75.</p>"""))
add("/hourly-to-salary/", S("A step-by-step conversion you can do on paper", """
<ol>
<li>Write the hourly rate: say $23.50.</li>
<li>Multiply by the hours you work in a week, say 38: $23.50 &times; 38 = $893.00.</li>
<li>Multiply by the paid weeks, 52: $893.00 &times; 52 = <b>$46,436.00</b>.</li>
<li>Divide by 12 for a monthly figure ($3,869.67), by 26 for a bi-weekly check ($1,786.00) or by 24 for a semi-monthly check ($1,934.83).</li>
</ol>
<p>Keep the unrounded numbers until the last step; rounding the weekly figure to the nearest dollar before multiplying by 52 can shift the result by tens of dollars.</p>"""))
add("/salary-to-hourly/", S("A step-by-step conversion you can do on paper", """
<ol>
<li>Write the annual salary: $48,000.</li>
<li>Work out the hours you really work in a year: 42 hours &times; 52 weeks = 2,184.</li>
<li>Divide: $48,000 &divide; 2,184 = <b>$21.98 an hour</b>. At exactly 40 hours (2,080) it would be $23.08.</li>
<li>Subtract any unpaid weeks first, if you have them: with 3 unpaid weeks, 42 &times; 49 = 2,058 hours and the rate is $23.32.</li>
</ol>
<p>The difference between $21.98 and $23.08 for the same salary is the reason to enter your true hours.</p>"""),
    S("Salary to hourly in different pay periods", """
<p>A salary is often communicated as a pay period amount rather than an annual figure. To convert a bi-weekly check to an hourly rate, divide by the hours in the two weeks: $1,800 &divide; 80 = $22.50. For a semi-monthly check of $2,000, multiply by 24 for the annual salary ($48,000) and divide by 2,080 for $23.08. For a monthly figure, multiply by 12. The calculator above uses the annual amount so that every case uses the same method.</p>"""))
add("/hours-calculator/", S("Answering common 'how many hours' questions", tbl(
    ["Question", "Answer"],
    [["How many hours from 7 am to 3 pm?", "8 hours"], ["How many hours from 9 pm to 5 am?", "8 hours"], ["How many hours from 6:30 am to 2:45 pm?", "8 hours 15 minutes (8.25)"], ["How many hours from 12 am to 12 pm?", "12 hours"], ["How many hours from 3:15 pm to 11:40 pm?", "8 hours 25 minutes (8.42)"]]) + """
<p>For any of these with an unpaid break, subtract it and the calculator above does the rest. Remember that 12:00 am is midnight and 12:00 pm is noon, which is a frequent source of 12-hour errors.</p>"""))
add("/lunch-break-calculator/", S("Keeping a lunch log", """
<p>If you are asked to record your lunch yourself, write the start and end times, not just the length. &ldquo;12:10 to 12:42&rdquo; is clearer evidence than &ldquo;30 minutes&rdquo; and shows days when the break was shorter than scheduled or was interrupted. A month of notes is enough to show a pattern to your supervisor or to payroll.</p>"""))
add("/military-time-converter/", S("Conversion examples", tbl(
    ["12-hour", "24-hour", "Military"],
    [["5:30 AM", "05:30", "0530"], ["12:00 PM (noon)", "12:00", "1200"], ["1:15 PM", "13:15", "1315"], ["6:45 PM", "18:45", "1845"], ["11:59 PM", "23:59", "2359"], ["12:01 AM", "00:01", "0001"]]) + """
<p>Notice the two traps: 12:00 PM is noon (stays 12) and 12:01 AM is just after midnight (becomes 00:01). Most mistakes come from these two cases.</p>"""),
    S("Shift lengths in military time", """
<p>Subtract the start from the end after converting to hours and minutes. For 1900 to 0300: 03:00 is earlier than 19:00 so add 24 hours: 27:00 &minus; 19:00 = 8:00. For 0545 to 1415: 14:15 &minus; 05:45 = 8 hours 30 minutes. For 2230 to 0600: 30:00 &minus; 22:30 = 7 hours 30 minutes. If you subtract the four-digit numbers directly (1415 &minus; 545 = 870), the result is meaningless, because the last two digits are minutes that roll over at 60.</p>"""))
add("/minutes-to-decimal-chart/", S("Reading minutes the way payroll does", """
<p>Payroll forms that ask for hours in decimals expect the minutes part to be a fraction of an hour, not a count of minutes. A time card entry of 7 hours 12 minutes becomes 7.20 (12 &divide; 60 = 0.20), which is easy to confuse with 7.12. The cleanest habit is to convert only at the end: total the hours and minutes, then convert once using the chart or the calculator. If you routinely work in 6-minute increments, each increment is exactly one tenth of an hour, which is why some time clocks use them.</p>"""))
add("/paycheck-calculator/", S("Using the estimator for planning", """
<p>The estimator is most useful for what-if questions: how much does a raise change take-home pay, what does a 401(k) contribution really cost after tax, how much of an overtime week is kept? Run it twice with one input changed and compare the net lines. For example, raising a $2,000 bi-weekly gross to $2,200 raises take-home by far less than $200, because 22 cents of every extra dollar is withheld at the 22% federal bracket at higher incomes. Use the paycheck estimator for the shape of the answer, not the penny.</p>"""))
add("/pto-accrual-calculator/", S("PTO planning example", box("15 days a year, bi-weekly, wants a 10-day trip in August", """
<p>Accrual is 4.62 hours per bi-weekly check. By the check dated August 15 (pay period 17, assuming the first check is January 3) the balance is about 17 &times; 4.62 = 78.5 hours, or 9.8 days, if none has been used. That is just short of a 10-day trip (80 hours), so waiting one more pay period (83.1 hours) gets there. Enter your own accrual in the calculator to find your date.</p>""")))
add("/semi-monthly-time-card-calculator/", S("Entering part of a month", """
<p>If you started or ended a job mid-period, enter only the days you worked and leave the rest blank. The result is the total for the days you entered. For a final paycheck or a partial first paycheck, compare the total to your pay stub; some employers pay partial periods by days instead of hours, so ask how yours is calculated.</p>"""))
add("/shift-differential-calculator/", S("Checking your pay stub for differentials", """
<p>A correct stub shows the differential either as a separate earnings line (&ldquo;night differential&rdquo;, hours and rate) or as a blended rate. Compare the hours on that line with the hours your shift spent in the window. If you worked 9:00 pm to 5:30 am with a 10:00 pm start for the differential, the shift has 7.5 hours in the window (before any break), not the full 8.5 hours.</p>"""))
add("/time-duration-calculator/", S("Common calculations people run here", tbl(
    ["Task", "Example", "Result"],
    [["Total a week of billable tasks", "2:30 + 1:45 + 3:15 + 0:50", "8:20"], ["Subtract lunch from a shift", "8:45 - 0:30", "8:15"], ["Add commute both ways", "0:42 + 0:48", "1:30"], ["Overtime beyond 8 hours", "10:20 - 8:00", "2:20"], ["Remaining time in a 40-hour week", "40:00 - 34:35", "5:25"], ["Total two shifts", "6:40 + 5:50", "12:30"]]) + """
<p>Each of these can be done in the first calculator above. Use <b>Subtract</b> on the second line to take time away from the first.</p>"""),
    S("Time zones, days and long durations", """
<p>This calculator treats a day as exactly 24 hours (1,440 minutes). It does not know about time zones or daylight saving changes; if a task spans a clock change, adjust by an hour. Durations over 24 hours are shown both in total hours and as days plus hours, so 52:30 appears as 52:30 and 2d 4:30.</p>"""))
add("/time-rounding-calculator/", S("Choosing the rounding that fits your payroll", """
<p>If your system stores time in tenths of an hour, use 6-minute rounding so that every entry is a clean decimal. If it uses quarter hours, use 15. If you are an employer deciding whether to round at all, run a sample of real punches through this calculator in both directions and compare the totals across several weeks before adopting a policy.</p>"""))
add("/timesheet/", S("Using the timesheet as a weekly habit", """
<p>People who check their hours weekly find mistakes while they are still easy to fix. Fill the timesheet on Friday afternoon (or at the end of your workweek), compare it with the hours you expect on your next stub and keep a copy. If the stub differs, you already have your own record. The same routine works for contractors who invoice weekly.</p>"""))
add("/work-schedule-planner/", S("Example: comparing two schedules", tbl(
    ["Plan", "Shifts per 14 days", "Hours at 12 h", "Highest week", "Average / week"],
    [["2-2-3", "7", "84", "60 h (5 shifts)", "42 h"], ["4 on, 4 off", "7 (varies)", "84", "48 h (4 shifts)", "42 h"], ["3 on, 4 off", "6", "72", "36 h", "36 h"], ["5 on, 2 off (8 h)", "10", "80", "40 h", "40 h"]]) + """
<p>The two 42-hour averages differ in how they are distributed, which matters for overtime. Use the calendar above with your own times to see each week.</p>"""))

# ---------------------------------------------------------------- guides
add("/guides/bi-weekly-vs-semi-monthly-pay/", S("How to convert between pay schedules", """
<ul>
<li>Bi-weekly check &times; 26 &divide; 24 = semi-monthly check ($2,307.69 &times; 26 &divide; 24 = $2,500.00).</li>
<li>Semi-monthly check &times; 24 &divide; 26 = bi-weekly check.</li>
<li>Either check &times; its number of periods = annual gross.</li>
<li>Monthly &times; 12 &divide; 52 = weekly equivalent.</li>
</ul>
<p>Use this when comparing job offers that quote different pay periods. Always convert to annual before comparing; a larger-looking check is not necessarily a higher salary.</p>"""))
add("/guides/exempt-vs-non-exempt/", S("Next steps if you are unsure", """
<p>Gather your job description, pay stub and typical weekly hours. Compare your salary with the fact-sheet level and your duties with the exemption description. Then ask your employer or HR for the basis of your classification, and if you still have questions contact the Wage and Hour Division or your state labor department.</p>"""))
add("/guides/how-to-calculate-hours-worked-with-breaks/", S("Putting it together: a worked week", """
<p>Take Monday 7:30-4:15 with a 45-minute unpaid meal (8:00), Tuesday 7:30-4:15 with 45 (8:00), Wednesday 7:30-5:45 with 45 (9:30), Thursday 7:30-4:15 with 45 (8:00) and Friday 7:30-3:45 with 30 (7:45). Total 8:00 + 8:00 + 9:30 + 8:00 + 7:45 = 41:15. Federal overtime is the 1:15 above 40 hours. Changing Friday's meal from 30 to 45 minutes would drop the total to 41:00, and a 60-minute meal on all five days would drop it to 39:15, which is no overtime. Break length is therefore not a detail.</p>"""))
add("/guides/how-to-fill-in-a-paper-time-card/", S("A one-minute daily routine", """
<p>Write the time the moment you clock in or out. Before you leave on Friday, total the week using minutes, then in decimals, and compare. Initial any corrections. Take a photo of the signed card. That routine takes about a minute a day and catches almost every error before payroll sees it.</p>"""))
add("/guides/how-to-read-a-timesheet/", S("When to ask payroll a question", """
<p>Ask when any total is off by more than a few minutes after you account for rounding, when overtime is missing for a week over 40 hours, when a punch was edited without your knowledge, or when a pay code is unfamiliar. Bring the dates, your own totals and the figure on the stub. Being specific gets a faster answer than a general complaint that the hours look wrong.</p>"""))
add("/guides/time-card-mistakes-and-how-to-fix-them/", S("How long a correction can take", """
<p>Policies differ. Some employers correct errors in the next payroll; others require a form and manager approval. Overtime due for a workweek is generally due on the regular payday for the period in which the workweek ends, so a prompt request matters, and if the amount cannot be determined until after the pay period it should be paid as soon as practicable (29 CFR 778.106). Keep dates for every request you make.</p>
<p>If you are an employer, treat each correction as a record: who requested it, what changed, who approved it and when it was paid.</p>"""))
add("/guides/tracking-hours-for-freelancers-and-contractors/", S("Billable utilisation: how many hours are really billable?", """
<p>Utilisation is billable hours divided by total working hours. A freelancer who works 40 hours a week and bills 24 has a 60% utilisation rate. At $60 an hour, that is $1,440 a week, an effective $36 for every hour worked. Admin, sales, invoicing, learning and unpaid revisions are the usual difference. Tracking non-billable time next to billable time lets you price accordingly and decide which work to automate or decline.</p>"""),
    S("Tools you can use for free", """
<p>A spreadsheet, a notebook, your phone's clock app or the printable timesheet on this site is enough to start. The best tool is the one you will use every day. If you use a timer app, still check its total against your own start and end times once a week, because forgotten timers are the most common source of inflated hours.</p>"""))

# ---------------------------------------------------------------- third batch (length top-ups with practical content)
add("/guides/bi-weekly-vs-semi-monthly-pay/", S("Holidays, weekends and direct deposit", """
<p>When a payday falls on a weekend or bank holiday, employers usually pay on the previous business day, though this is a payroll policy that varies. Direct deposit timing also differs by bank. If your rent or loan is due the day after payday, build in a one-day cushion, and check the pay calendar your employer publishes at the start of each year.</p>"""))
add("/guides/how-to-calculate-hours-worked-with-breaks/", S("When the answer is unclear", """
<p>Some situations do not fit neatly: a meal period interrupted twice, a break where you must stay at your post, or a break in which you are allowed to leave but must carry a phone. The federal test is whether you are completely relieved from duty, so the more your employer limits what you can do, the more likely the time is hours worked. Write down what happened and ask payroll or your state labor department if it keeps happening.</p>"""))
add("/guides/how-to-fill-in-a-paper-time-card/", S("What to do when you lose or damage a card", """
<p>Tell your supervisor immediately. Reconstruct the days from your own notes, a schedule, messages or a coworker's recollection, and ask for a replacement card marked as reconstructed and signed by you and your supervisor. Photograph the new card once it is complete so you always have a backup.</p>"""))
add("/guides/time-card-mistakes-and-how-to-fix-them/", S("A weekly five-minute audit", """
<p>Every Friday, check five things: every day has both punches, the AM/PM looks right, the meal deductions match what you took, the weekly total matches your own count and any hours over 40 are marked as overtime. Fix anything immediately. Five minutes a week prevents most disputes.</p>"""))
add("/guides/tracking-hours-for-freelancers-and-contractors/", S("Invoicing from your log", """
<p>Group the log by client and by week, show the date, task and hours on separate lines, and total the hours and the amount. A line-by-line invoice gets paid faster than a single &ldquo;consulting, 12 hours&rdquo; line because the client can see what they are paying for. Keep the log as an attachment or share the relevant rows.</p>"""))
add("/salary-to-hourly/", S("Rounding and the final answer", """
<p>An hourly rate derived from a salary rarely divides evenly, so you will see cents that repeat: $62,000 &divide; 2,080 = $29.8077. Employers who convert salaries usually round to the nearest cent for display but keep the exact figure for payroll. When you compare offers, compare the unrounded numbers or the annual totals.</p>"""))
add("/timesheet/", S("For managers: reviewing a stack of timesheets", """
<p>Check that each sheet has the week start date, daily totals that match the in and out times, the break deducted and a signature. Look first at the weeks with the longest hours: that is where overtime and errors cluster. Compare the totals with the schedule, and ask the employee about any difference before payroll runs.</p>"""))
add("/work-schedule-planner/", S("Printing your plan", """
<p>Press Print this result to produce a clean calendar with the weekly hours for the weeks you selected. Share it with your family or manager to agree on days off, or compare two patterns by printing each one. Because nothing is saved on a server, print before you close the page.</p>"""))
