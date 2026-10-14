# Rangkuman Belajar Data Analyst (Bahasa Santai)

> Target: kerja entry-level dalam 6 bulan, 1 jam/hari. Tools utama: Python + VS Code.

## Fase 0 - Persiapan ✅ Selesai
- **Inti:** Data Analyst menjawab "apa yang terjadi dan kenapa" lewat alur: tanya (ask) → kumpulkan (prepare) → bersihkan (process) → analisis (analyze) → sajikan (share) → sarankan aksi (act).
- **Beda peran:** Analyst = pakai data yang ada. Scientist = bikin prediksi pakai machine learning. Engineer = bikin pipa agar data mengalir rapi tiap hari.
- **Setup:** VS Code + Python + `pandas numpy matplotlib seaborn` + GitHub sebagai etalase.
- **Hasil:** Repo `data-analyst-portfolio` rapi, notebook bisa di-run ulang dari atas ke bawah.

## Fase 1 - Python untuk Data ✅ Selesai
- **Modul 1 - Python khusus data:** `list` = daftar struk, `dict` = 1 struk, `list of dict` = cikal bakal tabel. Senjata harian: loop + if (filter), function (biar reusable), list comprehension (loop 1 baris).
- **Modul 2 - NumPy:** `array` = 1 kolom Excel khusus angka. Hitung sekaligus tanpa loop (vectorized). Kunci: boolean masking `arr[arr > x]` untuk filter, `sum(axis=0)` ke bawah per kolom, `axis=1` ke samping per baris. Selalu cek `shape` dan `dtype` kalau error.
- **Modul 3 - Pandas dasar:** `DataFrame` = sheet Excel beneran. Alur wajib: `read_csv` → `shape/info/head` → filter `df[kondisi]` → `sort_values`. Tambah kolom baru harus pakai `.copy()` dulu biar aman.
- **Modul 4 - Pandas lanjut:** `groupby` = rekap per kategori (jangan lupa `reset_index`). `merge` = tempel 2 tabel pakai kunci (cek duplikat dulu biar baris tidak meledak). `pivot_table` = rekap silang ala Excel, isi lubang pakai `fill_value=0`.
- **Dataset:** `data/tips.csv` (244 transaksi restoran). Dipakai sampai Fase 1 tamat.

## Fase 2 - Data Cleaning ⏳ Berikutnya
- **Inti:** Data nyata itu kotor. Tugas: tangani missing value (kosong), duplikat, tipe salah (tanggal jadi teks), outlier (angka tidak wajar), dan rapikan teks (spasi, kapital).
- **Hasil:** Dataset siap analisis + `cleaning log`: catatan "apa yang diubah dan kenapa" supaya bisa dijelaskan ke manajer.
- **Contoh:** Kolom tanggal `12/01/2026` diubah ke tipe tanggal, harga `"Rp 20.000"` dibersihkan jadi `20000`.

## Fase 3 - Statistik ⏳
- **Inti:** Intuisi dulu, rumus belakangan. Mean = rata-rata (sensitif outlier), median = nilai tengah (aman), modus = paling sering. Standar deviasi = seberapa menyebar.
- **Lanjutan:** Korelasi (hubungan, bukan sebab), sampling, confidence interval, p-value, t-test / chi-square, dan A/B testing (misal: desain A vs B, mana yang menang signifikan?).

## Fase 4 - EDA dan Visualisasi ⏳
- **Inti:** Cerita dari data, bukan grafik cantik. Pola: univariate (1 kolom, misal distribusi harga), bivariate (2 kolom, misal harga vs tip), multivariate (banyak kolom sekaligus).
- **Tools:** Matplotlib + Seaborn. Aturan: pilih chart yang jawab pertanyaan bisnis (bar untuk perbandingan, line untuk tren, scatter untuk hubungan).

## Fase 5 - SQL ⏳
- **Inti:** Bahasa untuk ambil data dari database. Urutan belajar: SELECT-WHERE-GROUP BY-HAVING → JOIN-subquery-CTE → window function (ranking, total berjalan).
- **Praktik:** SQLite / BigQuery sandbox + panggil SQL dari Python.

## Fase 6 - BI Tools dan Sheets ⏳
- **Inti:** Dashboard yang jawab pertanyaan bisnis, bukan tempelan grafik. Google Sheets: XLOOKUP, IF, pivot table. Looker Studio: dashboard gratis interaktif. Kenalan Power BI / Tableau buat loker.
- **Hasil:** 1 dashboard + 1 laporan Sheets yang bisa diklik atasan.

## Fase 7 - Bonus (Opsional) ⏳
- **Inti:** Nilai plus: regresi / klasifikasi sederhana pakai scikit-learn, dan automation laporan Python (misal kirim rekap mingguan otomatis).

## Fase 8 - Portofolio dan Karier ⏳
- **Inti:** 3 proyek naik level: 1) analisis penjualan, 2) perilaku pelanggan, 3) dashboard bisnis. Tiap proyek: README jelas + notebook bisa di-run ulang + insight 1-2 kalimat aksi.
- **Plus:** CV Data Analyst, latihan studi kasus dan interview SQL + studi kasus Indonesia.

---
*Update tiap selesai 1 modul. 
*Terakhir: Fase 1 selesai.*