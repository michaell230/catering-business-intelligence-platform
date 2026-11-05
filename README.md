# 🍱 Dashboard Analitik Penjualan & Manajemen Pesanan Nabila Catering
### Program Mahasiswa Berdampak — Studi Independen Bersertifikat PT Vinix Seven Aurum (Vinix7)
**Disusun oleh:** Mahasiswa S1 Sains Data, Universitas Negeri Surabaya (UNESA)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📌 Ringkasan Proyek

Repositori ini berisi sistem intelijen bisnis (*Business Intelligence*) dan otomasi analitik penjualan berbiaya Rp 0 (*Zero-Cost Data Pipeline*) yang dikembangkan untuk memodernisasi tata kelola operasional pada **UMKM Nabila Catering** (Jombang, Jawa Timur). 

Sistem ini mentransformasikan alur pencatatan pesanan fisik kertas manual menjadi sistem digital terpadu, memantau omzet penjualan dan realisasi pesanan, mengawal antrean dapur (*kitchen workflow*), mengidentifikasi menu terlaris (*menu engineering*), serta melakukan segmentasi pelanggan **B2B (Institusi/Sekolah) vs B2C (Perorangan)** dengan model **RFM (*Recency, Frequency, Monetary*)**.

---

## 📂 Struktur Direktori Proyek

```text
Proyek Stupen/
│
├── .streamlit/
│   ├── config.toml           # Konfigurasi antarmuka tema gelap & server Streamlit
│   └── user_settings.json    # Menyimpan preferensi pengguna (mode sumber data & URL)
│
├── data/
│   ├── historis_transaksi_catering.csv  # Basis data transaksi utama (1.200 baris riil 2025)
│   └── master_menu.csv                  # Katalog referensi 26 menu makanan & harga satuan baku
│
├── notebooks/
│   └── eda_analitik_nabila_catering.ipynb # Analisis eksplorasi data (EDA) & pemodelan RFM
│
├── scripts/
│   └── validasi_data.py      # Skrip verifikasi integritas skema data & kalkulasi matematika
│
├── app.py                    # Aplikasi web dashboard interaktif Streamlit (6 Modul Utama)
├── requirements.txt          # Daftar pustaka dependensi Python untuk instalasi
├── .gitignore                # Berkas pengecualian Git agar berkas cache tidak terunggah
└── README.md                 # Panduan komprehensif penggunaan dan dokumentasi sistem
```

### Penjelasan Fungsi Berkas Utama:
* **`app.py`**: Berkas inti aplikasi web. Memuat 6 tab analitik interaktif, grafik visualisasi Plotly, filter dinamis multi-dimensi, formulir pencatatan pesanan digital, serta integrasi webhook awan.
* **`data/historis_transaksi_catering.csv`**: Basis data transaksi katering sepanjang tahun 2025 (1.200 transaksi, Rp 1,77 Miliar omzet).
* **`data/master_menu.csv`**: Daftar master menu resmi (Paket Nasi, Lauk Satuan, Paket Acara/Tumpeng) lengkap dengan kode menu dan harga standar.
* **`scripts/validasi_data.py`**: Utilitas terminal untuk memastikan tidak ada ID pesanan ganda, format tanggal seragam, dan perkalian omzet valid sebelum aplikasi dijalankan.
* **`notebooks/eda_analitik_nabila_catering.ipynb`**: Lembar kerja riset sains data yang mendokumentasikan pembuktian matematis metrik finansial dan algoritma segmentasi pelanggan.

---

## 🧭 Fitur & Modul Dashboard (`app.py`)

