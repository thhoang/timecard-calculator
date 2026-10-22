/* Time Card Calculator - page wiring for the calculators. Needs calc.js (window.TC). No dependencies. */
(function () {
"use strict";
const TC = window.TC;
if (!TC) return;

const $ = (s, r) => (r || document).querySelector(s);
const $$ = (s, r) => Array.prototype.slice.call((r || document).querySelectorAll(s));
const esc = s => String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const money = TC.money;
const MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
const DAYN = TC.WD;
const dayShort = i => DAYN[i].slice(0, 3);
function fmtDate(iso, withYear) {
  const d = TC.isoToDays(iso); if (d == null) return "";
  const dt = new Date(d * 86400000);
  return dayShort(dt.getUTCDay()) + " " + MONTHS[dt.getUTCMonth()] + " " + dt.getUTCDate() + (withYear ? ", " + dt.getUTCFullYear() : "");
}
const hrs = m => TC.fmtHM(m) + " (" + TC.fmtDecimal(m) + " h)";
const num = (el, def) => { if (!el) return def == null ? 0 : def; const v = parseFloat(el.value); return isFinite(v) ? v : (def == null ? 0 : def); };
const dur = el => { if (!el || !el.value.trim()) return 0; const v = TC.parseDuration(el.value); return v == null ? NaN : v; };
function todayIso() { const d = new Date(); return new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate())).toISOString().slice(0, 10); }
function store(key, val) { try { if (val === undefined) return JSON.parse(localStorage.getItem(key) || "null"); localStorage.setItem(key, JSON.stringify(val)); } catch (e) { return null; } return null; }

/* Common result renderer. o: {big, sub, steps[], extra, good} ; o === null hides. */
function show(p, o) {
  const a = document.getElementById(p + "-answer"), e = document.getElementById(p + "-empty");
  const b = document.getElementById(p + "-bd"), x = document.getElementById(p + "-extra");
  if (!o) {
    if (a) a.hidden = true; if (b) b.hidden = true; if (e) e.hidden = false; if (x) x.innerHTML = "";
    return;
  }
  if (e) e.hidden = true;
  if (a) {
    a.hidden = false; a.classList.toggle("good", !!o.good);
    document.getElementById(p + "-big").innerHTML = o.big || "";
    document.getElementById(p + "-sub").innerHTML = o.sub || "";
  }
  if (x) x.innerHTML = o.extra || "";
  if (b) {
    b.hidden = !(o.steps && o.steps.length);
    document.getElementById(p + "-steps").innerHTML = (o.steps || []).map(s => "<li>" + s + "</li>").join("");
  }
}
const note = (t, cls) => '<div class="note ' + (cls || "") + '">' + t + "</div>";
const stat = (l, v) => '<div class="stat"><div class="l">' + l + '</div><div class="v">' + v + "</div></div>";
const statGrid = arr => '<div class="stat-grid">' + arr.join("") + "</div>";
const kv = (l, v, cls) => '<div class="kv ' + (cls || "") + '"><span>' + l + "</span><b>" + v + "</b></div>";
const tbl = (head, rows, numFrom) => '<div class="table-wrap"><table><thead><tr>' + head.map((h, i) => "<th" + (i >= (numFrom == null ? 1 : numFrom) ? ' class="num"' : "") + ">" + h + "</th>").join("") +
  "</tr></thead><tbody>" + rows.map(r => "<tr" + (r.cls ? ' class="' + r.cls + '"' : "") + ">" + r.c.map((c, i) => (i === 0 ? "<th scope=\"row\">" : "<td" + (i >= (numFrom == null ? 1 : numFrom) ? ' class="num"' : "") + ">") + c + (i === 0 ? "</th>" : "</td>")).join("") + "</tr>").join("") + "</tbody></table></div>";

const inits = {};

