import pandas as pd

df = pd.read_csv("https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv")

print(df.shape)
print(df.head(3))
print(df.dtypes)
print(f"Kolom angka: {df.select_dtypes('number').shape[1]}")
print(f"Kolom teks : {df.select_dtypes(exclude='number').shape[1]}")

lunch_besar = df[(df["time"] == "Lunch") & (df["total_bill"] > 20)]
print(f"Jumlah baris: {len(lunch_besar)}")
print(lunch_besar.sort_values("tip", ascending=False).head(5))

df_tip = df.copy()
df_tip["tip_pct"] = df_tip["tip"] / df_tip["total_bill"] * 100
print(df_tip.nlargest(5, "tip_pct"))

anomali = df[(df["size"] >= 5) & (df["total_bill"] < 30)]
print(anomali)