# Pengangguran & Pasar Kerja di Indonesia

Analisis Tingkat Pengangguran Terbuka (TPT) berdasarkan provinsi, tingkat pendidikan,
dan wilayah (kota/desa), menggunakan data BPS.

## Pertanyaan Bisnis
Bagaimana kondisi pengangguran di Indonesia berdasarkan provinsi, tingkat pendidikan,
dan wilayah (kota/desa), dan kelompok mana yang paling sulit mendapat pekerjaan?

Sub-pertanyaan:
1. Bagaimana tren TPT nasional dalam beberapa tahun terakhir?
2. Provinsi mana yang TPT-nya tertinggi dan terendah, dan apakah polanya konsisten?
3. Apakah ada perbedaan TPT berdasarkan tingkat pendidikan?
4. Bagaimana perbedaan perkotaan vs perdesaan, serta laki-laki vs perempuan?
5. (Opsional) Apakah ada hubungan TPT dengan upah minimum / kemiskinan per provinsi?

## Sumber Data
| Tabel BPS | Periode | URL | Tanggal Unduh |
|---|---|---|---|
| _(diisi saat Tahap 2)_ | | | |

## Struktur
- `data/raw/` - file mentah BPS (jangan diedit)
- `data/clean/` - hasil cleaning (tidy/long format)
- `notebooks/` - 01_cleaning, 02_eda, 03_analysis
- `outputs/` - gambar chart & screenshot dashboard

## Cara Menjalankan Ulang
1. Aktifkan venv: `.\.venv\Scripts\Activate.ps1`
2. Install: `pip install -r requirements.txt`
3. Buka notebook di VS Code, pilih kernel `.venv`, lalu Restart Kernel + Run All.

## Temuan Utama
_(diisi setelah analisis)_

## Keterbatasan
_(diisi setelah analisis)_