Dashboard dirancang dengan 6 modul utama:
1. **Ringkasan Finansial:** Scorecard metrik KPI (Total Omzet, Realisasi Selesai, Total Porsi Terjual, Average Order Value/AOV), grafik tren omzet fleksibel (**Harian, Mingguan, Bulanan**), serta diagram komposisi status pesanan.
2. **Analisis Menu:** Peringkat 10 menu terlaris berdasarkan volume porsi (*volume drivers*), 10 menu penyumbang omzet terbesar (*revenue drivers*), dan peta panas (*Heatmap*) tren musiman kategori menu per bulan.
3. **Antrean Dapur:** Pemantauan daftar pesanan yang sedang diproses (*lead time* pengerjaan dapur) dan tombol unduh berkas operasional kerja dapur (*Kitchen Work Order CSV*).
4. **Segmentasi Pelanggan:** Pengelompokan pelanggan menggunakan model RFM. Memetakan sebaran pelanggan setia institusi (B2B) dan pembeli eceran/hajatan (B2C) yang dapat disesuaikan menurut rentang tanggal filter aktif.
5. **Input Pesanan & Katalog Menu:** Formulir pencatatan pesanan masuk kasir (*Order Intake*) dengan fitur kalkulasi harga instan, fitur pembaruan status pesanan (*Upsert: update in-place* tanpa baris ganda), serta manajemen tambah/hapus menu makanan.
6. **Panduan Sistem:** Panduan ringkas operasional sistem dan dokumentasi bagi staf katering.

---

## 🌐 Panduan Sumber Data (Mode Ganda / Hybrid)

Aplikasi mendukung mode ganda yang dapat dialihkan sewaktu-waktu melalui menu bilah samping (**Sidebar**):

### 1. Mode Google Sheets (Cloud Live)
Digunakan saat presentasi, pengawasan jarak jauh oleh pemilik usaha, atau pencatatan kolaboratif antar-perangkat secara daring.
* **Cara Menggunakan:**
  1. Pilih opsi **`Google Sheets`** di sidebar kiri.
  2. Tempelkan (*paste*) URL Google Sheets Anda pada kotak input yang tersedia.
* **Ketentuan Google Sheets:**
  * Hak akses spreadsheet wajib diatur publik: **"Anyone with the link can view"** (*Siapa saja yang memiliki link dapat melihat*).
  * Struktur tabel di Google Sheets **wajib memiliki 11 kolom baku** yang urutannya sesuai dengan ketentuan skema di bawah.
* **Integrasi Otomatis (Google Apps Script):**
  Agar pesanan yang diinput lewat dashboard langsung otomatis tertulis ke Google Sheets secara *real-time*, pasang skrip Web App di Google Sheets melalui menu *Extensions -> Apps Script* (kode dan tata caranya tersedia lengkap di Tab 5 sub-tab *Integrasi Apps Script*).

### 2. Mode Lokal (File CSV)
Digunakan untuk operasional kasir harian di lokasi dapur tanpa bergantung pada koneksi internet (*offline-ready*).
* **Cara Menggunakan:**
  1. Pilih opsi **`Lokal (CSV)`** di sidebar kiri.
  2. Sistem akan membaca dan menyimpan langsung ke berkas `data/historis_transaksi_catering.csv`.
* **Keunggulan:** Sangat cepat, tidak memerlukan izin akses cloud, dan data tersimpan aman di penyimpanan fisik komputer.

---

## 📋 Ketentuan Skema Data (11 Kolom Baku)

Baik pada berkas CSV lokal maupun Google Sheets, kolom tabel transaksi **wajib mengikuti format standar berikut**:

| No | Nama Kolom | Tipe Data | Contoh Nilai | Keterangan |
| :---: | :--- | :---: | :--- | :--- |
| 1 | `ID_Pesanan` | Teks / String | `CTR1201` | Pengenal unik pesanan (tidak boleh duplikat). |
| 2 | `Nama_Pemesan` | Teks / String | `MAN 2 Jombang` | Nama perorangan atau nama instansi/sekolah. |
| 3 | `Tanggal_Pesanan` | Tanggal / Date | `2025-10-15` | Format baku: `YYYY-MM-DD`. |
| 4 | `Tanggal_Selesai` | Tanggal / Date | `2025-10-17` | Tanggal acara/pengiriman (`YYYY-MM-DD`). |
| 5 | `Kode_Menu` | Teks / String | `PN01` | Kode unik referensi menu katering. |
| 6 | `Kategori_Pesanan` | Teks / String | `Paket Nasi` | Pilihan: *Paket Nasi*, *Lauk Satuan*, *Paket Acara*. |
| 7 | `Nama_Menu` | Teks / String | `Nasi Kotak Ayam Kampung` | Nama hidangan yang dipesan. |
| 8 | `Jumlah_Pesanan` | Angka Bulat | `50` | Total porsi / kotak yang dipesan. |
| 9 | `Harga_Satuan` | Angka Bulat | `35000` | Harga per porsi dalam Rupiah (tanpa titik/koma). |
| 10 | `Total_Penjualan` | Angka Bulat | `1750000` | Hasil kali `Jumlah_Pesanan` × `Harga_Satuan`. |
| 11 | `Status_Pesanan` | Teks / String | `Selesai` | Status operasional: *Diproses* atau *Selesai*. |

