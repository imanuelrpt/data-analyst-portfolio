"""Uji hipotesis pada clean_tips.csv: t-test, chi-square, dan A/B mini."""

from pathlib import Path

import pandas as pd
from scipy import stats

CANDIDATE_PATHS = [
    Path("data/clean_tips.csv"),
    Path("../data/clean_tips.csv"),
    Path(__file__).parent / "clean_tips.csv",
]
ALPHA = 0.05
FAR_OUT_MULTIPLIER = 3.0
MIN_EXPECTED_COUNT = 5


def find_data_path(candidates: list[Path]) -> Path:
    """Kembalikan path pertama yang ada, atau error jika tidak ada satupun."""
    for path in candidates:
        if path.exists():
            return path
    raise FileNotFoundError(f"clean_tips.csv tidak ditemukan di: {candidates}")


def drop_input_errors(df: pd.DataFrame) -> pd.DataFrame:
    """Buang baris error input: tip negatif atau total_bill di luar pagar 3xIQR."""
    q1, q3 = df["total_bill"].quantile([0.25, 0.75])
    far_upper = q3 + FAR_OUT_MULTIPLIER * (q3 - q1)
    return df[(df["tip"] >= 0) & (df["total_bill"] <= far_upper)]


def decision(p_value: float) -> str:
    """Keputusan H0 pada tingkat signifikansi ALPHA."""
    return "tolak H0" if p_value < ALPHA else "gagal tolak H0"


def welch_ttest(group_a: pd.Series, group_b: pd.Series) -> tuple[float, float]:
    """Kembalikan (t, p) untuk Welch t-test (tidak mengasumsikan varians sama)."""
    result = stats.ttest_ind(group_a, group_b, equal_var=False)
    return result.statistic, result.pvalue


def compare_groups(df: pd.DataFrame, column: str, mask: pd.Series, label_a: str, label_b: str) -> None:
    """Cetak n, mean, t, p, dan keputusan untuk dua grup pada satu kolom."""
    group_a, group_b = df.loc[mask, column], df.loc[~mask, column]
    t_stat, p_value = welch_ttest(group_a, group_b)
    print(f"   {label_a}: n={len(group_a)}, mean={group_a.mean():.2f}")
    print(f"   {label_b}: n={len(group_b)}, mean={group_b.mean():.2f}")
    print(f"   t={t_stat:.3f}, p={p_value:.4f} -> {decision(p_value)}")


def chi_square_day_time(df: pd.DataFrame) -> tuple[pd.DataFrame, float, pd.DataFrame]:
    """Kembalikan (crosstab, p-value, tabel frekuensi harapan)."""
    table = pd.crosstab(df["day"], df["time"])
    chi2, p_value, dof, expected = stats.chi2_contingency(table)
    expected = pd.DataFrame(expected, index=table.index, columns=table.columns)
    return table, p_value, expected


def report(df: pd.DataFrame, title: str) -> None:
    """Cetak keempat analisis untuk satu versi data."""
    print(f"\n{'=' * 8} {title} ({len(df)} baris) {'=' * 8}")
    is_weekend = df["is_weekend"]

    print("1) t-test total_bayar: Weekend vs Weekday")
    compare_groups(df, "total_bayar", is_weekend, "Weekend", "Weekday")

    print("\n2) t-test tip_pct: Weekend vs Weekday")
    compare_groups(df, "tip_pct", is_weekend, "Weekend", "Weekday")
    print(f"   median: Weekend {df.loc[is_weekend, 'tip_pct'].median():.2f} | "
          f"Weekday {df.loc[~is_weekend, 'tip_pct'].median():.2f}")

    table, p_value, expected = chi_square_day_time(df)
    print("\n3) Chi-square day vs time\n", table)
    print(f"   p={p_value:.4g} -> {decision(p_value)}")
    small = int((expected < MIN_EXPECTED_COUNT).sum().sum())
    print(f"   sel dengan frekuensi harapan < {MIN_EXPECTED_COUNT}: {small} dari {expected.size}")

    print("\n4) A/B mini: Weekend High (B) vs lainnya (A), total_bayar")
    is_b = is_weekend & (df["bill_level"] == "High")
    compare_groups(df, "total_bayar", is_b, "B (Weekend High)", "A (lainnya)")


def main() -> None:
    df = pd.read_csv(find_data_path(CANDIDATE_PATHS))
    report(drop_input_errors(df), "SETELAH BUANG ERROR INPUT")
    report(df, "DATA APA ADANYA")


if __name__ == "__main__":
    main()