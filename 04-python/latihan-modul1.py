"""Visualisasi clean_tips.csv: histogram, boxplot, bar median, dan scatter."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # simpan ke file tanpa membuka jendela; hapus baris ini jika ingin plt.show()
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

CANDIDATE_PATHS = [
    Path("data/clean_tips.csv"),
    Path("../data/clean_tips.csv"),
    Path(__file__).parent / "clean_tips.csv",
]
OUTPUT_DIR = Path(__file__).parent / "grafik"
BILL_LEVELS = ["Low", "Mid", "High"]
FAR_OUT_MULTIPLIER = 3.0
WEEKEND_LABELS = {False: "Weekday", True: "Weekend"}


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


def save_figure(fig: plt.Figure, name: str) -> Path:
    """Simpan figure ke folder grafik/ lalu tutup."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    path = OUTPUT_DIR / name
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path


# ---------------------------------------------------------------- Task 1
def plot_tip_pct_hist(df: pd.DataFrame) -> Path:
    """Histogram tip_pct (bins=20) dengan garis mean dan median."""
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(df["tip_pct"], bins=20, ax=ax)
    ax.axvline(df["tip_pct"].mean(), color="red", linestyle="--", label="mean")
    ax.axvline(df["tip_pct"].median(), color="green", linestyle="-", label="median")
    ax.set(title="Distribusi tip_pct", xlabel="tip_pct (%)", ylabel="Jumlah transaksi")
    ax.legend()
    # Komentar: ekor memanjang ke KANAN (miring kanan), mean > median karena segelintir tip_pct besar.
    return save_figure(fig, "1_hist_tip_pct.png")


# ---------------------------------------------------------------- Task 2
def plot_box_total_bayar(df: pd.DataFrame) -> Path:
    """Boxplot total_bayar per is_weekend."""
    data = df.assign(grup=df["is_weekend"].map(WEEKEND_LABELS))
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.boxplot(data=data, x="grup", y="total_bayar", order=["Weekday", "Weekend"], ax=ax)
    ax.set(title="total_bayar: Weekday vs Weekend", xlabel="", ylabel="total_bayar")
    return save_figure(fig, "2_box_total_bayar.png")


def boxplot_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Median dan jumlah outlier (aturan 1,5xIQR per grup) total_bayar per grup."""
    rows = {}
    for flag, label in WEEKEND_LABELS.items():
        values = df.loc[df["is_weekend"] == flag, "total_bayar"]
        q1, q3 = values.quantile([0.25, 0.75])
        iqr = q3 - q1
        n_outlier = int((~values.between(q1 - 1.5 * iqr, q3 + 1.5 * iqr)).sum())
        rows[label] = {"n": len(values), "median": round(values.median(), 2), "outlier": n_outlier}
    return pd.DataFrame(rows).T


# ---------------------------------------------------------------- Task 3
def plot_bar_median_by_level(df: pd.DataFrame) -> Path:
    """Bar median total_bayar per bill_level (urut Low, Mid, High)."""
    medians = df.groupby("bill_level")["total_bayar"].median().reindex(BILL_LEVELS)
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.barplot(x=medians.index, y=medians.values, order=BILL_LEVELS, ax=ax)
    ax.bar_label(ax.containers[0], fmt="%.2f")
    ax.set(title="Median total_bayar per bill_level", xlabel="bill_level", ylabel="median total_bayar")
    return save_figure(fig, "3_bar_median_level.png")


# ---------------------------------------------------------------- Task 4
def plot_scatter_price_vs_tip(df: pd.DataFrame) -> Path:
    """Scatter harga_per_orang vs tip_pct, warna per is_weekend."""
    data = df.assign(grup=df["is_weekend"].map(WEEKEND_LABELS))
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.scatterplot(data=data, x="harga_per_orang", y="tip_pct", hue="grup",
                    hue_order=["Weekday", "Weekend"], alpha=0.7, ax=ax)
    ax.set(title="harga_per_orang vs tip_pct", xlabel="harga_per_orang", ylabel="tip_pct (%)")
    return save_figure(fig, "4_scatter_harga_vs_tip.png")


def main() -> None:
    df = drop_input_errors(pd.read_csv(find_data_path(CANDIDATE_PATHS)))
    print(f"Data: {len(df)} baris (setelah buang 2 baris error input)")

    print("skew tip_pct:", round(df["tip_pct"].skew(), 2),
          "| mean", round(df["tip_pct"].mean(), 2), "| median", round(df["tip_pct"].median(), 2))
    print(plot_tip_pct_hist(df))

    print(boxplot_summary(df))
    print(plot_box_total_bayar(df))

    print(df.groupby("bill_level")["total_bayar"].median().reindex(BILL_LEVELS).round(2).to_dict())
    print(plot_bar_median_by_level(df))

    print(df.groupby("is_weekend")[["harga_per_orang", "tip_pct"]].corr().round(2).iloc[[1, 3], 0].to_dict())
    print(plot_scatter_price_vs_tip(df))


if __name__ == "__main__":
    main()