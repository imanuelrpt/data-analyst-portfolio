"""Latihan Modul 4 (Fase 5): roundtrip SQL x Python pada tips.db."""

import sqlite3
from pathlib import Path

import pandas as pd

CSV_PATH = Path("data/clean_tips.csv") if Path("data/clean_tips.csv").exists() else Path("../data/clean_tips.csv")
DB_PATH = CSV_PATH.parent / "tips.db"
TOP_PER_DAY = 3
EXPECTED_DAYS = 4

# ---------------------------------------------------------------- Task 1
QUERY_BY_TIME = """
SELECT time,
       COUNT(*)         AS n,
       SUM(total_bayar) AS omzet,
       AVG(total_bayar) AS avg_bill
FROM tips
GROUP BY time
"""


def build_rekap_time(connection: sqlite3.Connection) -> pd.DataFrame:
    """Agregat di SQL, kolom turunan (share omzet %) di pandas, simpan ke rekap_time, lalu baca balik."""
    df = pd.read_sql(QUERY_BY_TIME, connection)
    df["share"] = (df["omzet"] / df["omzet"].sum() * 100).round(2)
    df.to_sql("rekap_time", connection, if_exists="replace", index=False)
    return pd.read_sql("SELECT * FROM rekap_time ORDER BY omzet DESC", connection)


# ---------------------------------------------------------------- Task 2
QUERY_TOP_N = """
SELECT day, time, total_bill, tip, total_bayar
FROM tips
ORDER BY total_bayar DESC, rowid
LIMIT :n
"""
# Komentar: binding (:n) lebih baik dari f-string karena nilai dikirim sebagai DATA terpisah dari
# teks query, sehingga aman dari SQL injection dan query yang sama bisa dipakai ulang untuk n berbeda.


def top_n_total_bayar(connection: sqlite3.Connection, n: int) -> pd.DataFrame:
    """Top-N total_bayar dengan parameter terikat."""
    return pd.read_sql(QUERY_TOP_N, connection, params={"n": n})


# ---------------------------------------------------------------- Task 3
QUERY_TOP_TIP_PER_DAY = """
WITH day_total AS (
    SELECT day, SUM(tip) AS total_tip_hari
    FROM tips
    GROUP BY day
),
ranked AS (
    SELECT t.day, t.tip, t.total_bill,
           ROW_NUMBER() OVER (PARTITION BY t.day
                              ORDER BY t.tip DESC, t.total_bill DESC, t.rowid) AS rn,
           SUM(t.tip) OVER (PARTITION BY t.day
                            ORDER BY t.tip DESC, t.total_bill DESC, t.rowid
                            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS tip_kumulatif
    FROM tips t
)
SELECT r.day, r.rn, r.tip, r.total_bill, ROUND(r.tip_kumulatif, 2) AS tip_kumulatif,
       ROUND(r.tip_kumulatif * 100.0 / d.total_tip_hari, 2) AS running_share_pct
FROM ranked r
JOIN day_total d ON d.day = r.day
WHERE r.rn <= :top_n
ORDER BY r.day, r.rn
"""


def top_tip_per_day(connection: sqlite3.Connection, top_n: int) -> pd.DataFrame:
    """Top-N tip per day + share kumulatif terhadap total tip hari itu."""
    return pd.read_sql(QUERY_TOP_TIP_PER_DAY, connection, params={"top_n": top_n})


def main() -> None:
    print(f"pakai: {CSV_PATH} -> {DB_PATH}")
    with sqlite3.connect(DB_PATH) as connection:
        print("\n1) rekap_time (share = % omzet)\n", build_rekap_time(connection))

        for n in (3, 10):
            print(f"\n2) Top {n} total_bayar\n", top_n_total_bayar(connection, n))

        result = top_tip_per_day(connection, TOP_PER_DAY)
        print(f"\n3) Top {TOP_PER_DAY} tip per day\n", result)
        expected = TOP_PER_DAY * EXPECTED_DAYS
        print(f"   Verifikasi: {len(result)} baris (harusnya {expected}) -> "
              f"{'OK' if len(result) == expected else 'TIDAK COCOK'}")


if __name__ == "__main__":
    main()