/* ===================================================== 1. Time card (weekly / bi-weekly / semi-monthly / monthly) */
inits.timecard = function (root, g, recompute) {
  const body = g("body"), KEY = "tcc-timecard-v2";
  const saved = store(KEY) || {};
  const entries = saved.entries || {};
  const preset = root.getAttribute("data-period");
  const locked = root.hasAttribute("data-locked");
  const settings = ["period", "start", "wk", "rule", "round", "rate", "prior", "name", "company"];
  if (saved.s && !locked) settings.forEach(k => { if (saved.s[k] != null && g(k) && !(k === "period" && preset)) g(k).value = saved.s[k]; });
  if (preset && g("period")) g("period").value = preset;
  if (g("period") && locked) g("period").value = "weekly";

  function defaultStart() {
    const t = g("period").value, today = todayIso();
    if (t === "weekly" || t === "biweekly") {
      const wk = parseInt(g("wk").value, 10);
      let d = TC.isoToDays(today), wd = TC.weekdayOf(today);
      d -= (wd - wk + 7) % 7;
      return TC.daysToIso(d);
    }
    return today;
  }
  function relabel() {
    const t = g("period").value;
    g("start-label").textContent = (t === "weekly" || t === "biweekly") ? "Pay period starts" : "Any date in the month";
  }
  function render() {
    relabel();
    if (!g("start").value) g("start").value = defaultStart();
    const dates = TC.periodDates(g("start").value, g("period").value);
    body.innerHTML = dates.map(iso => {
      const e = entries[iso] || {};
      return '<tr data-d="' + iso + '"><th scope="row">' + fmtDate(iso) + '</th>' +
        '<td><input class="in" type="text" inputmode="text" placeholder="8:00 am" aria-label="Clock in ' + fmtDate(iso) + '" value="' + esc(e.i || "") + '"></td>' +
        '<td><input class="out" type="text" inputmode="text" placeholder="5:00 pm" aria-label="Clock out ' + fmtDate(iso) + '" value="' + esc(e.o || "") + '"></td>' +
        '<td><input class="brk" type="number" min="0" step="5" placeholder="30" aria-label="Unpaid break minutes ' + fmtDate(iso) + '" value="' + esc(e.b || "") + '"></td>' +
        '<td class="num day-total"></td></tr>';
    }).join("");
  }
  function readRows() {
    $$("tr[data-d]", body).forEach(tr => {
      const iso = tr.getAttribute("data-d");
      entries[iso] = { i: $(".in", tr).value, o: $(".out", tr).value, b: $(".brk", tr).value };
    });
  }
  const compute = function () {
    readRows();
    const dates = TC.periodDates(g("start").value, g("period").value);
    const step = parseInt(g("round").value, 10) || 0;
    const rule = g("rule").value, wk = parseInt(g("wk").value, 10), rate = num(g("rate"));
    const mins = [], rows = $$("tr[data-d]", body);
    let bad = 0, anyEntry = false;
    rows.forEach(tr => {
      const inEl = $(".in", tr), outEl = $(".out", tr);
      const a = TC.parseTime(inEl.value), b = TC.parseTime(outEl.value);
      inEl.setAttribute("aria-invalid", inEl.value.trim() && a == null ? "true" : "false");
      outEl.setAttribute("aria-invalid", outEl.value.trim() && b == null ? "true" : "false");
      if ((inEl.value.trim() && a == null) || (outEl.value.trim() && b == null)) bad++;
      let m = 0;
      if (a != null && b != null) {
        anyEntry = true;
        let span = b - a; if (span <= 0) span += 1440;
        const brk = Math.max(0, parseInt($(".brk", tr).value, 10) || 0);
        m = Math.max(0, TC.roundMinutes(a + span, step) - TC.roundMinutes(a, step) - brk);
      }
      mins.push(m);
      $(".day-total", tr).textContent = m ? TC.fmtHM(m) : "";
    });
    const prior = Math.max(0, dur(g("prior")) || 0);
    const res = TC.periodOvertime(dates, mins, rule, wk, prior);
    const ppEl = g("pp");
    if (ppEl) {
      const bits = [];
      if (g("name") && g("name").value) bits.push(g("name").value);
      if (g("company") && g("company").value) bits.push(g("company").value);
      bits.push(fmtDate(dates[0], true) + " to " + fmtDate(dates[dates.length - 1], true));
      ppEl.textContent = bits.join(" - ");
    }
    store(KEY, { entries: entries, s: (function () { const o = {}; settings.forEach(k => { if (g(k)) o[k] = g(k).value; }); return o; })() });
    if (!anyEntry) { show("tc", null); return; }
    const R = TC.RULES[rule];
    let pay = 0, straightPay = 0, otPay = 0, dtPay = 0;
    res.weeks.forEach(w => { const p = TC.overtimePay(w, rate, 0); pay += p.total; straightPay += p.straight; otPay += p.otPremium; dtPay += p.dtPremium; });
    const steps = [];
    steps.push("For each day: clock out minus clock in" + (step ? " (each punch rounded to the nearest " + step + " minutes first)" : "") + ", minus the unpaid break. A clock-out earlier than the clock-in counts as an overnight shift.");
    res.weeks.forEach((w, i) => {
      const first = dates[w.dateIdx[0]], last = dates[w.dateIdx[w.dateIdx.length - 1]];
      let line = "<b>Workweek " + (i + 1) + "</b> (" + fmtDate(first) + " to " + fmtDate(last) + "): " + TC.fmtHM(w.total) + " worked";
      if (w.prior) line += " plus " + TC.fmtHM(w.prior) + " already worked earlier that week";
      line += " &rarr; " + TC.fmtHM(w.regular) + " regular";
      if (w.ot) line += ", " + TC.fmtHM(w.ot) + " at 1.5x";
      if (w.dt) line += ", " + TC.fmtHM(w.dt) + " at 2x";
      steps.push(line + ".");
    });
    steps.push("Overtime rule used: " + esc(R.label) + ". Overtime is figured per workweek (a 7-day block starting on " + DAYN[wk] + "), never averaged across weeks.");
    steps.push("Period total = " + TC.fmtHM(res.regular) + " regular + " + TC.fmtHM(res.ot) + " overtime" + (res.dt ? " + " + TC.fmtHM(res.dt) + " double time" : "") + " = <b>" + TC.fmtHM(res.total) + "</b> (" + TC.fmtDecimal(res.total) + " decimal hours).");
    if (rate > 0) steps.push("Pay = " + money(straightPay) + " straight time (" + TC.fmtDecimal(res.total) + " h x " + money(rate) + ") + " + money(otPay) + " time-and-a-half premium" + (dtPay ? " + " + money(dtPay) + " double-time premium" : "") + " = <b>" + money(pay) + "</b> gross.");
    const wkRows = res.weeks.map((w, i) => ({ c: ["Week " + (i + 1) + " (" + fmtDate(dates[w.dateIdx[0]]) + ")", TC.fmtHM(w.total), TC.fmtHM(w.regular), TC.fmtHM(w.ot), TC.fmtHM(w.dt)] }));
    wkRows.push({ cls: "total", c: ["Period total", TC.fmtHM(res.total), TC.fmtHM(res.regular), TC.fmtHM(res.ot), TC.fmtHM(res.dt)] });
    const extra = statGrid([stat("Total", TC.fmtHM(res.total)), stat("Regular", TC.fmtHM(res.regular)), stat("Overtime 1.5x", TC.fmtHM(res.ot))].concat(res.dt ? [stat("Double time 2x", TC.fmtHM(res.dt))] : []).concat(rate > 0 ? [stat("Gross pay", money(pay))] : [])) +
      tbl(["Workweek", "Total", "Regular", "1.5x", "2x"], wkRows) + (bad ? note("Some times could not be read. Try formats like 8, 8:30, 8am, 5:15 pm or 17:15.") : "");
    show("tc", { big: TC.fmtHM(res.total) + ' <small>hours:minutes</small>', sub: "= <b>" + TC.fmtDecimal(res.total) + "</b> decimal hours" + (rate > 0 ? " &middot; gross pay <b>" + money(pay) + "</b>" : ""), steps: steps, extra: extra, good: true });
  };
  root._fill = function () {
    $$("tr[data-d]", body).forEach(tr => {
      const wd = TC.weekdayOf(tr.getAttribute("data-d"));
      const on = wd >= 1 && wd <= 5;
      $(".in", tr).value = on ? "8:00 am" : ""; $(".out", tr).value = on ? "5:00 pm" : ""; $(".brk", tr).value = on ? "30" : "";
    });
    recompute();
  };
  const fillBtn = $("[data-fill]", root);
  if (fillBtn) fillBtn.addEventListener("click", root._fill);
  root._reset = function () { Object.keys(entries).forEach(k => delete entries[k]); render(); recompute(); };
  ["period", "start", "wk"].forEach(k => g(k) && g(k).addEventListener("change", function () { readRows(); if (k !== "start" && !(k === "wk" && (g("period").value === "semimonthly1" || g("period").value === "semimonthly2" || g("period").value === "monthly"))) { if (k === "period" || k === "wk") g("start").value = defaultStart(); } render(); recompute(); }));
  render();
  return compute;
};

