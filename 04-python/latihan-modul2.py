"""Grafik ber-insight dari clean_tips.csv: judul berisi temuan + angka (dihitung otomatis)."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # simpan ke file tanpa buka jendela
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

CANDIDATE_PATHS = [
    Path("data/clean_tips.csv"),
    Path("../data/clean_tips.csv"),
    Path(__file__).parent / "clean_tips.csv",
]
OUTPUT_DIR = Path(__file__).parent / "grafik"
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


def save_figure(fig: plt.Figure, name: str) -> Path:
    """Simpan figure ke folder grafik/ lalu tutup."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    path = OUTPUT_DIR / name
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path

WEEKEND_LABELS = {False: "Weekday", True: "Weekend"}
TIME_ORDER = ["Lunch", "Dinner"]


def fmt(value: float, decimals: int = 2) -> str:
    """Format angka gaya Indonesia (koma desimal) untuk judul grafik."""
    return f"{value:.{decimals}f}".replace(".", ",")


# ---------------------------------------------------------------- Task 1
def plot_median_bar(df: pd.DataFrame) -> Path:
    """Bar median total_bayar Weekday vs Weekend, judul = temuan + angka."""
    # Komentar: bar BENAR karena yang dibandingkan satu angka ringkas (median) antar 2 kategori;
    # kelemahannya bar menyembunyikan sebaran, jadi boxplot lebih cocok bila sebaran yang ditanyakan.
    medians = df.groupby(df["is_weekend"].map(WEEKEND_LABELS))["total_bayar"].median()
    gap_pct = (medians["Weekend"] / medians["Weekday"] - 1) * 100
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.barplot(x=medians.index, y=medians.values, order=["Weekday", "Weekend"], ax=ax)
    ax.bar_label(ax.containers[0], fmt="%.2f")
    ax.set(xlabel="", ylabel="median total_bayar")
    ax.set_title(f"Median tagihan Weekend {fmt(medians['Weekend'])} vs Weekday "
                 f"{fmt(medians['Weekday'])} (+{fmt(gap_pct, 1)}%)", fontsize=11)
    return save_figure(fig, "5_bar_median_insight.png")


# ---------------------------------------------------------------- Task 2
def plot_tip_pct_hist_insight(df: pd.DataFrame) -> Path:
    """Versi ber-insight dari histogram tip_pct (Modul 1)."""
    share_core = ((df["tip_pct"] >= 12) & (df["tip_pct"] <= 19)).mean() * 100
    n_extreme = int((df["tip_pct"] > 30).sum())
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.histplot(df["tip_pct"], bins=20, ax=ax)
    ax.axvspan(12, 19, color="green", alpha=0.12, label="12-19%")
    ax.set(xlabel="tip_pct (%)", ylabel="Jumlah transaksi")
    ax.set_title(f"{fmt(share_core, 0)}% tip ada di 12-19%, tapi {n_extreme} transaksi >30% "
                 f"(maks {fmt(df['tip_pct'].max(), 0)}%) -> waspada outlier", fontsize=11)
    ax.legend()
    return save_figure(fig, "6_hist_tip_pct_insight.png")


# ---------------------------------------------------------------- Task 3
def plot_scatter_by_time(df: pd.DataFrame) -> Path:
    """Scatter total_bill vs tip, warna per time, plus garis tren per time."""
    corr = {t: df.loc[df["time"] == t, "total_bill"].corr(df.loc[df["time"] == t, "tip"]) for t in TIME_ORDER}
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.scatterplot(data=df, x="total_bill", y="tip", hue="time", hue_order=TIME_ORDER, alpha=0.7, ax=ax)
    for time_value, color in zip(TIME_ORDER, sns.color_palette()[:2]):
        subset = df[df["time"] == time_value]
        sns.regplot(data=subset, x="total_bill", y="tip", scatter=False, ci=None, color=color, ax=ax)
    ax.set_title(f"Tip naik seiring tagihan di Lunch & Dinner; Lunch lebih rapat "
                 f"(r={fmt(corr['Lunch'])} vs {fmt(corr['Dinner'])})", fontsize=11)
    # Insight: pola searah (tagihan besar -> tip besar) di kedua waktu, tapi Dinner lebih menyebar.
    # Aksi: tempatkan staf paling berpengalaman di Dinner (tagihan lebih besar & variatif), untuk upselling.
    return save_figure(fig, "7_scatter_total_bill_vs_tip_time.png")


# ---------------------------------------------------------------- Task 4
def omzet_share(df: pd.DataFrame) -> pd.Series:
    """Share % total_bayar untuk Weekday dan Weekend."""
    totals = df.groupby(df["is_weekend"].map(WEEKEND_LABELS))["total_bayar"].sum()
    return (totals / totals.sum() * 100).reindex(["Weekday", "Weekend"])


def plot_omzet_share(df: pd.DataFrame) -> Path:
    """Bar horizontal share omzet Weekend vs Weekday dengan anotasi %."""
    share = omzet_share(df)
    totals = df.groupby(df["is_weekend"].map(WEEKEND_LABELS))["total_bayar"].sum()
    fig, ax = plt.subplots(figsize=(8, 3.5))
    sns.barplot(x=share.values, y=share.index, order=["Weekend", "Weekday"], orient="h", ax=ax)
    for bar, label in zip(ax.patches, ["Weekend", "Weekday"]):
        ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height() / 2,
                f"{fmt(share[label], 1)}% ({totals[label]:,.0f})", va="center")
    ax.set(xlim=(0, 100), xlabel="Share omzet (% total_bayar)", ylabel="")
    ax.set_title(f"Weekend menyumbang {fmt(share['Weekend'], 1)}% omzet, Weekday hanya {fmt(share['Weekday'], 1)}%",
                 fontsize=11)
    # Komentar: Weekend (Sabtu-Minggu) memberi 70% omzet dari jumlah hari yang sama dengan Weekday
    # (2 hari), jadi alokasikan sekitar 70% jam kerja staf ke Sabtu-Minggu, terutama shift Dinner.
    # Di Weekday cukup staf ramping: Kamis fokus Lunch, Jumat minimal karena kontribusinya kecil.
    return save_figure(fig, "8_share_omzet.png")


def main() -> None:
    df = drop_input_errors(pd.read_csv(find_data_path(CANDIDATE_PATHS)))
    print(f"Data: {len(df)} baris (setelah buang 2 baris error input)")
    for plot in (plot_median_bar, plot_tip_pct_hist_insight, plot_scatter_by_time, plot_omzet_share):
        print(plot(df))


if __name__ == "__main__":
    main()