"""Latihan Modul 2 Fase 5: JOIN, subquery, CTE pada tips.db (SQLite)."""

from pathlib import Path

import pandas as pd
import sqlite3

CANDIDATE_CSV = [
    Path("data/clean_tips.csv"),
    Path("../data/clean_tips.csv"),
    Path(__file__).parent / "clean_tips.csv",
]
MIN_HIGH = "High"

# ---------------------------------------------------------------- Setup
def find_csv(candidates: list[Path]) -> Path:
    """Kembalikan path CSV pertama yang ada."""
    for path in candidates:
        if path.exists():
            return path
    raise FileNotFoundError(f"clean_tips.csv tidak ditemukan di: {candidates}")


def ensure_db() -> sqlite3.Connection:
    """Buka tips.db (di folder yang sama dengan CSV); buat ulang tabel bila belum ada."""
    csv = find_csv(CANDIDATE_CSV)
    db = csv.parent / "tips.db"
    db.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(db)
    # Tabel tips: dari CSV bersih (buang 2 baris error input), pola modul-modul sebelumnya.
    df = pd.read_csv(csv)
    df = df[(df["tip"] >= 0) & (df["total_bill"] < 100)]
    df.to_sql("tips", con, if_exists="replace", index=False)
    # Tabel kamus hari: day = kunci, wajib unik (dicek di Soal 1 via HAVING).
    day_info = pd.DataFrame({
        "day": ["Thur", "Fri", "Sat", "Sun"],
        "hari_id": ["Kamis", "Jumat", "Sabtu", "Minggu"],
        "jenis": ["Weekday", "Weekday", "Weekend", "Weekend"],
    })
    day_info.to_sql("day_info", con, if_exists="replace", index=False)
    return con


def run(con: sqlite3.Connection, query: str, params: dict | None = None) -> pd.DataFrame:
    """Jalankan query dengan parameter terikat, kembalikan DataFrame."""
    return pd.read_sql_query(query, con, params=params)


# ---------------------------------------------------------------- Soal 1: LEFT JOIN + cek NULL
QUERY_JOIN_5 = """
SELECT d.hari_id, t.total_bayar, t.tip
FROM tips t
LEFT JOIN day_info d ON t.day = d.day
LIMIT 5
"""
QUERY_NULL_CHECK = """
SELECT COUNT(*) AS n_null
FROM tips t
LEFT JOIN day_info d ON t.day = d.day
WHERE d.hari_id IS NULL
"""
QUERY_KEY_CHECK = """
SELECT day, COUNT(*) AS n FROM day_info GROUP BY day HAVING COUNT(*) > 1
"""
# Komentar: LEFT JOIN benar karena semua struk harus tetap ada walau kamusnya hilang;
# kunci day_info unik (cek HAVING kosong) jadi COUNT tidak kembung (tetap 241).

# ---------------------------------------------------------------- Soal 2: subquery di atas rata-rata High
QUERY_AVG_HIGH = "SELECT AVG(total_bayar) AS v FROM tips WHERE bill_level = :lvl"
QUERY_ABOVE_HIGH = """
SELECT day, total_bayar FROM tips
WHERE bill_level = :lvl AND total_bayar > (SELECT AVG(total_bayar) FROM tips WHERE bill_level = :lvl)
ORDER BY total_bayar DESC
"""

# ---------------------------------------------------------------- Soal 3: CTE base + rekap per jenis
QUERY_CTE_JENIS = """
WITH base AS (
    SELECT t.total_bayar, d.jenis
    FROM tips t LEFT JOIN day_info d ON t.day = d.day
),
rekap AS (
    SELECT jenis, COUNT(*) AS n, SUM(total_bayar) AS omzet
    FROM base GROUP BY jenis
)
SELECT jenis, n, ROUND(omzet, 2) AS omzet,
       ROUND(omzet * 100.0 / (SELECT SUM(omzet) FROM rekap), 1) AS share_pct
FROM rekap ORDER BY omzet DESC
"""
# Komentar: CTE base (join) dipisah dari rekap (agregat) agar tiap langkah bisa dites 1-1;
# share Weekend harusnya ~70.4% seperti temuan pandas Fase 2-4.

# ---------------------------------------------------------------- Soal 4: CTE 2 tingkat, hari di atas rata-rata
QUERY_CTE_DAY = """
WITH avg_day AS (
    SELECT day, AVG(tip_pct) AS avg_tip FROM tips GROUP BY day
),
overall AS (
    SELECT AVG(tip_pct) AS v FROM tips
)
SELECT a.day, ROUND(a.avg_tip, 2) AS avg_tip,
       ROUND(a.avg_tip - o.v, 2) AS selisih
FROM avg_day a, overall o
WHERE a.avg_tip > o.v
ORDER BY selisih DESC
"""
# Keputusan bisnis: hari di atas rata-rata dipertahankan strateginya (staf + slot promo),
# hari di bawah dievaluasi (cek n kecil seperti Fri=19 sebelum simpulkan).


def main() -> None:
    with ensure_db() as con:
        print("Kunci day_info duplikat (harusnya kosong):\n", run(con, QUERY_KEY_CHECK))
        print("\n1) JOIN 5 baris\n", run(con, QUERY_JOIN_5))
        print("   hari_id NULL:", run(con, QUERY_NULL_CHECK).iloc[0, 0], "(harusnya 0)")

        avg_high = run(con, QUERY_AVG_HIGH, {"lvl": MIN_HIGH}).iloc[0, 0]
        above = run(con, QUERY_ABOVE_HIGH, {"lvl": MIN_HIGH})
        print(f"\n2) Rata-rata High = {avg_high:.2f}; di atasnya: {len(above)} transaksi")
        print(above.head(3).to_string())

        print("\n3) CTE per jenis\n", run(con, QUERY_CTE_JENIS).to_string())

        print("\n4) Hari di atas rata-rata tip_pct\n", run(con, QUERY_CTE_DAY).to_string())


if __name__ == "__main__":
    main()
