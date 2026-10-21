/* Checks calculator math against hand-worked examples. Run: node tests/test_calc.js */
"use strict";
var assert = require("assert");
var C = require("../assets/calc.js");
var n = 0;
function eq(actual, expected, label) {
  n++;
  assert.strictEqual(actual, expected, label + ": expected " + expected + " got " + actual);
}
function near(actual, expected, label, tol) {
  n++;
  assert.ok(Math.abs(actual - expected) <= (tol || 0.005), label + ": expected " + expected + " got " + actual);
}
var H = function (h) { return h * 60; };

/* --- parsing --- */
eq(C.parseTime("8"), 480, "8");
eq(C.parseTime("8am"), 480, "8am");
eq(C.parseTime("12am"), 0, "12am");
eq(C.parseTime("12 pm"), 720, "12 pm");
eq(C.parseTime("5:30 pm"), 1050, "5:30 pm");
eq(C.parseTime("17:45"), 1065, "17:45");
eq(C.parseTime("0830"), 510, "0830");
eq(C.parseTime("1730"), 1050, "1730");
eq(C.parseTime("13pm"), null, "13pm invalid");
eq(C.parseTime("8:75"), null, "8:75 invalid");
eq(C.parseDuration("1:30"), 90, "1:30");
eq(C.parseDuration("1h 30m"), 90, "1h 30m");
eq(C.parseDuration("45 min"), 45, "45 min");
eq(C.parseDuration("1.5"), 90, "1.5 hours");

/* --- worked minutes --- */
eq(C.workedMinutes(C.parseTime("8am"), C.parseTime("5pm"), 60), H(8), "8-5 with 60 break = 8 h");
eq(C.workedMinutes(C.parseTime("8am"), C.parseTime("5pm"), 30), 510, "8-5 with 30 break = 8.5 h");
eq(C.workedMinutes(C.parseTime("10pm"), C.parseTime("6am"), 0), H(8), "overnight 10pm-6am = 8 h");
eq(C.elapsedMinutes("2026-03-01", 22 * 60, "2026-03-02", 6 * 60), H(8), "date crossing");
eq(C.elapsedMinutes("2026-03-01", 8 * 60, "2026-03-03", 8 * 60), H(48), "two full days");
eq(C.elapsedMinutes("", 9 * 60, "", 17 * 60), H(8), "no dates same day");

/* --- formatting --- */
eq(C.fmtHM(525), "8:45", "fmtHM");
eq(C.fmtDecimal(525), "8.75", "fmtDecimal 8:45");
eq(C.fmtHMwords(135), "2 hours 15 minutes", "words");
eq(C.fmtTime12(13 * 60 + 5), "1:05 PM", "12h");
eq(C.fmtTime24(0), "00:00", "24h midnight");
eq(C.fmtMilitary(17 * 60 + 30), "1730 hours", "military");
eq(C.hmToDecimal(7, 20), "7.33", "7:20 = 7.33");
eq(JSON.stringify(C.decimalToHM(7.75)), '{"hours":7,"minutes":45}', "7.75 = 7:45");

/* --- rounding (29 CFR 785.48(b) practice; 7-minute rule) --- */
eq(C.roundMinutes(7, 15), 0, "7 min rounds down at 15");
eq(C.roundMinutes(8, 15), 15, "8 min rounds up at 15");
eq(C.roundMinutes(22, 15), 15, "22 -> 15");
eq(C.roundMinutes(23, 15), 30, "23 -> 30");
eq(C.roundMinutes(2, 5), 0, "2 -> 0 at 5");
eq(C.roundMinutes(3, 5), 5, "3 -> 5 at 5");
eq(C.roundMinutes(2, 6), 0, "2 -> 0 at 6");
eq(C.roundMinutes(3, 6), 6, "3 -> 6 at 6");
eq(C.roundMinutes(61, 15, "up"), 75, "up");
eq(C.roundMinutes(74, 15, "down"), 60, "down");

/* --- federal overtime: 5 x 9 h = 45 h -> 40 regular + 5 OT --- */
var fed = C.computeOvertime([H(9), H(9), H(9), H(9), H(9), 0, 0], "federal");
eq(fed.regular, H(40), "fed regular"); eq(fed.ot, H(5), "fed ot"); eq(fed.dt, 0, "fed dt");
var pay = C.overtimePay(fed, 20);
near(pay.total, 40 * 20 + 5 * 30, "fed pay $20 x 45h = $950"); // 800 + 150
near(pay.total, 950, "fed pay total");
// no daily OT federally: 12 + 12 + 0... = 24 h is all regular
var f2 = C.computeOvertime([H(12), H(12), 0, 0, 0, 0, 0], "federal");
eq(f2.ot, 0, "no daily OT federally");
// prior hours in the same workweek count toward 40
var f3 = C.computeOvertime([H(8), H(8), 0, 0, 0, 0, 0], "federal", H(30));
eq(f3.ot, H(6), "30 prior + 16 = 46 -> 6 OT");
eq(f3.regular, H(10), "10 regular");

