/* Time Card Calculator - client-side tools. No dependencies. */
"use strict";

/* ---------- core time helpers (also unit-tested in node) ---------- */

/* Parse "8", "8am", "8:15", "8:15 am", "17:30", "5.5" into minutes since
   midnight. Returns null when the text is not a time. Overnight shifts are
   handled by callers (out < in means next day). */
function parseTime(str) {
  if (str == null) return null;
  var s = String(str).trim().toLowerCase();
  if (!s) return null;
  var ampm = null;
  var m = s.match(/(a\.?m\.?|p\.?m\.?)$/);
  if (m) { ampm = m[1][0]; s = s.slice(0, m.index).trim(); }
  var h, min = 0;
  var parts = s.split(/[:\.]/);
  if (parts.length === 1) {
    if (!/^\d{1,2}$/.test(parts[0])) return null;
    h = parseInt(parts[0], 10);
  } else if (parts.length === 2) {
    if (!/^\d{1,2}$/.test(parts[0]) || !/^\d{1,2}$/.test(parts[1])) return null;
    h = parseInt(parts[0], 10); min = parseInt(parts[1], 10);
    if (s.indexOf(".") !== -1 && parts[1].length <= 1) return null; // "8.5" is ambiguous
  } else return null;
  if (min > 59) return null;
  if (ampm) {
    if (h < 1 || h > 12) return null;
    if (h === 12) h = 0;
    if (ampm === "p") h += 12;
  } else {
    if (h > 24) return null;
    if (h === 24) h = 0;
  }
  return h * 60 + min;
}

/* Worked minutes between clock-in and clock-out, minus break minutes.
   out <= in is treated as an overnight shift. */
function workedMinutes(inMin, outMin, breakMin) {
  if (inMin == null || outMin == null) return 0;
  var span = outMin - inMin;
  if (span <= 0) span += 24 * 60;
  var b = Math.max(0, breakMin || 0);
  return Math.max(0, span - b);
}

function roundMinutes(mins, step) {
  if (!step) return mins;
  return Math.round(mins / step) * step;
}

function fmtHM(mins) {
  var sign = mins < 0 ? "-" : "";
  mins = Math.abs(Math.round(mins));
  var h = Math.floor(mins / 60), m = mins % 60;
  return sign + h + ":" + (m < 10 ? "0" : "") + m;
}

function fmtDecimal(mins, digits) {
  return (mins / 60).toFixed(digits == null ? 2 : digits);
}

/* Split a week of worked minutes into regular / overtime.
   rule: "weekly40" (1.5x over 40h/wk), "daily8" (also 1.5x over 8h/day),
   "none". Daily minutes arrive as an array of 7 numbers. */
function splitOvertime(dailyMinutes, rule) {
  var total = dailyMinutes.reduce(function (a, b) { return a + b; }, 0);
  var reg = 0, ot = 0, i, d;
  if (rule === "daily8") {
    var weeklyPool = 0;
    for (i = 0; i < dailyMinutes.length; i++) {
      d = dailyMinutes[i];
      var dayReg = Math.min(d, 8 * 60);
      ot += d - dayReg;
      weeklyPool += dayReg;
    }
    var weeklyOT = Math.max(0, weeklyPool - 40 * 60);
    ot += weeklyOT;
    reg = total - ot;
  } else if (rule === "weekly40") {
    reg = Math.min(total, 40 * 60);
    ot = total - reg;
  } else {
    reg = total; ot = 0;
  }
  return { total: total, regular: reg, overtime: ot };
}

if (typeof module !== "undefined" && module.exports) {
  module.exports = { parseTime: parseTime, workedMinutes: workedMinutes,
    splitOvertime: splitOvertime, fmtHM: fmtHM, fmtDecimal: fmtDecimal,
    roundMinutes: roundMinutes };
}