/* ===================================================== 2. Hours between two times (date crossing, overnight) */
inits.hb = function (root, g) {
  const q = new URLSearchParams(location.search);
  if (q.get("in") && g("stime")) g("stime").value = q.get("in");
  if (q.get("out") && g("etime")) g("etime").value = q.get("out");
  if (q.get("brk") && g("break")) g("break").value = q.get("brk");
  return function () {
    const a = TC.parseTime(g("stime").value), b = TC.parseTime(g("etime").value);
    const sd = g("sdate") ? g("sdate").value : "", ed = g("edate") ? g("edate").value : "";
    if (a == null || b == null) { show("hb", null); return; }
    const brk = Math.max(0, num(g("break")));
    const rate = num(g("rate")), days = num(g("days"), 5);
    const el = TC.elapsedMinutes(sd, a, ed, b);
    if (el < 0) { show("hb", { big: "End is before start", sub: "Check the dates: the end date and time must come after the start.", steps: [] }); return; }
    const net = Math.max(0, el - brk);
    const crosses = (sd && ed && sd !== ed) || (!sd && !ed && b <= a);
    const steps = [];
    steps.push("Start: " + (sd ? fmtDate(sd, true) + ", " : "") + TC.fmtTime12(a) + ". End: " + (ed ? fmtDate(ed, true) + ", " : "") + TC.fmtTime12(b) + (!sd && !ed && b <= a ? " (next day, because the end time is not after the start time)" : "") + ".");
    steps.push("Clock-to-clock time = end minus start = <b>" + TC.fmtHM(el) + "</b> (" + el + " minutes).");
    steps.push(brk ? "Subtract the unpaid break: " + TC.fmtHM(el) + " &minus; " + brk + " min = <b>" + TC.fmtHM(net) + "</b>." : "No unpaid break was entered, so nothing is subtracted.");
    steps.push("Decimal hours = " + net + " minutes &divide; 60 = <b>" + TC.fmtDecimal(net) + "</b>.");
    if (days > 0) steps.push("Over " + days + " days: " + net + " x " + days + " = " + TC.fmtHM(net * days) + " (" + TC.fmtDecimal(net * days) + " h)" + (net * days > 2400 ? " - above 40 hours, so federal overtime could apply." : "."));
    if (rate > 0) steps.push("Pay for this one shift at " + money(rate) + "/h = " + TC.fmtDecimal(net) + " x " + money(rate) + " = <b>" + money(net / 60 * rate) + "</b> (before any overtime).");
    const extra = statGrid([stat("Hours:minutes", TC.fmtHM(net)), stat("Decimal hours", TC.fmtDecimal(net)), stat("Total minutes", net)].concat(brk ? [stat("Clock to clock", TC.fmtHM(el))] : [])) +
      (crosses ? note("This time span crosses midnight" + (el >= 1440 ? " and covers more than one full day" : "") + ".", "info") : "") +
      (el >= 1440 && !sd ? "" : "");
    show("hb", { big: TC.fmtHMwords(net), sub: "= <b>" + TC.fmtHM(net) + "</b> &middot; <b>" + TC.fmtDecimal(net) + "</b> decimal hours" + (brk ? " (after a " + brk + "-minute break)" : ""), steps: steps, extra: extra, good: true });
  };
};

/* ===================================================== 3. Overtime pay */
inits.ot = function (root, g) {
  const labels = () => { const w = parseInt(g("wk").value, 10); for (let i = 0; i < 7; i++) { const l = $("label[for='" + g("d" + i).id + "']", root); if (l) l.textContent = DAYN[(w + i) % 7] + (i === 6 ? " (day 7)" : ""); } };
  const syncCustom = () => { $$(".custom-only", root).forEach(x => x.hidden = g("preset").value !== "custom"); };
  g("wk").addEventListener("change", labels); g("preset").addEventListener("change", syncCustom);
  labels(); syncCustom();
  return function () {
    const w = parseInt(g("wk").value, 10);
    const d = [], bad = [];
    for (let i = 0; i < 7; i++) { const v = dur(g("d" + i)); if (v !== v) { bad.push(DAYN[(w + i) % 7]); d.push(0); } else d.push(v); }
    const total = d.reduce((a, b) => a + b, 0);
    if (!total) { show("ot", null); return; }
    let rule, otM = 1.5, dtM = 2, label;
    const key = g("preset").value;
    if (key === "custom") {
      const dOT = g("cd").value.trim() ? num(g("cd")) : null, dDT = g("cdt").value.trim() ? num(g("cdt")) : null, wk = g("cw").value.trim() ? num(g("cw")) : null;
      rule = { dailyOT: dOT, dailyDT: dDT, weeklyOT: wk, seventh: false };
      otM = num(g("cm1"), 1.5); dtM = num(g("cm2"), 2);
      label = "Custom rule: daily overtime after " + (dOT == null ? "n/a" : dOT + " h") + ", double time after " + (dDT == null ? "n/a" : dDT + " h") + ", weekly overtime after " + (wk == null ? "n/a" : wk + " h");
    } else { rule = key; label = TC.RULES[key].label; }
    const rate = num(g("rate")), bonus = num(g("bonus"));
    const s = TC.computeOvertime(d, rule, 0);
    const pay = TC.overtimePay(s, rate, bonus, otM, dtM);
    const steps = [];
    steps.push("Hours per day: " + d.map((m, i) => DAYN[(w + i) % 7].slice(0, 3) + " " + TC.fmtHM(m)).join(", ") + " = <b>" + TC.fmtHM(total) + "</b> in the week.");
    steps.push("Rule applied: " + esc(label) + ".");
    const dailyOT = s.days.reduce((a, x) => a + x.ot + x.dt, 0) - s.weeklyOT;
    if (key !== "federal" && key !== "none" && key !== "nv_high") steps.push("Daily step: hours past the daily limit are overtime first (" + TC.fmtHM(Math.max(0, dailyOT)) + "). Those hours are set aside so they are not counted twice toward the weekly limit.");
    steps.push("Weekly step: straight-time hours left after the daily step are compared with the weekly limit. Weekly overtime = <b>" + TC.fmtHM(s.weeklyOT) + "</b>.");
    steps.push("Result: <b>" + TC.fmtHM(s.regular) + "</b> regular, <b>" + TC.fmtHM(s.ot) + "</b> at " + otM + "x" + (s.dt ? ", <b>" + TC.fmtHM(s.dt) + "</b> at " + dtM + "x" : "") + ".");
    if (rate > 0) {
      if (bonus > 0) steps.push("Regular rate = (" + TC.fmtDecimal(total) + " h x " + money(rate) + " + " + money(bonus) + " bonus) &divide; " + TC.fmtDecimal(total) + " h = <b>" + money(pay.regularRate) + "/h</b>. A non-discretionary bonus raises the rate that overtime is based on.");
      steps.push("Straight-time pay for all hours = " + money(pay.straight) + ". Overtime premium = " + TC.fmtDecimal(s.ot) + " h x " + (otM - 1) + " x " + money(pay.regularRate) + " = " + money(pay.otPremium) + (s.dt ? "; double-time premium = " + money(pay.dtPremium) : "") + ".");
      steps.push("Total gross pay = " + money(pay.straight) + " + " + money(pay.otPremium + pay.dtPremium) + " = <b>" + money(pay.total) + "</b>.");
    }
    const rows = s.days.map((x, i) => ({ c: [DAYN[(w + i) % 7], TC.fmtHM(x.minutes), TC.fmtHM(x.regular), TC.fmtHM(x.ot), TC.fmtHM(x.dt)] }));
    rows.push({ cls: "total", c: ["Week", TC.fmtHM(s.total), TC.fmtHM(s.regular), TC.fmtHM(s.ot), TC.fmtHM(s.dt)] });
    let extra = statGrid([stat("Regular hours", TC.fmtDecimal(s.regular)), stat("Overtime hours", TC.fmtDecimal(s.ot)), stat("Double-time hours", TC.fmtDecimal(s.dt))].concat(rate > 0 ? [stat("Gross pay", money(pay.total))] : [])) + tbl(["Day", "Worked", "Regular", "1.5x", "2x"], rows);
    if (bad.length) extra += note("Could not read hours for: " + bad.join(", ") + ". Use formats like 8, 8.5 or 8:30.");
    if (key === "co") extra += note("Colorado also requires overtime after 12 <i>consecutive</i> hours, even across two workdays. This calculator does not model that rule.", "info");
    if (key === "ca") extra += note("California also has special rules (for example for some industries and for workers on alternative workweek schedules). This is the general rule only.", "info");
    show("ot", { big: rate > 0 ? money(pay.total) : TC.fmtHM(s.ot) + " <small>overtime</small>", sub: rate > 0 ? "gross pay for " + TC.fmtDecimal(total) + " hours, including " + TC.fmtDecimal(s.ot + s.dt) + " overtime hours" : "Enter an hourly rate to see pay.", steps: steps, extra: extra, good: rate > 0 });
  };
};

