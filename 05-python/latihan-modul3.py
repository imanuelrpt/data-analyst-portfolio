"""Window function SQL (SQLite >= 3.25) pada tips.db."""

import sqlite3
from pathlib import Path

import pandas as pd

CANDIDATE_PATHS = [
    Path("data/tips.db"),
    Path("../data/tips.db"),
    Path(__file__).parent / "tips.db",
]
TOP_PER_DAY = 2
TOP_GLOBAL = 6
TOP_DIFF = 5
CUMULATIVE_TARGET_PCT = 50

# ---------------------------------------------------------------- Task 1
QUERY_TOP_TIP_PER_DAY = """
SELECT day, tip, total_bill, rn
FROM (
    SELECT day, tip, total_bill,
           ROW_NUMBER() OVER (PARTITION BY day ORDER BY tip DESC, total_bill DESC, rowid) AS rn
    FROM tips
)
WHERE rn <= :top_n
ORDER BY day, rn
"""

# ---------------------------------------------------------------- Task 2
QUERY_RANKS = """
SELECT total_bayar,
       RANK()       OVER (ORDER BY total_bayar DESC) AS peringkat_rank,
       DENSE_RANK() OVER (ORDER BY total_bayar DESC) AS peringkat_dense
FROM tips
ORDER BY total_bayar DESC, rowid
LIMIT :top_n
"""
QUERY_RANKS_ALL = QUERY_RANKS.replace("LIMIT :top_n", "")
# Komentar: di 6 teratas tidak ada nilai kembar sehingga keduanya sama; beda muncul saat ada nilai kembar: RANK melompat nomor setelah seri
# (1,2,2,4), DENSE_RANK tidak melompat (1,2,2,3).

# ---------------------------------------------------------------- Task 3
QUERY_RUNNING_TOTAL = """
WITH total AS (
    SELECT SUM(total_bayar) AS omzet FROM tips
),
ordered AS (
    SELECT total_bayar,
           ROW_NUMBER() OVER (ORDER BY total_bayar DESC, rowid) AS baris,
           SUM(total_bayar) OVER (ORDER BY total_bayar DESC, rowid
                                  ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS kumulatif
    FROM tips
)
SELECT o.baris, o.total_bayar, ROUND(o.kumulatif, 2) AS kumulatif,
       ROUND(o.kumulatif * 100.0 / t.omzet, 2)       AS persen_kumulatif
FROM ordered o CROSS JOIN total t
ORDER BY o.baris
"""

# ---------------------------------------------------------------- Task 4
QUERY_DIFF_FROM_DAY_AVG = """
WITH diffs AS (
    SELECT day, tip,
           tip - AVG(tip) OVER (PARTITION BY day) AS selisih
    FROM tips
)
SELECT day, tip, ROUND(selisih, 2) AS selisih
FROM diffs
WHERE selisih > 0
ORDER BY selisih DESC
LIMIT :top_n
"""

QUERY_SHARE_ABOVE_AVG = """
WITH diffs AS (
    SELECT day, tip - AVG(tip) OVER (PARTITION BY day) AS selisih
    FROM tips
)
SELECT day,
       COUNT(*)                                    AS n,
       SUM(selisih > 0)                            AS di_atas_rata_rata,
       ROUND(AVG(selisih > 0) * 100, 1)            AS persen_di_atas
FROM diffs
GROUP BY day
ORDER BY persen_di_atas DESC
"""


def find_data_path(candidates: list[Path]) -> Path:
    """Kembalikan path pertama yang ada, atau error jika tidak ada satupun."""
    for path in candidates:
        if path.exists():
            return path
    raise FileNotFoundError(f"tips.db tidak ditemukan di: {candidates}")


def run_query(connection: sqlite3.Connection, query: str, params: dict | None = None) -> pd.DataFrame:
    """Jalankan query dengan parameter terikat dan kembalikan DataFrame."""
    return pd.read_sql_query(query, connection, params=params)


def main() -> None:
    with sqlite3.connect(find_data_path(CANDIDATE_PATHS)) as connection:
        top_tips = run_query(connection, QUERY_TOP_TIP_PER_DAY, {"top_n": TOP_PER_DAY})
        print(f"1) Top {TOP_PER_DAY} tip per day\n", top_tips, f"\n   Total baris: {len(top_tips)}")

        print("\n2) RANK vs DENSE_RANK\n", run_query(connection, QUERY_RANKS, {"top_n": TOP_GLOBAL}))
        all_ranks = run_query(connection, QUERY_RANKS_ALL)
        first_gap = all_ranks.index[all_ranks["peringkat_rank"] != all_ranks["peringkat_dense"]][0]
        print("   Beda pertama muncul di sini (nilai kembar sebelumnya):\n",
              all_ranks.iloc[first_gap - 3:first_gap + 2])

        running = run_query(connection, QUERY_RUNNING_TOTAL)
        crossing = running[running["persen_kumulatif"] >= CUMULATIVE_TARGET_PCT].iloc[0]
        print("\n3) Running total (5 baris pertama)\n", running.head(5))
        print(f"   Tembus {CUMULATIVE_TARGET_PCT}% di baris ke-{int(crossing['baris'])} "
              f"dari {len(running)} ({crossing['persen_kumulatif']:.2f}%)")

        print("\n4) 5 selisih tip positif terbesar vs rata-rata harinya\n",
              run_query(connection, QUERY_DIFF_FROM_DAY_AVG, {"top_n": TOP_DIFF}))
        print("\n   Porsi transaksi di atas rata-rata harinya\n", run_query(connection, QUERY_SHARE_ABOVE_AVG))


if __name__ == "__main__":
    main()