/* --- California: 10 h x 4 days = 40 h -> 8 reg + 2 OT per day = 32 reg, 8 OT --- */
var ca1 = C.computeOvertime([H(10), H(10), H(10), H(10), 0, 0, 0], "ca");
eq(ca1.regular, H(32), "CA 4x10 regular"); eq(ca1.ot, H(8), "CA 4x10 ot"); eq(ca1.dt, 0, "CA dt 0");
// 14-hour day: 8 reg, 4 OT (8-12), 2 DT
var ca2 = C.computeOvertime([H(14), 0, 0, 0, 0, 0, 0], "ca");
eq(ca2.regular, H(8), "CA 14h reg"); eq(ca2.ot, H(4), "CA 14h ot"); eq(ca2.dt, H(2), "CA 14h dt");
// 7 consecutive days of 8 h: days 1-6 = 48 h regular-by-day -> weekly extra over 40 = 8 OT ; day 7 = 8 h at 1.5 -> 16 OT total
var ca3 = C.computeOvertime([H(8), H(8), H(8), H(8), H(8), H(8), H(8)], "ca");
eq(ca3.total, H(56), "CA 7x8 total");
eq(ca3.ot, H(8) + H(8), "CA 7x8: 8 h weekly OT + 7th-day 8 h at 1.5");
eq(ca3.regular, H(40), "CA 7x8 regular"); eq(ca3.dt, 0, "CA 7x8 dt");
// 7th day with 10 h: 8 at 1.5x, 2 at 2x
var ca4 = C.computeOvertime([H(8), H(8), H(8), H(8), H(8), H(8), H(10)], "ca");
eq(ca4.dt, H(2), "CA 7th day dt 2 h"); eq(ca4.ot, H(8) + H(8), "CA 7th day ot");
// only 6 days worked: no 7th-day premium
var ca5 = C.computeOvertime([H(8), H(8), H(8), H(8), H(8), H(8), 0], "ca");
eq(ca5.ot, H(8), "CA 6x8 = 48 h -> 8 weekly OT"); eq(ca5.regular, H(40), "CA 6x8 reg");

/* --- Alaska: daily OT not double counted toward weekly --- */
var ak = C.computeOvertime([H(10), H(10), H(10), H(10), 0, 0, 0], "ak");
eq(ak.ot, H(8), "AK 4x10 -> 8 OT"); eq(ak.regular, H(32), "AK reg");
var ak2 = C.computeOvertime([H(9), H(9), H(9), H(9), H(9), H(9), 0], "ak"); // 54h: daily OT 6, regular-by-day 48 -> +8 weekly OT
eq(ak2.ot, H(6) + H(8), "AK 6x9: 6 daily + 8 weekly"); eq(ak2.regular, H(40), "AK reg 40");

/* --- Nevada --- */
eq(C.computeOvertime([H(10), H(10), H(10), H(10), 0, 0, 0], "nv_low").ot, H(8), "NV low-wage daily OT");
eq(C.computeOvertime([H(10), H(10), H(10), H(10), 0, 0, 0], "nv_high").ot, 0, "NV high-wage: 40 h exactly, no OT");

/* --- Colorado: 13 h day -> 1 h OT; 12-hour days x 4 = 48 h -> 8 weekly OT --- */
var co1 = C.computeOvertime([H(13), 0, 0, 0, 0, 0, 0], "co");
eq(co1.ot, H(1), "CO 13 h day 1 OT");
var co2 = C.computeOvertime([H(12), H(12), H(12), H(12), 0, 0, 0], "co");
eq(co2.ot, H(8), "CO 4x12 = 48 -> 8 OT"); eq(co2.regular, H(40), "CO reg 40");

/* --- regular rate with a non-discretionary bonus (DOL fact sheet 23 / 56A) ---
   45 h at $20 = $900 + $90 bonus = $990 straight; regular rate = $22.00; premium = 5 x 0.5 x 22 = $55; total $1,045 */
var bp = C.overtimePay(fed, 20, 90);
near(bp.regularRate, 22, "regular rate with bonus"); near(bp.otPremium, 55, "OT premium with bonus"); near(bp.total, 1045, "total with bonus");