/* ===================================================== 4. Time duration (add/subtract) */
inits.duration = function (root, g) {
  return function () {
    let total = 0, any = false, bad = 0; const steps = [];
    for (let i = 0; i < 6; i++) {
      const el = g("v" + i); if (!el.value.trim()) continue;
      const m = TC.parseDuration(el.value);
      el.setAttribute("aria-invalid", m == null ? "true" : "false");
      if (m == null) { bad++; continue; }
      const sign = g("s" + i).value === "-" ? -1 : 1;
      any = true; total += sign * m;
      steps.push((sign < 0 ? "Subtract " : (steps.length ? "Add " : "Start with ")) + "<b>" + TC.fmtHM(m) + "</b> (" + m + " minutes). Running total: " + TC.fmtHM(total) + ".");
    }
    if (!any) { show("du", null); return; }
    const a = Math.abs(total), d = Math.floor(a / 1440), rem = a % 1440;
    const extra = statGrid([stat("Hours:minutes", TC.fmtHM(total)), stat("Decimal hours", (total / 60).toFixed(2)), stat("Total minutes", total)].concat(d ? [stat("Days + hours", (total < 0 ? "-" : "") + d + "d " + TC.fmtHM(rem))] : [])) + (bad ? note(bad + " entr" + (bad > 1 ? "ies" : "y") + " could not be read. Use 1:30, 1h 30m, 45m or 1.5.") : "");
    show("du", { big: TC.fmtHMwords(total), sub: "= <b>" + TC.fmtHM(total) + "</b> &middot; <b>" + (total / 60).toFixed(2) + "</b> decimal hours", steps: steps, extra: extra, good: true });
  };
};
inits.timeplus = function (root, g) {
  return function () {
    const t = TC.parseTime(g("time").value), d = TC.parseDuration(g("dur").value);
    if (t == null || d == null) { show("tp", null); return; }
    const sign = g("op").value === "-" ? -1 : 1;
    const raw = t + sign * d, day = Math.floor(raw / 1440);
    const when = day === 0 ? "the same day" : day > 0 ? day + (day === 1 ? " day later" : " days later") : -day + (day === -1 ? " day earlier" : " days earlier");
    const steps = ["Start time " + TC.fmtTime12(t) + " = " + t + " minutes after midnight.", (sign < 0 ? "Subtract " : "Add ") + TC.fmtHM(d) + " (" + d + " minutes): " + t + (sign < 0 ? " &minus; " : " + ") + d + " = " + raw + ".",
      "Wrap around a 24-hour day (1,440 minutes): " + raw + " &rarr; " + (((raw % 1440) + 1440) % 1440) + " minutes after midnight = <b>" + TC.fmtTime12(raw) + "</b> (" + when + ")."];
    show("tp", { big: TC.fmtTime12(raw), sub: TC.fmtTime24(raw) + " in 24-hour time &middot; " + when, steps: steps, good: true });
  };
};

/* ===================================================== 5. Decimal <-> hh:mm */
inits.hm2dec = function (root, g) {
  return function () {
    const h = g("h").value.trim() === "" ? null : num(g("h")), m = g("m").value.trim() === "" ? null : num(g("m"));
    if (h == null && m == null) { show("hd", null); return; }
    const tm = (h || 0) * 60 + (m || 0);
    const steps = ["Total minutes = " + (h || 0) + " x 60 + " + (m || 0) + " = " + tm + ".", "Decimal hours = " + tm + " &divide; 60 = <b>" + (tm / 60).toFixed(4).replace(/0+$/, "").replace(/\.$/, "") + "</b>.", "Rounded to two places: <b>" + (tm / 60).toFixed(2) + "</b> hours (use this on most payroll systems)."];
    show("hd", { big: (tm / 60).toFixed(2) + " <small>hours</small>", sub: TC.fmtHM(tm) + " = " + tm + " minutes", steps: steps, good: true });
  };
};
inits.dec2hm = function (root, g) {
  return function () {
    const v = g("v").value.trim(); if (v === "" || !isFinite(+v)) { show("dh", null); return; }
    const x = Math.abs(parseFloat(v)), r = TC.decimalToHM(x), sign = parseFloat(v) < 0 ? "-" : "";
    const whole = Math.floor(x), frac = x - whole;
    const steps = ["Whole hours = " + whole + ".", "Minutes = the decimal part x 60 = " + frac.toFixed(4).replace(/0+$/, "").replace(/\.$/, "") + " x 60 = " + (frac * 60).toFixed(2) + " &rarr; " + Math.round(frac * 60) + " minutes (rounded).", "Answer: <b>" + sign + r.hours + ":" + (r.minutes < 10 ? "0" : "") + r.minutes + "</b> (" + r.hours + " hours " + r.minutes + " minutes)."];
    show("dh", { big: sign + r.hours + ":" + (r.minutes < 10 ? "0" : "") + r.minutes, sub: sign + r.hours + " hours " + r.minutes + " minutes &middot; " + Math.round(x * 60) + " total minutes", steps: steps, good: true });
  };
};
inits.mins = function (root, g) {
  return function () {
    const v = g("v").value.trim(); if (v === "" || !isFinite(+v) || +v < 0) { show("mc", null); return; }
    const m = parseFloat(v);
    const steps = ["Decimal hours = " + m + " minutes &divide; 60 = <b>" + (m / 60).toFixed(4).replace(/0+$/, "").replace(/\.$/, "") + "</b>.", "Hours and minutes: " + Math.floor(m / 60) + " whole hours with " + (Math.round(m) % 60) + " minutes left = <b>" + TC.fmtHM(m) + "</b>."];
    show("mc", { big: (m / 60).toFixed(2) + " <small>hours</small>", sub: "= " + TC.fmtHM(m) + " (hours:minutes)", steps: steps, good: true });
  };
};

