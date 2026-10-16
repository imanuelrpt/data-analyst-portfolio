"""Query SQL (SQLite) pada tips.db: filter, rekap, HAVING, dan segmentasi."""

import sqlite3
from pathlib import Path

import pandas as pd

CANDIDATE_PATHS = [
    Path("data/tips.db"),
    Path("../data/tips.db"),
    Path(__file__).parent / "tips.db",
]
MIN_BILL = 20
MIN_TRANSACTIONS = 20
TOP_N = 5

# ---------------------------------------------------------------- Task 1
QUERY_TOP_LUNCH = """
SELECT day, total_bill, tip
FROM tips
WHERE time = 'Lunch' AND total_bill > :min_bill
ORDER BY tip DESC, total_bill DESC
LIMIT :top_n
"""

# ---------------------------------------------------------------- Task 2
QUERY_BY_TIME = """
SELECT time,
       COUNT(*)                     AS n,
       ROUND(AVG(total_bayar), 2)   AS rata_rata_total_bayar,
       ROUND(SUM(total_bayar), 2)   AS total_omzet
FROM tips
GROUP BY time
ORDER BY total_omzet DESC
"""

# ---------------------------------------------------------------- Task 3
QUERY_BY_DAY = """
SELECT day,
       COUNT(*)                 AS n,
       ROUND(AVG(tip_pct), 2)   AS rata_rata_tip_pct
FROM tips
GROUP BY day
HAVING COUNT(*) >= :min_n
ORDER BY rata_rata_tip_pct DESC
"""
# Komentar: Fri hilang karena hanya 19 transaksi (< 20), HAVING menyaring grup SETELAH GROUP BY,
# sedangkan WHERE menyaring baris sebelum dikelompokkan.
# Catatan: AVG(tip_pct) di sini sensitif skew 3.38 (Sun 16.85 vs median pandas 16.17);
# untuk klaim "paling royal", bandingkan dengan median di Modul 4 Fase 4.

# ---------------------------------------------------------------- Task 4
QUERY_BY_SEGMENT = """
SELECT CASE is_weekend WHEN 1 THEN 'Weekend' ELSE 'Weekday' END AS grup,
       bill_level,
       COUNT(*)                     AS n,
       ROUND(SUM(total_bayar), 2)   AS total_omzet,
       ROUND(AVG(tip_pct), 2)       AS rata_rata_tip_pct
FROM tips
GROUP BY is_weekend, bill_level
ORDER BY total_omzet DESC
"""

QUERY_TOTAL_OMZET = "SELECT SUM(total_bayar) FROM tips"
QUERY_WEEKEND_OMZET = "SELECT SUM(total_bayar) FROM tips WHERE is_weekend = 1"


def find_data_path(candidates: list[Path]) -> Path:
    """Kembalikan path pertama yang ada, atau error jika tidak ada satupun."""
    for path in candidates:
        if path.exists():
            return path
    raise FileNotFoundError(f"tips.db tidak ditemukan di: {candidates}")


def run_query(connection: sqlite3.Connection, query: str, params: dict | None = None) -> pd.DataFrame:
    """Jalankan query (dengan parameter terikat, bukan f-string) dan kembalikan DataFrame."""
    return pd.read_sql_query(query, connection, params=params)


def main() -> None:
    path = find_data_path(CANDIDATE_PATHS)
    with sqlite3.connect(path) as connection:
        print("1) Top 5 Lunch (total_bill > 20) by tip\n",
              run_query(connection, QUERY_TOP_LUNCH, {"min_bill": MIN_BILL, "top_n": TOP_N}))
        print("\n2) Rekap per time\n", run_query(connection, QUERY_BY_TIME))
        print("\n3) Rekap per day (n >= 20)\n",
              run_query(connection, QUERY_BY_DAY, {"min_n": MIN_TRANSACTIONS}))

        segments = run_query(connection, QUERY_BY_SEGMENT)
        print("\n4) Rekap is_weekend x bill_level\n", segments)
        total = connection.execute(QUERY_TOTAL_OMZET).fetchone()[0]
        weekend = connection.execute(QUERY_WEEKEND_OMZET).fetchone()[0]
        top = segments.iloc[0]
        print(f"   Terbesar: {top['grup']} {top['bill_level']} ({top['total_omzet'] / total * 100:.1f}% omzet) | "
              f"Weekend total {weekend / total * 100:.1f}%")


if __name__ == "__main__":
    main()