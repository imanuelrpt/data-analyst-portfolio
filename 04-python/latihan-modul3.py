"""EDA lengkap clean_tips.csv: univariat, bivariat, multivariat, dan laporan 5 baris."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # simpan ke file tanpa buka jendela
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy import stats

CANDIDATE_PATHS = [
    Path("data/clean_tips.csv"),
    Path("../data/clean_tips.csv"),
    Path(__file__).parent / "clean_tips.csv",
]
OUTPUT_DIR = Path(__file__).parent / "grafik"
FAR_OUT_MULTIPLIER = 3.0
BILL_LEVELS = ["Low", "Mid", "High"]


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


def fmt(value: float, decimals: int = 2) -> str:
    """Format angka gaya Indonesia (koma desimal) untuk judul grafik."""
    return f"{value:.{decimals}f}".replace(".", ",")

NUMERIC_COLUMNS = ["total_bayar", "tip_pct", "harga_per_orang"]
DAY_ORDER = ["Thur", "Fri", "Sat", "Sun"]
WEEKEND_LABELS = {False: "Weekday", True: "Weekend"}


# ---------------------------------------------------------------- Task 1: UNI
def numeric_summary(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """describe() dan skew() untuk kolom numerik utama."""
    return df[NUMERIC_COLUMNS].describe().round(2), df[NUMERIC_COLUMNS].skew().round(2)


def imbalance_ratio(counts: pd.Series) -> float:
    """Rasio kategori terbesar : terkecil (makin besar makin timpang)."""
    return counts.max() / counts.min()


# ---------------------------------------------------------------- Task 2: BI
def corr_by_weekend(df: pd.DataFrame) -> pd.Series:
    """Korelasi harga_per_orang vs tip_pct, dipisah Weekday/Weekend."""
    return df.groupby(df["is_weekend"].map(WEEKEND_LABELS)).apply(
        lambda g: g["harga_per_orang"].corr(g["tip_pct"]), include_groups=False
    ).round(2)


def plot_median_tip_by_day(df: pd.DataFrame) -> str:
    """Bar median tip_pct per day (urut Thur-Sun) dengan judul ber-insight."""
    medians = df.groupby("day")["tip_pct"].median().reindex(DAY_ORDER)
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.barplot(x=medians.index, y=medians.values, order=DAY_ORDER, ax=ax)
    ax.bar_label(ax.containers[0], fmt="%.2f")
    ax.set(xlabel="day", ylabel="median tip_pct (%)")
    ax.set_title(f"Median tip_pct per hari hampir sama ({fmt(medians.min())}-{fmt(medians.max())}%), "
                 f"{medians.idxmax()} tertinggi", fontsize=11)
    return str(save_figure(fig, "9_bar_median_tip_per_day.png"))


# ---------------------------------------------------------------- Task 3: MULTI
def pivot_day_time(df: pd.DataFrame) -> pd.DataFrame:
    """Omzet (total_bayar) per day x time."""
    return pd.pivot_table(df, index="day", columns="time", values="total_bayar",
                          aggfunc="sum", fill_value=0).reindex(DAY_ORDER).round(2)


def omzet_by_segment(df: pd.DataFrame) -> pd.Series:
    """Omzet per is_weekend x bill_level, diurutkan dari terbesar."""
    return (df.groupby(["is_weekend", "bill_level"])["total_bayar"].sum()
            .round(2).sort_values(ascending=False))


# ---------------------------------------------------------------- Task 4: laporan
def build_report(df: pd.DataFrame) -> list[str]:
    """Laporan EDA 5 baris: 3 temuan ber-angka, 1 keterbatasan, 1 next step."""
    total = df["total_bayar"].sum()
    weekend = df["is_weekend"]
    weekend_share = df.loc[weekend, "total_bayar"].sum() / total * 100
    tip_by_level = df.groupby("bill_level")["tip_pct"].median()
    _, p_value = stats.ttest_ind(df.loc[weekend, "total_bayar"], df.loc[~weekend, "total_bayar"],
                                 equal_var=False)
    n_friday = int((df["day"] == "Fri").sum())
    n_dates = df["tanggal"].nunique()
    n_nat = int(df["tanggal"].isna().sum())
    return [
        f"1) Weekend menyumbang {fmt(weekend_share, 1)}% omzet ({df.loc[weekend, 'total_bayar'].sum():,.0f} "
        f"dari {total:,.0f}); semuanya dari Dinner Sabtu-Minggu.",
        f"2) Tagihan Low paling royal: tip_pct {fmt(tip_by_level['Low'])}% vs High {fmt(tip_by_level['High'])}%.",
        f"3) Total bayar Weekend lebih tinggi signifikan (p={fmt(p_value, 3)}), tapi tip_pct Weekend vs Weekday sama.",
        f"4) Keterbatasan: Jumat hanya n={n_friday}, dan tanggal tidak bisa dipakai "
        f"({n_dates} tanggal unik, {n_nat} NaT, tidak cocok dengan kolom day) sehingga tren waktu tak terlihat.",
        "5) Next step: butuh transaksi min. 3 bulan dengan tanggal valid (termasuk Lunch akhir pekan dan "
        "Jumat) untuk memastikan 70% Weekend stabil per bulan, lalu uji promo dengan A/B sungguhan.",
    ]


def main() -> None:
    df = drop_input_errors(pd.read_csv(find_data_path(CANDIDATE_PATHS)))
    print(f"Data: {len(df)} baris (setelah buang 2 baris error input)")

    summary, skew = numeric_summary(df)
    print("\n1) describe\n", summary, "\nskew\n", skew)
    for column in ("day", "time"):
        counts = df[column].value_counts()
        print(f"\n{counts}\n   proporsi %: {(counts / len(df) * 100).round(1).to_dict()} "
              f"| rasio max:min = {imbalance_ratio(counts):.1f}")

    print("\n2) korelasi harga_per_orang vs tip_pct\n", corr_by_weekend(df))
    print(df.groupby("day")["tip_pct"].median().reindex(DAY_ORDER).round(2).to_dict())
    print(plot_median_tip_by_day(df))

    print("\n3) pivot day x time\n", pivot_day_time(df))
    print(omzet_by_segment(df))

    print("\n4) Laporan EDA")
    for line in build_report(df):
        print(" ", line)


if __name__ == "__main__":
    main()