/* ===================================================== 6. Paycheck estimator */
inits.pc = function (root, g) {
  const sync = () => { const hourly = g("mode").value === "hourly"; $$(".hourly-only", root).forEach(x => x.hidden = !hourly); $$(".gross-only", root).forEach(x => x.hidden = hourly); };
  g("mode").addEventListener("change", sync); sync();
  return function () {
    const periods = parseInt(g("freq").value, 10), status = g("status").value;
    let gross, steps = [];
    if (g("mode").value === "hourly") {
      const rate = num(g("rate")), reg = num(g("reg"), 40), ot = num(g("ot"));
      if (!(rate > 0)) { show("pc", null); return; }
      const weekly = rate * reg + rate * 1.5 * ot;
      gross = weekly * 52 / periods;
      steps.push("Weekly gross = " + reg + " h x " + money(rate) + (ot ? " + " + ot + " overtime h x " + money(rate * 1.5) : "") + " = " + money(weekly) + ".");
      steps.push("Gross per pay period = weekly gross x 52 weeks &divide; " + periods + " pay periods = <b>" + money(gross) + "</b>.");
    } else {
      gross = num(g("gross"));
      if (!(gross > 0)) { show("pc", null); return; }
      steps.push("Gross pay per period entered: <b>" + money(gross) + "</b>.");
    }
    const cfg = { status: status, pretaxFica: num(g("sec125")), pretaxIncome: num(g("k401")), stateRate: num(g("state")), otherWithholding: num(g("other")) };
    const r = TC.estimatePaycheck(gross, periods, cfg);
    steps.push("Pre-tax deductions: " + money(r.pretax) + " (health/cafeteria plan reduces income tax <i>and</i> Social Security/Medicare wages; 401(k)-type deferrals reduce income-tax wages only).");
    steps.push("Federal income tax withholding (IRS Pub 15-T, 2026 percentage method, " + (status === "married" ? "married filing jointly" : "single") + ", standard Step 1 only): annualised taxable wages " + money(r.gross - r.pretax + 0) + " x " + periods + " &minus; " + money(TC.TAX2026.lineG[status === "married" ? "married" : "single"]) + " = " + money(r.adjustedAnnual) + " adjusted annual wages &rarr; " + money(r.fedYear) + " per year &divide; " + periods + " = <b>" + money(r.federal) + "</b> per pay period.");
    steps.push("Social Security 6.2% = <b>" + money(r.socialSecurity) + "</b> (stops after the $184,500 annual wage base); Medicare 1.45% = <b>" + money(r.medicare) + "</b>.");
    if (r.state) steps.push("State/local income tax at your " + cfg.stateRate + "% estimate = <b>" + money(r.state) + "</b>.");
    if (r.other) steps.push("Other withholding you entered: " + money(r.other) + ".");
    steps.push("Take-home = gross &minus; pre-tax deductions &minus; taxes = " + money(gross) + " &minus; " + money(r.pretax) + " &minus; " + money(r.federal + r.socialSecurity + r.medicare + r.state + r.other) + " = <b>" + money(r.net) + "</b>.");
    const rows = [{ c: ["Gross pay", money(r.gross), money(r.gross * periods)] }, { c: ["Pre-tax deductions", "-" + money(r.pretax), "-" + money(r.pretax * periods)] }, { c: ["Federal income tax (est.)", "-" + money(r.federal), "-" + money(r.federal * periods)] },
      { c: ["Social Security", "-" + money(r.socialSecurity), "-" + money(r.socialSecurity * periods)] }, { c: ["Medicare", "-" + money(r.medicare), "-" + money(r.medicare * periods)] }];
    if (r.state) rows.push({ c: ["State/local (your %)", "-" + money(r.state), "-" + money(r.state * periods)] });
    if (r.other) rows.push({ c: ["Other withholding", "-" + money(r.other), "-" + money(r.other * periods)] });
    rows.push({ cls: "total", c: ["Estimated take-home", money(r.net), money(r.net * periods)] });
    const extra = tbl(["Item", "Per pay period", "Per year"], rows) + note("<b>Estimate only.</b> Federal figures use the IRS 2026 Publication 15-T percentage method for a Form W-4 with no Step 2 box, credits or adjustments. Your employer's payroll system, your W-4, state and local taxes, and other deductions will change the real number.");
    show("pc", { big: money(r.net) + " <small>estimated take-home</small>", sub: "per pay period &middot; " + (100 * r.net / gross).toFixed(1) + "% of gross &middot; about " + money(r.net * periods) + " per year", steps: steps, extra: extra, good: true });
  };
};

/* ===================================================== 7. Hourly <-> salary */
inits.hs = function (root, g) {
  const mode = root.getAttribute("data-mode");
  return function () {
    const hpw = num(g("hpw"), 40), unpaid = num(g("off")), weeks = Math.max(1, 52 - unpaid);
    if (mode === "h2s") {
      const r = num(g("v")); if (!(r > 0)) { show("hs", null); return; }
      const s = TC.hourlyToSalary(r, hpw, weeks);
      const steps = ["Hours per year = " + hpw + " hours x " + weeks + " paid weeks = " + (hpw * weeks).toLocaleString() + ".", "Annual = " + (hpw * weeks).toLocaleString() + " x " + money(r) + " = <b>" + money(s.annual, 0) + "</b>.", "Monthly = annual &divide; 12 = " + money(s.monthly) + ". Bi-weekly (26 checks) = " + money(s.biweekly) + ". Semi-monthly (24 checks) = " + money(s.semimonthly) + "."];
      const rows = [["Hourly", money(r)], ["Daily (" + hpw / 5 + " h)", money(s.daily)], ["Weekly (worked)", money(s.weeklyWorked)], ["Bi-weekly", money(s.biweekly)], ["Semi-monthly", money(s.semimonthly)], ["Monthly", money(s.monthly)], ["Annual", money(s.annual, 0)]];
      show("hs", { big: money(s.annual, 0) + " <small>per year (gross)</small>", sub: money(s.monthly, 0) + "/month &middot; " + money(s.biweekly, 0) + " bi-weekly &middot; before taxes", steps: steps, extra: tbl(["Period", "Gross pay"], rows.map(x => ({ c: x }))), good: true });
    } else {
      const a = num(g("v")); if (!(a > 0)) { show("hs", null); return; }
      const h = TC.salaryToHourly(a, hpw, weeks);
      const steps = ["Hours per year = " + hpw + " hours x " + weeks + " weeks = " + (hpw * weeks).toLocaleString() + ".", "Hourly = " + money(a, 0) + " &divide; " + (hpw * weeks).toLocaleString() + " = <b>" + money(h) + "</b>.", "Check: " + money(h) + " x " + (hpw * weeks).toLocaleString() + " = " + money(h * hpw * weeks, 0) + "."];
      const s = TC.hourlyToSalary(h, hpw, weeks);
      const rows = [["Hourly", money(h)], ["Daily (" + hpw / 5 + " h)", money(s.daily)], ["Weekly", money(s.weeklyWorked)], ["Bi-weekly check", money(a / 26)], ["Semi-monthly check", money(a / 24)], ["Monthly", money(a / 12)]];
      show("hs", { big: money(h) + " <small>per hour</small>", sub: "based on " + hpw + " hours a week and " + weeks + " paid weeks", steps: steps, extra: tbl(["Period", "Gross pay"], rows.map(x => ({ c: x }))) + (hpw > 40 ? note("Above 40 hours a week an hourly (non-exempt) worker would also earn overtime. A salary only equals this hourly figure if the job is exempt or the salary is set up to cover those hours.", "info") : ""), good: true });
    }
  };
};