/* ---------- page bootstrapping (browser only) ---------- */
if (typeof document !== "undefined") {

function $(sel, root) { return (root || document).querySelector(sel); }
function $$(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }
function money(n) { return "$" + n.toFixed(2); }

/* ============ 1. Weekly time card (index) ============ */
function initTimeCard() {
  var table = $("#tc-body");
  if (!table) return;
  var DAYS = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"];
  var STORE = "tcc-timecard-v1";

  function readInputs() {
    return $$("tr", table).map(function (tr) {
      return {
        inT: $(".in", tr).value,
        outT: $(".out", tr).value,
        brk: parseInt($(".brk", tr).value, 10) || 0
      };
    });
  }
  function compute() {
    var rows = readInputs();
    var rule = $("#ot-rule").value;
    var roundStep = parseInt($("#round").value, 10) || 0;
    var rate = parseFloat($("#rate").value) || 0;
    var otMult = parseFloat($("#ot-mult").value) || 1.5;
    var daily = [];
    $$("tr", table).forEach(function (tr, i) {
      var mins = workedMinutes(parseTime(rows[i].inT), parseTime(rows[i].outT), rows[i].brk);
      mins = roundMinutes(mins, roundStep);
      daily.push(mins);
      $(".day-total", tr).textContent = mins ? fmtHM(mins) : "";
    });
    var s = splitOvertime(daily, rule);
    $("#r-total").textContent = fmtHM(s.total) + " (" + fmtDecimal(s.total) + " h)";
    $("#r-regular").textContent = fmtHM(s.regular) + " (" + fmtDecimal(s.regular) + " h)";
    $("#r-ot").textContent = fmtHM(s.overtime) + " (" + fmtDecimal(s.overtime) + " h)";
    var pp = $("#pp-name");
    if (pp) {
      var bits = [];
      if ($("#emp-name") && $("#emp-name").value) bits.push($("#emp-name").value);
      if ($("#emp-company") && $("#emp-company").value) bits.push($("#emp-company").value);
      if ($("#week-start") && $("#week-start").value) bits.push("week starting " + $("#week-start").value);
      pp.textContent = bits.join(" - ");
    }
    if (rate > 0) {
      var pay = s.regular / 60 * rate + s.overtime / 60 * rate * otMult;
      $("#r-pay-row").style.display = "";
      $("#r-pay").textContent = money(pay);
      $("#r-pay-note").textContent = "regular " + money(s.regular / 60 * rate) +
        " + overtime " + money(s.overtime / 60 * rate * otMult) + " at " + otMult + "x";
    } else {
      $("#r-pay-row").style.display = "none";
    }
    try { localStorage.setItem(STORE, JSON.stringify({
      rows: rows, rule: rule, round: roundStep, rate: $("#rate").value, otMult: otMult,
      name: $("#emp-name") ? $("#emp-name").value : "", company: $("#emp-company") ? $("#emp-company").value : "",
      week: $("#week-start") ? $("#week-start").value : "" })); } catch (e) {}
  }
  // restore
  try {
    var saved = JSON.parse(localStorage.getItem(STORE) || "null");
    if (saved) {
      $$("tr", table).forEach(function (tr, i) {
        if (saved.rows && saved.rows[i]) {
          $(".in", tr).value = saved.rows[i].inT || "";
          $(".out", tr).value = saved.rows[i].outT || "";
          $(".brk", tr).value = saved.rows[i].brk || "";
        }
      });
      if (saved.rule) $("#ot-rule").value = saved.rule;
      if (saved.round != null) $("#round").value = saved.round;
      if (saved.rate) $("#rate").value = saved.rate;
      if (saved.otMult) $("#ot-mult").value = saved.otMult;
      if (saved.name && $("#emp-name")) $("#emp-name").value = saved.name;
      if (saved.company && $("#emp-company")) $("#emp-company").value = saved.company;
      if (saved.week && $("#week-start")) $("#week-start").value = saved.week;
    }
  } catch (e) {}
  document.addEventListener("input", function (e) {
    if (e.target.closest && e.target.closest("#timecard-app")) compute();
  });
  document.addEventListener("change", function (e) {
    if (e.target.closest && e.target.closest("#timecard-app")) compute();
  });
  var clearBtn = $("#tc-clear");
  if (clearBtn) clearBtn.addEventListener("click", function () {
    $$("tr", table).forEach(function (tr) {
      $(".in", tr).value = ""; $(".out", tr).value = ""; $(".brk", tr).value = "";
    });
    compute();
  });
  var printBtn = $("#tc-print");
  if (printBtn) printBtn.addEventListener("click", function () { window.print(); });
  compute();
}

/* ============ 2. Hours between two times ============ */
function initHoursBetween() {
  var form = $("#hb-app");
  if (!form) return;
  function compute() {
    var a = parseTime($("#hb-in").value), b = parseTime($("#hb-out").value);
    var brk = parseInt($("#hb-break").value, 10) || 0;
    if (a == null || b == null) { $("#hb-result").style.display = "none"; return; }
    var mins = workedMinutes(a, b, brk);
    var gross = workedMinutes(a, b, 0);
    $("#hb-result").style.display = "";
    $("#hb-hm").textContent = fmtHM(mins);
    $("#hb-dec").textContent = fmtDecimal(mins) + " hours";
    $("#hb-gross").textContent = brk ? "including your " + brk + "-minute break, that is "
      + fmtHM(gross) + " (" + fmtDecimal(gross) + " hours) clock to clock" :
      "no break deducted";
    $("#hb-week").textContent = fmtHM(mins * 5) + " (" + fmtDecimal(mins * 5) + " hours) over a 5-day week";
  }
  form.addEventListener("input", compute);
  form.addEventListener("change", compute);
  var pre = new URLSearchParams(location.search);
  if (pre.get("in")) $("#hb-in").value = pre.get("in");
  if (pre.get("out")) $("#hb-out").value = pre.get("out");
  compute();
}

/* ============ 3. Hourly <-> salary ============ */
function initHourlySalary() {
  var form = $("#hs-app");
  if (!form) return;
  function compute() {
    var hourly = parseFloat($("#hs-hourly").value);
    var hpw = parseFloat($("#hs-hpw").value) || 40;
    var wpy = parseFloat($("#hs-wpy").value) || 52;
    if (!(hourly > 0)) { $("#hs-result").style.display = "none"; return; }
    var annual = hourly * hpw * wpy;
    $("#hs-result").style.display = "";
    $("#hs-annual").textContent = "$" + annual.toLocaleString("en-US", {maximumFractionDigits: 0});
    $("#hs-monthly").textContent = "$" + (annual / 12).toLocaleString("en-US", {maximumFractionDigits: 0}) + " / month";
    $("#hs-weekly").textContent = "$" + (annual / wpy).toLocaleString("en-US", {maximumFractionDigits: 0}) + " / week";
    $("#hs-daily").textContent = "$" + (hourly * (hpw / 5)).toLocaleString("en-US", {maximumFractionDigits: 0}) + " / day (5-day week)";
  }
  form.addEventListener("input", compute);
  compute();
}

/* ============ 4. Printable weekly timesheet ============ */
function initTimesheet() {
  var app = $("#ts-app");
  if (!app) return;
  // default week start = most recent Monday
  var ws = $("#ts-app #week-start");
  if (ws && !ws.value) {
    var d = new Date();
    var day = (d.getDay() + 6) % 7; // Mon=0
    d.setDate(d.getDate() - day);
    ws.value = d.toISOString().slice(0, 10);
  }
  var printBtn = $("#ts-print");
  if (printBtn) printBtn.addEventListener("click", function () { window.print(); });
}

document.addEventListener("DOMContentLoaded", function () {
  initTimeCard(); initHoursBetween(); initHourlySalary(); initTimesheet();
  var y = $("#year"); if (y) y.textContent = new Date().getFullYear();
});
}
