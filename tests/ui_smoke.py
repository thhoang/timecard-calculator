#!/usr/bin/env python3
"""Browser smoke test: drives each calculator in headless Edge/Chrome and checks the displayed answer.
Needs Microsoft Edge or Google Chrome installed (skips with a notice otherwise). No downloads, no dependencies.
Run after generate.py:  python tests/ui_smoke.py"""
import html
import http.server
import json
import os
import re
import shutil
import socketserver
import subprocess
import sys
import tempfile
import threading

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "public"))
BROWSERS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "/usr/bin/google-chrome", "/usr/bin/chromium", "/usr/bin/chromium-browser",
]

# (page, js steps, ids to read, expected substrings per id)
CASES = [
    ("/time-card-calculator/", "set('tc-start','2026-02-02','change');set('tc-wk','1','change');document.querySelector('[data-fill]').click();",
     ["tc-big", "tc-sub", "tc-extra"], {"tc-big": "42:30", "tc-sub": "42.5", "tc-extra": "2:30"}),
    ("/semi-monthly-time-card-calculator/",
     "set('tc-period','semimonthly2','change');set('tc-start','2026-01-16','change');set('tc-wk','1','change');set('tc-prior','40');"
     "var tr=document.querySelector('tr[data-d=\"2026-01-16\"]');tr.querySelector('.in').value='8:00 am';tr.querySelector('.out').value='4:30 pm';tr.querySelector('.brk').value='30';tr.querySelector('.in').dispatchEvent(new Event('input',{bubbles:true}));",
     ["tc-big", "tc-extra"], {"tc-big": "8:00", "tc-extra": "8:00"}),
    ("/overtime-calculator/", "set('ot-preset','ca','change');set('ot-rate','24');['13','10','8','8','8'].forEach(function(v,i){set('ot-d'+i,v);});",
     ["ot-big", "ot-extra"], {"ot-big": "$1,224.00"}),
    ("/overtime-calculator/", "set('ot-rate','20');['9','10','8','11','9'].forEach(function(v,i){set('ot-d'+i,v);});", ["ot-big"], {"ot-big": "$1,010.00"}),
    ("/overtime-calculator/", "set('ot-rate','20');set('ot-bonus','90');['9','9','9','9','9'].forEach(function(v,i){set('ot-d'+i,v);});", ["ot-big"], {"ot-big": "$1,045.00"}),
    ("/hours-calculator/", "set('hb-stime','10pm');set('hb-etime','6:30am');set('hb-break','30');", ["hb-big", "hb-sub"], {"hb-big": "8 hours", "hb-sub": "8:00"}),
    ("/hours-calculator/", "set('hb-sdate','2026-03-06');set('hb-stime','6pm');set('hb-edate','2026-03-09');set('hb-etime','6am');", ["hb-sub"], {"hb-sub": "60:00"}),
    ("/paycheck-calculator/", "set('pc-mode','gross','change');set('pc-gross','2000');set('pc-freq','26','change');", ["pc-big"], {"pc-big": "$1,690.85"}),
    ("/hourly-to-salary/", "set('hs-v','20');", ["hs-big"], {"hs-big": "$41,600"}),
    ("/salary-to-hourly/", "set('hs-v','62000');", ["hs-big"], {"hs-big": "$29.81"}),
    ("/pto-accrual-calculator/", "set('pto-method','days','change');set('pto-days','15');", ["pto-big"], {"pto-big": "120.0"}),
    ("/lunch-break-calculator/", "set('lb-in','8:00 am');set('lb-out','5:00 pm');set('lb-meal','30');", ["lb-big"], {"lb-big": "8:30"}),
    ("/shift-differential-calculator/", "set('sd-rate','20');set('sd-diff','2');set('sd-in','6pm');set('sd-out','3am');set('sd-break','30');set('sd-days','5');",
     ["sd-big", "sd-sub"], {"sd-big": "$180.00", "sd-sub": "$926.47"}),
    ("/work-schedule-planner/", "set('sp-pattern','4-3','change');set('sp-in','7:00 am');set('sp-out','5:30 pm');set('sp-start','2026-03-02','change');", ["sp-big"], {"sp-big": "40:00"}),
    ("/military-time-converter/", "set('mt-v','5:30 pm');set('mh-a','0700');set('mh-b','1530');", ["mt-big", "mh-big"], {"mt-big": "17:30", "mh-big": "8 hours 30 minutes"}),
    ("/time-rounding-calculator/", "set('rd-in','8:08 am');set('rd-out','5:07 pm');", ["rd-big", "rd-extra"], {"rd-big": "8:15", "rd-extra": "-14"}),
    ("/time-duration-calculator/", "set('du-v0','3:45');set('du-v1','2:30');set('du-v2','1:15');set('tp-time','10:15 pm');set('tp-dur','7:45');", ["du-big", "du-sub", "tp-big"], {"du-sub": "7:30", "tp-big": "6:00 AM"}),
    ("/decimal-hours-converter/", "set('hd-h','7');set('hd-m','45');set('dh-v','7.75');", ["hd-big", "dh-big"], {"hd-big": "7.75", "dh-big": "7:45"}),
    ("/minutes-to-decimal-chart/", "set('mc-v','410');", ["mc-big", "mc-sub"], {"mc-big": "6.83", "mc-sub": "6:50"}),
    ("/", "set('hb-stime','8am');set('hb-etime','5pm');set('hb-break','60');", ["hb-sub"], {"hb-sub": "8:00"}),
]