/* ===================================================== 8. PTO accrual */
inits.pto = function (root, g) {
  const sync = () => { const m = g("method").value; $$("[data-m]", root).forEach(x => x.hidden = x.getAttribute("data-m").split(",").indexOf(m) < 0); };
  g("method").addEventListener("change", sync); sync();
  return function () {
    const periods = parseInt(g("freq").value, 10), hpw = num(g("hpw"), 40), start = num(g("start")), cap = num(g("cap")), used = num(g("used"));
    const m = g("method").value; let per, how;
    if (m === "perperiod") { per = num(g("pp")); how = per + " hours per pay period (entered)"; }
    else if (m === "days") { const dpy = num(g("days")); per = dpy * num(g("hday"), 8) / periods; how = dpy + " days x " + num(g("hday"), 8) + " h &divide; " + periods + " pay periods = " + per.toFixed(3) + " h"; }
    else { const ratio = num(g("ratio"), 30); per = (hpw * 52 / periods) / ratio; how = "(" + hpw + " h/week x 52 &divide; " + periods + " = " + (hpw * 52 / periods).toFixed(2) + " h per period) &divide; " + ratio + " = " + per.toFixed(3) + " h"; }
    if (!(per > 0)) { show("pto", null); return; }
    const n = Math.max(1, Math.min(104, Math.round(num(g("n"), periods))));
    const sch = TC.ptoSchedule({ perPeriod: per, periods: n, start: start, cap: cap || 0, usedPerPeriod: used / periods });
    const yr = per * periods, hday = num(g("hday"), 8);
    const steps = ["Accrual per pay period: " + how + ".", "Per year: " + per.toFixed(3) + " x " + periods + " = <b>" + yr.toFixed(1) + " hours</b> (" + (yr / hday).toFixed(1) + " days of " + hday + " h).", "Balance after " + n + " pay periods starting from " + start + " h" + (used ? ", using " + used + " h a year spread evenly" : "") + (cap ? ", capped at " + cap + " h" : "") + ": <b>" + sch.final.toFixed(1) + " hours</b>."];
    if (cap && sch.lostToCap > 0) steps.push("The cap would stop " + sch.lostToCap.toFixed(1) + " hours from accruing over this time - use or cash out PTO before reaching the cap.");
    const pick = sch.rows.filter((r, i) => i < 6 || (i + 1) % periods === 0 || i === sch.rows.length - 1).slice(0, 14);
    const extra = statGrid([stat("Per pay period", per.toFixed(2) + " h"), stat("Per year", yr.toFixed(1) + " h"), stat("Days per year", (yr / hday).toFixed(1)), stat("Balance at end", sch.final.toFixed(1) + " h")]) +
      tbl(["Pay period", "Accrued", "Balance after"], pick.map(r => ({ c: ["#" + r.period, "+" + r.accrued.toFixed(2) + " h", r.balance.toFixed(2) + " h"] })));
    show("pto", { big: yr.toFixed(1) + " <small>hours of PTO per year</small>", sub: "= " + (yr / hday).toFixed(1) + " days &middot; " + per.toFixed(2) + " h each pay period", steps: steps, extra: extra, good: true });
  };
};

/* ===================================================== 9. Lunch / unpaid break */
inits.lb = function (root, g) {
  return function () {
    const a = TC.parseTime(g("in").value), b = TC.parseTime(g("out").value);
    if (a == null || b == null) { show("lb", null); return; }
    const gross = TC.workedMinutes(a, b, 0);
    const meal = Math.max(0, num(g("meal"))), thr = g("thr").value.trim() ? num(g("thr")) * 60 : 0;
    const restN = Math.max(0, num(g("rn"))), restM = Math.max(0, num(g("rm")));
    const days = num(g("days"), 5), rate = num(g("rate"));
    const auto = !thr || gross > thr;
    const ded = auto ? meal : 0;
    const paid = Math.max(0, gross - ded);
    const steps = ["Shift from clock-in to clock-out: <b>" + TC.fmtHM(gross) + "</b>."];
    if (thr) steps.push("Automatic meal deduction applies only to shifts longer than " + (thr / 60) + " hours. This shift is " + (auto ? "longer, so the deduction applies." : "not longer, so nothing is deducted."));
    steps.push("Unpaid meal period deducted: " + ded + " minutes &rarr; paid time = " + TC.fmtHM(gross) + " &minus; " + ded + " min = <b>" + TC.fmtHM(paid) + "</b> (" + TC.fmtDecimal(paid) + " h).");
    if (restN && restM) steps.push(restN + " paid rest break" + (restN > 1 ? "s" : "") + " of " + restM + " minutes stay inside the paid time (they are not subtracted).");
    steps.push("Over " + days + " days: " + TC.fmtHM(paid * days) + " (" + TC.fmtDecimal(paid * days) + " h).");
    if (rate > 0) steps.push("Weekly pay at " + money(rate) + "/h before overtime = <b>" + money(paid / 60 * days * rate) + "</b>. Without the meal deduction it would be " + money(gross / 60 * days * rate) + ", so the unpaid meal accounts for " + money(ded / 60 * days * rate) + " a week.");
    let extra = statGrid([stat("Paid per day", TC.fmtHM(paid)), stat("Paid per week", TC.fmtHM(paid * days)), stat("Clock to clock", TC.fmtHM(gross))].concat(rate > 0 ? [stat("Weekly pay", money(paid / 60 * days * rate))] : []));
    if (ded > 0 && ded < 30) extra += note("Federal guidance (29 CFR 785.19) says 30 minutes or more is ordinarily long enough for a bona fide meal period. A shorter break may have to be paid, and some states set their own minimums. Check your state.");
    if (restM >= 5 && restM <= 20) extra += note("Short rest breaks of about 5 to 20 minutes are generally counted as paid working time under 29 CFR 785.18.", "info");
    if (ded > 0) extra += note("An unpaid meal period only works if the employee is completely relieved of duty. If you work through lunch, that time is generally hours worked - see <a href=\"/guides/how-to-calculate-hours-worked-with-breaks/\">our guide</a>.", "info");
    show("lb", { big: TC.fmtHM(paid) + " <small>paid hours</small>", sub: "= " + TC.fmtDecimal(paid) + " decimal hours per day after a " + ded + "-minute unpaid meal", steps: steps, extra: extra, good: true });
  };
};

