# Sumber Data (Data Sources Log)

Catatan: setiap file di `data/raw/` wajib punya barisnya di sini.

## Format
| File lokal | Judul tabel BPS | Subjek | Periode | URL | Tanggal unduh | Catatan definisi |
|---|---|---|---|---|---|---|
| _(contoh)_ tpt_provinsi_2019-2024.xlsx | Tingkat Pengangguran Terbuka Menurut Provinsi | Tenaga Kerja | 2019-2024 (Agustus) | https://www.bps.go.id/... | 2026-10-17 | TPT = pengangguran / angkatan kerja x 100; pemerintahan daerah "..." |

## Unduhan

| File lokal | Judul tabel BPS | Subjek | Periode | URL | Tanggal unduh | Catatan definisi |
|---|---|---|---|---|---|---|
| tpt_provinsi_bps_embed.csv | Tingkat Pengangguran Terbuka Menurut Provinsi (var 543) | Tenaga Kerja | 2026 (Februari) | https://www.bps.go.id/id/statistics-table/2/NTQzIzI=/tingkat-pengangguran-terbuka-menurut-provinsi.html | 2026-10-17 | TPT=(Pengangguran/Angkatan Kerja)*100%; data dari payload SSR BPS (sampel 1 periode). |

https://www.bps.go.id/id/statistics-table/2/Njc0IzI=/pengangguran-terbuka-menurut-pendidikan-tertinggi-yang-ditamatkan.html | 2026-10-17 | TPT= (Pengangguran Terbuka Menurut Pendidikan Tertinggi yang Ditamatkan, 2025)*100%; data dari payload SSR BPS (sampel 1 periode).

## Catatan penting
- Perubahan jumlah provinsi antar tahun: ...............................
- Perbedaan periode rilis Sakernas (Feb/Mei/Agu/Nov) yang dipakai: ...............................
- Sumber cross-check (opsional): press release "Keadaan Ketenagakerjaan" BPS, tanggal ...............................
