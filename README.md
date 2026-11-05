# Catering Business Intelligence & Operations Platform
> An End-to-End Sales Analytics, Kitchen Workflow, and RFM Customer Segmentation Platform for Culinary Enterprises.

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-Streamlit-red.svg)](https://streamlit.io)
[![Data Engine](https://img.shields.io/badge/Engine-Pandas%20%7C%20Plotly-teal.svg)](https://pandas.pydata.org/)
[![Architecture](https://img.shields.io/badge/Architecture-Hybrid%20Cloud-success.svg)](#arsitektur-sistem)
[![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)](LICENSE)

---

## Ringkasan Eksekutif

Platform ini adalah sistem intelijen bisnis (*Business Intelligence*) dan manajemen operasional terintegrasi yang dirancang untuk industri jasa boga (*culinary & catering services*). Sistem ini mengotomasi siklus bisnis hulu-ke-hilir: mulai dari pencatatan pesanan kasir (*Order Intake*), pengendalian antrean dapur (*Kitchen Operations*), analitik kinerja finansial multi-periode, hingga pemodelan segmentasi pelanggan strategis berbasis algoritma **RFM (*Recency, Frequency, Monetary*)**.

Dibangun di atas arsitektur data hibrida berbiaya pemeliharaan nol (*Zero-Cost Data Pipeline*), platform ini dapat beroperasi penuh secara lokal (offline) maupun terhubung langsung ke basis data awan (*Google Cloud Ecosystem*) secara real-time.

### Metrik Sistem Terkelola:
* **Volume Transaksi:** 1.200+ Pesanan Terdata
* **Akumulasi Omzet:** Rp 1,77 Miliar
* **Volume Produksi:** 67.500+ Porsi Hidangan
* **Katalog Produk:** 26 Item Master Menu Aktif

---

## Arsitektur Sistem

Platform dirancang modular menggunakan alur data terintegrasi:

```text
[ Front-end Order Intake ] ──► [ Storage Engine (Local CSV / Google Sheets) ]
                                          │
                                          ▼
[ BI Dashboard Platform ] ◄── [ Analytics Engine (Pandas, Plotly, RFM) ]
          │
          └──► [ Data Mart Export (Power BI / Excel Ready) ]
```

1. **Transaction Capture:** Formulir pemesanan reaktif dengan kalkulasi otomatis dan proteksi baris ganda (*Upsert mechanism*).
2. **Dual-Mode Data Engine:** Fleksibilitas peralihan instan antara *Local Storage* dan *Cloud Live Spreadsheet*.
3. **Analytical Processing:** Pemrosesan agregasi omzet harian/mingguan/bulanan, perhitungan *lead time*, dan klasterisasi RFM.
4. **Decision Support Dashboard:** Antarmuka visual analitik interaktif yang dioptimalkan untuk perangkat seluler maupun desktop.

---

## Struktur Direktori

```text
catering-business-intelligence-platform/
│
├── .streamlit/
│   ├── config.toml                     # Konfigurasi tema visual dan server Streamlit
│   └── user_settings.json              # State persistensi preferensi sumber data
│
├── data/
│   ├── historis_transaksi_catering.csv # Basis data historis transaksi utama
│   └── master_menu.csv                 # Katalog master menu, kode produk, dan harga satuan
│
├── notebooks/
│   └── eda_analitik_nabila_catering.ipynb # Lembar kerja analisis eksplorasi data (EDA) & RFM
│
├── scripts/
│   └── validasi_data.py                # Utilitas audit integritas skema data & kalkulasi matematis
│
├── app.py                              # Entry-point aplikasi web dashboard utama
├── requirements.txt                    # Dependensi paket Python lingkungan produksi
├── .gitignore                          # Konfigurasi pengecualian direktori Git
└── README.md                           # Dokumentasi teknis platform
```

---

## Modul Analitik & Fungsionalitas

### 1. Ringkasan Kinerja Finansial
* **Metrik Utama (KPIs):** Pemantauan *Total Omzet*, *Realisasi Omzet Selesai*, *Total Porsi Terjual*, dan *Average Order Value (AOV)*.
* **Granularitas Waktu Fleksibel:** Grafik tren omzet yang dapat dialihkan secara dinamis antara agregasi **Harian**, **Mingguan**, dan **Bulanan**.
* **Distribusi Status Transaksi:** Visualisasi komposisi status pesanan (*Selesai*, *Diproses*, *Dibatalkan*).

### 2. Analisis Menu (Menu Engineering)
* **Volume vs Revenue Drivers:** Peringkat 10 menu dengan kuantitas porsi terbanyak versus 10 menu kontributor pendapatan terbesar.
* **Seasonal Heatmap:** Matriks pola musiman pesanan per kategori menu (*Paket Nasi*, *Lauk Satuan*, *Paket Acara*) sepanjang periode kalender.

### 3. Pemantauan Antrean Dapur & Operasional
* **Work Order Queue:** Pengawalan pesanan berstatus *Diproses* untuk memastikan pemenuhan waktu persiapan (*Lead Time*).
* **Ekspor Lembar Kerja:** Tombol unduh satu-klik berkas operasional dapur berformat CSV untuk staf produksi.

### 4. Segmentasi Pelanggan (Customer Intelligence)
* **Algoritma RFM:** Pengelompokan pelanggan berdasarkan keterkinian belanja (*Recency*), tingkat loyalitas (*Frequency*), dan nilai pengeluaran (*Monetary*).
* **Klasifikasi Entitas:** Pemisahan otomatis antara klien institusi/sekolah (**B2B**) dan pelanggan perorangan (**B2C**).
* **Filter Waktu Responsif:** Segmentasi dapat dievaluasi menurut rentang filter tanggal aktif maupun riwayat kumulatif.

### 5. Input Pesanan & Manajemen Master Menu
* **Pencatatan Pesanan (Order Intake):** Validasi input real-time, pencarian harga dinamis, dan kalkulasi tagihan otomatis.
* **Pembaruan Data In-Place (Upsert):** Fitur edit pesanan yang langsung memperbarui baris bersangkutan tanpa menyebabkan duplikasi data finansial.
* **Katalog Master Menu:** Antarmuka penambahan dan penghapusan item hidangan, kategori, serta pembaruan harga standar.

### 6. Panduan Sistem
* Dokumentasi internal yang disematkan langsung di dalam aplikasi untuk kemudahan operasional staf.

---

## Integrasi Sumber Data (Hybrid Architecture)

Platform mendukung dua metode penyimpanan data yang dapat dipilih melalui bilah menu samping (*sidebar*):

### Mode 1: Google Sheets (Cloud Live)
Dirancang untuk pelaporan terpusat dan akses multi-pengguna via internet.
* **Mekanisme Baca:** Menggunakan endpoint publik Google Visualization API (GViz) berkecepatan tinggi tanpa beban kuota berbayar.
* **Mekanisme Tulis (Otomatis):** Mendukung webhook *Google Apps Script (Web App)* untuk menuliskan pesanan baru langsung ke spreadsheet online secara real-time.
* **Ketentuan Akses:** Tautan Google Sheets wajib diatur dengan izin visibilitas: *"Anyone with the link can view"*.

### Mode 2: Lokal (File CSV)
Dirancang untuk keandalan operasional kasir harian di lokasi fisik tanpa ketergantungan jaringan internet.
* **Mekanisme:** Operasi baca dan tulis langsung dieksekusi ke berkas `data/historis_transaksi_catering.csv`.
* **Ketahanan:** Menyediakan cadangan (*backup*) data deterministik di penyimpanan lokal komputer.

---

## Skema Data Baku (Data Schema)

Seluruh sumber data (baik CSV lokal maupun Google Sheets) wajib memenuhi struktur 11 kolom baku berikut:

| No | Field | Tipe Data | Format / Nilai | Deskripsi |
| :---: | :--- | :---: | :--- | :--- |
| 1 | `ID_Pesanan` | String | `CTR0001` | Kunci primer unik tiap transaksi |
| 2 | `Nama_Pemesan` | String | Teks Bebas | Nama pelanggan individu atau institusi |
| 3 | `Tanggal_Pesanan` | Date | `YYYY-MM-DD` | Tanggal pesanan masuk ke sistem |
| 4 | `Tanggal_Selesai` | Date | `YYYY-MM-DD` | Tanggal pengiriman hidangan / acara |
| 5 | `Kode_Menu` | String | `PN01`, `LS01`, `PA01` | Kode klasifikasi katalog hidangan |
| 6 | `Kategori_Pesanan` | String | `Paket Nasi`, `Lauk Satuan`, `Paket Acara` | Kategori utama menu makanan |
| 7 | `Nama_Menu` | String | Teks Bebas | Nama varian menu yang dipesan |
| 8 | `Jumlah_Pesanan` | Integer | $\ge 1$ | Kuantitas porsi pesanan |
| 9 | `Harga_Satuan` | Integer | Angka Numerik | Tarif per porsi dalam Rupiah |
| 10 | `Total_Penjualan` | Integer | `Jumlah_Pesanan` × `Harga_Satuan` | Total nominal nilai transaksi |
| 11 | `Status_Pesanan` | String | `Diproses` atau `Selesai` | Status operasional pesanan |

---

## Panduan Instalasi & Menjalankan Sistem

### 1. Prasyarat Lingkungan
* Python 3.10 atau versi di atasnya
* Git CLI

### 2. Langkah Instalasi

1. **Kloning Repositori:**
   ```bash
   git clone https://github.com/USERNAME/catering-business-intelligence-platform.git
   cd catering-business-intelligence-platform
   ```

2. **Siapkan Virtual Environment (Disarankan):**
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # macOS / Linux:
   source venv/bin/activate
   ```

3. **Instalasi Dependensi:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verifikasi Integritas Data:**
   Jalankan skrip audit untuk memastikan kepatuhan skema dan kalkulasi numerik:
   ```bash
   python scripts/validasi_data.py
   ```

5. **Jalankan Aplikasi:**
   ```bash
   streamlit run app.py
   ```
   Akses antarmuka melalui peramban di `http://localhost:8501`.

---

## Panduan Deployment ke Cloud

Platform siap di-deploy secara instan ke **Streamlit Community Cloud**:

1. Pastikan seluruh perubahan kode telah di-commit ke repositori GitHub:
   ```bash
   git add .
   git commit -m "feat: production release of catering BI platform"
   git push origin main
   ```
2. Buka portal **[share.streamlit.io](https://share.streamlit.io)** dan hubungkan dengan akun GitHub Anda.
3. Klik **New app**, pilih repositori proyek ini, atur Branch ke `main`, dan set Main file path ke `app.py`.
4. Klik **Deploy**. Aplikasi akan online dengan URL publik dalam hitungan menit.

---

## Lisensi

Proyek ini didistribusikan di bawah lisensi terbuka [MIT License](LICENSE).
