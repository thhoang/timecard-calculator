/* Time Card Calculator - pure calculation functions. No DOM, no dependencies.
   Loaded in the browser as window.TC and in node (tests/test_calc.js) via require(). */
(function (root) {
"use strict";

var DAY = 1440;

/* ---------- parsing / formatting ---------- */

/* "8", "8am", "8:15", "8:15 pm", "17:30", "0830", "1730", "noon", "midnight" -> minutes since midnight, or null. */
function parseTime(str) {
  if (str == null) return null;
  var s = String(str).trim().toLowerCase();
  if (!s) return null;
  if (s === "noon") return 720;
  if (s === "midnight") return 0;
  var ampm = null;
  var m = s.match(/\s*(a\.?m?\.?|p\.?m?\.?)$/);
  if (m) { ampm = m[1].charAt(0); s = s.slice(0, m.index).trim(); }
  var h, min = 0;
  if (/^\d{3,4}$/.test(s)) {
    h = parseInt(s.slice(0, s.length - 2), 10); min = parseInt(s.slice(-2), 10);
  } else {
    var parts = s.split(/[:\.]/);
    if (parts.length === 1) {
      if (!/^\d{1,2}$/.test(parts[0])) return null;
      h = parseInt(parts[0], 10);
    } else if (parts.length === 2) {
      if (!/^\d{1,2}$/.test(parts[0]) || !/^\d{2}$/.test(parts[1])) return null;
      h = parseInt(parts[0], 10); min = parseInt(parts[1], 10);
    } else return null;
  }
  if (min > 59) return null;
  if (ampm) {
    if (h < 1 || h > 12) return null;
    if (h === 12) h = 0;
    if (ampm === "p") h += 12;
  } else {
    if (h > 24 || (h === 24 && min > 0)) return null;
    if (h === 24) h = 0;
  }
  return h * 60 + min;
}

/* "1:30", "1h 30m", "90m", "2h", "1.5" (hours) -> minutes, or null. */
function parseDuration(str) {
  if (str == null) return null;
  var s = String(str).trim().toLowerCase();
  if (!s) return null;
  var m;
  if ((m = s.match(/^(\d+):(\d{1,2})$/))) {
    if (parseInt(m[2], 10) > 59) return null;
    return parseInt(m[1], 10) * 60 + parseInt(m[2], 10);
  }
  if ((m = s.match(/^(?:(\d+(?:\.\d+)?)\s*(?:h|hr|hrs|hour|hours))?\s*(?:(\d+(?:\.\d+)?)\s*(?:m|min|mins|minute|minutes))?$/)) && (m[1] || m[2])) {
    return Math.round((parseFloat(m[1] || 0) * 60) + parseFloat(m[2] || 0));
  }
  if (/^\d+(\.\d+)?$/.test(s)) return Math.round(parseFloat(s) * 60);
  return null;
}

function fmtHM(mins) {
  var sign = mins < 0 ? "-" : "";
  mins = Math.abs(Math.round(mins));
  var h = Math.floor(mins / 60), m = mins % 60;
  return sign + h + ":" + (m < 10 ? "0" : "") + m;
}
function fmtHMwords(mins) {
  mins = Math.round(mins);
  var h = Math.floor(Math.abs(mins) / 60), m = Math.abs(mins) % 60;
  var out = [];
  if (h) out.push(h + (h === 1 ? " hour" : " hours"));
  if (m || !h) out.push(m + (m === 1 ? " minute" : " minutes"));
  return (mins < 0 ? "-" : "") + out.join(" ");
}
function fmtDecimal(mins, digits) { return (mins / 60).toFixed(digits == null ? 2 : digits); }
function fmtTime12(mins) {
  mins = ((Math.round(mins) % DAY) + DAY) % DAY;
  var h = Math.floor(mins / 60), m = mins % 60;
  var ap = h < 12 ? "AM" : "PM";
  return (h % 12 || 12) + ":" + (m < 10 ? "0" : "") + m + " " + ap;
}
function fmtTime24(mins) {
  mins = ((Math.round(mins) % DAY) + DAY) % DAY;
  var h = Math.floor(mins / 60), m = mins % 60;
  return (h < 10 ? "0" : "") + h + ":" + (m < 10 ? "0" : "") + m;
}
function fmtMilitary(mins) { return fmtTime24(mins).replace(":", "") + " hours"; }
function round2(n) { return Math.round((n + 1e-9) * 100) / 100; }
function money(n) {
  var neg = n < 0; n = Math.abs(round2(n));
  return (neg ? "-" : "") + "$" + n.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

/* ---------- worked time ---------- */

/* Minutes between clock-in and clock-out, minus break. out <= in = overnight. */
function workedMinutes(inMin, outMin, breakMin) {
  if (inMin == null || outMin == null) return 0;
  var span = outMin - inMin;
  if (span <= 0) span += DAY;
  return Math.max(0, span - Math.max(0, breakMin || 0));
}

/* Date helpers on ISO yyyy-mm-dd, timezone-free (UTC day numbers). */
function isoToDays(iso) {
  var m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(iso || "");
  if (!m) return null;
  return Math.round(Date.UTC(+m[1], +m[2] - 1, +m[3]) / 86400000);
}
function daysToIso(d) { return new Date(d * 86400000).toISOString().slice(0, 10); }
function weekdayOf(iso) { return new Date(isoToDays(iso) * 86400000).getUTCDay(); } // 0=Sun
var WD = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];

/* Minutes from (startDate,startTime) to (endDate,endTime). Dates may be blank: then the end
   is the same day, or the next day if the end time is not after the start (overnight). */
function elapsedMinutes(startDate, startMin, endDate, endMin) {
  if (startMin == null || endMin == null) return null;
  var sd = isoToDays(startDate), ed = isoToDays(endDate);
  if (sd == null && ed == null) { var s = endMin - startMin; return s <= 0 ? s + DAY : s; }
  if (sd == null) sd = ed; if (ed == null) ed = sd;
  return (ed - sd) * DAY + endMin - startMin;
}

/* Rounding. mode: "nearest" | "up" | "down". Nearest rounds half-steps up; with a 15-minute
   step that gives the DOL "7-minute rule": 1-7 minutes down, 8-14 up. */
function roundMinutes(mins, step, mode) {
  if (!step) return mins;
  var r = mins % step, base = mins - r;
  if (r === 0) return mins;
  mode = mode || "nearest";
  if (mode === "down") return base;
  if (mode === "up") return base + step;
  return r * 2 >= step ? base + step : base;
}

/* hh:mm <-> decimal */
function hmToDecimal(h, m, digits) { return ((h * 60 + m) / 60).toFixed(digits == null ? 2 : digits); }
function decimalToHM(dec) {
  var total = Math.round(dec * 60);
  return { hours: Math.floor(total / 60), minutes: total % 60 };
}

/* ---------- overtime ---------- */
/* Rule presets. dailyOT / dailyDT in hours (null = none), weeklyOT in hours, seventh = CA 7th-day rule.
   Sources: see /overtime-rules/ (DOL fact sheet 23; CA DIR DLSE; AK AS 23.10.060; NV NRS 608.018; CO COMPS Order). */
var RULES = {
  federal: { label: "Federal (FLSA): over 40 h in the workweek", dailyOT: null, dailyDT: null, weeklyOT: 40, seventh: false },
  ca:      { label: "California: daily 8 h / 12 h, weekly 40 h, 7th day", dailyOT: 8, dailyDT: 12, weeklyOT: 40, seventh: true },
  ak:      { label: "Alaska: over 8 h a day and over 40 h a week", dailyOT: 8, dailyDT: null, weeklyOT: 40, seventh: false },
  nv_low:  { label: "Nevada, pay under 1.5x state minimum: over 8 h a day and 40 h a week", dailyOT: 8, dailyDT: null, weeklyOT: 40, seventh: false },
  nv_high: { label: "Nevada, pay at or above 1.5x state minimum: over 40 h a week", dailyOT: null, dailyDT: null, weeklyOT: 40, seventh: false },
  co:      { label: "Colorado: over 12 h a day and over 40 h a week", dailyOT: 12, dailyDT: null, weeklyOT: 40, seventh: false },
  none:    { label: "No overtime", dailyOT: null, dailyDT: null, weeklyOT: null, seventh: false }
};

/* dailyMinutes: array (workweek order, up to 7). Returns minutes at straight time (regular),
   time-and-a-half (ot) and double time (dt), plus a per-day breakdown. Hours that count as daily
   overtime are not counted again toward the weekly limit. priorMinutes = regular hours already worked
   earlier in the same workweek (for pay periods that split a workweek). */
function computeOvertime(dailyMinutes, rule, priorMinutes) {
  var r = typeof rule === "string" ? RULES[rule] : rule;
  var prior = priorMinutes || 0;
  var days = [], total = 0, regPool = prior, i;
  var all7 = dailyMinutes.length >= 7 && dailyMinutes.slice(0, 7).every(function (d) { return d > 0; });
  for (i = 0; i < dailyMinutes.length; i++) {
    var d = dailyMinutes[i] || 0, reg = d, ot = 0, dt = 0;
    total += d;
    if (r.seventh && all7 && i === 6) {
      reg = 0; ot = Math.min(d, 8 * 60); dt = d - ot;
    } else {
      if (r.dailyDT != null && d > r.dailyDT * 60) { dt = d - r.dailyDT * 60; reg = r.dailyDT * 60; }
      if (r.dailyOT != null && reg > r.dailyOT * 60) { ot = reg - r.dailyOT * 60; reg = r.dailyOT * 60; }
      regPool += reg;
    }
    days.push({ minutes: d, regular: reg, ot: ot, dt: dt });
  }
  var weeklyExtra = 0;
  if (r.weeklyOT != null && regPool > r.weeklyOT * 60) {
    weeklyExtra = regPool - r.weeklyOT * 60;
    // move the extra minutes from the latest regular minutes backwards into overtime
    var left = Math.min(weeklyExtra, regPool - prior);
    for (i = days.length - 1; i >= 0 && left > 0; i--) {
      var mv = Math.min(days[i].regular, left);
      days[i].regular -= mv; days[i].ot += mv; left -= mv;
    }
    weeklyExtra = Math.min(weeklyExtra, regPool - prior);
  }
  var out = { total: total, regular: 0, ot: 0, dt: 0, days: days, weeklyOT: weeklyExtra };
  days.forEach(function (x) { out.regular += x.regular; out.ot += x.ot; out.dt += x.dt; });
  return out;
}

/* Pay for a split. rate in $/h. bonus = non-discretionary pay added to the regular rate (FLSA regular rate
   = total straight-time earnings / total hours; each overtime hour then earns the extra half (or full) rate). */
function overtimePay(split, rate, bonus, otMult, dtMult) {
  otMult = otMult || 1.5; dtMult = dtMult || 2; bonus = bonus || 0;
  var hours = split.total / 60;
  var straight = hours * rate + bonus;
  var regularRate = hours > 0 ? straight / hours : rate;
  var otPremium = (split.ot / 60) * (otMult - 1) * regularRate;
  var dtPremium = (split.dt / 60) * (dtMult - 1) * regularRate;
  return { straight: straight, regularRate: regularRate, otPremium: otPremium, dtPremium: dtPremium,
           total: straight + otPremium + dtPremium };
}

/* ---------- pay periods ---------- */
function monthLength(y, m) { return new Date(Date.UTC(y, m, 0)).getUTCDate(); } // m = 1..12

/* Returns array of ISO dates. type: weekly | biweekly | semimonthly1 (1st-15th) | semimonthly2 (16th-end) | monthly */
function periodDates(startIso, type) {
  var s = isoToDays(startIso);
  if (s == null) return [];
  var d = new Date(s * 86400000), y = d.getUTCFullYear(), mo = d.getUTCMonth() + 1, out = [], i, n, first;
  if (type === "weekly") { n = 7; first = s; }
  else if (type === "biweekly") { n = 14; first = s; }
  else if (type === "semimonthly1") { first = isoToDays(y + "-" + (mo < 10 ? "0" : "") + mo + "-01"); n = 15; }
  else if (type === "semimonthly2") { first = isoToDays(y + "-" + (mo < 10 ? "0" : "") + mo + "-16"); n = monthLength(y, mo) - 15; }
  else { first = isoToDays(y + "-" + (mo < 10 ? "0" : "") + mo + "-01"); n = monthLength(y, mo); }
  for (i = 0; i < n; i++) out.push(daysToIso(first + i));
  return out;
}

/* Group dates into workweeks that start on weekStartDay (0=Sun..6=Sat). Returns [{dates:[idx...], startIdx}]. */
function groupWorkweeks(dates, weekStartDay) {
  var groups = [], cur = null;
  dates.forEach(function (iso, idx) {
    var wd = weekdayOf(iso);
    if (!cur || wd === weekStartDay) { cur = { idx: [] }; groups.push(cur); }
    cur.idx.push(idx);
  });
  return groups;
}

/* Time card across a pay period. entries: [{minutes}] aligned with dates. Overtime is computed per workweek.
   The first (possibly partial) week can carry prior hours. */
function periodOvertime(dates, minutes, rule, weekStartDay, priorMinutes) {
  var groups = groupWorkweeks(dates, weekStartDay), weeks = [];
  groups.forEach(function (g, gi) {
    var arr = [], pos = 0;
    // align to workweek positions: first partial week starts at its weekday offset
    var firstWd = weekdayOf(dates[g.idx[0]]);
    var offset = (firstWd - weekStartDay + 7) % 7;
    for (pos = 0; pos < offset; pos++) arr.push(0);
    g.idx.forEach(function (ix) { arr.push(minutes[ix] || 0); });
    var prior = gi === 0 ? (priorMinutes || 0) : 0;
    var res = computeOvertime(arr, rule, prior);
    res.dateIdx = g.idx; res.offset = offset; res.prior = prior;
    weeks.push(res);
  });
  var tot = { total: 0, regular: 0, ot: 0, dt: 0, weeks: weeks };
  weeks.forEach(function (w) { tot.total += w.total; tot.regular += w.regular; tot.ot += w.ot; tot.dt += w.dt; });
  return tot;
}

/* ---------- shift differential ---------- */
/* Minutes of a shift [startMin, endMin) (overnight if end<=start) that fall inside a daily window [wStart, wEnd)
   (window may cross midnight). */
function overlapMinutes(startMin, endMin, wStart, wEnd) {
  var len = endMin - startMin; if (len <= 0) len += DAY;
  var cnt = 0;
  for (var t = 0; t < len; t++) {
    var x = (startMin + t) % DAY;
    var inside = wStart < wEnd ? (x >= wStart && x < wEnd) : (x >= wStart || x < wEnd);
    if (inside) cnt++;
  }
  return cnt;
}

/* ---------- salary conversions ---------- */
function hourlyToSalary(rate, hoursPerWeek, weeksPerYear) {
  var annual = rate * hoursPerWeek * weeksPerYear;
  return { annual: annual, monthly: annual / 12, semimonthly: annual / 24, biweekly: annual / 26,
           weekly: annual / 52, weeklyWorked: rate * hoursPerWeek, daily: rate * hoursPerWeek / 5 };
}
function salaryToHourly(annual, hoursPerWeek, weeksPerYear) {
  return annual / (hoursPerWeek * weeksPerYear);
}

/* ---------- PTO accrual ---------- */
/* Simulates accrual per pay period. cfg: {perPeriod, periodsPerYear, start, cap, usedPerPeriod, periods} */
function ptoSchedule(cfg) {
  var bal = cfg.start || 0, rows = [], i, cappedOut = 0;
  for (i = 1; i <= cfg.periods; i++) {
    var add = cfg.perPeriod, used = cfg.usedPerPeriod || 0;
    bal += add;
    if (cfg.cap && bal > cfg.cap) { cappedOut += bal - cfg.cap; bal = cfg.cap; }
    bal -= used; if (bal < 0) bal = 0;
    rows.push({ period: i, accrued: add, used: used, balance: bal });
  }
  return { rows: rows, lostToCap: cappedOut, final: bal };
}

/* ---------- paycheck estimate (federal figures: IRS Pub 15-T and Pub 15, 2026) ---------- */
var TAX2026 = {
  ssRate: 0.062, medicareRate: 0.0145, ssWageBase: 184500,
  lineG: { single: 8600, married: 12900 },
  // [floor, base tax, rate, over]
  brackets: {
    single: [[0, 0, 0, 0], [7500, 0, 0.10, 7500], [19900, 1240, 0.12, 19900], [57900, 5800, 0.22, 57900],
             [113200, 17966, 0.24, 113200], [209275, 41024, 0.32, 209275], [263725, 58448, 0.35, 263725],
             [648100, 192979.25, 0.37, 648100]],
    married: [[0, 0, 0, 0], [19300, 0, 0.10, 19300], [44100, 2480, 0.12, 44100], [120100, 11600, 0.22, 120100],
              [230700, 35932, 0.24, 230700], [422850, 82048, 0.32, 422850], [531750, 116896, 0.35, 531750],
              [788000, 206583.5, 0.37, 788000]]
  }
};
function annualWithholding(adjustedAnnual, status) {
  var t = TAX2026.brackets[status] || TAX2026.brackets.single, row = t[0], i;
  for (i = 0; i < t.length; i++) if (adjustedAnnual >= t[i][0]) row = t[i];
  return Math.max(0, row[1] + (adjustedAnnual - row[3]) * row[2]);
}
/* gross per period; periods per year; cfg: {status, pretaxFica (section 125), pretaxIncome (401k etc), stateRate (%), otherWithholding} */
function estimatePaycheck(grossPeriod, periods, cfg) {
  var ficaWages = Math.max(0, grossPeriod - (cfg.pretaxFica || 0));
  var incomeWages = Math.max(0, grossPeriod - (cfg.pretaxFica || 0) - (cfg.pretaxIncome || 0));
  var annualInc = incomeWages * periods;
  var adjusted = Math.max(0, annualInc - TAX2026.lineG[cfg.status === "married" ? "married" : "single"]);
  var fedYear = annualWithholding(adjusted, cfg.status === "married" ? "married" : "single");
  var fed = fedYear / periods;
  var annualFica = ficaWages * periods;
  var ssTaxable = Math.min(annualFica, TAX2026.ssWageBase) / periods;
  var ss = ssTaxable * TAX2026.ssRate, med = ficaWages * TAX2026.medicareRate;
  var state = incomeWages * ((cfg.stateRate || 0) / 100);
  var other = cfg.otherWithholding || 0;
  var pre = (cfg.pretaxFica || 0) + (cfg.pretaxIncome || 0);
  var net = grossPeriod - pre - fed - ss - med - state - other;
  return { gross: grossPeriod, pretax: pre, federal: fed, socialSecurity: ss, medicare: med, state: state,
           other: other, net: net, adjustedAnnual: adjusted, fedYear: fedYear };
}

var api = {
  parseTime: parseTime, parseDuration: parseDuration, fmtHM: fmtHM, fmtHMwords: fmtHMwords, fmtDecimal: fmtDecimal,
  fmtTime12: fmtTime12, fmtTime24: fmtTime24, fmtMilitary: fmtMilitary, money: money, round2: round2,
  workedMinutes: workedMinutes, elapsedMinutes: elapsedMinutes, roundMinutes: roundMinutes,
  hmToDecimal: hmToDecimal, decimalToHM: decimalToHM, isoToDays: isoToDays, daysToIso: daysToIso, weekdayOf: weekdayOf,
  RULES: RULES, computeOvertime: computeOvertime, overtimePay: overtimePay, periodDates: periodDates,
  groupWorkweeks: groupWorkweeks, periodOvertime: periodOvertime, overlapMinutes: overlapMinutes,
  hourlyToSalary: hourlyToSalary, salaryToHourly: salaryToHourly, ptoSchedule: ptoSchedule,
  TAX2026: TAX2026, annualWithholding: annualWithholding, estimatePaycheck: estimatePaycheck, WD: WD
};
if (typeof module !== "undefined" && module.exports) module.exports = api;
else root.TC = api;
})(typeof window !== "undefined" ? window : this);