PRE = """<script>
function set(id,v,ev){var e=document.getElementById(id);if(!e){throw new Error('missing #'+id);}e.value=v;e.dispatchEvent(new Event(ev||'input',{bubbles:true}));}
window.addEventListener('load',function(){setTimeout(function(){var err='';try{STEPS}catch(e){err=String(e)}
var o={__err:err};IDS.forEach(function(i){var el=document.getElementById(i);o[i]=el?el.textContent:null;});
var p=document.createElement('pre');p.id='__out';p.textContent=JSON.stringify(o);document.body.appendChild(p);},80);});
</script>"""


def find_browser():
    for b in BROWSERS:
        if os.path.exists(b):
            return b
    return shutil.which("msedge") or shutil.which("chrome")


def main():
    browser = find_browser()
    if not browser:
        print("SKIP: no Edge/Chrome found")
        return 0
    tmp = tempfile.mkdtemp(prefix="tcc_ui_")
    site = os.path.join(tmp, "site")
    shutil.copytree(ROOT, site)

    class Q(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k):
            super().__init__(*a, directory=site, **k)

        def log_message(self, *a):
            pass

    srv = socketserver.TCPServer(("127.0.0.1", 0), Q)
    port = srv.server_address[1]
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    fails, n = [], 0
    for i, (page, steps, ids, expect) in enumerate(CASES):
        src = os.path.join(site, page.strip("/"), "index.html") if page != "/" else os.path.join(site, "index.html")
        raw = open(src, encoding="utf-8").read()
        inject = PRE.replace("STEPS", steps).replace("IDS", json.dumps(ids))
        name = "__t%d.html" % i
        open(os.path.join(site, name), "w", encoding="utf-8").write(raw.replace("</body>", inject + "</body>"))
        out = subprocess.run([browser, "--headless=new", "--disable-gpu", "--no-sandbox", "--user-data-dir=" + os.path.join(tmp, "prof%d" % i),
                              "--virtual-time-budget=4000", "--dump-dom", "http://127.0.0.1:%d/%s" % (port, name)],
                             capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=90).stdout or ""
        m = re.search(r'<pre id="__out">(.*?)</pre>', out, re.S)
        n += 1
        if not m:
            fails.append("%s: harness output missing" % page)
            continue
        data = json.loads(html.unescape(m.group(1)))
        if data.get("__err"):
            fails.append("%s: script error %s" % (page, data["__err"]))
            continue
        for k, want in expect.items():
            got = data.get(k) or ""
            if want not in got:
                fails.append("%s: #%s expected %r in %r" % (page, k, want, got[:200]))
    srv.shutdown()
    shutil.rmtree(tmp, ignore_errors=True)
    for f in fails:
        print("FAIL", f)
    print("ran %d browser cases, %d failures" % (n, len(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
