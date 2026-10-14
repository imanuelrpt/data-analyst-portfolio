"""Membersihkan dirty_tips.csv: missing value, duplikat, dan tipe data size."""

from pathlib import Path

import pandas as pd

CANDIDATE_PATHS = [
    Path("data/dirty_tips.csv"),
    Path("../data/dirty_tips.csv"),
    Path(__file__).parent / "dirty_tips.csv",
]
WORD_TO_NUMBER = {"satu": 1, "dua": 2, "tiga": 3, "empat": 4, "lima": 5, "enam": 6}


def find_data_path(candidates: list[Path]) -> Path:
    """Kembalikan path pertama yang ada, atau error jika tidak ada satupun."""
    for path in candidates:
        if path.exists():
            return path
    raise FileNotFoundError(f"dirty_tips.csv tidak ditemukan di: {candidates}")


# ---------------------------------------------------------------- Task 1
def missing_percent(df: pd.DataFrame) -> pd.Series:
    """Persentase missing value per kolom."""
    return (df.isna().mean() * 100).round(2)


def duplicate_count(df: pd.DataFrame) -> int:
    """Jumlah baris duplikat (baris ke-2 dan seterusnya yang identik)."""
    return int(df.duplicated().sum())


# ---------------------------------------------------------------- Task 3 (bagian size)
def size_to_int(size: pd.Series) -> pd.Series:
    """Ubah size ke int; kata angka ("dua") dikonversi, nilai hilang diisi median."""
    cleaned = size.astype("string").str.strip().str.lower().replace(WORD_TO_NUMBER)
    numeric = pd.to_numeric(cleaned, errors="coerce")  # NaN/teks aneh jadi NaN, bukan error
    return numeric.fillna(numeric.median()).round().astype(int)


# ---------------------------------------------------------------- Task 4
def clean_dirty(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    """Bersihkan df, kembalikan (df_bersih, log langkah yang dilakukan)."""
    df = df.copy()
    log = [f"Awal: {df.shape[0]} baris, {df.shape[1]} kolom"]

    # size dibersihkan lebih dulu agar duplikat yang tersamarkan ('dua' vs 2) ikut terdeteksi
    df["size"] = size_to_int(df["size"])
    log.append("size diubah ke int (kata angka dikonversi)")

    n_dup = duplicate_count(df)
    df = df.drop_duplicates().reset_index(drop=True)
    log.append(f"Drop {n_dup} baris duplikat")

    # median & modus dihitung setelah duplikat dibuang agar tidak bias
    median_tip = df["tip"].median()
    mode_day = df["day"].mode()[0]
    n_tip, n_day = df["tip"].isna().sum(), df["day"].isna().sum()
    # tip miring kanan (ada nilai besar), mean ketarik naik, median lebih aman.
    df["tip"] = df["tip"].fillna(median_tip)
    df["day"] = df["day"].fillna(mode_day)
    log.append(f"Isi {n_tip} tip kosong dengan median ({median_tip:.2f})")
    log.append(f"Isi {n_day} day kosong dengan modus ('{mode_day}')")

    log.append("cek: tips.csv asli sudah ada 1 duplikat alami")
    log.append(f"Akhir: {df.shape[0]} baris, {df.shape[1]} kolom")
    return df, log


def main() -> None:
    path = find_data_path(CANDIDATE_PATHS)
    print(f"pakai: {path}")
    df = pd.read_csv(path)
    print(df.shape)

    print("\n1) % missing per kolom\n", missing_percent(df))
    print(f"   Duplikat: {duplicate_count(df)} baris")

    df_clean, log = clean_dirty(df)
    print("\n4) Log pembersihan")
    for step in log:
        print(" -", step)

    print("\nCek hasil:")
    print(df_clean.isna().sum().sum(), "missing |", df_clean.duplicated().sum(), "duplikat")
    print(df_clean.dtypes)


if __name__ == "__main__":
    main()
