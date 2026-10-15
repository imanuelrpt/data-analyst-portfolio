"""Pipeline lengkap dirty_tips2.csv: bersihkan, buat fitur, simpan clean_tips.csv."""

from pathlib import Path

import pandas as pd

CANDIDATE_PATHS = [
    Path("data/dirty_tips2.csv"),
    Path("../data/dirty_tips2.csv"),
    Path(__file__).parent / "dirty_tips2.csv",
]
OUTPUT_NAME = "clean_tips.csv"
IQR_MULTIPLIER = 1.5
WEEKEND_DAYS = {"Sat", "Sun"}
BILL_LEVELS = ["Low", "Mid", "High"]

WORD_TO_NUMBER = {"satu": 1, "dua": 2, "tiga": 3, "empat": 4, "lima": 5, "enam": 6}
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


def format_log(what: str, how_many: str, why: str) -> str:
    """Satu baris log dengan pola APA | BERAPA | KENAPA."""
    return f"APA: {what} | BERAPA: {how_many} | KENAPA: {why}"


# ------------------------------------------------------------ pembersihan
def size_to_int(size: pd.Series) -> pd.Series:
    """Ubah size ke int; kata angka ("dua") dikonversi, nilai hilang diisi median."""
    cleaned = size.astype("string").str.strip().str.lower().replace(WORD_TO_NUMBER)
    numeric = pd.to_numeric(cleaned, errors="coerce")
    return numeric.fillna(numeric.median()).round().astype(int)


def standardize_category(raw: pd.Series, aliases: dict[str, set[str]]) -> pd.Series:
    """Samakan penulisan kategori; nilai yang tidak dikenali jadi NA."""
    lookup = {v: std for std, variants in aliases.items() for v in variants}
    normalized = raw.astype("string").str.strip().str.lower().str.rstrip(".")
    return normalized.map(lookup).astype("string")


def iqr_bounds(values: pd.Series, k: float = IQR_MULTIPLIER) -> tuple[float, float]:
    """Batas outlier: Q1 - k*IQR dan Q3 + k*IQR."""
    q1, q3 = values.quantile([0.25, 0.75])
    iqr = q3 - q1
    return q1 - k * iqr, q3 + k * iqr


# ------------------------------------------------------------------ fitur
def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """Tambah tip_pct, total_bayar, harga_per_orang. Pembagian dengan 0 jadi NA, bukan inf."""
    df = df.copy()
    safe_bill = df["total_bill"].where(df["total_bill"] > 0)
    safe_size = df["size"].where(df["size"] > 0)
    df["tip_pct"] = df["tip"] / safe_bill * 100
    df["total_bayar"] = df["total_bill"] + df["tip"]
    df["harga_per_orang"] = df["total_bill"] / safe_size  # harga makanan per orang, sebelum tip
    return df


def add_segments(df: pd.DataFrame) -> pd.DataFrame:
    """Tambah is_weekend dan bill_level (qcut 3 kelompok sama besar)."""
    df = df.copy()
    df["is_weekend"] = df["day"].isin(WEEKEND_DAYS)
    df["bill_level"] = pd.qcut(df["total_bill"], q=3, labels=BILL_LEVELS).astype("string")
    return df


