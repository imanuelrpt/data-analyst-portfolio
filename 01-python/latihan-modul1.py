"""Fase 1 Modul 1 - Latihan Python Khusus Data."""

penjualan = [
    {"kota": "Jakarta", "produk": "Kopi", "qty": 10, "harga": 20000},
    {"kota": "Bandung", "produk": "Teh", "qty": 5, "harga": 15000},
    {"kota": "Jakarta", "produk": "Teh", "qty": 3, "harga": 15000},
    {"kota": "Surabaya", "produk": "Kopi", "qty": 7, "harga": 20000},
]


# 1. (Mudah) Total semua qty
def total_qty(data):
    # sum + generator: jumlahkan qty tiap item
    return sum(item["qty"] for item in data)


print(total_qty(penjualan))  # 25


# 2. (Sedang) Kota yang beli Kopi, pakai list comprehension
# pola: [hasil for item in list if syarat]
kota_kopi = [item["kota"] for item in penjualan if item["produk"] == "Kopi"]
print(kota_kopi)  # ['Jakarta', 'Surabaya']


# 3. (Sedang+) Omzet per kota tertentu
def omzet_per_kota(data, kota):
    # omzet = sum(qty*harga) hanya untuk kota yang diminta
    return sum(item["qty"] * item["harga"] for item in data if item["kota"] == kota)


print(omzet_per_kota(penjualan, "Jakarta"))  # 245000


# 4. (Sulit) Rekap omzet semua kota pakai loop + dict
rekap = {}
for item in penjualan:
    kota = item["kota"]
    omzet = item["qty"] * item["harga"]
    if kota in rekap:
        rekap[kota] += omzet
    else:
        rekap[kota] = omzet

print(rekap)  # {'Jakarta': 245000, 'Bandung': 75000, 'Surabaya': 140000}