/* --- pay periods --- */
eq(C.periodDates("2026-02-02", "weekly").length, 7, "weekly 7 days");
eq(C.periodDates("2026-02-02", "biweekly")[13], "2026-02-15", "biweekly last day");
eq(C.periodDates("2026-02-10", "semimonthly1")[0], "2026-02-01", "semimonthly 1st");
eq(C.periodDates("2026-02-10", "semimonthly1").length, 15, "1-15");
eq(C.periodDates("2026-02-10", "semimonthly2").length, 13, "Feb 16-28 2026 = 13 days");
eq(C.periodDates("2026-01-10", "semimonthly2").length, 16, "Jan 16-31 = 16 days");
eq(C.periodDates("2024-02-10", "monthly").length, 29, "Feb 2024 leap");
eq(C.weekdayOf("2026-01-01"), 4, "Jan 1 2026 is a Thursday");

/* bi-weekly time card: 2 weeks x 45 h, Mon start, federal -> 10 OT hours total, per-week not averaged */
var dates = C.periodDates("2026-02-02", "biweekly"); // Mon Feb 2
var mins = dates.map(function (d, i) { var wd = C.weekdayOf(d); return wd >= 1 && wd <= 5 ? H(9) : 0; });
var per = C.periodOvertime(dates, mins, "federal", 1, 0);
eq(per.total, H(90), "biweekly total"); eq(per.ot, H(10), "biweekly OT 5+5"); eq(per.regular, H(80), "biweekly reg");
// averaging is not allowed: 50 h then 30 h = 10 OT, not 0
var m2 = dates.map(function (d, i) { var wd = C.weekdayOf(d); if (!(wd >= 1 && wd <= 5)) return 0; return i < 7 ? H(10) : H(6); });
eq(C.periodOvertime(dates, m2, "federal", 1, 0).ot, H(10), "no averaging across weeks");

/* --- salary conversions --- */
var hs = C.hourlyToSalary(20, 40, 52);
eq(hs.annual, 41600, "$20/h annual"); near(hs.monthly, 3466.67, "monthly"); eq(hs.biweekly, 1600, "biweekly"); eq(hs.weekly, 800, "weekly");
near(C.salaryToHourly(52000, 40, 52), 25, "$52,000 = $25/h");
near(C.salaryToHourly(60000, 40, 50), 30, "$60,000 w/ 2 unpaid weeks = $30/h");

/* --- shift differential window --- */
eq(C.overlapMinutes(C.parseTime("6pm"), C.parseTime("2am"), C.parseTime("10pm"), C.parseTime("6am")), 4 * 60, "6pm-2am overlaps 10pm-6am by 4 h");
eq(C.overlapMinutes(C.parseTime("11pm"), C.parseTime("7am"), C.parseTime("10pm"), C.parseTime("6am")), 7 * 60, "11pm-7am overlaps 7 h");
eq(C.overlapMinutes(C.parseTime("9am"), C.parseTime("5pm"), C.parseTime("10pm"), C.parseTime("6am")), 0, "day shift no overlap");

/* --- PTO --- */
var pto = C.ptoSchedule({ perPeriod: 4, periods: 26, start: 0, usedPerPeriod: 0 });
eq(pto.final, 104, "4 h x 26 pay periods = 104 h"); // 13 days of 8 h
var capd = C.ptoSchedule({ perPeriod: 4, periods: 26, start: 0, cap: 80 });
eq(capd.final, 80, "cap 80"); eq(capd.lostToCap, 24, "24 h lost to cap");

/* --- paycheck estimate (IRS Pub 15-T 2026 annual percentage method, standard schedule, hand-worked) ---
   $2,000 biweekly, single, no deductions: annual 52,000 - 8,600 = 43,400.
   Over 19,900: 1,240 + 12% x (43,400-19,900=23,500) = 1,240 + 2,820 = 4,060 per year -> 156.15 biweekly.
   FICA: 2,000 x 6.2% = 124.00; 2,000 x 1.45% = 29.00; net = 2000 - 156.15 - 124 - 29 = 1,690.85 */
var pc = C.estimatePaycheck(2000, 26, { status: "single" });
near(pc.fedYear, 4060, "fed withholding per year"); near(pc.federal, 156.154, "fed biweekly", 0.01);
near(pc.socialSecurity, 124, "SS"); near(pc.medicare, 29, "Medicare"); near(pc.net, 1690.85, "net", 0.01);
// married filing jointly, $4,000 semimonthly(24): annual 96,000 - 12,900 = 83,100; 2,480 + 12% x (83,100-44,100=39,000) = 2,480+4,680 = 7,160/yr -> 298.33
var pcm = C.estimatePaycheck(4000, 24, { status: "married" });
near(pcm.fedYear, 7160, "MFJ fed year"); near(pcm.federal, 298.33, "MFJ fed per period", 0.01);
// Social Security wage base: annualised $200,000 -> only 184,500 taxable
var hi = C.estimatePaycheck(200000 / 26, 26, { status: "single" });
near(hi.socialSecurity * 26, 184500 * 0.062, "SS wage base cap", 0.05);

console.log("OK - " + n + " assertions passed");
