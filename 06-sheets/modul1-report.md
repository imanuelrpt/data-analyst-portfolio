# Phase 6 - Module 1: Google Sheets (Formulas + Pivot Table)

Dataset: `data/clean_tips.csv` imported into Google Sheets (`tips-analysis`).
Sheet has 244 rows (1 header + 243 data rows, including 2 flagged error rows).

## 1. Core formulas practiced

| Purpose | Formula | Raw result (243 rows) | Clean result (241 rows) |
|---|---|---|---|
| Total revenue | `=SUM(E2:E244)` | 6020.70 | 5514.35 |
| Average tip % | `=AVERAGE(F2:F244)` | 15.79 | ~15.8 |
| Weekend transactions | `=COUNTIF(G2:G244, TRUE)` | 163 | 161 |
| Weekend + High revenue | `=SUMIFS(E2:E244, G2:G244, TRUE, H2:H244, "High")` | - | 2123 (Sat/Sun High) |
| Saturday avg tip % | `=AVERAGEIFS(F2:F244, C2:C244, "Sat")` | - | ~15.3 |
| Row label | `=IF(F2>20, "royal", "normal")` | - | 39 royal = 16.2% |
| Lookup example | `=XLOOKUP("Sat", C2:C244, A2:A244)` | - | (modern replacement for VLOOKUP) |

## 2. Pivot table: day (rows) x time (columns), SUM of total_bayar

Clean version (241 rows, 2 error rows removed):

```
        Dinner   Lunch
Thur     21.78 1231.38
Fri     271.24  106.60
Sat    2063.31    0.00
Sun    1820.04    0.00
```

Raw version (243 rows) shows Sat Dinner = 2569.66 because it still contains the
flagged 500 bill and the -5 tip.

## 3. Cross-check with Python (pandas)

Same numbers reproduced in pandas, proving Sheets and Python agree:

```python
df = pd.read_csv("data/clean_tips.csv")
clean = df[(df["tip"] >= 0) & (df["total_bill"] < 100)]   # 241 rows
clean["total_bayar"].sum()                                # 5514.35
(clean["is_weekend"] == True).sum()                       # 161
(clean["tip_pct"] > 20).mean()                            # 0.162 -> 16.2% royal
```

## 4. Findings and business action

- **Sat Dinner is the revenue champion** (2063.31 on the clean version) - the single
  highest day x time cell by far.
- Recommendation: add a senior server + extra kitchen staff on Saturday dinner to
  protect service speed during the peak.
- **Honest reporting note:** always state which version (243 flagged vs 241 clean) a
  number comes from, because the 500 outlier moves Sat Dinner by ~506.

## Key lessons

1. Import a CSV with the correct separator (Comma), otherwise every row lands in one column.
2. Use ranges starting at row 2 so `AVERAGE`/`SUM` do not count header text.
3. `COUNTIF(..., TRUE)` on a boolean column counts the TRUE rows directly.
4. A number must match across tools (Sheets = pandas = SQL) or one of them is wrong.
5. `XLOOKUP` is the modern, flexible replacement for `VLOOKUP`.
