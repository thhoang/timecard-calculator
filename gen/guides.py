"""Plain-English guides. Rules are stated only where an official source is linked at the bottom of the page."""
from .core import article_page, table, example
from .tools_a import S


def build():
    # ------------------------------------------------------------------ overtime rules by state
    article_page(
        "/overtime-rules/", "Overtime Rules by State",
        "Overtime Rules by State: Federal, CA, AK, NV & CO Explained",
        "Plain-English overtime guide: the federal 40-hour rule plus daily overtime and double time in California, Alaska, Nevada and Colorado, with examples and sources.",
        "Overtime Rules by State",
        "Most US hourly workers fall under the federal weekly overtime rule, but a few states add daily thresholds or double time. This guide explains the rule we can document from official sources, shows how each one changes a paycheck, and links to the calculator that applies it.",
        [
            S("The federal rule (FLSA)", """
<p>The Fair Labor Standards Act requires covered employees who are not exempt to be paid at least <b>one and one-half times their regular rate</b> for hours worked over <b>40 in a workweek</b>. The U.S. Department of Labor defines the workweek as a fixed and regularly recurring period of 168 hours: seven consecutive 24-hour periods. It need not be a calendar week and can start on any day or hour. Two points matter for every calculation:</p>
<ul>
<li><b>No averaging.</b> The Department of Labor states that averaging hours over two or more weeks is not permitted. A 50-hour week and a 30-hour week contain 10 hours of overtime, not zero.</li>
<li><b>No daily overtime by itself.</b> Federal overtime is measured by the workweek. The Department notes that the Act does not require overtime pay for work on Saturdays, Sundays, holidays or rest days as such, and an agreement that only 8 hours a day or 40 hours a week counts as working time does not satisfy the Act.</li>
</ul>
<p>The <b>regular rate</b> includes all remuneration for employment, with specific exclusions such as discretionary bonuses, expense reimbursements and pay for leave. A non-discretionary bonus therefore raises the rate that overtime is based on. Try it in the <a href="/overtime-calculator/">overtime calculator</a>."""),
            S("Where states add daily overtime", """
<p>States can require more than the federal law. These four are implemented in our calculators, each with the agency source linked below.</p>""" + table(
                ["State", "Daily rule", "Weekly rule", "Notes"],
                [["California", "1.5x over 8 hours in a workday; 2x over 12 hours; on the 7th consecutive day in a workweek, 1.5x for the first 8 hours and 2x after 8", "1.5x over 40 hours in a workweek", "The Department of Industrial Relations publishes the rules; some industries and alternative workweek schedules differ."],
                 ["Alaska", "1.5x over 8 hours in a day", "1.5x over 40 hours in a week", "Daily overtime hours are not counted again toward the weekly total. Exemptions include employers with three or fewer employees and certain flexible work-hour plans approved by the Department."],
                 ["Nevada", "1.5x over 8 hours in a 24-hour period, only for employees paid less than 1.5 times the state minimum wage", "1.5x over 40 hours in a scheduled week for the same lower-paid employees", "Higher-paid employees are not covered by the statute's daily rule. The Labor Commissioner issued Advisory Opinion AO-2025-05 on daily vs weekly overtime."],
                 ["Colorado", "1.5x for work over 12 hours in a workday or over 12 consecutive hours, whichever calculation gives the greater payment", "1.5x over 40 hours in a workweek", "Hours cannot be averaged across workweeks; qualifying meal periods may be subtracted when counting 12 consecutive hours."]], num_from=9) +
              "<p>Every other state has its own wage-hour law, and many simply follow the federal rule; some set different weekly thresholds or industry-specific rules. We do not list them because we can only publish what we can cite: look up your state labor department's overtime page, and use the &ldquo;Federal&rdquo; option in our calculators only if your state follows that standard.</p>"),
            S("Worked examples: same hours, different pay", example("Three days of 10 hours plus one of 12, at $25.00", """
<p>Mon 10, Tue 10, Wed 10, Thu 12 = 42 hours.</p>
<ul>
<li><b>Federal:</b> 40 regular + 2 overtime = 40 &times; $25 + 2 &times; $37.50 = $1,000 + $75 = <b>$1,075.00</b>.</li>
<li><b>California:</b> Mon-Wed: 2 overtime hours each (6); Thu: 4 overtime hours (hours 9-12) = 10 overtime hours, 32 regular. Pay = 32 &times; $25 + 10 &times; $37.50 = $800 + $375 = <b>$1,175.00</b>.</li>
<li><b>Colorado:</b> no day passes 12 hours, so only the weekly rule applies: 2 overtime hours, <b>$1,075.00</b>.</li>
<li><b>Alaska:</b> same as California without double time: 10 daily overtime hours, regular-by-day hours 32 (below 40 so no weekly overtime), <b>$1,175.00</b>.</li>
</ul>
<p>The $100 gap between the federal and California results is the cost of the daily rule for this particular week.</p>""")),
            S("California's seventh day and double time", """
<p>According to the California Department of Industrial Relations, double pay applies to hours beyond 12 in a workday and to hours beyond 8 on the seventh consecutive day of work in a workweek. In the calculator the seventh-day rule applies only when all seven days of the workweek have hours. A week of 8 hours Monday to Sunday (56 hours) is 8 hours at the weekly 1.5x for hours over 40, plus 8 hours on the seventh day at 1.5x, for 16 overtime hours and 40 regular hours.</p>"""),
            S("How to pick the right rule in a calculator", """
<ol>
<li>Choose the rule for the state where you <i>work</i>, not where you live.</li>
<li>If you are not sure whether you are exempt from overtime, read the <a href="/guides/exempt-vs-non-exempt/">exempt vs non-exempt guide</a> first.</li>
<li>Enter hours actually worked per day, starting with the first day of your employer's workweek.</li>
<li>Compare the result with your pay stub. If it differs, ask payroll to explain; then see <a href="/guides/time-card-mistakes-and-how-to-fix-them/">time card mistakes</a>.</li>
</ol>"""),
        ],
        [("When does overtime start?", "Under federal law, after 40 hours in a workweek. California, Alaska, Colorado and (for lower-paid workers) Nevada also have daily thresholds, as described above."),
         ("Does every state have daily overtime?", "No. Many states follow the federal weekly standard only. Check your state labor department for your own rules."),
         ("Do I get overtime if I am salaried?", "Only if you are non-exempt. The salary basis is one of several tests for exemption; see the exempt vs non-exempt guide."),
         ("Can my employer give me time off instead of overtime pay?", "Rules on compensatory time are narrow and depend on the employer and the state. For example, Nevada's regulations say an employer may not substitute compensatory time for overtime wages, and Colorado's COMPS Order does not allow comp time for covered private employers. Ask your state labor department."),
         ("Does a holiday count as overtime?", "The Department of Labor says the FLSA does not require overtime pay for work on holidays as such. Your employer or union contract may pay a premium.")],
        sources=["dol23", "dol56a", "ca_ot", "ak_ot", "nv_ot", "co_ot"],
        related=["/overtime-calculator/", "/time-card-calculator/", "/guides/exempt-vs-non-exempt/", "/guides/how-to-calculate-hours-worked-with-breaks/"],
    )

    # ------------------------------------------------------------------ exempt vs non-exempt
    article_page(
        "/guides/exempt-vs-non-exempt/", "Exempt vs Non-Exempt",
        "FLSA Exempt vs Non-Exempt Employees: What It Means for Overtime",
        "Exempt vs non-exempt explained: who gets overtime under the FLSA, the salary basis test, why job title is not enough, and how to check your own status before you track hours.",
        "Exempt vs Non-Exempt: Who Gets Overtime?",
        "Whether you are owed overtime depends on your classification, not on whether you are paid hourly or by salary. Here is how the federal categories work and how to check where you fit.",
        [
            S("The basic definitions", """
<p><b>Non-exempt</b> employees are covered by the Fair Labor Standards Act's minimum wage and overtime rules: they must be paid at least one and one-half times their regular rate for hours over 40 in a workweek. <b>Exempt</b> employees are excluded from the overtime requirement because they meet specific legal tests. Most hourly workers are non-exempt. Some salaried employees are exempt and some are not.</p>
<p>The Department of Labor's fact sheet on the executive, administrative, professional and computer exemptions explains that to qualify, an employee generally must be paid on a salary basis at not less than a specified weekly amount (the fact sheet lists $684 per week) <i>and</i> must perform the duties described for that exemption. Because exemption requires a salary basis, a worker paid strictly by the hour cannot qualify under those white-collar exemptions.</p>"""),
            S("The three questions to ask", """
<ol>
<li><b>How am I paid?</b> A fixed salary regardless of hours, or an hourly wage? An hourly wage points to non-exempt.</li>
<li><b>Is the salary high enough?</b> The salary level in the Department of Labor fact sheet is a minimum for the white-collar exemptions. Falling below it means non-exempt. The figure is updated by rulemaking and court decisions, so check dol.gov for the current number rather than relying on a copy.</li>
<li><b>Do my duties fit the exemption?</b> Duties, not the job title, decide. Calling someone a &ldquo;manager&rdquo; does not make them exempt if they do not perform the exempt duties.</li>
</ol>"""),
            S("A comparison table", table(
                ["", "Non-exempt", "Exempt"],
                [["Overtime pay at 1.5x over 40 h/week (federal)", "Yes", "No (under the FLSA)"], ["Typical pay method", "Hourly, or salary plus overtime", "Salary basis"],
                 ["Must track hours for pay", "Employer must keep records of hours", "Pay does not vary with hours; tracking is optional but useful"],
                 ["Rate used for overtime", "Regular rate (includes non-discretionary bonuses)", "Not applicable"]], num_from=9)),
            S("Worked examples", example("Salaried but non-exempt", """
<p>An office clerk is paid $640 a week, below the weekly minimum cited in the DOL fact sheet, so the clerk cannot be treated as exempt under these tests. Suppose the $640 is understood to cover a 40-hour week: the regular rate is $640 &divide; 40 = $16.00. In a 46-hour week, 6 hours are overtime at 1.5 &times; $16.00 = $24.00, so the clerk is owed $640 + 6 &times; $24 = <b>$784.00</b>. How the regular rate is set for a salary depends on what hours the salary was agreed to cover, so confirm with the Department of Labor or your state before relying on this illustration.</p>""") +
              example("Hourly worker who asks for a promotion to 'salaried manager'", """
<p>An hourly employee at $22/hour regularly works 48 hours, earning 40 &times; $22 + 8 &times; $33 = $1,144 per week. If they become a salaried &ldquo;manager&rdquo; at $52,000 ($1,000 a week) without meeting the duties test, they could be non-exempt and still owed overtime. If they do meet the duties and salary tests, they lose overtime and might earn less per hour worked. Compare offers with the <a href="/salary-to-hourly/">salary to hourly calculator</a>.</p>""")),
            S("Why this matters when you track hours", """
<p>If you are non-exempt, your time card is the basis of your pay, and mistakes cost money: use the <a href="/time-card-calculator/">time card calculator</a> and keep your own record. If you are exempt, you may still want to track hours to see your effective hourly rate or to document a dispute. State laws can be stricter than federal rules: some states set higher salary thresholds, so being exempt federally may not mean exempt in your state.</p>"""),
        ],
        [("Is every salaried employee exempt from overtime?", "No. Under the tests described by the Department of Labor, a salaried employee must meet the salary level and the duties test to be exempt."),
         ("Can an hourly employee be exempt?", "Not under the executive, administrative, professional or computer exemptions in the DOL fact sheet, which require a salary basis."),
         ("What is the federal salary threshold?", "The DOL fact sheet 17A (revised September 2019) lists $684 per week. Salary thresholds have been the subject of rulemaking and court decisions, so confirm the current level at dol.gov before relying on it."),
         ("Does job title decide exempt status?", "No. Duties and pay decide. The title alone does not."),
         ("What should I do if I think I am misclassified?", "Gather your time records and pay stubs and contact the U.S. Department of Labor's Wage and Hour Division or your state labor department.")],
        sources=["dol23", "dol17a"],
        related=["/overtime-rules/", "/overtime-calculator/", "/salary-to-hourly/", "/guides/time-card-mistakes-and-how-to-fix-them/"],
    )

    # ------------------------------------------------------------------ hours worked with breaks
    article_page(
        "/guides/how-to-calculate-hours-worked-with-breaks/", "Calculating Hours Worked with Breaks",
        "How to Calculate Hours Worked With Breaks and Lunch (Paid vs Unpaid)",
        "How to calculate hours worked with breaks: which breaks are paid or unpaid, the formula, worked examples with lunch and rest breaks, and what federal regulations say.",
        "How to Calculate Hours Worked With Breaks",
        "Subtract the unpaid meal, keep the paid rest breaks. It sounds simple, but one wrong break can move you across the 40-hour overtime line. This guide gives the formula, the rules and the common traps.",
        [
            S("The formula", """
<div class="formula">hours worked = (clock-out &minus; clock-in) &minus; unpaid meal periods</div>
<p>Work in hours and minutes, then convert to decimal hours for pay. Example: 7:55 am to 4:35 pm with a 30-minute unpaid lunch. 7:55 to 4:35 is 8 hours 40 minutes; minus 30 minutes is <b>8 hours 10 minutes</b> (8.17 decimal hours). The <a href="/hours-calculator/">hours calculator</a> and <a href="/lunch-break-calculator/">lunch break calculator</a> show the same working.</p>"""),
            S("Rest breaks versus meal periods", """
<p>Federal regulations draw the line this way:</p>
<ul>
<li><b>Rest periods (about 5 to 20 minutes):</b> 29 CFR 785.18 says rest periods of short duration, running from 5 minutes to about 20 minutes, are common in industry, and they are usually paid as working time and must be counted as hours worked.</li>
<li><b>Bona fide meal periods:</b> 29 CFR 785.19 says bona fide meal periods are not worktime. The employee must be completely relieved from duty for the purposes of eating regular meals, and ordinarily 30 minutes or more is long enough.</li>
</ul>
<p>So a 15-minute coffee break stays in your hours; a 30-minute lunch where you are completely off duty comes out. A lunch at your desk where you answer calls is not a bona fide meal period and should be paid.</p>"""),
            S("Worked examples", example("A week with different breaks", """
<table class="plain" style="width:auto"><tbody>
<tr><td>Mon 8:00-4:30, 30 min lunch</td><td>8:00</td></tr>
<tr><td>Tue 8:00-4:30, 30 min lunch</td><td>8:00</td></tr>
<tr><td>Wed 8:00-5:00, 30 min lunch scheduled, but 10 min was spent answering the phone (only 20 min unpaid)</td><td>9:00 - 0:20 = 8:40</td></tr>
<tr><td>Thu 7:30-4:30, 60 min lunch</td><td>8:00</td></tr>
<tr><td>Fri 8:00-4:30, 30 min lunch</td><td>8:00</td></tr>
</tbody></table>
<p>Corrected total: 8:00 + 8:00 + 8:40 + 8:00 + 8:00 = 40:40, so 40 minutes are overtime under the federal weekly rule. The 10 recovered minutes land entirely in overtime: 1/6 hour &times; $30.00 = $5.00 at $20.00/hour, compared with $3.33 at straight time. Small corrections matter at the overtime line.</p>""") +
              example("Break length chosen vs break actually taken", """
<p>A scheduler lists a 60-minute lunch, but the employee takes 35 minutes before returning to the line. Hours worked should reflect the 35-minute break actually taken (if it was unpaid), not the 60 minutes on the schedule: 8:00 to 5:00 is 9:00 less 0:35 = 8:25.</p>""")),
            S("Common traps", """
<ul>
<li><b>Automatic deductions.</b> A timekeeping system that takes 30 minutes every day is only accurate on the days you really took 30 minutes. Report days you worked through lunch.</li>
<li><b>Short unpaid breaks.</b> A 10-minute &ldquo;unpaid&rdquo; break is a rest period and generally should be paid.</li>
<li><b>Travel and waiting.</b> Time spent waiting or on call can be hours worked in some circumstances; the answer depends on the facts. This guide covers breaks only.</li>
<li><b>State rules.</b> States may require meal or rest breaks, or specify when they are paid; see <a href="/guides/meal-and-rest-break-laws/">meal and rest break laws by state</a>.</li>
</ul>"""),
            S("Checklist for your own time card", """
<ol>
<li>Write down your real clock-in, clock-out and lunch start/end.</li>
<li>Subtract only the unpaid meal that you took off duty.</li>
<li>Convert to decimal hours with the <a href="/decimal-hours-converter/">converter</a> if your payroll uses decimals.</li>
<li>Add the days, then check the weekly total against 40 for overtime.</li>
</ol>"""),
        ],
        [("Are 15-minute breaks paid?", "Generally yes under federal regulations: rest periods of about 5 to 20 minutes are usually paid and counted as hours worked."),
         ("Is an unpaid lunch deducted from hours worked?", "Yes, if it is a bona fide meal period during which you are completely relieved from duty. 30 minutes or more is ordinarily long enough."),
         ("What if I work during my lunch?", "That time is generally hours worked and should be paid. Report it so the time card can be corrected."),
         ("Does federal law require breaks?", "Federal regulations say when breaks count as paid or unpaid time; the Department of Labor lists break requirements state by state, because they come from state law."),
         ("How do I calculate hours worked from clock times?", "Subtract clock-in from clock-out, then subtract unpaid meal periods.")],
        sources=["cfr785_18", "cfr785_19", "dol_meal"],
        related=["/lunch-break-calculator/", "/hours-calculator/", "/guides/meal-and-rest-break-laws/", "/time-card-calculator/"],
    )

    # ------------------------------------------------------------------ rounding time cards
    article_page(
        "/guides/rounding-time-cards/", "Rounding Time Cards Legally",
        "Rounding Time Cards: What the Federal Rule Allows (5, 6 & 15 Minutes)",
        "Rounding time cards: the 29 CFR 785.48 rule, how the 7-minute rule works, how to test whether rounding is fair, and when employers get into trouble. Worked examples included.",
        "Rounding Time Cards: What Is Allowed?",
        "Time clocks often round your punches to the nearest 5, 6 or 15 minutes. Federal regulation permits the practice in some circumstances. This guide explains what the rule actually says and how to check whether rounding at your workplace is fair.",
        [
            S("What the regulation says", """
<p>29 CFR 785.48(b) addresses &ldquo;rounding&rdquo; practices. It recognises the practice, used for many years, of recording employees' starting and stopping time to the nearest 5 minutes, or to the nearest one-tenth or quarter of an hour. It treats this as acceptable for enforcement purposes where the practice is applied in a way that will not result, over a period of time, in failure to compensate the employees properly. In other words, rounding is allowed when it is neutral: sometimes up, sometimes down, and on average it does not cost workers time.</p>
<p>The regulation does not use the phrase &ldquo;7-minute rule&rdquo;. That is the common name for how quarter-hour rounding works in practice (below). The rule also does not say your state allows rounding: states may have their own limits, so check your state labor department.</p>"""),
            S("How the 7-minute rule works", """
<p>With a quarter-hour grid, the marks are :00, :15, :30 and :45. A punch within 7 minutes of a mark rounds to that mark; a punch 8 minutes or more past a mark rounds forward to the next one. Rounding to 5 minutes and 6 minutes (tenths of an hour) works the same way with a smaller grid. Use the <a href="/time-rounding-calculator/">time rounding calculator</a> to test your own punches.</p>""" + table(
                ["Actual punch", "Rounded (15 min)", "Effect on paid time"],
                [["In at 7:52 am", "7:45 am", "+7 min paid"], ["In at 7:53 am", "8:00 am", "-7 min paid"], ["In at 8:07 am", "8:00 am", "+7 min paid"], ["In at 8:08 am", "8:15 am", "-7 min paid"], ["Out at 5:07 pm", "5:00 pm", "-7 min paid"], ["Out at 5:08 pm", "5:15 pm", "+7 min paid"]], num_from=1)),
            S("A fairness test with real numbers", example("Is this rounding neutral?", """
<p>An employee arrives early to get ready and clocks in at 7:53 every morning and out at exactly 4:30. The 7:53 punch is 8 minutes past 7:45, so it rounds <i>up</i> to 8:00 and the employee loses 7 minutes of paid time a day. Over 20 days that is <b>140 minutes (2 hours 20 minutes) of unpaid work</b>, worth $46.67 at $20.00/hour. If the same employee clocked in at 7:52 instead, the punch would round down to 7:45 and gain 7 minutes. Rounding is neutral only if both kinds of punches appear about equally. If most punches fall where rounding goes against the employee &mdash; for example when workers must clock in a few minutes early to get ready &mdash; the rounding shortchanges them every day.</p>
<p><b>What to do:</b> keep a log of actual punches for a month, total the rounded and unrounded hours using the <a href="/time-card-calculator/">time card calculator</a>, and see which way the difference runs. A persistent gap in one direction is the pattern the regulation's &ldquo;over a period of time&rdquo; language is aimed at.</p>""")),
            S("Common questions employers and employees ask", """
<ul>
<li><b>Can the employer always round down?</b> Rounding that systematically favors the employer is the practice that attracts scrutiny; the regulation's condition is that it does not result in failure to compensate employees properly over time.</li>
<li><b>Should rounding apply to start and end, or to the total?</b> The regulation speaks of recording starting and stopping time; punch rounding is the standard application. Rounding a total can distort overtime differently.</li>
<li><b>What about rounding that crosses the 40-hour line?</b> Overtime depends on the rounded hours your employer pays; a few minutes can mean a few overtime minutes. See the example in the <a href="/overtime-calculator/">overtime calculator</a>.</li>
<li><b>Do states ban rounding?</b> Some may; we only publish what we can cite, so check your state labor department's guidance.</li>
</ul>"""),
            S("Tips for employees and small employers", """
<ul>
<li>Employees: keep your own record and compare it to the pay stub every period.</li>
<li>Employers: if you round, document the rule, apply it to every punch in both directions and audit periodically with a sample of real punches.</li>
<li>If time to the minute is practical, many employers simply pay to the minute, which avoids the question.</li>
</ul>"""),
        ],
        [("What is the 7-minute rule?", "The common name for rounding punches to the nearest quarter hour: 1-7 minutes past a mark rounds down and 8-14 minutes rounds up."),
         ("Is rounding to the nearest 15 minutes legal?", "Federal regulation 29 CFR 785.48(b) accepts rounding to the nearest 5 minutes, tenth or quarter hour when it does not, over time, result in failure to compensate employees properly. State law may add limits."),
         ("Can my employer round my time in their favor only?", "A practice that consistently favors the employer risks failing the regulation's condition. If you think it applies to you, document your actual punches and ask payroll or your labor department."),
         ("Does rounding apply to breaks?", "Check your employer's policy; the regulation discusses starting and stopping time."),
         ("How can I check my rounding?", "Use the rounding calculator on your real punches, and compare rounded and actual totals over several weeks.")],
        sources=["cfr785_48"],
        related=["/time-rounding-calculator/", "/decimal-hours-converter/", "/time-card-calculator/", "/guides/time-card-mistakes-and-how-to-fix-them/"],
    )

    # ------------------------------------------------------------------ paper time card
    article_page(
        "/guides/how-to-fill-in-a-paper-time-card/", "Filling In a Paper Time Card",
        "How to Fill In a Paper Time Card Step by Step (With Example)",
        "How to fill in a paper time card: what each column means, how to write times, record breaks, total hours in hours and minutes, convert to decimals and avoid common mistakes.",
        "How to Fill In a Paper Time Card",
        "Paper cards still run many shops, farms, job sites and small offices. This is a practical walk-through of every column, with a completed example you can check against our calculator.",
        [
            S("What is on a typical time card", """
<table class="plain" style="width:auto"><tbody>
<tr><td><b>Employee name / ID</b></td><td>Exactly as on payroll.</td></tr>
<tr><td><b>Pay period or week ending</b></td><td>The start and end dates, or the week-ending date. This also identifies the workweek.</td></tr>
<tr><td><b>Date / day</b></td><td>One row per day.</td></tr>
<tr><td><b>In / Out</b></td><td>Clock-in and clock-out. Some cards have two in/out pairs per day for split shifts.</td></tr>
<tr><td><b>Lunch or break</b></td><td>Unpaid minutes, or the out and in times for the meal.</td></tr>
<tr><td><b>Daily hours</b></td><td>Hours worked that day.</td></tr>
<tr><td><b>Total hours / overtime</b></td><td>Weekly total and any hours over the overtime threshold.</td></tr>
<tr><td><b>Signatures</b></td><td>Employee and supervisor, often with the date.</td></tr>
</tbody></table>"""),
            S("Step by step", """
<ol>
<li><b>Write the name and period first.</b> A card without dates cannot be matched to a pay run.</li>
<li><b>Use the same time style throughout.</b> Either 12-hour with AM/PM (8:02 AM) or 24-hour (0802). Mixing styles causes errors.</li>
<li><b>Enter times when they happen,</b> not at the end of the week from memory.</li>
<li><b>Record the meal break</b> as the unpaid minutes, or the exact out and in times.</li>
<li><b>Calculate the day:</b> out minus in minus unpaid break. Write it as hours:minutes.</li>
<li><b>Add the days</b> in minutes if the minutes get awkward (hours &times; 60 + minutes).</li>
<li><b>Convert</b> to decimal hours if your payroll uses decimals: minutes &divide; 60.</li>
<li><b>Sign and date</b> the card and ask your supervisor to sign.</li>
</ol>"""),
            S("A completed example", example("Week ending Friday, $19.00 an hour", """
<table class="plain" style="width:auto"><thead><tr><th>Day</th><th>In</th><th>Out</th><th>Lunch</th><th>Hours</th></tr></thead><tbody>
<tr><td>Mon</td><td>7:58</td><td>4:32</td><td>30</td><td>8:04</td></tr>
<tr><td>Tue</td><td>8:01</td><td>4:30</td><td>30</td><td>7:59</td></tr>
<tr><td>Wed</td><td>7:55</td><td>5:15</td><td>30</td><td>8:50</td></tr>
<tr><td>Thu</td><td>8:00</td><td>4:30</td><td>30</td><td>8:00</td></tr>
<tr><td>Fri</td><td>8:03</td><td>12:03</td><td>0</td><td>4:00</td></tr>
</tbody></table>
<p>Check Monday: 7:58 to 4:32 is 8 hours 34 minutes; minus 30 = <b>8:04</b>. Total: 8:04 + 7:59 + 8:50 + 8:00 + 4:00 = 36:53. Decimal: 36 + 53/60 = <b>36.88 hours</b>. Pay = 36.88 &times; $19.00 = $700.72 (using the rounded hours; using exact minutes, 36.8833 &times; $19 = $700.78). No overtime because the week is under 40.</p>""")),
            S("Common paper-card mistakes", """
<ul>
<li>Writing 5:00 when you mean 5:00 PM on a 24-hour card, or the other way round.</li>
<li>Forgetting to deduct lunch, or deducting it on a day you worked through it.</li>
<li>Totalling hours as decimals (adding 8:45 as 8.45).</li>
<li>Correction fluid: cross out one line, write the fix, and initial it so the change is traceable.</li>
<li>Missing signatures, which delays payroll.</li>
</ul>
<p>Practice by entering the same week in the <a href="/time-card-calculator/">time card calculator</a> and compare totals, or print the <a href="/timesheet/">weekly timesheet</a> as a blank template.</p>"""),
        ],
        [("How do I write times on a time card?", "Use one style consistently: 12-hour with AM/PM, or 24-hour (for example 1630). Be exact; avoid rounding yourself unless your employer instructs it."),
         ("How do I add hours and minutes?", "Convert to minutes, add, and convert back, or add the hours and the minutes separately and carry 60 minutes into one hour."),
         ("How do I convert 36:53 to decimal?", "36 + 53/60 = 36.88 hours."),
         ("What if I make a mistake?", "Draw a single line through it, write the correction and initial it. Tell your supervisor. See our guide to time card mistakes."),
         ("Who keeps the paper card?", "Your employer is responsible for the official record. Take a photo or keep your own copy for your records.")],
        sources=["cfr516_2"],
        related=["/timesheet/", "/time-card-calculator/", "/guides/how-to-read-a-timesheet/", "/decimal-hours-converter/"],
    )

    # ------------------------------------------------------------------ bi-weekly vs semi-monthly
    article_page(
        "/guides/bi-weekly-vs-semi-monthly-pay/", "Bi-Weekly vs Semi-Monthly Pay",
        "Bi-Weekly vs Semi-Monthly Pay: Differences, Checks Per Year, Examples",
        "Bi-weekly vs semi-monthly pay explained: 26 versus 24 paychecks, how the amount of each check changes, three-paycheck months, overtime and which to expect.",
        "Bi-Weekly vs Semi-Monthly Pay",
        "Both mean &ldquo;twice a month&rdquo; to a lot of people, but they are different schedules. The difference changes how much each paycheck is, when the money arrives and how your hours line up with the pay period.",
        [
            S("The definitions", """
<ul>
<li><b>Weekly:</b> 52 paychecks a year, every week.</li>
<li><b>Bi-weekly:</b> every other week, 26 paychecks a year, always on the same weekday (for example every second Friday). Each pay period is exactly 14 days.</li>
<li><b>Semi-monthly:</b> twice per month on fixed dates, such as the 15th and the last day, 24 paychecks a year. Pay periods are 13 to 16 days long.</li>
<li><b>Monthly:</b> 12 paychecks a year.</li>
</ul>"""),
            S("How the amounts compare", table(
                ["Annual pay", "Weekly", "Bi-weekly (26)", "Semi-monthly (24)", "Monthly (12)"],
                [["$40,000", "$769.23", "$1,538.46", "$1,666.67", "$3,333.33"], ["$52,000", "$1,000.00", "$2,000.00", "$2,166.67", "$4,333.33"], ["$60,000", "$1,153.85", "$2,307.69", "$2,500.00", "$5,000.00"], ["$75,000", "$1,442.31", "$2,884.62", "$3,125.00", "$6,250.00"]], num_from=1) +
              "<p>Each column shows gross pay before taxes. A bi-weekly check is smaller than a semi-monthly check because there are more of them, but the annual total is identical. For an hourly rate, see the <a href=\"/hourly-to-salary/\">hourly to salary calculator</a>.</p>"),
            S("Worked example: the same salary, two schedules", example("$60,000 a year", """
<p><b>Bi-weekly:</b> $60,000 &divide; 26 = <b>$2,307.69</b> per check. In two months of the year you receive three checks instead of two. That is not extra pay: 26 smaller checks add up to the same annual total as 24 larger ones.</p>
<p><b>Semi-monthly:</b> $60,000 &divide; 24 = <b>$2,500.00</b> per check, on the same two dates every month. Budgeting is simpler because each month has the same two paydays, but the date of a payday may fall on a weekend, so employers pay on the prior business day.</p>""")),
            S("What it means for hourly workers", """
<p>Pay frequency does not change overtime. Under the federal rule overtime is counted per workweek, so a bi-weekly period contains exactly two workweeks while a semi-monthly period may split one across two checks. If a workweek straddles two pay periods, 29 CFR 778.106 says overtime pay is generally due on the regular payday for the pay period in which the workweek ends. The <a href="/semi-monthly-time-card-calculator/">semi-monthly time card calculator</a> lets you carry earlier hours into the second period, and the <a href="/bi-weekly-time-card-calculator/">bi-weekly calculator</a> handles two full workweeks.</p>
<p>Hourly semi-monthly checks vary with the number of working days in the period: a period with 12 weekdays pays more than one with 10. A bi-weekly hourly check varies only with hours worked.</p>"""),
            S("Which does the law require?", """
<p>Pay frequency is set mostly by state law. The U.S. Department of Labor publishes a state payday table, last revised January 1, 2023. It shows, for example, that Nevada and Alaska list semi-monthly and monthly pay and that California lists weekly, bi-weekly, semi-monthly and monthly pay (the frequency can depend on the occupation). The table may be out of date and covers only a summary; check your state labor department for your own rules and for exceptions.</p>"""),
        ],
        [("How many pay periods are there in bi-weekly vs semi-monthly pay?", "26 bi-weekly and 24 semi-monthly."),
         ("Which is better, bi-weekly or semi-monthly?", "Neither is better in total pay. Bi-weekly gives two three-paycheck months a year; semi-monthly gives steadier monthly amounts and is common for salaried staff."),
         ("Do I get paid for hours worked in the last week before payday?", "Many employers pay in arrears, with a lag between the end of the pay period and the payday. Look at your pay stub for the period dates."),
         ("How do I calculate a bi-weekly paycheck?", "Annual salary divided by 26, or hourly rate times hours in the two weeks (with overtime figured per workweek)."),
         ("Can an employer change the pay schedule?", "Rules depend on state law and any agreements. Check your state labor department.")],
        sources=["dol_payday", "cfr778_106", "dol23"],
        related=["/bi-weekly-time-card-calculator/", "/semi-monthly-time-card-calculator/", "/hourly-to-salary/", "/paycheck-calculator/"],
    )

    # ------------------------------------------------------------------ how to read a timesheet
    article_page(
        "/guides/how-to-read-a-timesheet/", "How to Read a Timesheet",
        "How to Read a Timesheet: Columns, Totals, Overtime & Pay Explained",
        "How to read a timesheet: what each column means, how to verify daily and weekly totals, spot overtime, match it to a pay stub and what records employers must keep.",
        "How to Read a Timesheet",
        "A timesheet is a small table that decides your pay. Reading it correctly takes a minute and can catch errors worth far more than that.",
        [
            S("The columns, one by one", """
<table class="plain" style="width:auto"><tbody>
<tr><td><b>Date / day</b></td><td>The workday. Your employer's workweek begins on a fixed day and time, which should be clear from the sheet.</td></tr>
<tr><td><b>Time in / time out</b></td><td>When you started and stopped work. Check each against what you actually did.</td></tr>
<tr><td><b>Break / lunch</b></td><td>Unpaid meal time deducted from the day. Paid rest breaks are not deducted.</td></tr>
<tr><td><b>Regular hours</b></td><td>Hours at the normal rate.</td></tr>
<tr><td><b>Overtime hours</b></td><td>Hours above the overtime threshold, paid at a higher rate.</td></tr>
<tr><td><b>PTO / holiday / sick</b></td><td>Paid time not worked. It is paid, but it is not &ldquo;hours worked&rdquo; and may be treated differently for overtime.</td></tr>
<tr><td><b>Total</b></td><td>Weekly or period total. Check whether it is in hours:minutes or decimals.</td></tr>
</tbody></table>"""),
            S("What employers must record", """
<p>The federal recordkeeping regulation for employees covered by the minimum wage and overtime provisions (29 CFR 516.2) requires employers to keep records that include the time of day and day of week on which the employee's workweek begins; the hours worked each workday and the total hours worked each workweek; the regular hourly rate for any workweek in which overtime is due; total daily or weekly straight-time earnings; total premium pay for overtime hours; total wages paid each pay period; and the date of payment and pay period covered. Your timesheet should support those numbers, and your pay stub should match them.</p>"""),
            S("How to verify a timesheet in five checks", """
<ol>
<li><b>Daily math.</b> Out minus in minus break equals the daily hours. Do two or three days by hand.</li>
<li><b>Decimal vs minutes.</b> 8:30 is 8.5, not 8.30. If the sheet shows 8.30 and you worked 8:30, you were shorted 12 minutes.</li>
<li><b>Weekly total.</b> Add the days. Compare with the sheet.</li>
<li><b>Overtime.</b> Hours above 40 in the workweek (and daily thresholds in some states) should show at the overtime rate.</li>
<li><b>Pay.</b> Hours times rate, plus the overtime premium, should equal gross pay on the stub.</li>
</ol>"""),
            S("Worked example: reading and checking a sheet", example("Weekly sheet, $21.00 an hour", """
<table class="plain" style="width:auto"><thead><tr><th>Day</th><th>In</th><th>Out</th><th>Break</th><th>Hours</th></tr></thead><tbody>
<tr><td>Mon</td><td>7:00 am</td><td>3:30 pm</td><td>30</td><td>8:00</td></tr>
<tr><td>Tue</td><td>7:00 am</td><td>4:30 pm</td><td>30</td><td>9:00</td></tr>
<tr><td>Wed</td><td>7:00 am</td><td>5:30 pm</td><td>30</td><td>10:00</td></tr>
<tr><td>Thu</td><td>7:00 am</td><td>5:00 pm</td><td>30</td><td>9:30</td></tr>
<tr><td>Fri</td><td>7:00 am</td><td>4:00 pm</td><td>30</td><td>8:30</td></tr>
</tbody></table>
<p>Total: 8:00 + 9:00 + 10:00 + 9:30 + 8:30 = <b>45:00</b>. Under the federal weekly rule that is 40 regular hours and 5 overtime hours. Pay = 40 &times; $21 + 5 &times; $31.50 = $840 + $157.50 = <b>$997.50</b>. If the pay stub shows 45 hours at straight time ($945.00), the overtime premium of $52.50 is missing and worth asking about. Verify by entering the sheet into the <a href="/time-card-calculator/">time card calculator</a>.</p>""")),
            S("Keeping your own record", """
<p>Photograph or copy your sheet each period, or keep a simple log of your actual punches. If you dispute anything later, your own contemporaneous record is useful evidence. The <a href="/timesheet/">printable timesheet</a> is a ready-made template.</p>"""),
        ],
        [("How do I read hours on a timesheet?", "Check whether they are shown as hours:minutes (8:30) or decimals (8.50). 8:30 equals 8.5 decimal hours."),
         ("What does regular vs overtime mean on a timesheet?", "Regular hours are paid at the normal rate; overtime hours are over the threshold and paid at a premium, usually 1.5 times the regular rate."),
         ("What records must employers keep?", "Among other items, the workweek start, hours worked each day and the total hours each workweek, and the pay details listed in 29 CFR 516.2."),
         ("What if the pay stub doesn't match my timesheet?", "Ask payroll to explain. Bring your own record of hours and compare daily totals first."),
         ("Does PTO appear as hours worked?", "PTO is paid time not worked; many timesheets show it on a separate line from worked hours.")],
        sources=["cfr516_2", "dol23"],
        related=["/time-card-calculator/", "/timesheet/", "/guides/time-card-mistakes-and-how-to-fix-them/", "/overtime-calculator/"],
    )

    # ------------------------------------------------------------------ meal and rest break laws
    article_page(
        "/guides/meal-and-rest-break-laws/", "Meal and Rest Break Laws by State",
        "Meal and Rest Break Laws by State: What the U.S. DOL Table Lists",
        "Meal and rest break rules for California, Colorado, Nevada, Alaska, New York, Oregon, Washington, Illinois and more, summarised from the U.S. Department of Labor table.",
        "Meal and Rest Break Laws by State",
        "Break rules are state law. This guide summarises the Department of Labor's published state table and adds the federal definitions, and it is careful to say only what that source says. Always confirm with your state labor department.",
        [
            S("Federal baseline", """
<p>Federal regulations define when breaks count as work time. Under 29 CFR 785.18, rest periods of short duration, running from 5 minutes to about 20 minutes, are usually paid and counted as hours worked. Under 29 CFR 785.19, bona fide meal periods are not worktime, but the employee must be completely relieved from duty, and ordinarily 30 minutes or more is long enough. The requirement to provide a break at all comes from state law, summarised below.</p>"""),
            S("What the Department of Labor's state table lists", """
<p>The table was last revised January 1, 2023, so check current law.</p>""" + table(
                ["State", "Meal period (as listed by DOL)", "Rest breaks"],
                [["California", "30 minutes if work is for more than 5 hours per day; a second 30-minute meal period for shifts over 10 hours; waiver rules apply", "Required (details are in state law)"],
                 ["Colorado", "30 minutes if the work shift exceeds 5 consecutive hours (set by wage order for covered industries)", "Required"],
                 ["Nevada", "30 minutes if work is for 8 continuous hours (employers with two or more employees)", "Required"],
                 ["Alaska", "No general adult meal period requirement listed", "Not listed"],
                 ["New York", "Varies by industry and shift; for example 30 minutes at noon for shifts over 6 hours that span the midday period", "Not listed"],
                 ["Oregon", "30 minutes with relief from all duty for each work period of 6 to 8 hours, with timing rules", "Required"],
                 ["Washington", "30 minutes if the work period is more than 5 consecutive hours, taken 2 to 5 hours into the shift", "Required"],
                 ["Illinois", "At least 20 minutes no later than 5 hours after the start for employees working 7.5 or more continuous hours", "Not listed"]], num_from=9) +
              "<p>The same table lists meal-period requirements for other jurisdictions, including Connecticut, Delaware, Kentucky, Maine, Maryland, Massachusetts, Minnesota, Nebraska, New Hampshire, North Dakota, Rhode Island, Tennessee, Vermont, West Virginia, Guam and Puerto Rico. The Department's table says only seven states have rest-break requirements: California, Colorado, Kentucky, Minnesota, Nevada, Oregon and Washington. We do not repeat details beyond what the table states; open the source for the full wording, exceptions and the state agency contact.</p>"),
            S("Worked examples", example("A 9-hour shift in California", """
<p>Per the DOL table, a 30-minute meal period applies when work is more than 5 hours. A shift from 8:00 am to 5:00 pm with a 30-minute unpaid meal is 8:30 paid. If the meal is interrupted or the employee is not relieved of duty, the time is generally hours worked and should be paid, as the federal definition of a bona fide meal period requires complete relief from duty. State rules may add what the employer owes when a required break is not provided; the DOL table does not say, so read the state's guidance.</p>""") +
              example("A 6-hour shift in Nevada", """
<p>The DOL table lists a meal period in Nevada after 8 continuous hours, so a 6-hour shift does not trigger that requirement as listed. Employers can still provide breaks by policy. Check the Nevada Labor Commissioner for rest-break details, which the DOL table does not spell out.</p>""")),
            S("How breaks affect your time card", """
<ul>
<li>Unpaid meal periods are subtracted. Paid rest breaks are not.</li>
<li>If a required meal period was not provided or was interrupted, tell payroll; the remedy depends on the state.</li>
<li>Use the <a href="/lunch-break-calculator/">lunch break calculator</a> to see how a 30- or 60-minute meal changes your weekly hours and overtime.</li>
</ul>"""),
        ],
        [("Does federal law require lunch breaks?", "The Department of Labor's published break requirements are state by state. Federal regulations explain whether a break counts as paid time, but the requirement to provide one comes from state law."),
         ("Are 15-minute breaks paid?", "Rest periods of about 5 to 20 minutes are generally paid and counted as hours worked under 29 CFR 785.18."),
         ("How long must a lunch break be?", "Federal regulations say ordinarily 30 minutes or more is long enough for a bona fide meal period. States set their own lengths, as listed above."),
         ("Which states require rest breaks?", "According to the DOL table: California, Colorado, Kentucky, Minnesota, Nevada, Oregon and Washington."),
         ("Where can I find the exact law for my state?", "On your state labor department's website. The DOL table links to each state agency.")],
        sources=["dol_meal", "cfr785_18", "cfr785_19"],
        related=["/lunch-break-calculator/", "/guides/how-to-calculate-hours-worked-with-breaks/", "/overtime-rules/", "/time-card-calculator/"],
    )

    # ------------------------------------------------------------------ time card mistakes
    article_page(
        "/guides/time-card-mistakes-and-how-to-fix-them/", "Time Card Mistakes and Fixes",
        "Time Card Mistakes and How to Fix Them (Missed Punches, Breaks, Overtime)",
        "The most common time card mistakes - missed punches, wrong breaks, decimal errors, rounding, missing overtime - and a step-by-step way to find, document and fix each one.",
        "Time Card Mistakes and How to Fix Them",
        "Almost everyone has had a time card that was wrong. Most errors are small and easy to fix if you spot them in the same pay period and bring evidence.",
        [
            S("The seven most common mistakes", """
<ol>
<li><b>Missed punch.</b> You forgot to clock in or out. The system estimates or leaves the day blank.</li>
<li><b>Wrong AM/PM.</b> 8:00 PM entered instead of 8:00 AM turns an 8-hour day into 12 hours or zero.</li>
<li><b>Lunch not taken but deducted.</b> An automatic 30-minute deduction on a day you worked through lunch.</li>
<li><b>Decimal vs minutes.</b> 7:30 typed as 7.30 pays 7 hours 18 minutes. See the <a href="/decimal-hours-converter/">decimal converter</a>.</li>
<li><b>Rounding that always goes one way.</b> See <a href="/guides/rounding-time-cards/">rounding time cards</a>.</li>
<li><b>Overtime not applied.</b> More than 40 hours in the workweek (or the state daily threshold) paid at straight time.</li>
<li><b>Wrong workweek or pay period.</b> Hours land in the wrong week, which shifts the overtime split.</li>
</ol>"""),
            S("How to fix a mistake: step by step", """
<ol>
<li><b>Write down what really happened,</b> with dates and times, as soon as you notice.</li>
<li><b>Collect evidence.</b> Messages, schedules, door-badge records, or a coworker who can confirm.</li>
<li><b>Recalculate</b> the day and the week using the <a href="/time-card-calculator/">time card calculator</a> so you know the exact difference in hours and pay.</li>
<li><b>Submit a correction request</b> to your supervisor or payroll in writing (email is ideal) before the payroll cutoff.</li>
<li><b>Check the next pay stub.</b> The correction may appear as an adjustment in a later period.</li>
<li><b>Escalate if needed.</b> Ask payroll to explain in writing. If the issue repeats or you are told it will not be paid, contact your state labor department or the U.S. Department of Labor's Wage and Hour Division.</li>
</ol>"""),
            S("Worked examples", example("Missed clock-out", """
<p>You clocked in 8:00 am and forgot to clock out; you left at 4:45 pm after a 30-minute lunch. Correct hours = 8:45 minus 0:30 = <b>8:15</b> (8.25 hours). At $17.00 an hour that is $140.25 for the day. Send: &ldquo;I forgot to clock out Tuesday 3/10; I left at 4:45 pm. Please correct to 8:15 paid hours.&rdquo;</p>""") +
              example("Overtime paid at straight time", """
<p>Your timesheet shows 44 hours at $20.00, but the stub pays $880.00 (44 &times; $20). The correct gross under the federal weekly rule is 40 &times; $20 + 4 &times; $30 = $920.00. The difference is the missing overtime premium: 4 &times; $10 = <b>$40.00</b>. Overtime for a workweek is generally due on the regular payday for the pay period in which the workweek ends (29 CFR 778.106), so ask for the adjustment promptly.</p>""") +
              example("Decimal entry error", """
<p>A 7:45 shift typed as 7.45 hours pays 7 hours 27 minutes, 18 minutes short. Over five days that is 1.5 hours, or $27.00 at $18.00 an hour.</p>""")),
            S("Prevention", """
<ul>
<li>Check your time card at the end of every shift or at least every Friday.</li>
<li>Take a screenshot or photo of the period before it is submitted.</li>
<li>Use one time format everywhere.</li>
<li>For recurring shifts, set a calendar reminder to punch out.</li>
<li>If you manage others: ask staff to review their cards before the cutoff and keep a log of corrections, with who approved each one.</li>
</ul>"""),
        ],
        [("What do I do if I forgot to clock out?", "Tell your supervisor as soon as you can, give the actual time you left and ask for a correction. Keep a written record."),
         ("Can I fix a time card after it was submitted?", "Usually you request a correction through your supervisor or payroll. Policies and cutoffs vary."),
         ("What if my employer won't fix an error?", "Keep your records and contact your state labor department or the U.S. Department of Labor's Wage and Hour Division."),
         ("How long should I keep my own time records?", "Keep them at least until your pay is confirmed correct, and longer if a dispute is open. Employers have their own retention rules under federal and state law."),
         ("Is the error my fault if I signed the card?", "A signature confirms what you reviewed, but it does not by itself determine what you were owed. Raise any error you notice.")],
        sources=["cfr516_2", "cfr778_106", "dol23"],
        related=["/guides/how-to-read-a-timesheet/", "/time-card-calculator/", "/overtime-calculator/", "/guides/rounding-time-cards/"],
    )

    # ------------------------------------------------------------------ freelancers
    article_page(
        "/guides/tracking-hours-for-freelancers-and-contractors/", "Tracking Hours for Freelancers and Contractors",
        "How to Track Hours as a Freelancer or Contractor (With Invoice Example)",
        "How to track hours as a freelancer or contractor: what to record, billable vs non-billable time, rounding for invoices, minutes to decimals and a worked invoice.",
        "How to Track Hours as a Freelancer or Contractor",
        "Employees have employers keeping time records. Freelancers have only themselves. A clean hours log is the difference between an invoice that gets paid without questions and one that does not.",
        [
            S("What to record for every work session", """
<table class="plain" style="width:auto"><tbody>
<tr><td><b>Date</b></td><td>The day the work happened.</td></tr>
<tr><td><b>Client / project</b></td><td>So you can invoice and report per client.</td></tr>
<tr><td><b>Start and end time</b></td><td>The actual clock times, not a guess at the end of the week.</td></tr>
<tr><td><b>Task description</b></td><td>One line: what was done. Clients ask.</td></tr>
<tr><td><b>Billable or not</b></td><td>Billable client work versus admin, marketing, learning.</td></tr>
</tbody></table>
<p>The free <a href="/timesheet/">printable timesheet</a> works as a weekly log, and the <a href="/hours-calculator/">hours calculator</a> gives the hours:minutes and decimals for each session.</p>"""),
            S("Billing increments and rounding", """
<p>Your contract decides how time is billed. Common choices are to the minute, in 6-minute tenths of an hour, or in 15-minute quarters. Agree the increment in writing, and round consistently. Rounding that always favors you is likely to be questioned by the client; rounding both ways or always <i>up</i> to a stated minimum is a clear contractual term, not a surprise. The rounding mechanics are the same as in the <a href="/time-rounding-calculator/">time rounding calculator</a>.</p>"""),
            S("Worked invoice example", example("One week, $65 an hour, 15-minute increments", """
<table class="plain" style="width:auto"><thead><tr><th>Day</th><th>Sessions</th><th>Actual</th><th>Billed (15 min up)</th></tr></thead><tbody>
<tr><td>Mon</td><td>9:02-11:47, 1:10-3:36</td><td>2:45 + 2:26 = 5:11</td><td>2:45 + 2:30 = 5:15</td></tr>
<tr><td>Tue</td><td>10:00-12:10</td><td>2:10</td><td>2:15</td></tr>
<tr><td>Thu</td><td>8:30-1:00</td><td>4:30</td><td>4:30</td></tr>
</tbody></table>
<p>Billed total = 5:15 + 2:15 + 4:30 = 12:00 = 12.00 hours. Invoice = 12 &times; $65.00 = <b>$780.00</b>. Without rounding the actual total is 11:51 = 11.85 hours = $770.25, so the increment adds $9.75 in this week. State the policy on the invoice.</p>""")),
            S("Contractors, employees and overtime", """
<p>If you are a true independent contractor, wage-and-hour overtime rules generally do not apply to your invoices, but your classification is determined by the facts of the relationship, not by what a contract calls you. If you are unsure whether you are an employee or a contractor, ask the U.S. Department of Labor's Wage and Hour Division or your state labor department. For employees, see <a href="/overtime-rules/">overtime rules</a>.</p>
<p>Also track your time to calculate your effective hourly rate: divide what a project paid by all the hours it took, including admin and revisions. The <a href="/salary-to-hourly/">salary to hourly calculator</a> can compare a freelance income target with a salaried offer.</p>"""),
            S("Good habits", """
<ul>
<li>Start the log when you start working, not afterwards.</li>
<li>Back up the log weekly (export or photo).</li>
<li>Invoice on a regular schedule with the hours attached.</li>
<li>Keep records as long as your accountant recommends; tax rules vary, so check IRS guidance for your situation.</li>
</ul>"""),
        ],
        [("What is the best way to track freelance hours?", "Record start and end times as you work, with the client and task. A spreadsheet, a notebook or a printed timesheet all work, as long as you do it consistently."),
         ("How should I round billable time?", "Whatever your contract says. Use the same increment every time and state it on the invoice."),
         ("How do I convert minutes to decimal hours for an invoice?", "Divide the minutes by 60: 45 minutes is 0.75 hours. See the minutes to decimal chart."),
         ("Do contractors get overtime?", "True independent contractors are not covered by overtime rules, but classification depends on facts. If you are unsure, ask the Department of Labor or your state."),
         ("How long should I keep time records?", "Ask your accountant; tax and contract needs differ. Keeping them at least until invoices are paid and any dispute window has passed is a sensible minimum.")],
        related=["/timesheet/", "/hours-calculator/", "/minutes-to-decimal-chart/", "/time-rounding-calculator/", "/salary-to-hourly/"],
    )
