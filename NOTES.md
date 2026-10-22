# NOTES - open items, unverified facts, and what you need to do

Branch: `feature/expand-timecard-tools`. Nothing was deployed; no Cloudflare/wrangler command was run.

## 1. Facts I could confirm from an official page during this work (2026-10-21)
- DOL Fact Sheet 23: 1.5x over 40 h in a workweek; workweek = fixed, recurring 168 hours; no averaging; no
  daily overtime as such; regular rate includes all remuneration for employment except listed exclusions.
- DOL Fact Sheet 56A: list of payments excludable from the regular rate.
- 29 CFR 785.18 (rest periods 5 to ~20 minutes are paid), 785.19 (bona fide meal period, completely relieved of
  duty, ordinarily 30+ minutes), 785.48(b) (rounding), 516.2 (required records), 778.106 (overtime payday).
- DOL state tables (meal/rest breaks and payday), both "last revised January 1, 2023".
- DOL minimum wage page: $7.25/hour. DOL vacation-leave page: FLSA does not require pay for time not worked.
- IRS Pub 15 (2026): Social Security 6.2%, wage base $184,500, Medicare 1.45%.
- IRS Pub 15-T (2026): annual percentage method tables (single and married filing jointly) and the $8,600 / $12,900 amounts.

## 2. Facts that rest on search-result summaries only - VERIFY before relying on them
These are implemented/stated, but I could not open the primary page (fetch failed or only a snippet was returned):
1. **California** (`ca_ot` source): 1.5x over 8 h/day, 2x over 12 h/day, 7th consecutive workday (1.5x first 8 h, 2x after),
   weekly over 40 h. The DIR page returned an error; the double-time and 7th-day parts were confirmed from search
   snippets of dir.ca.gov, the "1.5x over 8 h" and "weekly 40 h" parts are standard Labor Code 510 but not re-read.
   The 7th-day premium is applied only when all 7 days of the workweek have hours (per a DLSE memo found in search).
2. **Nevada** (NRS 608.018): daily 8 h only for employees paid under 1.5x the state minimum wage; AO-2025-05 is only linked,
   its content was not read. I deliberately did not state the dollar threshold.
3. **Alaska** (AS 23.10.060): 8 h/day and 40 h/week, daily overtime not double-counted, exemption for employers with three
   or fewer employees. From search summary of the Alaska wage-and-hour pamphlet.
4. **Colorado** COMPS Order #39 Rule 4.1.1: 12 h/day, 12 consecutive hours, 40 h/week, greatest of three. The calculator
   models 12 h/day and 40 h/week only (12 consecutive hours is NOT modeled; a note appears on the result). Check whether a
   newer COMPS order (#40+) replaced #39. The statement that Colorado does not allow comp time and Nevada's NAC 608.125
   comp-time statement come from search snippets.
5. **DOL Fact Sheet 17A** salary level $684/week: the page is "Revised September 2019" and does not mention the 2024 rule or
   its status. The site tells readers to confirm the current level at dol.gov; please check what is current.
6. **IRS 2026 withholding**: tables were extracted by a page reader from irs.gov, not from the PDF. Compare the single and
   MFJ tables and the $8,600/$12,900 amounts with Pub 15-T before relying on `TAX2026` (assets/calc.js). The statement that
   401(k) deferrals reduce income-tax wages but not Social Security/Medicare wages, and that section 125 premiums reduce
   both, is general IRS knowledge that I did NOT verify on a fetched page (Pub 15-B / Pub 15).
7. **Shift differentials and the regular rate**: Fact Sheet 56A's exclusion list does not mention shift differentials, and the
   site says the weighted rate includes them. Confirm with DOL guidance.
8. **Meal/rest table details**: "Alaska: none listed", "New York varies by industry" and the seven rest-break states are taken
   from the DOL table summary (revised 2023; may be out of date).

## 3. Left out on purpose (could not cite)
- Other states' overtime rules (Oregon, Minnesota, etc.) - the earlier page had uncited claims; they were removed.
- Whether paid leave counts toward the 40 hours (only the DOL point that leave pay may be excluded from the regular rate is stated).
- Retention periods for time cards (516.5 page confirmed 3 years for payroll records only; not stated on the site).
- Colorado pay frequency, additional Medicare tax, the "8 and 80" hospital rule, the regular-rate method for salaried
  non-exempt workers (the exempt guide's example states its own assumption and tells readers to confirm).
- State rounding rules.

## 4. Known limitations of the calculators
- California's 7th-day rule only applies when the shown period contains all seven days of the workweek.
- Colorado "12 consecutive hours" and California alternative workweek schedules / industry orders are not modeled.
- Semi-monthly/monthly periods carry earlier-week hours through the "hours already worked" box (regular hours only).
- Daylight-saving changes are not applied to date-crossing spans (stated on the hours page).
- The paycheck estimator: federal only, standard Step 1 only, no Step 2-4, no additional Medicare tax, state is a user percentage.

## 5. Things you must do (I did not and must not)
1. **Review** sections 2 and 3, then update wording or the `CHECKED` date in `gen/core.py` if you change any fact.
2. **Deploy**: Cloudflare Pages, build command none, output directory `public`. (`public/_headers` is included.)
3. **Domain**: if you use a custom domain, change `BASE` in `gen/core.py` and rerun `python generate.py`.
4. **Contact**: the old site showed an invented e-mail address on a pages.dev domain, which cannot receive mail. I replaced it
   with the repository's GitHub Issues link (`REPO_ISSUES` in `gen/core.py`). Make sure that repo is public, or put a real address there.
5. **Search Console / Bing Webmaster**: verify the property and submit `/sitemap.xml`. Check Coverage/Indexing and Core Web Vitals after a few weeks.
6. **AdSense later**: apply after the site has traffic; add `ads.txt` to `public/`; paste ad units inside the existing
   `<aside class="ad-slot">` containers (slots `in-content-1`, `in-content-2`, `home-1`, `home-2`); add the AdSense loader script
   in `gen/core.py` `layout()`; **update `/privacy/`** (it currently says no ads/analytics are used) and add a consent
   mechanism if you serve visitors in regions that require one (check Google's current requirements).
7. **Yearly**: refresh `TAX2026` and the text on the paycheck/rate pages from the new IRS Pub 15-T and Pub 15; re-check the
   state overtime pages and the DOL tables; bump `CHECKED`.
8. Optional but valuable for ranking: real outside links, and a short "about the author/reviewer" with a real name if you want
   stronger E-E-A-T signals for payroll topics (I did not invent a team or credentials).
