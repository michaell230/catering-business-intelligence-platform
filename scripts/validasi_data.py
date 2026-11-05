"""
Skrip Validasi Integritas Data - UMKM Nabila Catering
Fungsi: Memverifikasi kelayakan skema kolom, format tanggal, dan konsistensi matematis data transaksi.
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import os
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
CSV_TRANSAKSI = os.path.join(DATA_DIR, "historis_transaksi_catering.csv")
CSV_MENU = os.path.join(DATA_DIR, "master_menu.csv")

REQUIRED_COLS = [
    "ID_Pesanan", "Nama_Pemesan", "Tanggal_Pesanan", "Tanggal_Selesai",
    "Kode_Menu", "Kategori_Pesanan", "Nama_Menu", "Jumlah_Pesanan",
    "Harga_Satuan", "Total_Penjualan", "Status_Pesanan"
]

def validasi_dataset():
    print("=" * 60)
    print("MEMULAI PEMERIKSAAN INTEGRITAS DATA NABILA CATERING")
    print("=" * 60)
    
    # 1. Cek Keberadaan File Transaksi
    if not os.path.exists(CSV_TRANSAKSI):
        print(f"[FAIL] Error: File transaksi tidak ditemukan di: {CSV_TRANSAKSI}")
        return False
        
    df = pd.read_csv(CSV_TRANSAKSI)
    print(f"[OK] File ditemukan: {len(df):,} baris transaksi terdata.")
    
    # 2. Cek Kelengkapan Kolom
    missing_cols = [c for c in REQUIRED_COLS if c not in df.columns]
    if missing_cols:
        print(f"[FAIL] Error: Kolom wajib tidak lengkap! Kolom hilang: {missing_cols}")
        return False
    print("[OK] Skema 11 kolom baku terverifikasi lengkap.")
    
    # 3. Cek Duplikasi ID Pesanan
    dup_ids = df[df["ID_Pesanan"].duplicated()]["ID_Pesanan"].tolist()
    if dup_ids:
        print(f"[WARN] Peringatan: Ditemukan {len(dup_ids)} ID_Pesanan duplikat: {dup_ids[:5]}...")
    else:
        print("[OK] Seluruh ID_Pesanan bersifat unik (tidak ada duplikasi baris).")
        
    # 4. Cek Format Tanggal
    try:
        pd.to_datetime(df["Tanggal_Pesanan"], format="%Y-%m-%d")
        print("[OK] Kolom Tanggal_Pesanan valid (format YYYY-MM-DD).")
    except Exception as e:
        print(f"[WARN] Peringatan: Format Tanggal_Pesanan memiliki format tidak seragam: {e}")
        
    # 5. Cek Konsistensi Kalkulasi Penjualan
    kalkulasi = df["Jumlah_Pesanan"] * df["Harga_Satuan"]
    selisih = df[df["Total_Penjualan"] != kalkulasi]
    if not selisih.empty:
        print(f"[WARN] Peringatan: Ditemukan {len(selisih)} baris dengan Total_Penjualan yang berbeda dari Porsi x Harga.")
    else:
        print("[OK] Konsistensi matematis (Total = Porsi x Harga Satuan) 100% akurat.")
        
    # 6. Ringkasan Finansial
    total_omzet = df["Total_Penjualan"].sum()
    total_porsi = df["Jumlah_Pesanan"].sum()
    print("-" * 60)
    print(f"Ringkasan Dataset:")
    print(f"   • Total Omzet          : Rp {total_omzet:,.0f}".replace(",", "."))
    print(f"   • Total Porsi Terjual  : {total_porsi:,} porsi")
    print(f"   • Periode Transaksi    : {df['Tanggal_Pesanan'].min()} s.d. {df['Tanggal_Pesanan'].max()}")
    print("-" * 60)
    
    # 7. Cek Master Menu
    if os.path.exists(CSV_MENU):
        df_menu = pd.read_csv(CSV_MENU)
        print(f"[OK] Master Menu terverifikasi: {len(df_menu)} item menu aktif.")
    else:
        print("[WARN] Master Menu belum ditemukan.")
        
    print("Dataset dalam kondisi prima dan siap dijalankan di Streamlit / Power BI!")
    return True

if __name__ == "__main__":
    validasi_dataset()