/* ===================================================== 10. Shift differential */
inits.sd = function (root, g) {
  return function () {
    const a = TC.parseTime(g("in").value), b = TC.parseTime(g("out").value);
    const base = num(g("rate")); if (a == null || b == null || !(base > 0)) { show("sd", null); return; }
    const ws = TC.parseTime(g("ws").value), we = TC.parseTime(g("we").value);
    if (ws == null || we == null) { show("sd", null); return; }
    const brk = Math.max(0, num(g("break"))), days = num(g("days"), 5);
    const diff = num(g("diff")), isPct = g("type").value === "pct";
    const diffRate = isPct ? base * diff / 100 : diff;
    const gross = TC.workedMinutes(a, b, 0), net = Math.max(0, gross - brk);
    const inWin0 = TC.overlapMinutes(a, b, ws, we);
    // the break is assumed to come out of non-window time first (state this in the steps)
    const inWin = Math.max(0, Math.min(inWin0, net));
    const outWin = net - inWin;
    const basePay = net / 60 * base, diffPay = inWin / 60 * diffRate, shiftPay = basePay + diffPay;
    const weekMin = net * days, weekStraight = shiftPay * days;
    const ot = Math.max(0, weekMin - 2400);
    const reg = weekMin > 0 ? weekStraight / (weekMin / 60) : base;
    const otPrem = ot / 60 * 0.5 * reg, week = weekStraight + otPrem;
    const steps = ["Shift " + TC.fmtTime12(a) + " to " + TC.fmtTime12(b) + " = " + TC.fmtHM(gross) + (brk ? "; minus " + brk + " min unpaid break = " + TC.fmtHM(net) : "") + ".",
      "Differential window " + TC.fmtTime12(ws) + " to " + TC.fmtTime12(we) + ": " + TC.fmtHM(inWin0) + " of the shift falls inside it" + (inWin0 !== inWin ? " (limited to paid time)" : "") + ".",
      "Differential per hour = " + (isPct ? diff + "% of " + money(base) + " = " : "") + "<b>" + money(diffRate) + "</b>.",
      "Base pay = " + TC.fmtDecimal(net) + " h x " + money(base) + " = " + money(basePay) + ". Differential pay = " + TC.fmtDecimal(inWin) + " h x " + money(diffRate) + " = " + money(diffPay) + ".",
      "One shift = <b>" + money(shiftPay) + "</b>; effective rate = " + money(net ? shiftPay / (net / 60) : base) + " per hour."];
    if (days > 1) steps.push(days + " shifts a week = " + TC.fmtHM(weekMin) + " worked, " + money(weekStraight) + " straight-time pay." + (ot ? " Over 40 hours: the differential is part of the regular rate, so the overtime premium is " + TC.fmtDecimal(ot) + " h x 0.5 x " + money(reg) + " (weighted regular rate) = " + money(otPrem) + ". Weekly total = <b>" + money(week) + "</b>." : ""));
    const extra = statGrid([stat("Hours in window", TC.fmtDecimal(inWin)), stat("Differential pay / shift", money(diffPay)), stat("Per shift", money(shiftPay)), stat("Per week", money(week))]) +
      note("Whether an overtime week's regular rate includes the differential depends on federal and state rules; under the FLSA the regular rate includes all pay for work except specific exclusions (<a href=\"https://www.dol.gov/agencies/whd/fact-sheets/56a-regular-rate\" rel=\"noopener\">DOL Fact Sheet 56A</a>). Confirm how your employer applies it.", "info");
    show("sd", { big: money(shiftPay) + " <small>per shift</small>", sub: "effective " + money(net ? shiftPay / (net / 60) : base) + "/h &middot; " + money(week) + " for " + days + " shifts", steps: steps, extra: extra, good: true });
  };
};

