"""Korelasi, sampling, dan confidence interval pada clean_tips.csv."""

from pathlib import Path

import numpy as np
import pandas as pd

CANDIDATE_PATHS = [
    Path("data/clean_tips.csv"),
    Path("../data/clean_tips.csv"),
    Path(__file__).parent / "clean_tips.csv",
]
CORR_COLUMNS = ["total_bill", "tip", "size", "tip_pct", "total_bayar"]
# total_bayar = total_bill + tip (turunan), selalu ~0.99. Untuk temuan, cari terkuat tanpa dia.
CORR_BERSIH = ["total_bill", "tip", "size", "tip_pct"]
SAMPLE_SIZE = 30
SEEDS = (42, 7)
Z_95 = 1.96  # nilai kritis normal untuk CI 95%
FAR_OUT_MULTIPLIER = 3.0


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


# ---------------------------------------------------------------- Task 1
def strongest_pair(corr: pd.DataFrame) -> tuple[str, str, float]:
    """Pasangan variabel dengan |korelasi| terbesar (bukan diagonal)."""
    pairs = corr.where(np.triu(np.ones(corr.shape, dtype=bool), k=1)).stack()
    (a, b), value = pairs.abs().idxmax(), pairs.loc[pairs.abs().idxmax()]
    return a, b, value


# ---------------------------------------------------------------- Task 2
def sample_vs_population(df: pd.DataFrame, column: str, seed: int) -> tuple[float, float, float]:
    """Kembalikan (mean_sampel, mean_populasi, selisih)."""
    sample_mean = df[column].sample(SAMPLE_SIZE, random_state=seed).mean()
    population_mean = df[column].mean()
    return sample_mean, population_mean, sample_mean - population_mean


# ---------------------------------------------------------------- Task 3 & 4
def confidence_interval(values: pd.Series, z: float = Z_95) -> tuple[float, float, float]:
    """Kembalikan (mean, batas_bawah, batas_atas): mean +- z * standard error."""
    # values.sem() = std(ddof=1)/sqrt(n), konsisten dengan std Modul 1 yang ddof=1.
    mean, sem = values.mean(), values.sem()
    return mean, mean - z * sem, mean + z * sem


def report(df: pd.DataFrame, title: str) -> None:
    """Cetak keempat analisis untuk satu versi data."""
    print(f"\n{'=' * 8} {title} ({len(df)} baris) {'=' * 8}")

    corr = df[CORR_COLUMNS].corr().round(2)
    print("1) Matriks korelasi\n", corr)
    a, b, value = strongest_pair(df[CORR_BERSIH].corr().round(2))
    print(f"   Terkuat bermakna: {a} vs {b} (r = {value:.2f})")

    print("\n2) Sampel 30 vs populasi (total_bayar)")
    for seed in SEEDS:
        s, p, diff = sample_vs_population(df, "total_bayar", seed)
        print(f"   seed {seed}: sampel {s:.2f} | populasi {p:.2f} | selisih {diff:+.2f}")

    mean, low, high = confidence_interval(df["tip_pct"])
    print(f"\n3) CI95% tip_pct: mean {mean:.2f}% -> [{low:.2f}, {high:.2f}]")

    print("\n4) CI95% total_bayar")
    for flag, label in ((True, "Weekend"), (False, "Weekday")):
        group = df.loc[df["is_weekend"] == flag, "total_bayar"]
        mean, low, high = confidence_interval(group)
        print(f"   {label} (n={len(group)}): mean {mean:.2f} -> [{low:.2f}, {high:.2f}], lebar {high - low:.2f}")


def main() -> None:
    df = pd.read_csv(find_data_path(CANDIDATE_PATHS))
    report(drop_input_errors(df), "SETELAH BUANG ERROR INPUT")
    report(df, "DATA APA ADANYA")


if __name__ == "__main__":
    main()