---

## ⚙️ Cara Menjalankan Aplikasi di Komputer Lokal

### 1. Prasyarat Sistem
* Python versi 3.10 atau yang lebih baru.
* Git terpasang di komputer.

### 2. Langkah Instalasi & Menjalankan

1. **Buka Terminal / Command Prompt / PowerShell:**
   Masuk ke direktori proyek:
   ```bash
   cd "D:\ckone data\Stupen Vinix7\Proyek Stupen"
   ```

2. **(Opsional) Buat & Aktifkan Virtual Environment:**
   ```bash
   python -m venv venv
   # Di Windows:
   venv\Scripts\activate
   # Di Mac/Linux:
   source venv/bin/activate
   ```

3. **Pasang Dependensi Pustaka Python:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Uji Validitas Integritas Data:**
   ```bash
   python scripts/validasi_data.py
   ```
   *Pastikan hasil validasi menampilkan seluruh indikator `[OK]`.*

5. **Jalankan Dashboard Streamlit:**
   ```bash
   streamlit run app.py
   ```
   Aplikasi akan otomatis terbuka pada peramban web di alamat: `http://localhost:8501`.

---

## 🚀 Panduan Deployment ke GitHub & Streamlit Community Cloud

### Langkah 1: Push Repositori ke GitHub
1. Inisialisasi repositori Git dan unggah berkas:
   ```bash
   git init
   git add .
   git commit -m "feat: inisialisasi sistem analitik dan BI Nabila Catering"
   ```
2. Hubungkan ke repositori GitHub Anda dan lakukan push:
   ```bash
   git branch -M main
   git remote add origin https://github.com/USERNAME_ANDA/NAMA_REPOSITORY.git
   git push -u origin main
   ```

### Langkah 2: Deploy ke Streamlit Community Cloud (Gratis)
1. Buka laman **[share.streamlit.io](https://share.streamlit.io)** dan masuk (*login*) menggunakan akun GitHub Anda.
2. Klik tombol **New app**.
3. Atur konfigurasi deployment:
   * **Repository:** Pilih repositori GitHub yang baru saja di-push.
   * **Branch:** `main`
   * **Main file path:** `app.py`
4. Klik **Deploy!** Dalam kurun waktu 1–2 menit, dashboard Anda akan aktif online dengan URL publik yang dapat diakses dari smartphone maupun laptop.

---

## 🎓 Relevansi Konversi Akademik (10 SKS UNESA)
Proyek ini memenuhi capaian pembelajaran pada 5 mata kuliah konversi:
* **Perencanaan Stupen (2 SKS):** Analisis kebutuhan mitra, perumusan WBS, dan arsitektur data *zero-cost*.
* **Evaluasi Stupen (2 SKS):** Validasi integritas data, pengujian performa katering, dan audit metrik finansial.
* **Bisnis Digital (2 SKS):** Transformasi digital kasir, pemodelan *Customer Lifetime Value*, segmentasi RFM, dan kesiapan *Data Mart* Power BI.
* **Berpikir Kreatif (2 SKS):** Rekayasa alur kerja terpadu Google Sheets & Streamlit tanpa beban biaya langganan ERP.
* **Tata Tulis Ilmiah (2 SKS):** Dokumentasi teknis terstruktur, standarisasi kode, dan penyusunan naskah laporan akhir.

---
**Nabila Catering — Kelezatan Rasa, Ketepatan Waktu, dan Modernitas Tata Kelola Boga.**
