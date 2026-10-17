# Rancangan Dashboard - Pengangguran & Pasar Kerja di Indonesia
**Tool:** Looker Studio (Google Data Studio)

## Tujuan
Dashboard 1 halaman (bisa dibaca < 1 menit) untuk menunjukkan kelompok dan wilayah yang paling rentan menganggur.

## Layout
| Bagian | Posisi | Chart |
|---|---|---|
| Header KPI | Atas | 4 Scorecard |
| Tren Nasional | Atas-Tengah | Line Chart (Tahun × TPT) — *belum tersedia (data 1 periode)* |
| Ranking Provinsi | Kiri/Tengah | Bar Chart (Provinsi × TPT) terurut descending |
| Breakdown | Kanan | Bar Chart (Pendidikan/Kota-Desa/Gender) — *nanti setelah data lengkap* |
| Filter | Atas Kanan | Tahun, Provinsi, Pendidikan, Wilayah, Gender |

## KPI
| KPI | Rumus/Data | Label |
|---|---|---|
| TPT Nasional (Terbaru) | Nilai INDONESIA (jika dipisah) / rerata | "TPT Nasional (Feb 2026)" |
| Provinsi TPT Tertinggi | Max TPT provinsi | "TPT Tertinggi" |
| Provinsi TPT Terendah | Min TPT provinsi | "TPT Terendah" |
| Gap | Max - Min | "Gap Tertinggi-Terendah" |

## Sumber Data
- `data/clean/tpt_provinsi_clean.csv` (saat ini)
- `data/clean/tpt_pendidikan_clean.csv` (tambah nanti jika sudah ada file)
- Format: long/tidy (tahun, provinsi, tpt, pendidikan, wilayah, gender)

## Catatan
- Data saat ini hanya 1 periode (Februari 2026). Tren nasional belum bisa ditampilkan; tambahkan tabel multi-tahun.
- Eksklusi INDONESIA dari ranking provinsi.
- Warna: merah untuk nilai tinggi (rentan).

## Langkah di Looker Studio
1. Buat laporan baru → Connect to data → Upload CSV → pilih `tpt_provinsi_clean.csv`
2. Tambah Scorecard untuk 4 KPI
3. Tambah Bar Chart: Provinsi (Dimensi, urut desc by TPT) × TPT (Metrik)
4. Tambah Line Chart nanti saat data multi-tahun tersedia
5. Tambah kontrol filter (Drop-down list) Tahun/Provinsi
6. Tata layout 1 halaman, judul jelas