/* ===================================================== 11. Work schedule / shift planner */
const PATTERNS = {
  "5-2": [1, 1, 1, 1, 1, 0, 0], "4-3": [1, 1, 1, 1, 0, 0, 0], "3-4": [1, 1, 1, 0, 0, 0, 0],
  "223": [1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0], "4-4": [1, 1, 1, 1, 0, 0, 0, 0], "7-7": [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
  "6-1": [1, 1, 1, 1, 1, 1, 0], "2-2": [1, 1, 0, 0]
};
inits.sp = function (root, g) {
  const sync = () => { $$(".custom-only", root).forEach(x => x.hidden = g("pattern").value !== "custom"); };
  g("pattern").addEventListener("change", sync); sync();
  if (!g("start").value) { const t = todayIso(); g("start").value = TC.daysToIso(TC.isoToDays(t) - (TC.weekdayOf(t) + 6) % 7); }
  return function () {
    const a = TC.parseTime(g("in").value), b = TC.parseTime(g("out").value), start = g("start").value;
    if (a == null || b == null || TC.isoToDays(start) == null) { show("sp", null); return; }
    let pat = PATTERNS[g("pattern").value];
    if (g("pattern").value === "custom") { const on = Math.max(1, Math.round(num(g("on"), 4))), off = Math.max(0, Math.round(num(g("offd"), 3))); pat = []; for (let i = 0; i < on; i++) pat.push(1); for (let i = 0; i < off; i++) pat.push(0); }
    const brk = Math.max(0, num(g("break"))), net = TC.workedMinutes(a, b, brk), weeks = Math.max(1, Math.min(12, Math.round(num(g("weeks"), 4)))), rate = num(g("rate"));
    const s0 = TC.isoToDays(start), calStart = s0 - (TC.weekdayOf(start) + 6) % 7; // Monday on/before start
    const rows = []; let all = 0, otTotal = 0, shiftsAll = 0; const steps = [];
    for (let w = 0; w < weeks; w++) {
      const cells = []; let shifts = 0;
      for (let d = 0; d < 7; d++) {
        const day = calStart + w * 7 + d, k = day - s0;
        const on = k >= 0 && pat[k % pat.length] === 1;
        if (on) shifts++;
        cells.push(on ? "<b>" + TC.fmtTime12(a).replace(":00", "") + "</b>" : (k < 0 ? "" : "off"));
      }
      const m = shifts * net, ot = Math.max(0, m - 2400); all += m; otTotal += ot; shiftsAll += shifts;
      rows.push({ c: ["Wk " + (w + 1) + " (" + fmtDate(TC.daysToIso(calStart + w * 7)) + ")"].concat(cells, [TC.fmtHM(m)]), cls: ot ? "hl" : "" });
    }
    const avg = all / weeks;
    steps.push("Each shift: " + TC.fmtTime12(a) + " to " + TC.fmtTime12(b) + (brk ? " minus " + brk + " min break" : "") + " = <b>" + TC.fmtHM(net) + "</b> paid.");
    steps.push("Pattern: " + pat.length + "-day cycle with " + pat.reduce((x, y) => x + y, 0) + " shifts per cycle, starting " + fmtDate(start, true) + ". Weeks are shown Monday to Sunday.");
    steps.push(weeks + " weeks contain " + shiftsAll + " shifts = <b>" + TC.fmtHM(all) + "</b> hours; average <b>" + TC.fmtHM(avg) + "</b> per week.");
    if (otTotal) steps.push("Weeks highlighted in green pass 40 hours; under the federal weekly rule that is " + TC.fmtHM(otTotal) + " of overtime across the weeks shown. Your state or employer rules may differ.");
    if (rate > 0) steps.push("Straight-time pay for the period = " + TC.fmtDecimal(all) + " h x " + money(rate) + " = " + money(all / 60 * rate) + "; overtime premium (0.5 x rate) = " + money(otTotal / 60 * rate * 0.5) + "; total = <b>" + money(all / 60 * rate + otTotal / 60 * rate * 0.5) + "</b>.");
    const extra = '<div class="table-wrap"><table><thead><tr><th>Week</th>' + ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"].map(x => "<th>" + x + "</th>").join("") + '<th class="num">Hours</th></tr></thead><tbody>' +
      rows.map(r => "<tr" + (r.cls ? ' class="' + r.cls + '"' : "") + "><th scope=\"row\">" + r.c[0] + "</th>" + r.c.slice(1, 8).map(c => "<td>" + c + "</td>").join("") + '<td class="num">' + r.c[8] + "</td></tr>").join("") + "</tbody></table></div>";
    show("sp", { big: TC.fmtHM(avg) + " <small>average hours per week</small>", sub: shiftsAll + " shifts in " + weeks + " weeks &middot; " + TC.fmtHM(all) + " total", steps: steps, extra: extra, good: true });
  };
};

/* ===================================================== 12. Military (24-hour) time */
inits.mt = function (root, g) {
  return function () {
    const raw = g("v").value.trim(); if (!raw) { show("mt", null); return; }
    const t = TC.parseTime(raw);
    if (t == null) { show("mt", { big: "Not a time", sub: "Try 5:30 pm, 17:30, 1730 or 0600.", steps: [] }); return; }
    const h = Math.floor(t / 60), m = t % 60;
    const was12 = /[ap]\.?m?\.?\s*$/i.test(raw);
    const steps = was12 ? ["12-hour to 24-hour: AM hours stay the same (except 12 AM becomes 00); PM hours add 12 (except 12 PM stays 12).", TC.fmtTime12(t) + " &rarr; <b>" + TC.fmtTime24(t) + "</b>, written in military style as <b>" + TC.fmtMilitary(t) + "</b>."] :
      ["24-hour to 12-hour: hours 1-11 are AM; 12 is 12 PM (noon); 13-23 subtract 12 and use PM; 00 is 12 AM (midnight).", TC.fmtTime24(t) + " &rarr; <b>" + TC.fmtTime12(t) + "</b>."];
    show("mt", { big: was12 ? TC.fmtTime24(t) : TC.fmtTime12(t), sub: "Military style: " + TC.fmtMilitary(t) + " &middot; " + (was12 ? TC.fmtTime12(t) : TC.fmtTime24(t)), steps: steps, good: true });
  };
};
inits.mh = function (root, g) {
  return function () {
    const a = TC.parseTime(g("a").value), b = TC.parseTime(g("b").value); if (a == null || b == null) { show("mh", null); return; }
    const m = TC.workedMinutes(a, b, 0);
    show("mh", { big: TC.fmtHMwords(m), sub: TC.fmtTime24(a) + " to " + TC.fmtTime24(b) + " &middot; " + TC.fmtDecimal(m) + " decimal hours" + (b <= a ? " (crosses midnight)" : ""), steps: ["Convert both to minutes after midnight: " + a + " and " + b + (b <= a ? " (+1,440 because the end is the next day)" : "") + ".", "Difference = <b>" + m + " minutes</b> = " + TC.fmtHM(m) + "."], good: true });
  };
};

/* ===================================================== 13. Time rounding / 7-minute rule */
inits.rd = function (root, g) {
  return function () {
    const a = TC.parseTime(g("in").value), b = TC.parseTime(g("out").value);
    if (a == null || b == null) { show("rd", null); return; }
    const step = parseInt(g("step").value, 10), mode = g("mode").value, rate = num(g("rate")), days = num(g("days"), 5);
    const brk = Math.max(0, num(g("break")));
    let span = b - a; if (span <= 0) span += 1440;
    const outAbs = a + span;
    const ra = TC.roundMinutes(a, step, mode), rb = TC.roundMinutes(outAbs, step, mode);
    const actual = Math.max(0, span - brk), rounded = Math.max(0, rb - ra - brk), diff = rounded - actual;
    const steps = ["Actual punches: in " + TC.fmtTime12(a) + ", out " + TC.fmtTime12(outAbs) + " &rarr; " + TC.fmtHM(span) + (brk ? " minus " + brk + " min break = " + TC.fmtHM(actual) : "") + ".",
      "Clock-in " + TC.fmtTime12(a) + " is " + (a % step) + " minute" + (a % step === 1 ? "" : "s") + " past a " + step + "-minute mark &rarr; " + (mode === "nearest" ? (step === 15 ? "7-minute rule: 1-7 minutes round down, 8-14 round up" : "nearest mark, halfway rounds up") : mode === "up" ? "always rounds up" : "always rounds down") + " &rarr; <b>" + TC.fmtTime12(ra) + "</b>.",
      "Clock-out " + TC.fmtTime12(outAbs) + " is " + (outAbs % step) + " minute" + (outAbs % step === 1 ? "" : "s") + " past a mark &rarr; <b>" + TC.fmtTime12(rb) + "</b>.",
      "Paid time after rounding: " + TC.fmtHM(rb - ra) + (brk ? " minus " + brk + " min = " : " = ") + "<b>" + TC.fmtHM(rounded) + "</b>. Difference from actual: <b>" + (diff >= 0 ? "+" : "") + diff + " minutes</b> for this shift."];
    if (rate > 0) steps.push("Effect on pay: " + (diff >= 0 ? "+" : "-") + money(Math.abs(diff) / 60 * rate) + " per shift; over " + days + " shifts a week and 52 weeks ~ " + (diff >= 0 ? "+" : "-") + money(Math.abs(diff) / 60 * rate * days * 52) + " per year for this one pattern. A single shift can go either way; legal rounding must not shortchange employees over time.");
    const extra = statGrid([stat("Actual", TC.fmtHM(actual)), stat("Rounded", TC.fmtHM(rounded)), stat("Difference", (diff >= 0 ? "+" : "") + diff + " min")]) +
      (mode !== "nearest" ? note("Always rounding in the employer's favor (always down) is the pattern federal regulators and courts look at most closely. Under 29 CFR 785.48(b), rounding is acceptable only if it does not result, over time, in failure to compensate employees properly. Some states do not allow rounding at all.") : "");
    show("rd", { big: TC.fmtHM(rounded), sub: "rounded paid time (actual " + TC.fmtHM(actual) + ")", steps: steps, extra: extra, good: true });
  };
};

/* ===================================================== bootstrap */
function setup(root) {
  const p = root.getAttribute("data-p"), t = root.getAttribute("data-tool");
  const g = n => document.getElementById(p + "-" + n);
  let compute = function () {};
  const recompute = () => compute();
  const fn = inits[t];
  if (!fn) return;
  const c = fn(root, g, recompute);
  if (typeof c === "function") compute = c;
  root.addEventListener("input", compute);
  root.addEventListener("change", compute);
  $$("[data-print]", root).forEach(b => b.addEventListener("click", () => window.print()));
  $$("[data-reset]", root).forEach(b => b.addEventListener("click", () => {
    $$("input,select", root).forEach(el => {
      if (el.type === "checkbox") el.checked = el.defaultChecked;
      else if (el.tagName === "SELECT") Array.prototype.forEach.call(el.options, o => { o.selected = o.defaultSelected; });
      else el.value = el.defaultValue;
    });
    if (root._reset) root._reset();
    $$("select", root).forEach(s => s.dispatchEvent(new Event("change", { bubbles: true })));
    compute();
  }));
  compute();
}
function boot() {
  $$("[data-tool]").forEach(setup);
  $$("[data-today]").forEach(el => { el.textContent = new Date().toLocaleDateString("en-US", { year: "numeric", month: "long", day: "numeric" }); });
}
if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot); else boot();
})();