# --------------------------------------------------------------- pipeline
def clean_all(path: Path) -> tuple[pd.DataFrame, list[str]]:
    """Baca CSV, bersihkan, buat fitur & segmen. Kembalikan (df_clean, log)."""
    df = pd.read_csv(path)
    log = [format_log("Baca data", f"{df.shape[0]} baris, {df.shape[1]} kolom", f"sumber: {path}")]

    df["size"] = size_to_int(df["size"])
    log.append(format_log("size -> int", "kata angka dikonversi", "size bertipe teks ('dua'), tidak bisa dihitung"))

    for column, aliases in (("sex", SEX_ALIASES), ("day", DAY_ALIASES)):
        cleaned = standardize_category(df[column], aliases)
        unknown = int((df[column].notna() & cleaned.isna()).sum())
        df[column] = cleaned
        log.append(format_log(f"Standarkan {column}", f"{unknown} nilai tak dikenali jadi NA",
                              "ejaan seragam agar groupby tidak terpecah"))

    n_dup = int(df.duplicated().sum())
    df = df.drop_duplicates().reset_index(drop=True)
    log.append(format_log("Drop duplikat", f"{n_dup} baris", "baris kembar menggandakan omzet"))

    median_tip, mode_day = df["tip"].median(), df["day"].mode()[0]
    n_tip, n_day = int(df["tip"].isna().sum()), int(df["day"].isna().sum())
    df["tip"] = df["tip"].fillna(median_tip)
    df["day"] = df["day"].fillna(mode_day)
    log.append(format_log("Isi tip kosong dengan median", f"{n_tip} baris (median {median_tip:.2f})",
                          "tip miring kanan, median tidak ketarik nilai besar"))
    log.append(format_log("Isi day kosong dengan modus", f"{n_day} baris ('{mode_day}')",
                          "day kategori, modus adalah nilai paling wajar"))

    lower, upper = iqr_bounds(df["total_bill"])
    df["is_outlier_total_bill"] = ~df["total_bill"].between(lower, upper)
    log.append(format_log("Flag outlier total_bill (tidak di-drop)",
                          f"{df['is_outlier_total_bill'].sum()} baris di luar [{lower:.2f}, {upper:.2f}]",
                          "transaksi besar bisa sah, cukup ditandai"))

    if "tanggal" in df.columns:
        raw_missing = df["tanggal"].isna()
        df["tanggal"] = pd.to_datetime(df["tanggal"], errors="coerce", format="mixed")
        df["tanggal_rusak"] = df["tanggal"].isna() & ~raw_missing
        df["tahun"] = df["tanggal"].dt.year.astype("Int64")
        df["bulan"] = df["tanggal"].dt.month.astype("Int64")
        log.append(format_log("Parse tanggal (coerce)", f"{int(df['tanggal'].isna().sum())} NaT dipertahankan",
                              "baris tetap valid untuk omzet, NaT diberi flag tanggal_rusak"))
    else:
        log.append(format_log("Parse tanggal", "dilewati", "kolom 'tanggal' tidak ada di file ini"))

    df = add_segments(add_features(df))
    log.append(format_log("Buat fitur tip_pct, total_bayar, harga_per_orang",
                          f"{int(df[['tip_pct', 'total_bayar', 'harga_per_orang']].isna().sum().sum())} NA",
                          "bahan analisis; bagi-0 dijaga jadi NA agar tidak inf"))
    log.append(format_log("Buat is_weekend & bill_level (qcut 3)",
                          f"{int(df['is_weekend'].sum())} baris weekend",
                          "segmentasi pelanggan untuk analisis bisnis"))
    log.append(format_log("Selesai", f"{df.shape[0]} baris, {df.shape[1]} kolom", "data siap dianalisis"))
    return df, log


def save_clean(df: pd.DataFrame, source: Path) -> Path:
    """Simpan df ke clean_tips.csv di folder yang sama dengan file sumber."""
    out_path = source.parent / OUTPUT_NAME
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)
    return out_path


def main() -> None:
    source = find_data_path(CANDIDATE_PATHS)

    # ---------------- Task 1: fitur pada data mentah (size dikonversi dulu agar bisa dibagi)
    raw = pd.read_csv(source)
    raw["size"] = size_to_int(raw["size"])
    features = add_features(raw)[["tip_pct", "total_bayar", "harga_per_orang"]]
    print("1) describe() fitur\n", features.describe().round(2))
    # Komentar (dirty_tips2): ADA minus karena tip -5 salah input -> tip_pct min -48.36%;
    # total_bayar max 501.01 karena bill 500 outlier; tidak ada inf (bagi-0 dijaga jadi NA).
    # tip_pct max ~71% (tip besar di tagihan kecil) layak dicek manual.

    # ---------------- Task 3: pipeline lengkap + simpan
    df_clean, log = clean_all(source)
    print("\n3) Log pembersihan")
    for step in log:
        print(" -", step)
    out_path = save_clean(df_clean, source)
    print(f"Tersimpan: {out_path}")

    # ---------------- Task 2: level tagihan paling royal
    by_level = (
        df_clean.groupby("bill_level", observed=True)
        .agg(rata_rata_tip_pct=("tip_pct", "mean"), jumlah_transaksi=("tip", "count"))
        .reindex(BILL_LEVELS)
        .round(2)
    )
    print("\n2) Per bill_level\n", by_level)
    print(f"   Paling royal: {by_level['rata_rata_tip_pct'].idxmax()}")
    # Komentar: level Low paling royal (tip_pct 18,27%) dan makin besar tagihan makin kecil persentase tipnya
    # (Mid 16,17%, High 13,73%), karena tip cenderung naik lebih lambat daripada tagihan.

    # ---------------- Task 4: segmen penyumbang omzet (baca ulang dari clean_tips.csv)
    saved = pd.read_csv(out_path)
    segments = (
        saved.groupby(["is_weekend", "bill_level"])["total_bayar"].sum().round(2)
        .sort_values(ascending=False)
    )
    print("\n4) Omzet (total_bayar) per segmen\n", segments)
    # Bisnis: segmen Weekend + High penyumbang omzet terbesar (2.121 dari total 5.543, sekitar 38%), jauh di atas
    # segmen lain. Aksi saya sebagai manajer: fokuskan staf senior dan reservasi meja besar di Sabtu-Minggu malam
    # untuk menjaga pelanggan tagihan tinggi ini, sambil menawarkan paket menu premium agar omzetnya naik lagi.


if __name__ == "__main__":
    main()