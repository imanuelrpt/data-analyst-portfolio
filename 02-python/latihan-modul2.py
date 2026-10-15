"""Tahap 2 pembersihan dirty_tips.csv: outlier IQR, tanggal, dan string kategori."""

from pathlib import Path

import pandas as pd

CANDIDATE_PATHS = [
    Path("data/dirty_tips2.csv"),
    Path("../data/dirty_tips2.csv"),
    Path(__file__).parent / "dirty_tips2.csv",
]
IQR_MULTIPLIER = 1.5

SEX_ALIASES = {
    "Male": {"male", "m", "l", "pria", "laki-laki", "laki laki"},
    "Female": {"female", "f", "p", "wanita", "perempuan"},
}
DAY_ALIASES = {
    "Thur": {"thur", "thu", "thurs", "thursday", "kamis"},
    "Fri": {"fri", "friday", "jumat", "jum'at"},
    "Sat": {"sat", "saturday", "sabtu"},
    "Sun": {"sun", "sunday", "minggu", "ahad"},
}


def find_data_path(candidates: list[Path]) -> Path:
    """Kembalikan path pertama yang ada, atau error jika tidak ada satupun."""
    for path in candidates:
        if path.exists():
            return path
    raise FileNotFoundError(f"dirty_tips2.csv tidak ditemukan di: {candidates}")


def require_columns(df: pd.DataFrame, columns: list[str]) -> None:
    """Hentikan dengan pesan jelas jika kolom yang dibutuhkan tidak ada."""
    missing = [col for col in columns if col not in df.columns]
    if missing:
        raise ValueError(f"Kolom wajib tidak ada di data: {missing}")


# ---------------------------------------------------------------- Task 1
def iqr_bounds(values: pd.Series, k: float = IQR_MULTIPLIER) -> tuple[float, float]:
    """Batas bawah dan atas outlier: Q1 - k*IQR dan Q3 + k*IQR."""
    q1, q3 = values.quantile([0.25, 0.75])
    iqr = q3 - q1
    return q1 - k * iqr, q3 + k * iqr


def outlier_mask(values: pd.Series, lower: float, upper: float) -> pd.Series:
    """True untuk nilai di luar [lower, upper]."""
    return ~values.between(lower, upper)


# ---------------------------------------------------------------- Task 2
def parse_dates(raw: pd.Series) -> pd.Series:
    """Parse ke datetime; yang tidak bisa dibaca jadi NaT (errors='coerce')."""
    return pd.to_datetime(raw, errors="coerce", format="mixed")


# ---------------------------------------------------------------- Task 3
def _invert_aliases(aliases: dict[str, set[str]]) -> dict[str, str]:
    """Ubah {standar: {varian}} menjadi {varian: standar}."""
    return {variant: standard for standard, variants in aliases.items() for variant in variants}


def standardize_category(raw: pd.Series, aliases: dict[str, set[str]]) -> pd.Series:
    """Samakan penulisan kategori; nilai yang tidak dikenali jadi NA."""
    normalized = raw.astype("string").str.strip().str.lower().str.rstrip(".")
    return normalized.map(_invert_aliases(aliases)).astype("string")


def standardize_strings(df: pd.DataFrame) -> pd.DataFrame:
    """Kembalikan salinan df dengan sex dan day sudah standar."""
    df = df.copy()
    df["sex"] = standardize_category(df["sex"], SEX_ALIASES)
    df["day"] = standardize_category(df["day"], DAY_ALIASES)
    return df


def count_string_fixes(raw: pd.Series, cleaned: pd.Series) -> tuple[int, int]:
    """Hitung (jumlah nilai dirapikan, jumlah nilai tidak dikenali)."""
    raw = raw.astype("string")
    unknown = int((raw.notna() & cleaned.isna()).sum())
    fixed = int((raw.notna() & cleaned.notna() & (raw != cleaned)).sum())
    return fixed, unknown


# ---------------------------------------------------------------- Task 4
def clean_dirty2(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    """Flag outlier, bersihkan tanggal & string. Kembalikan (df_bersih, log)."""
    require_columns(df, ["total_bill", "sex", "day", "tanggal"])
    df = df.copy()
    log = [f"Awal: {df.shape[0]} baris, {df.shape[1]} kolom"]

    # Outlier: hanya di-flag, tidak di-drop (bisa jadi transaksi besar yang sah).
    lower, upper = iqr_bounds(df["total_bill"])
    df["is_outlier_total_bill"] = outlier_mask(df["total_bill"], lower, upper)
    log.append(
        f"Outlier total_bill: batas [{lower:.2f}, {upper:.2f}], "
        f"{df['is_outlier_total_bill'].sum()} baris di-flag (tidak di-drop)"
    )

    # Keputusan: tanggal rusak TIDAK membuang baris (total_bill & tip-nya masih valid);
    # baris itu dipertahankan dengan tahun/bulan kosong dan diberi flag tanggal_rusak.
    raw_missing = df["tanggal"].isna()
    df["tanggal"] = parse_dates(df["tanggal"])
    df["tanggal_rusak"] = df["tanggal"].isna() & ~raw_missing
    df["tahun"] = df["tanggal"].dt.year.astype("Int64")
    df["bulan"] = df["tanggal"].dt.month.astype("Int64")
    log.append(
        f"Tanggal: {df['tanggal'].notna().sum()} terbaca, {df['tanggal'].isna().sum()} NaT "
        f"({raw_missing.sum()} kosong asli, {df['tanggal_rusak'].sum()} format rusak)"
    )
    log.append("Keputusan: baris tanggal rusak dipertahankan, tahun/bulan = NA, diberi flag tanggal_rusak")

    for column, aliases in (("sex", SEX_ALIASES), ("day", DAY_ALIASES)):
        cleaned = standardize_category(df[column], aliases)
        fixed, unknown = count_string_fixes(df[column], cleaned)
        df[column] = cleaned
        log.append(f"{column}: {fixed} nilai dirapikan, {unknown} tidak dikenali (jadi NA)")

    undocumented = int((df["tanggal"].isna() & ~raw_missing & ~df["tanggal_rusak"]).sum())
    remaining = int(df["tanggal"].isna().sum())
    log.append(
        f"Akhir: {df.shape[0]} baris, {df.shape[1]} kolom | "
        f"{undocumented} NaT tak terdokumentasi (sisa NaT: {remaining}, semua tercatat)"
    )
    return df, log


def main() -> None:
    df = pd.read_csv(find_data_path(CANDIDATE_PATHS))
    print(df.shape)

    lower, upper = iqr_bounds(df["total_bill"])
    outliers = df[outlier_mask(df["total_bill"], lower, upper)]
    print(f"\n1) Batas IQR total_bill: [{lower:.2f}, {upper:.2f}]")
    print(outliers)
    print(f"   Jumlah outlier: {len(outliers)}")

    print("\n3) value_counts setelah dibersihkan")
    cleaned = standardize_strings(df)
    print(cleaned["sex"].value_counts(dropna=False))
    print(cleaned["day"].value_counts(dropna=False))

    if "tanggal" not in df.columns:
        print("\nKolom 'tanggal' tidak ada di file ini, jadi task 2 dan clean_dirty2 dilewati.")
        return

    df_clean, log = clean_dirty2(df)
    print("\n4) Log pembersihan")
    for step in log:
        print(" -", step)


if __name__ == "__main__":
    main()
