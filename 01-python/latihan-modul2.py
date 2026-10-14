import numpy as np

harian = np.array([200, 150, 300, 250, 400, 100, 350])  # omzet 7 hari (rb rupiah)
mingguan = np.array([[10, 12, 8, 15], [5, 7, 6, 9]])    # 2 kota x 4 minggu, qty kopi

OMZET_THRESHOLD = 250    # rb rupiah
KONTRIBUSI_THRESHOLD = 15  # persen


# 1. Statistik dasar omzet harian
total = harian.sum()
rata_rata = harian.mean()
omzet_max = harian.max()
omzet_min = harian.min()

print(f"Total     : {total}")      # 1750
print(f"Rata-rata : {rata_rata}")  # 250.0
print(f"Max       : {omzet_max}")  # 400
print(f"Min       : {omzet_min}")  # 100


# 2. Hari dengan omzet > 250 (masking)
mask_tinggi = harian > OMZET_THRESHOLD
omzet_tinggi = harian[mask_tinggi]
jumlah_hari_tinggi = mask_tinggi.sum()

print(f"Omzet > {OMZET_THRESHOLD}: {omzet_tinggi}")      # [300 400 350]
print(f"Jumlah hari          : {jumlah_hari_tinggi}")    # 3


# 3. Total qty per kota dan per minggu
total_per_kota = mingguan.sum(axis=1)
total_per_minggu = mingguan.sum(axis=0)

print(f"Total per kota   : {total_per_kota}")    # [45 27]
print(f"Total per minggu : {total_per_minggu}")  # [15 19 14 24]


# 4. Persentase kontribusi tiap hari
kontribusi = harian / harian.sum() * 100
mask_kontribusi = kontribusi > KONTRIBUSI_THRESHOLD
hari_ke = np.flatnonzero(mask_kontribusi) + 1  # indeks mulai dari 1

print(f"Kontribusi (%)        : {np.round(kontribusi, 2)}")
# [11.43  8.57 17.14 14.29 22.86  5.71 20.  ]
print(f"Hari kontribusi > {KONTRIBUSI_THRESHOLD}%  : {hari_ke}")             # [3 5 7]
print(f"Kontribusinya (%)     : {np.round(kontribusi[mask_kontribusi], 2)}")  # [17.14 22.86 20.  ]