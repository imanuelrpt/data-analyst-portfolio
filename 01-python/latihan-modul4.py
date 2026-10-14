"""Analisis dataset tips.csv: omzet, tip, dan pola hari/jam."""

import pandas as pd

DATA_PATH = "data/tips.csv"  # file lokal, run dari C:\Voiceover


def load_data(path: str) -> pd.DataFrame:
    """Baca CSV dan tambahkan kolom tip_pct (tip / total_bill * 100)."""
    df = pd.read_csv(path)
    df["tip_pct"] = df["tip"] / df["total_bill"] * 100
    return df


# ---------------------------------------------------------------- Task 1
def summary_per_time(df: pd.DataFrame) -> pd.DataFrame:
    """Total, rata-rata total_bill, dan jumlah transaksi per time."""
    return (
        df.groupby("time")["total_bill"]
        .agg(total="sum", rata_rata="mean", jumlah_transaksi="count")
        .round(2)
    )


# ---------------------------------------------------------------- Task 2
def tip_pct_per_day(df: pd.DataFrame) -> pd.Series:
    """Rata-rata tip_pct per day, diurutkan dari yang terbesar."""
    return df.groupby("day")["tip_pct"].mean().sort_values(ascending=False).round(2)


# ---------------------------------------------------------------- Task 3
def build_day_mapping() -> pd.DataFrame:
    """Tabel referensi: nama hari (Indonesia) dan jenis hari."""
    return pd.DataFrame(
        {
            "day": ["Thur", "Fri", "Sat", "Sun"],
            "hari": ["Kamis", "Jumat", "Sabtu", "Minggu"],
            "jenis": ["Weekday", "Weekday", "Weekend", "Weekend"],
        }
    )


def summary_per_jenis(df: pd.DataFrame, mapping: pd.DataFrame) -> pd.DataFrame:
    """Merge mapping ke df, lalu hitung total omzet & rata-rata tip per jenis."""
    merged = df.merge(mapping, on="day", how="left")
    return (
        merged.groupby("jenis")
        .agg(total_omzet=("total_bill", "sum"), rata_rata_tip=("tip", "mean"))
        .round(2)
    )


# ---------------------------------------------------------------- Task 4
def pivot_omzet(df: pd.DataFrame) -> pd.DataFrame:
    """Pivot omzet: baris = day, kolom = time."""
    return pd.pivot_table(
        df,
        index="day",
        columns="time",
        values="total_bill",
        aggfunc="sum",
        fill_value=0,
    ).round(2)


def main() -> None:
    df = load_data(DATA_PATH)

    print("1) Ringkasan per time\n", summary_per_time(df), "\n")

    tip_day = tip_pct_per_day(df)
    print("2) Rata-rata tip_pct (%) per day\n", tip_day)
    print(f"   Paling royal: {tip_day.idxmax()} ({tip_day.max():.2f}%)\n")

    print("3) Weekday vs Weekend\n", summary_per_jenis(df, build_day_mapping()), "\n")

    pivot = pivot_omzet(df)
    print("4) Pivot omzet\n", pivot)

    # Pertanyaan bisnis: hari + jam apa penyumbang terbesar, dan aksi manajer?
    # Jawaban: Sabtu malam (Sat Dinner) memberi omzet terbesar, jadi sebagai
    # manajer saya akan menambah staf & stok di jam itu serta menaruh promo di
    # slot lemah (misal Jumat/Kamis Dinner) untuk meratakan pendapatan.
    hari, jam = pivot.stack().idxmax()
    print(f"\nPenyumbang terbesar: {hari} {jam} ({pivot.stack().max():,.2f})")


if __name__ == "__main__":
    main()