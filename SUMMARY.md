# Data Analyst Learning Summary

> Goal: entry-level job in 6 months, 1 hour/day. Main tools: Python + VS Code.

## Phase 0 - Setup ✅ Done
- **Core:** A Data Analyst answers "what happened and why" through: ask → prepare → process → analyze → share → act.
- **Roles:** Analyst = use existing data. Scientist = build predictions with machine learning. Engineer = build pipelines so data flows cleanly every day.
- **Setup:** VS Code + Python + `pandas numpy matplotlib seaborn` + GitHub as showcase.
- **Result:** Tidy `data-analyst-portfolio` repo, notebooks re-runnable top to bottom.

## Phase 1 - Python for Data ✅ Done
- **Module 1 - Python for data:** `list` = receipt list, `dict` = one receipt, `list of dict` = proto-table. Daily tools: loop + if (filter), function (reusable), list comprehension (one-line loop).
- **Module 2 - NumPy:** `array` = one numeric Excel column. Vectorized ops, no loops. Keys: boolean masking `arr[arr > x]`, `sum(axis=0)` down columns, `axis=1` across rows. Always check `shape` and `dtype` on error.
- **Module 3 - Pandas basics:** `DataFrame` = a real sheet. Mandatory flow: `read_csv` → `shape/info/head` → filter `df[cond]` → `sort_values`. Use `.copy()` before adding columns.
- **Module 4 - Advanced pandas:** `groupby` = recap per category (don't forget `reset_index`). `merge` = join two tables on keys (check duplicates first). `pivot_table` = Excel-style cross-tab, fill gaps with `fill_value=0`.
- **Dataset:** `data/tips.csv` (244 restaurant transactions).

## Phase 2 - Data Cleaning ✅ Done
- **Core:** Real data is dirty. Handle missing values, duplicates, wrong types (dates as text), outliers, messy text (spaces, caps).
- **Result:** Analysis-ready dataset + `cleaning log`: "what changed and why" for managers.
- **Method:** Median for skewed numerics, mode for categories, flag (don't drop) outliers, `to_datetime(coerce)` for dates, `strip-lower-map` for strings. Log format: WHAT | HOW MANY | WHY.

## Phase 3 - Statistics ✅ Done
- **Module 1 - Descriptive:** Mean (outlier-sensitive), median (robust), mode (categories), std + quartiles, skew. Key finding: one 500 bill moved the mean +3.97 while the median (20.81) never moved.
- **Module 2 - Correlation, sampling, CI:** Meaningful r=0.67 (bill vs tip), trivial r=0.99 excluded (derived column). Sampling with `random_state`. CI95% = mean ± 1.96·SE; bigger n → narrower.
- **Module 3 - Hypothesis testing:** Welch t-test (Weekend pays ~3.7 more, p=0.004), tip% no significant difference (p=0.649), chi-square day vs time (p~1e-46, Sat/Sun = Dinner only). Segment comparison noted as observational, not causal A/B.

## Phase 4 - EDA & Visualization ⏳ In progress
- **Core:** Stories from data, not pretty charts. Patterns: univariate (distributions), bivariate (bill vs tip), multivariate (hue/segments).
- **Rules:** Chart answers the question (bar = compare, line = trend, hist/box = spread, scatter = relationship). Median bars for skewed data. Every portfolio chart: insight title + numbers + 1 action.
- **Tools:** Matplotlib + Seaborn, figures saved to `04-python/grafik/`.

## Phase 5 - SQL ⏳
- **Core:** Query databases. Order: SELECT-WHERE-GROUP BY-HAVING → JOIN-subquery-CTE → window functions (ranking, running totals).
- **Practice:** SQLite / BigQuery sandbox + SQL from Python.

## Phase 6 - BI Tools & Sheets ⏳
- **Core:** Dashboards that answer business questions. Google Sheets: XLOOKUP, IF, pivot tables. Looker Studio: free interactive dashboards. Intro to Power BI / Tableau for job listings.
- **Result:** 1 dashboard + 1 Sheets report.

## Phase 7 - Bonus (Optional) ⏳
- **Core:** Plus points: simple regression/classification with scikit-learn, Python report automation (e.g. weekly recap).

## Phase 8 - Portfolio & Career ⏳
- **Core:** 3 leveled projects: 1) sales analysis, 2) customer behavior, 3) business dashboard. Each: clear README + re-runnable notebook + 1-2 action insights.
- **Plus:** Data Analyst CV, case-study drills, SQL + Indonesia case interviews.

---
*Updated after each module. Last: Phase 4 Module 2 done.*
