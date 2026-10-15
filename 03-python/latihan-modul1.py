"""Statistik deskriptif clean_tips.csv: sebaran, perbandingan segmen, outlier, skewness."""

from pathlib import Path

import pandas as pd

CANDIDATE_PATHS = [
    Path("data/clean_tips.csv"),
    Path("../data/clean_tips.csv"),
    Path(__file__).parent / "clean_tips.csv",
]
IQR_MULTIPLIER = 1.5
FAR_OUT_MULTIPLIER = 3.0  # pagar "sangat ekstrem" untuk mendeteksi error input


def find_data_path(candidates: list[Path]) -> Path:
    """Kembalikan path pertama yang ada, atau error jika tidak ada satupun."""
    for path in candidates:
        if path.exists():
            return path
    raise FileNotFoundError(f"clean_tips.csv tidak ditemukan di: {candidates}")


def iqr_bounds(values: pd.Series, k: float = IQR_MULTIPLIER) -> tuple[float, float, float, float]:
    """Kembalikan (Q1, Q3, batas_bawah, batas_atas)."""
    q1, q3 = values.quantile([0.25, 0.75])
    iqr = q3 - q1
    return q1, q3, q1 - k * iqr, q3 + k * iqr


# ---------------------------------------------------------------- Task 1
def describe_stats(values: pd.Series) -> pd.Series:
    """Mean, median, std, min, max."""
    # Catatan: median total_bayar 20.81 tidak bergerak sebelum/sesudah buang error (tahan outlier),
    # sedangkan mean 24.78 -> 22.88 ketarik 1 baris 500.
    return values.agg(["mean", "median", "std", "min", "max"]).round(2)


# ---------------------------------------------------------------- Task 2
def compare_weekend(df: pd.DataFrame) -> pd.DataFrame:
    """tip_pct: mean, median, count untuk Weekday vs Weekend."""
    table = df.groupby("is_weekend")["tip_pct"].agg(["mean", "median", "count"]).round(2)
    table.index = table.index.map({False: "Weekday", True: "Weekend"})
    return table


# ---------------------------------------------------------------- Task 3
def find_outliers(values: pd.Series) -> tuple[float, float, float, float, pd.Series]:
    """Kembalikan (Q1, Q3, batas_bawah, batas_atas, nilai_outlier)."""
    q1, q3, lower, upper = iqr_bounds(values)
    return q1, q3, lower, upper, values[~values.between(lower, upper)]


# ---------------------------------------------------------------- Task 4
def skewness(df: pd.DataFrame, columns: list[str]) -> pd.Series:
    """Skewness tiap kolom, diurutkan dari yang paling miring."""
    return df[columns].skew().round(2).sort_values(ascending=False)


def drop_input_errors(df: pd.DataFrame) -> pd.DataFrame:
    """Buang baris yang jelas error input: tip negatif atau total_bill di luar pagar 3xIQR."""
    _, _, _, far_upper = iqr_bounds(df["total_bill"], FAR_OUT_MULTIPLIER)
    return df[(df["tip"] >= 0) & (df["total_bill"] <= far_upper)]


def report(df: pd.DataFrame, title: str) -> None:
    """Cetak keempat analisis untuk satu versi data."""
    print(f"\n{'=' * 8} {title} ({len(df)} baris) {'=' * 8}")
    print("1) total_bayar\n", describe_stats(df["total_bayar"]))
    print("\n2) tip_pct Weekday vs Weekend\n", compare_weekend(df))
    q1, q3, lower, upper, outliers = find_outliers(df["harga_per_orang"])
    print(f"\n3) harga_per_orang: Q1={q1:.2f} Q3={q3:.2f} IQR={q3 - q1:.2f} "
          f"batas=[{lower:.2f}, {upper:.2f}] outlier={len(outliers)}")
    print("   outlier terbesar:", outliers.sort_values(ascending=False).head(3).round(2).tolist())
    print("\n4) skew\n", skewness(df, ["total_bill", "size"]))


def main() -> None:
    df = pd.read_csv(find_data_path(CANDIDATE_PATHS))
    report(df, "DATA APA ADANYA")
    report(drop_input_errors(df), "SETELAH BUANG ERROR INPUT")


if __name__ == "__main__":
    main()