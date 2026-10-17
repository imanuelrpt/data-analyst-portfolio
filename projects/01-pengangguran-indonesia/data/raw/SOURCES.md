# Sumber Data (Data Sources Log)

Catatan sumber data yang digunakan dalam proyek ini. Seluruh data berasal dari Badan Pusat Statistik (BPS).

## Unduhan

| No | File lokal | Judul tabel BPS | Subjek | Periode | Sumber | Tanggal unduh |
|----|------------|-----------------|--------|---------|--------|---------------|
| 1 | `tpt_provinsi_bps_embed.csv` | Tingkat Pengangguran Terbuka Menurut Provinsi (var 543) | Tenaga Kerja | 2026 (Februari) | [BPS](https://www.bps.go.id/id/statistics-table/2/NTQzIzI=/tingkat-pengangguran-terbuka-menurut-provinsi.html) | 2026-10-17 |
| 2 | `TODO` | Pengangguran Terbuka Menurut Pendidikan Tertinggi yang Ditamatkan | Tenaga Kerja | 2025 | [BPS](https://www.bps.go.id/id/statistics-table/2/Njc0IzI=/pengangguran-terbuka-menurut-pendidikan-tertinggi-yang-ditamatkan.html) | 2026-10-17 |

## Catatan Definisi

**Rumus TPT (berlaku untuk kedua tabel):**

```
TPT = (Pengangguran / Angkatan Kerja) × 100%
```

| No | Catatan |
|----|---------|
| 1 | Data diambil dari payload SSR BPS (sampel 1 periode). |
| 2 | Data diambil dari payload SSR BPS (sampel 1 periode). |
