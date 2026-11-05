import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
import json
import requests
import io
import re

# ==============================================================================
# 1. KONFIGURASI HALAMAN & TEMA STREAMLIT
# ==============================================================================
st.set_page_config(
    page_title="Business Intelligence & Analitik Penjualan Nabila Catering",
    page_icon="🍱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS elegan bertema Modern Dark Slate & Emerald Gold
st.markdown("""
<style>
    /* Kartu Metrik / Indikator Angka */
    div[data-testid="stMetric"] {
        background-color: #1E293B;
        border: 1px solid #334155;
        padding: 16px 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        border-color: #10B981;
    }
    div[data-testid="stMetric"] label {
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        color: #94A3B8 !important;
    }
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        font-size: 1.65rem !important;
        font-weight: 800 !important;
        color: #F8FAFC !important;
    }
    
    /* Header Utama Dashboard */
    .header-box {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 16px 22px;
        margin-bottom: 20px;
    }
    .header-title {
        font-size: 1.55rem;
        font-weight: 700;
        color: #F8FAFC;
        margin: 0;
    }
</style>
""", unsafe_allow_html=True)

# Path File Data & Pengaturan
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
CSV_TRANSAKSI = os.path.join(DATA_DIR, "historis_transaksi_catering.csv")
CSV_MASTER_MENU = os.path.join(DATA_DIR, "master_menu.csv")
SETTINGS_FILE = os.path.join(BASE_DIR, ".streamlit", "user_settings.json")

DEFAULT_SETTINGS = {
    "source_type": "Google Sheets",
    "sheet_url": "https://docs.google.com/spreadsheets/d/1GM4ZSZ1_kdSYIGcbYWpojG_Z5lvRIiLwafxNH0iyE5o/edit?gid=946040988#gid=946040988",
    "script_url": ""
}

# ==============================================================================
# 2. PENGELOLAAN PREFERENSI PENGGUNA (PERSISTENSI SETTINGS)
# ==============================================================================
def load_user_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                saved = json.load(f)
                return {**DEFAULT_SETTINGS, **saved}
        except Exception:
            pass
    return DEFAULT_SETTINGS.copy()

def save_user_settings(settings_dict):
    try:
        os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(settings_dict, f, indent=2)
    except Exception:
        pass

# Ekstraksi URL CSV Google Sheets (GViz API)
def extract_gviz_url(sheet_url):
    if not sheet_url or not isinstance(sheet_url, str):
        return None
    match_id = re.search(r"/spreadsheets/d/([a-zA-Z0-9-_]+)", sheet_url)
    if not match_id:
        return None
    sheet_id = match_id.group(1)
    match_gid = re.search(r"[#&?]gid=([0-9]+)", sheet_url)
    gid = match_gid.group(1) if match_gid else "0"
    return f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&gid={gid}"

# ==============================================================================
# 3. PENGELOLAAN MASTER MENU
# ==============================================================================
def load_master_menu():
    if os.path.exists(CSV_MASTER_MENU):
        try:
            return pd.read_csv(CSV_MASTER_MENU)
        except Exception:
            pass
            
    default_menus = [
        {"Kode_Menu": "PN01", "Kategori_Pesanan": "Paket Nasi", "Nama_Menu": "Nasi Kotak Ayam Kampung", "Harga_Satuan": 35000, "Status": "Tersedia"},
        {"Kode_Menu": "PN02", "Kategori_Pesanan": "Paket Nasi", "Nama_Menu": "Nasi Kuning", "Harga_Satuan": 35000, "Status": "Tersedia"},
        {"Kode_Menu": "PN03", "Kategori_Pesanan": "Paket Nasi", "Nama_Menu": "Nasi Bento", "Harga_Satuan": 20000, "Status": "Tersedia"},
        {"Kode_Menu": "PN04", "Kategori_Pesanan": "Paket Nasi", "Nama_Menu": "Nasi Ayam Bakar", "Harga_Satuan": 25000, "Status": "Tersedia"},
        {"Kode_Menu": "PN05", "Kategori_Pesanan": "Paket Nasi", "Nama_Menu": "Nasi Ayam Goreng Lengkuas", "Harga_Satuan": 25000, "Status": "Tersedia"},
        {"Kode_Menu": "PN06", "Kategori_Pesanan": "Paket Nasi", "Nama_Menu": "Nasi Ayam Goreng Upin-Ipin", "Harga_Satuan": 23000, "Status": "Tersedia"},
        {"Kode_Menu": "PN07", "Kategori_Pesanan": "Paket Nasi", "Nama_Menu": "Nasi Rendang Lapis", "Harga_Satuan": 35000, "Status": "Tersedia"},
        {"Kode_Menu": "PN08", "Kategori_Pesanan": "Paket Nasi", "Nama_Menu": "Nasi Mujair Sambal", "Harga_Satuan": 25000, "Status": "Tersedia"},
        {"Kode_Menu": "LS01", "Kategori_Pesanan": "Lauk Satuan", "Nama_Menu": "Ayam Bakar", "Harga_Satuan": 18000, "Status": "Tersedia"},
        {"Kode_Menu": "LS02", "Kategori_Pesanan": "Lauk Satuan", "Nama_Menu": "Ayam Goreng Lengkuas", "Harga_Satuan": 18000, "Status": "Tersedia"},
        {"Kode_Menu": "LS03", "Kategori_Pesanan": "Lauk Satuan", "Nama_Menu": "Ayam Goreng Upin-Ipin", "Harga_Satuan": 16000, "Status": "Tersedia"},
        {"Kode_Menu": "LS04", "Kategori_Pesanan": "Lauk Satuan", "Nama_Menu": "Ayam Teriyaki", "Harga_Satuan": 18000, "Status": "Tersedia"},
        {"Kode_Menu": "LS05", "Kategori_Pesanan": "Lauk Satuan", "Nama_Menu": "Ayam Kecap", "Harga_Satuan": 17000, "Status": "Tersedia"},
        {"Kode_Menu": "LS06", "Kategori_Pesanan": "Lauk Satuan", "Nama_Menu": "Rendang Daging", "Harga_Satuan": 28000, "Status": "Tersedia"},
        {"Kode_Menu": "LS07", "Kategori_Pesanan": "Lauk Satuan", "Nama_Menu": "Ayam Bali", "Harga_Satuan": 18000, "Status": "Tersedia"},
        {"Kode_Menu": "LS08", "Kategori_Pesanan": "Lauk Satuan", "Nama_Menu": "Mujair Goreng", "Harga_Satuan": 20000, "Status": "Tersedia"},
        {"Kode_Menu": "LS09", "Kategori_Pesanan": "Lauk Satuan", "Nama_Menu": "Pepes Pindang", "Harga_Satuan": 15000, "Status": "Tersedia"},
        {"Kode_Menu": "LS10", "Kategori_Pesanan": "Lauk Satuan", "Nama_Menu": "Perkedel Kentang", "Harga_Satuan": 5000, "Status": "Tersedia"},
        {"Kode_Menu": "LS11", "Kategori_Pesanan": "Lauk Satuan", "Nama_Menu": "Bakwan Jagung", "Harga_Satuan": 5000, "Status": "Tersedia"},
        {"Kode_Menu": "LS12", "Kategori_Pesanan": "Lauk Satuan", "Nama_Menu": "Tahu Tempe Bacem", "Harga_Satuan": 7000, "Status": "Tersedia"},
        {"Kode_Menu": "LS13", "Kategori_Pesanan": "Lauk Satuan", "Nama_Menu": "Telur Balado", "Harga_Satuan": 8000, "Status": "Tersedia"},
        {"Kode_Menu": "LS14", "Kategori_Pesanan": "Lauk Satuan", "Nama_Menu": "Telur Dadar Tebal", "Harga_Satuan": 10000, "Status": "Tersedia"},
        {"Kode_Menu": "PA01", "Kategori_Pesanan": "Paket Acara", "Nama_Menu": "Nasi Tumpeng Mini", "Harga_Satuan": 45000, "Status": "Tersedia"},
        {"Kode_Menu": "PA02", "Kategori_Pesanan": "Paket Acara", "Nama_Menu": "Nasi Tumpeng 10 Porsi", "Harga_Satuan": 350000, "Status": "Tersedia"},
        {"Kode_Menu": "PA03", "Kategori_Pesanan": "Paket Acara", "Nama_Menu": "Nasi Tumpeng 20 Porsi", "Harga_Satuan": 650000, "Status": "Tersedia"},
        {"Kode_Menu": "PA04", "Kategori_Pesanan": "Paket Acara", "Nama_Menu": "Nasi Tumpeng 30 Porsi", "Harga_Satuan": 950000, "Status": "Tersedia"}
    ]
    df_def = pd.DataFrame(default_menus)
    df_def.to_csv(CSV_MASTER_MENU, index=False)
    return df_def

def save_master_menu(df_menu):
    df_menu.to_csv(CSV_MASTER_MENU, index=False)

# ==============================================================================
# 4. PEMBERSIHAN DATA & PIPELINE ANALITIK
# ==============================================================================
def clean_and_format_data(df):
    if df is None or df.empty:
        return pd.DataFrame()
    df = df.copy().dropna(how="all")
    
    col_mapping = {}
    for c in df.columns:
        clean_c = re.sub(r"\(.*?\)", "", str(c)).strip()
        clean_c = clean_c.replace(" ", "_").lower()
        if "id" in clean_c and "pesan" in clean_c:
            col_mapping[c] = "ID_Pesanan"
        elif "tanggal" in clean_c and "selesai" in clean_c:
            col_mapping[c] = "Tanggal_Selesai"
        elif "tanggal" in clean_c and ("pesan" in clean_c or "order" in clean_c):
            col_mapping[c] = "Tanggal_Pesanan"
        elif "nama" in clean_c and ("pemesan" in clean_c or "pelanggan" in clean_c or "klien" in clean_c):
            col_mapping[c] = "Nama_Pemesan"
        elif "kode" in clean_c and "menu" in clean_c:
            col_mapping[c] = "Kode_Menu"
        elif "kategori" in clean_c:
            col_mapping[c] = "Kategori_Pesanan"
        elif "nama" in clean_c and "menu" in clean_c:
            col_mapping[c] = "Nama_Menu"
        elif "jumlah" in clean_c or "porsi" in clean_c or "qty" in clean_c or "pcs" in clean_c:
            col_mapping[c] = "Jumlah_Pesanan"
        elif "harga" in clean_c or "satuan" in clean_c:
            col_mapping[c] = "Harga_Satuan"
        elif "total" in clean_c or "penjualan" in clean_c or "omzet" in clean_c or "biaya" in clean_c:
            col_mapping[c] = "Total_Penjualan"
        elif "status" in clean_c:
            col_mapping[c] = "Status_Pesanan"
    df = df.rename(columns=col_mapping)
    
    standard_cols = [
        "ID_Pesanan", "Nama_Pemesan", "Tanggal_Pesanan", "Tanggal_Selesai",
        "Kode_Menu", "Kategori_Pesanan", "Nama_Menu", "Jumlah_Pesanan",
        "Harga_Satuan", "Total_Penjualan", "Status_Pesanan"
    ]
    for sc in standard_cols:
        if sc not in df.columns:
            df[sc] = np.nan
            
    df["Tanggal_Pesanan"] = pd.to_datetime(df["Tanggal_Pesanan"], errors="coerce")
    df["Tanggal_Selesai"] = pd.to_datetime(df["Tanggal_Selesai"], errors="coerce")
    
    if "Timestamp" in df.columns:
        ts = pd.to_datetime(df["Timestamp"], errors="coerce")
        df["Tanggal_Pesanan"] = df["Tanggal_Pesanan"].fillna(ts)
        
    df["Tanggal_Pesanan"] = df["Tanggal_Pesanan"].fillna(pd.Timestamp.now())
    
    df["Jumlah_Pesanan"] = pd.to_numeric(df["Jumlah_Pesanan"], errors="coerce").fillna(1).astype(int)
    df["Harga_Satuan"] = pd.to_numeric(df["Harga_Satuan"], errors="coerce").fillna(0)
    df["Total_Penjualan"] = pd.to_numeric(df["Total_Penjualan"], errors="coerce")
    
    mask_calc = (df["Total_Penjualan"].isna()) | (df["Total_Penjualan"] == 0)
    df.loc[mask_calc, "Total_Penjualan"] = df.loc[mask_calc, "Jumlah_Pesanan"] * df.loc[mask_calc, "Harga_Satuan"]
    df["Total_Penjualan"] = df["Total_Penjualan"].fillna(0)
    
    df["Nama_Pemesan"] = df["Nama_Pemesan"].fillna("Pemesan Umum").astype(str).str.strip().str.title()
    df["Kategori_Pesanan"] = df["Kategori_Pesanan"].fillna("Paket Nasi").astype(str).str.strip()
    df["Nama_Menu"] = df["Nama_Menu"].fillna("Menu Standar").astype(str).str.strip()
    
    df["Status_Pesanan"] = df["Status_Pesanan"].fillna("Selesai").astype(str).str.strip()
    df["Status_Pesanan"] = df["Status_Pesanan"].replace({"Lunas": "Selesai", "Belum Lunas": "Diproses"})
    
    for i in range(len(df)):
        val_id = df.loc[df.index[i], "ID_Pesanan"]
        if pd.isna(val_id) or str(val_id).strip() in ["", "nan", "None"]:
            df.loc[df.index[i], "ID_Pesanan"] = f"CTR{i+1:04d}"
            
    df["Lead_Time_Days"] = (df["Tanggal_Selesai"] - df["Tanggal_Pesanan"]).dt.days
    df["Lead_Time_Days"] = df["Lead_Time_Days"].apply(lambda x: max(0, int(x)) if pd.notnull(x) and not np.isnan(x) else np.nan)
    
    inst_pattern = r"(man|sma|smk|smp|mts|ma\b|darul ulum|yayasan|kantor|instansi|dinas|dprd|desa|kecamatan|kelurahan|bank|bem|fakultas|kampus|sekolah)"
    df["Tipe_Klien"] = df["Nama_Pemesan"].apply(
        lambda x: "Institusi (B2B)" if re.search(inst_pattern, str(x), flags=re.IGNORECASE) else "Perorangan (B2C)"
    )
    
    df["Bulan_Tahun"] = df["Tanggal_Pesanan"].dt.to_period("M").astype(str)
    df["Bulan_Nama"] = df["Tanggal_Pesanan"].dt.strftime("%B")
    df["Tahun"] = df["Tanggal_Pesanan"].dt.year
    df["Kuartal"] = "Q" + df["Tanggal_Pesanan"].dt.quarter.astype(str)
    
    return df

# Caching Loader Data
@st.cache_data(ttl=10)
def fetch_google_sheets_data(gviz_url):
    try:
        res = requests.get(gviz_url, timeout=7)
        if res.status_code == 200:
            df = pd.read_csv(io.StringIO(res.text))
            return clean_and_format_data(df)
    except Exception:
        pass
    return None

@st.cache_data(ttl=10)
def fetch_local_csv_data():
    if os.path.exists(CSV_TRANSAKSI):
        try:
            df = pd.read_csv(CSV_TRANSAKSI)
            return clean_and_format_data(df)
        except Exception:
            pass
    return None

# ==============================================================================
# 5. INISIALISASI SETTINGS & PEMUATAN DATA AKTIF
# ==============================================================================
user_cfg = load_user_settings()
df_master_menu = load_master_menu()

# ==============================================================================
# 6. SIDEBAR: PENGATURAN SUMBER DATA & FILTER
# ==============================================================================
with st.sidebar:
    st.title("Nabila Catering")
    st.divider()
    
    # KONTROL PILIHAN SUMBER DATA
    st.subheader("Sumber Data")
    
    source_options = ["Google Sheets", "Lokal (CSV)"]
    current_idx = 0 if user_cfg["source_type"] == "Google Sheets" else 1
    
    selected_source_label = st.radio(
        "Pilih Sumber Data:",
        options=source_options,
        index=current_idx,
        help="Pilih apakah ingin membaca langsung dari Google Sheets online atau dari file CSV lokal."
    )
    
    new_source_type = "Google Sheets" if "Google Sheets" in selected_source_label else "Lokal"
    
    # Input URL jika memilih Google Sheets
    current_sheet_url = user_cfg.get("sheet_url", DEFAULT_SETTINGS["sheet_url"])
    current_script_url = user_cfg.get("script_url", "")
    
    if new_source_type == "Google Sheets":
        input_sheet_url = st.text_input(
            "URL Google Sheets:",
            value=current_sheet_url,
            help="Tempelkan link Google Sheets Anda di sini."
        )
        
        with st.expander("⚡ Webhook Apps Script (Auto-Sync Cloud)", expanded=bool(current_script_url)):
            input_script_url = st.text_input(
                "URL Google Apps Script Exec:",
                value=current_script_url,
                placeholder="https://script.google.com/macros/s/.../exec",
                help="Tempelkan URL Web App Google Apps Script untuk menyimpan pesanan langsung ke Google Sheets secara otomatis."
            )
            if current_script_url:
                st.caption("Status: Terhubung")
            else:
                st.caption("Status: Belum diatur")
                
        settings_changed = False
        if new_source_type != user_cfg.get("source_type"):
            user_cfg["source_type"] = new_source_type
            settings_changed = True
        if input_sheet_url.strip() != current_sheet_url:
            user_cfg["sheet_url"] = input_sheet_url.strip()
            settings_changed = True
        if input_script_url.strip() != current_script_url:
            user_cfg["script_url"] = input_script_url.strip()
            settings_changed = True
            
        if settings_changed:
            save_user_settings(user_cfg)
            st.cache_data.clear()
            st.rerun()
    else:
        if new_source_type != user_cfg.get("source_type"):
            user_cfg["source_type"] = new_source_type
            save_user_settings(user_cfg)
            st.cache_data.clear()
            st.rerun()

    # Memuat data berdasarkan sumber aktif
    df_raw = pd.DataFrame()
    data_source_status = ""
    
    if user_cfg["source_type"] == "Google Sheets":
        gviz_url = extract_gviz_url(user_cfg["sheet_url"])
        if gviz_url:
            df_raw = fetch_google_sheets_data(gviz_url)
            if df_raw is not None and not df_raw.empty:
                data_source_status = f"Data: {len(df_raw):,} Transaksi (Google Sheets)"
            else:
                st.error("⚠️ Gagal membaca Google Sheets. Periksa koneksi atau hak akses share link!")
                # Fallback otomatis ke data lokal jika gagal
                df_raw = fetch_local_csv_data()
                if df_raw is not None:
                    data_source_status = f"Data: {len(df_raw):,} Transaksi (Lokal Fallback)"
        else:
            st.error("⚠️ Format tautan Google Sheets tidak valid.")
    else:
        df_raw = fetch_local_csv_data()
        if df_raw is not None and not df_raw.empty:
            data_source_status = f"Data: {len(df_raw):,} Transaksi (Lokal CSV)"
        else:
            data_source_status = "🔴 Data lokal belum ditemukan."
            
    st.caption(data_source_status)
    
    if st.button("🔄 Muat Ulang Data (Refresh)", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
        
    st.divider()
    
    # FILTER ANALITIK
    st.subheader("Filter Data")
    if df_raw is not None and not df_raw.empty:
        min_date = df_raw["Tanggal_Pesanan"].min().date()
        max_date = df_raw["Tanggal_Pesanan"].max().date()
        date_range = st.date_input(
            "📅 Rentang Tanggal Pesanan:",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
        if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
            start_date, end_date = date_range
        else:
            start_date, end_date = min_date, max_date
            
        all_categories = sorted(df_raw["Kategori_Pesanan"].dropna().unique().tolist())
        selected_categories = st.multiselect(
            "Kategori Menu:",
            options=all_categories,
            default=all_categories
        )
        
        status_options = ["Semua"] + sorted(df_raw["Status_Pesanan"].dropna().unique().tolist())
        selected_status = st.selectbox("Status Pesanan:", status_options, index=0)
        
        client_options = ["Semua", "🏛️ Institusi / B2B", "👤 Perorangan / B2C"]
        selected_client = st.selectbox("👥 Tipe Pelanggan:", client_options, index=0)
        
        search_kw = st.text_input("🔎 Cari Menu / Pemesan:", placeholder="Ketik nama menu/pemesan...")
    
    st.divider()
    st.markdown("### 📊 Ekspor Data Mart")
    
    if df_raw is not None and not df_raw.empty:
        export_csv = df_raw.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Unduh Data Mart (Power BI Ready)",
            data=export_csv,
            file_name=f"datamart_nabila_catering_powerbi_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )

# Filter Data Berdasarkan Pilihan Sidebar
if df_raw is not None and not df_raw.empty:
    df_filtered = df_raw[
        (df_raw["Tanggal_Pesanan"].dt.date >= start_date) &
        (df_raw["Tanggal_Pesanan"].dt.date <= end_date) &
        (df_raw["Kategori_Pesanan"].isin(selected_categories))
    ].copy()
    
    if selected_status != "Semua":
        df_filtered = df_filtered[df_filtered["Status_Pesanan"] == selected_status]
        
    if selected_client != "Semua":
        df_filtered = df_filtered[df_filtered["Tipe_Klien"] == selected_client]
        
    if search_kw:
        mask_search = (
            df_filtered["Nama_Pemesan"].str.contains(search_kw, case=False, na=False) |
            df_filtered["Nama_Menu"].str.contains(search_kw, case=False, na=False) |
            df_filtered["ID_Pesanan"].str.contains(search_kw, case=False, na=False)
        )
        df_filtered = df_filtered[mask_search]
else:
    st.warning("⚠️ Basis data transaksi masih kosong. Silakan periksa koneksi Google Sheets atau file CSV lokal.")
    st.stop()

if df_filtered.empty:
    st.warning("⚠️ Tidak ada data transaksi yang sesuai dengan kombinasi filter yang dipilih.")
    st.stop()

# ==============================================================================
# 7. HEADER UTAMA DASHBOARD
# ==============================================================================
st.markdown("""
<div class="header-box">
    <div class="header-title">Dashboard Analitik Penjualan Nabila Catering</div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 8. TAB TAMPILAN DASHBOARD
# ==============================================================================
tab_titles = [
    "Ringkasan Finansial",
    "Analisis Menu",
    "Antrean Dapur",
    "Segmentasi Pelanggan",
    "Input Pesanan",
    "Panduan Sistem"
]

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(tab_titles)

# ------------------------------------------------------------------------------
# TAB 1: RINGKASAN OMZET & PERFORMA PENJUALAN
# ------------------------------------------------------------------------------
with tab1:
    st.subheader("Ringkasan Kinerja Finansial")
    
    
    total_omzet = df_filtered["Total_Penjualan"].sum()
    total_porsi = df_filtered["Jumlah_Pesanan"].sum()
    total_order = len(df_filtered)
    avg_order_value = total_omzet / total_order if total_order > 0 else 0
    
    df_selesai = df_filtered[df_filtered["Status_Pesanan"] == "Selesai"]
    omzet_selesai = df_selesai["Total_Penjualan"].sum()
    order_selesai_count = len(df_selesai)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(
            label="Total Omzet",
            value=f"Rp {total_omzet:,.0f}".replace(",", "."),
            delta=f"{total_order:,} Total Pesanan"
        )
    with col2:
        st.metric(
            label="Realisasi Omzet (Selesai)",
            value=f"Rp {omzet_selesai:,.0f}".replace(",", "."),
            delta=f"{order_selesai_count} Pesanan Tuntas"
        )
    with col3:
        st.metric(
            label="Total Porsi Terjual",
            value=f"{total_porsi:,} Porsi".replace(",", "."),
            delta=f"Rata-rata {int(total_porsi/total_order if total_order else 0)} porsi / nota"
        )
    with col4:
        st.metric(
            label="Rata-rata Nilai Pesanan (AOV)",
            value=f"Rp {avg_order_value:,.0f}".replace(",", "."),
            delta="Per Transaksi"
        )
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    c_left, c_right = st.columns([2, 1])
    with c_left:
        t_header_col, t_opt_col = st.columns([1, 1])
        
        date_range_days = (df_filtered["Tanggal_Pesanan"].max() - df_filtered["Tanggal_Pesanan"].min()).days if not df_filtered.empty else 365
        default_idx = 0 if date_range_days <= 45 else 2
        
        with t_opt_col:
            time_granularity = st.radio(
                "Agregasi Waktu:",
                ["Harian", "Mingguan", "Bulanan"],
                index=default_idx,
                horizontal=True,
                label_visibility="collapsed",
                key="trend_time_granularity"
            )
            
        with t_header_col:
            st.markdown(f"##### Tren Omzet ({time_granularity})")
            
        temp_df = df_filtered.copy()
        if time_granularity == "Harian":
            temp_df["Sort_Key"] = temp_df["Tanggal_Pesanan"].dt.date
            temp_df["Label_X"] = temp_df["Tanggal_Pesanan"].dt.strftime("%d %b %Y")
            x_label = "Tanggal"
        elif time_granularity == "Mingguan":
            temp_df["Sort_Key"] = temp_df["Tanggal_Pesanan"].dt.to_period("W").apply(lambda r: r.start_time.date())
            temp_df["Label_X"] = temp_df["Tanggal_Pesanan"].dt.to_period("W").apply(lambda r: "Mgg " + r.start_time.strftime("%d %b"))
            x_label = "Awal Minggu"
        else:
            temp_df["Sort_Key"] = temp_df["Tanggal_Pesanan"].dt.to_period("M").astype(str)
            temp_df["Label_X"] = temp_df["Tanggal_Pesanan"].dt.strftime("%B %Y")
            x_label = "Bulan"
            
        trend_df = temp_df.groupby(["Sort_Key", "Label_X"]).agg(
            Omzet=("Total_Penjualan", "sum"),
            Porsi=("Jumlah_Pesanan", "sum"),
            Transaksi=("ID_Pesanan", "count")
        ).reset_index().sort_values("Sort_Key")
        
        fig_trend = px.line(
            trend_df,
            x="Label_X",
            y="Omzet",
            markers=True,
            labels={"Label_X": x_label, "Omzet": "Total Omzet (Rp)"},
            template="plotly_dark"
        )
        fig_trend.update_traces(
            line_color="#10B981", 
            line_width=3, 
            marker=dict(size=7, color="#38BDF8"),
            customdata=np.stack((trend_df['Porsi'], trend_df['Transaksi']), axis=-1),
            hovertemplate="<b>%{x}</b><br>Total Omzet: Rp %{y:,.0f}<br>Porsi Terjual: %{customdata[0]:,} porsi<br>Jumlah Pesanan: %{customdata[1]:,} nota<extra></extra>"
        )
        fig_trend.update_layout(
            margin=dict(l=20, r=20, t=20, b=20), 
            plot_bgcolor="rgba(0,0,0,0)", 
            paper_bgcolor="rgba(0,0,0,0)", 
            hovermode="x unified"
        )
        st.plotly_chart(fig_trend, use_container_width=True)
        
    with c_right:
        st.markdown("##### Komposisi Status Pesanan")
        status_df = df_filtered.groupby("Status_Pesanan").agg(Total_Omzet=("Total_Penjualan", "sum")).reset_index()
        fig_pie = px.pie(
            status_df,
            names="Status_Pesanan",
            values="Total_Omzet",
            hole=0.55,
            color="Status_Pesanan",
            color_discrete_map={"Selesai": "#10B981", "Diproses": "#F59E0B", "Dibatalkan": "#EF4444"},
            template="plotly_dark"
        )
        fig_pie.update_layout(margin=dict(l=10, r=10, t=20, b=10), plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5))
        st.plotly_chart(fig_pie, use_container_width=True)

# ------------------------------------------------------------------------------
# TAB 2: ANALISIS MENU TERLARIS (MENU ENGINEERING)
# ------------------------------------------------------------------------------
with tab2:
    st.subheader("Analisis Menu Katering")

    
    b_col1, b_col2 = st.columns(2)
    with b_col1:
        st.markdown("##### Top 10 Menu Terlaris (Volume Porsi)")
        menu_vol = df_filtered.groupby("Nama_Menu")["Jumlah_Pesanan"].sum().reset_index().sort_values("Jumlah_Pesanan", ascending=True).tail(10)
        fig_vol = px.bar(
            menu_vol,
            x="Jumlah_Pesanan",
            y="Nama_Menu",
            orientation="h",
            color="Jumlah_Pesanan",
            labels={"Jumlah_Pesanan": "Total Porsi / Pcs", "Nama_Menu": ""},
            template="plotly_dark",
            color_continuous_scale="Teal"
        )
        fig_vol.update_layout(showlegend=False, margin=dict(l=20, r=20, t=20, b=20), plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_vol, use_container_width=True)
        
    with b_col2:
        st.markdown("##### Top 10 Menu Omzet Terbesar (Rp)")
        menu_rev = df_filtered.groupby("Nama_Menu")["Total_Penjualan"].sum().reset_index().sort_values("Total_Penjualan", ascending=True).tail(10)
        fig_rev = px.bar(
            menu_rev,
            x="Total_Penjualan",
            y="Nama_Menu",
            orientation="h",
            color="Total_Penjualan",
            labels={"Total_Penjualan": "Total Omzet (Rp)", "Nama_Menu": ""},
            template="plotly_dark",
            color_continuous_scale="Viridis"
        )
        fig_rev.update_layout(showlegend=False, margin=dict(l=20, r=20, t=20, b=20), plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_rev, use_container_width=True)
        
    st.markdown("##### Pola Musiman Kategori Menu (Heatmap)")
    pivot_catering = df_filtered.pivot_table(index="Kategori_Pesanan", columns="Bulan_Tahun", values="Jumlah_Pesanan", aggfunc="sum", fill_value=0)
    fig_heat = px.imshow(pivot_catering, text_auto=True, aspect="auto", labels=dict(x="Periode Bulan", y="Kategori Pesanan", color="Total Porsi"), template="plotly_dark", color_continuous_scale="YlGnBu")
    fig_heat.update_layout(margin=dict(l=20, r=20, t=20, b=20), plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_heat, use_container_width=True)

# ------------------------------------------------------------------------------
# TAB 3: ANTREAN PESANAN & OPERASIONAL DAPUR
# ------------------------------------------------------------------------------
with tab3:
    st.subheader("Pemantauan Antrean Dapur")
    
    
    df_active = df_filtered[df_filtered["Status_Pesanan"] == "Diproses"].copy()
    
    o1, o2, o3 = st.columns(3)
    with o1:
        st.metric("Pesanan Sedang Diproses", f"{len(df_active)} Pesanan", delta="Perlu Disiapkan Dapur", delta_color="inverse")
    with o2:
        st.metric("Total Porsi Antrean Dapur", f"{df_active['Jumlah_Pesanan'].sum():,} Porsi".replace(",", "."))
    with o3:
        avg_lt = df_filtered["Lead_Time_Days"].dropna().mean()
        st.metric("Rata-rata Waktu Persiapan (Lead Time)", f"{avg_lt:.1f} Hari", delta="Pemesanan s.d. Kirim")
        
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("##### Daftar Kerja Dapur")
    
    if not df_active.empty:
        display_active = df_active[[
            "ID_Pesanan", "Tanggal_Pesanan", "Nama_Pemesan", "Tipe_Klien",
            "Kategori_Pesanan", "Nama_Menu", "Jumlah_Pesanan", "Total_Penjualan", "Status_Pesanan"
        ]].copy()
        display_active["Tanggal_Pesanan"] = display_active["Tanggal_Pesanan"].dt.strftime("%d-%m-%Y")
        display_active["Total_Penjualan"] = display_active["Total_Penjualan"].apply(lambda x: f"Rp {x:,.0f}".replace(",", "."))
        display_active.columns = [
            "No. Pesanan", "Tgl Pesan", "Nama Pemesan", "Tipe Pelanggan",
            "Kategori", "Nama Menu", "Porsi", "Total Biaya", "Status Dapur"
        ]
        st.dataframe(display_active, use_container_width=True, hide_index=True)
        
        csv_kitchen = df_active.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Unduh Lembar Kerja Dapur (Kitchen Work Order CSV)",
            data=csv_kitchen,
            file_name=f"lembar_kerja_dapur_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    else:
        st.success("🎉 Tidak ada antrean pesanan yang tertunda. Semua pesanan telah selesai dikerjakan!")

# ------------------------------------------------------------------------------
# TAB 4: SEGMENTASI PELANGGAN (B2B & B2C)
# ------------------------------------------------------------------------------
with tab4:
    st.subheader("Segmentasi Pelanggan")
    
    cakupan_rfm = st.radio(
        "Cakupan Periode Analisis:",
        ["Sesuai Rentang Tanggal Filter Aktif", "Seluruh Riwayat Kumulatif"],
        horizontal=True,
        key="radio_cakupan_rfm"
    )
    
    df_rfm_target = df_filtered if "Rentang Tanggal" in cakupan_rfm else df_raw
    
    if df_rfm_target is None or df_rfm_target.empty:
        st.warning("Tidak ada transaksi pelanggan yang ditemukan pada rentang filter ini.")
    else:
        snapshot_date = df_rfm_target["Tanggal_Pesanan"].max() + timedelta(days=1)
        rfm = df_rfm_target.groupby("Nama_Pemesan").agg(
            Recency=("Tanggal_Pesanan", lambda x: (snapshot_date - x.max()).days),
            Frequency=("ID_Pesanan", "count"),
            Monetary=("Total_Penjualan", "sum"),
            Menu_Favorit=("Nama_Menu", lambda x: x.mode()[0] if not x.empty else "-"),
            Tipe_Klien=("Tipe_Klien", "first")
        ).reset_index()
        
        def classify_catering_customer(row):
            freq = row["Frequency"]
            mon = row["Monetary"]
            is_b2b = "B2B" in str(row.get("Tipe_Klien", ""))
            
            if is_b2b:
                if freq >= 3:
                    return "Mitra Institusi (B2B Rutin)"
                else:
                    return "Institusi / Organisasi (B2B)"
            else:
                if freq >= 3:
                    return "Pelanggan Rutin (B2C)"
                elif mon >= 3000000:
                    return "Klien Acara Besar"
                elif mon >= 1000000:
                    return "Pemesan Menengah"
                else:
                    return "Pelanggan Retail"
                
        rfm["Segmen_Pelanggan"] = rfm.apply(classify_catering_customer, axis=1)
        
        s_col1, s_col2 = st.columns([1, 1])
        with s_col1:
            st.markdown("##### Sebaran Pelanggan (Frekuensi vs Total Belanja)")
            fig_scatter = px.scatter(
                rfm,
                x="Frequency",
                y="Monetary",
                size="Monetary",
                color="Segmen_Pelanggan",
                hover_name="Nama_Pemesan",
                labels={"Frequency": "Frekuensi Pesanan (Kali)", "Monetary": "Total Belanja Akumulasi (Rp)"},
                template="plotly_dark"
            )
            fig_scatter.update_layout(margin=dict(l=20, r=20, t=20, b=20), plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", legend=dict(orientation="h", yanchor="bottom", y=-0.35, xanchor="center", x=0.5))
            st.plotly_chart(fig_scatter, use_container_width=True)
            
        with s_col2:
            st.markdown("##### Proporsi Omzet per Segmen")
            seg_pie = rfm.groupby("Segmen_Pelanggan")["Monetary"].sum().reset_index()
            fig_spie = px.pie(seg_pie, names="Segmen_Pelanggan", values="Monetary", hole=0.45, template="plotly_dark", color_discrete_sequence=px.colors.qualitative.Bold)
            fig_spie.update_layout(margin=dict(l=10, r=10, t=20, b=10), plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", legend=dict(orientation="h", yanchor="bottom", y=-0.35, xanchor="center", x=0.5))
            st.plotly_chart(fig_spie, use_container_width=True)
            
        st.markdown("##### Direktori Pelanggan & Menu Favorit")
        rfm_show = rfm[["Nama_Pemesan", "Tipe_Klien", "Segmen_Pelanggan", "Frequency", "Monetary", "Menu_Favorit"]].copy()
        rfm_show["Monetary"] = rfm_show["Monetary"].apply(lambda x: f"Rp {x:,.0f}".replace(",", "."))
        rfm_show.columns = ["Nama Pemesan / Instansi", "Tipe Klien", "Kategori Segmen", "Jumlah Pesan", "Total Omzet (Rp)", "Menu Paling Sering Dipesan"]
        st.dataframe(rfm_show.sort_values("Jumlah Pesan", ascending=False), use_container_width=True, hide_index=True)

# ------------------------------------------------------------------------------
# TAB 5: INPUT PESANAN & KELOLA MENU (KONDISIONAL SESUAI SUMBER DATA)
# ------------------------------------------------------------------------------
with tab5:
    st.subheader("Input Pesanan & Katalog Menu")
    
    sub_tab1, sub_tab2, sub_tab3 = st.tabs([
        "🛒 Catat Pesanan Baru & Update Status", 
        "🍲 Kelola Katalog Menu Makanan", 
        "⚡ Integrasi Cloud (Google Apps Script)"
    ])
    
    # --------------------------------------------------------------------------
    # SUB TAB 1: FORM INPUT PESANAN (AKTIF & IDENTIK DI SEMUA MODE)
    # --------------------------------------------------------------------------
    with sub_tab1:
        st.markdown("#### Formulir Input & Perubahan Pesanan")
        
        
        # Banner Status Penyimpanan
        if user_cfg.get("source_type") == "Google Sheets":
            if user_cfg.get("script_url"):
                st.success("🟢 **Mode Aktif: Google Sheets Cloud Live** (Sinkronisasi Otomatis Cloud Aktif via Google Apps Script Webhook).")
            else:
                st.info("ℹ️ **Mode Aktif: Google Sheets Cloud Live**. Pesanan yang Anda simpan akan masuk ke database lokal. *Pasang URL Apps Script di tab '⚡ Integrasi Cloud' agar otomatis terkirim ke Google Sheets.*")
        else:
            st.success("🟢 **Mode Aktif: Lokal (File CSV)**. Pesanan tersimpan langsung ke database lokal `data/historis_transaksi_catering.csv`.")
            
        form_mode = st.radio(
            "Pilih Tindakan:",
            ["Catat Pesanan Baru", "Edit / Update Status Pesanan"],
            horizontal=True,
            key="order_form_mode"
        )
        
        # Nilai Bawaan
        next_order_num = len(df_raw) + 1 if df_raw is not None and not df_raw.empty else 1
        default_order_id = f"CTR{next_order_num:04d}"
        init_pemesan = ""
        init_tgl_pesan = datetime.today()
        init_tgl_selesai = datetime.today() + timedelta(days=2)
        init_kategori = "Paket Nasi"
        init_menu = "Nasi Kotak Ayam Kampung"
        init_porsi = 50
        init_harga = 35000
        init_status = "Diproses"
        
        if form_mode == "✏️ Edit / Update Status Pesanan yang Ada" and df_raw is not None and not df_raw.empty:
            # Urutkan pesanan dari yang paling baru / status diproses
            order_list = df_raw["ID_Pesanan"].astype(str).tolist()
            selected_edit_id = st.selectbox(
                "🔍 Pilih Nomor Pesanan yang Ingin Diperbarui / Diselesaikan:",
                options=order_list[::-1],
                help="Pilih ID pesanan untuk memuat datanya ke formulir di bawah."
            )
            
            row_match = df_raw[df_raw["ID_Pesanan"].astype(str) == selected_edit_id]
            if not row_match.empty:
                cur_row = row_match.iloc[0]
                default_order_id = selected_edit_id
                init_pemesan = str(cur_row.get("Nama_Pemesan", ""))
                if pd.notnull(cur_row.get("Tanggal_Pesanan")):
                    try:
                        init_tgl_pesan = pd.to_datetime(cur_row["Tanggal_Pesanan"]).date()
                    except Exception:
                        pass
                if pd.notnull(cur_row.get("Tanggal_Selesai")):
                    try:
                        init_tgl_selesai = pd.to_datetime(cur_row["Tanggal_Selesai"]).date()
                    except Exception:
                        pass
                init_kategori = str(cur_row.get("Kategori_Pesanan", "Paket Nasi"))
                init_menu = str(cur_row.get("Nama_Menu", "Nasi Kotak Ayam Kampung"))
                try:
                    init_porsi = int(cur_row.get("Jumlah_Pesanan", 50))
                except Exception:
                    init_porsi = 50
                try:
                    init_harga = int(cur_row.get("Harga_Satuan", 25000))
                except Exception:
                    init_harga = 25000
                init_status = str(cur_row.get("Status_Pesanan", "Selesai"))
        
        with st.container():
            f1, f2 = st.columns(2)
            
            with f1:
                input_id = st.text_input(
                    "No. Pesanan (ID):",
                    value=default_order_id,
                    key=f"input_order_id_{form_mode}_{default_order_id}"
                )
                input_pemesan = st.text_input(
                    "Nama Pemesan / Instansi:",
                    value=init_pemesan,
                    placeholder="Contoh: MAN 2 Jombang atau Ibu Rahayu",
                    key=f"input_order_pemesan_{default_order_id}"
                )
                input_tgl_pesan = st.date_input(
                    "Tanggal Pesanan Masuk:",
                    value=init_tgl_pesan,
                    key=f"input_order_tgl_pesan_{default_order_id}"
                )
                input_tgl_selesai = st.date_input(
                    "Tanggal Pengiriman:",
                    value=init_tgl_selesai,
                    key=f"input_order_tgl_selesai_{default_order_id}"
                )
                
            with f2:
                active_menus = df_master_menu[df_master_menu["Status"] == "Tersedia"].copy()
                kategori_list = ["Paket Nasi", "Lauk Satuan", "Paket Acara"]
                
                cat_index = kategori_list.index(init_kategori) if init_kategori in kategori_list else 0
                sel_kategori = st.selectbox(
                    "Kategori Menu:",
                    options=kategori_list,
                    index=cat_index,
                    key=f"sel_kategori_{default_order_id}"
                )
                
                filtered_menus = active_menus[active_menus["Kategori_Pesanan"] == sel_kategori]
                menu_options = filtered_menus["Nama_Menu"].tolist()
                if not menu_options:
                    menu_options = ["Menu Standar"]
                    
                menu_index = menu_options.index(init_menu) if init_menu in menu_options else 0
                sel_menu = st.selectbox(
                    "Nama Menu:",
                    options=menu_options,
                    index=menu_index,
                    key=f"sel_menu_{default_order_id}_{sel_kategori}"
                )
                
                row_menu = filtered_menus[filtered_menus["Nama_Menu"] == sel_menu]
                default_price = int(row_menu["Harga_Satuan"].values[0]) if not row_menu.empty else init_harga
                sel_kode_menu = str(row_menu["Kode_Menu"].values[0]) if not row_menu.empty else "PN01"
                
                p1, p2 = st.columns(2)
                with p1:
                    input_porsi = st.number_input(
                        "Jumlah Pesanan (Porsi):",
                        min_value=1,
                        value=init_porsi,
                        step=1,
                        key=f"input_porsi_{default_order_id}"
                    )
                with p2:
                    input_harga = st.number_input(
                        "Harga Satuan (Rp):",
                        min_value=1000,
                        value=default_price,
                        step=1000,
                        key=f"input_harga_{default_order_id}_{sel_menu}"
                    )
                    
                total_kalkulasi = int(input_porsi * input_harga)
                
                st.markdown(f"""
                <div style="background-color: #0F172A; border: 1px solid #10B981; border-radius: 10px; padding: 12px 16px; margin: 12px 0;">
                    <div style="color: #94A3B8; font-size: 0.85rem; font-weight: 600;">💰 Total Nilai Penjualan:</div>
                    <div style="color: #38BDF8; font-size: 1.35rem; font-weight: 800; margin-top: 2px;">
                        Rp {total_kalkulasi:,.0f} 
                        <span style="color: #64748B; font-size: 0.85rem; font-weight: normal;">({input_porsi:,} porsi × Rp {input_harga:,.0f})</span>
                    </div>
                </div>
                """.replace(",", "."), unsafe_allow_html=True)
                
                status_options = ["Diproses", "Selesai"]
                status_idx = status_options.index(init_status) if init_status in status_options else 0
                input_status = st.selectbox(
                    "Status Pesanan:",
                    status_options,
                    index=status_idx,
                    key=f"input_status_{default_order_id}"
                )
                
            st.markdown("<br>", unsafe_allow_html=True)
            btn_label = "Simpan Perubahan Pesanan" if form_mode.startswith("✏️") else "Simpan Pesanan Baru"
            submit_order = st.button(btn_label, use_container_width=True, type="primary")
            
            if submit_order:
                if not input_pemesan.strip():
                    st.error("⚠️ Nama Pemesan / Instansi wajib diisi sebelum menyimpan!")
                else:
                    new_row = {
                        "ID_Pesanan": input_id.strip(),
                        "Nama_Pemesan": input_pemesan.strip().title(),
                        "Tanggal_Pesanan": str(input_tgl_pesan),
                        "Tanggal_Selesai": str(input_tgl_selesai),
                        "Kode_Menu": sel_kode_menu,
                        "Kategori_Pesanan": sel_kategori,
                        "Nama_Menu": sel_menu,
                        "Jumlah_Pesanan": int(input_porsi),
                        "Harga_Satuan": int(input_harga),
                        "Total_Penjualan": total_kalkulasi,
                        "Status_Pesanan": input_status
                    }
                    
                    # 1. Simpan ke Database Lokal CSV (Upsert: Update jika ID sudah ada, Insert jika baru)
                    local_saved = False
                    action_mode = "inserted"
                    if os.path.exists(CSV_TRANSAKSI):
                        df_db = pd.read_csv(CSV_TRANSAKSI)
                        existing_mask = df_db["ID_Pesanan"].astype(str).str.strip() == input_id.strip()
                        
                        if existing_mask.any():
                            action_mode = "updated"
                            match_idx = df_db[existing_mask].index[0]
                            for col_name, col_val in new_row.items():
                                df_db.loc[match_idx, col_name] = col_val
                            df_db.to_csv(CSV_TRANSAKSI, index=False)
                        else:
                            df_db = pd.concat([df_db, pd.DataFrame([new_row])], ignore_index=True)
                            df_db.to_csv(CSV_TRANSAKSI, index=False)
                    else:
                        pd.DataFrame([new_row]).to_csv(CSV_TRANSAKSI, index=False)
                    local_saved = True
                    
                    # 2. Sinkronisasi Otomatis ke Google Sheets (Opsi 2 via Web App Apps Script)
                    cloud_synced = False
                    if user_cfg.get("source_type") == "Google Sheets":
                        script_url = user_cfg.get("script_url", "").strip()
                        if script_url:
                            with st.spinner("⏳ Mengirim dan menyinkronkan data langsung ke Google Sheets..."):
                                try:
                                    res = requests.post(script_url, json=new_row, timeout=12)
                                    if res.status_code == 200:
                                        cloud_synced = True
                                    else:
                                        st.warning(f"⚠️ Data tersimpan di database lokal, namun Google Apps Script merespons: HTTP {res.status_code}")
                                except Exception as ex:
                                    st.warning(f"⚠️ Data tersimpan di database lokal, namun gagal menghubungi Google Sheets: {ex}")
                        else:
                            st.info("💡 **Tips:** Data berhasil tersimpan ke database lokal! Pasang URL Google Apps Script di tab '⚡ Integrasi Cloud' di atas agar otomatis masuk ke Google Sheets.")
                            
                    if cloud_synced:
                        if action_mode == "updated":
                            st.success(f"☁️🎉 Pesanan **{input_id}** ({input_pemesan}) berhasil DIPERBARUI di Google Sheets dan database lokal!")
                        else:
                            st.success(f"☁️🎉 Pesanan baru **{input_id}** atas nama **{input_pemesan}** berhasil DISIMPAN langsung ke Google Sheets dan database lokal!")
                    elif local_saved:
                        if action_mode == "updated":
                            st.success(f"✏️ Pesanan **{input_id}** atas nama **{input_pemesan}** berhasil DIPERBARUI menjadi status **'{input_status}'**!")
                        else:
                            st.success(f"🎉 Pesanan baru **{input_id}** atas nama **{input_pemesan}** berhasil DISIMPAN ke database lokal!")
                            
                    st.balloons()
                    st.cache_data.clear()
                    st.rerun()

    # --------------------------------------------------------------------------
    # SUB TAB 2: KELOLA MASTER MENU MAKANAN
    # --------------------------------------------------------------------------
    with sub_tab2:
        st.markdown("#### Katalog & Harga Menu Makanan")
        
        st.dataframe(df_master_menu, use_container_width=True, hide_index=True)
        
        m_col1, m_col2 = st.columns(2)
        with m_col1:
            st.markdown("##### Tambah Menu Baru")
            with st.form("form_tambah_menu"):
                new_cat = st.selectbox("Kategori Menu:", ["Paket Nasi", "Lauk Satuan", "Paket Acara"])
                new_name = st.text_input("Nama Menu Baru:", placeholder="Contoh: Nasi Goreng Jawa Spesial")
                new_price = st.number_input("Harga Satuan (Rp):", min_value=1000, value=25000, step=1000)
                
                prefix = "PN" if new_cat == "Paket Nasi" else ("LS" if new_cat == "Lauk Satuan" else "PA")
                existing_codes = df_master_menu[df_master_menu["Kode_Menu"].str.startswith(prefix)]["Kode_Menu"].tolist()
                next_code = f"{prefix}{len(existing_codes)+1:02d}"
                new_code = st.text_input("Kode Menu:", value=next_code)
                
                submit_new_menu = st.form_submit_button("➕ Tambah Menu ke Katalog")
                if submit_new_menu:
                    if not new_name.strip():
                        st.error("⚠️ Nama Menu Baru tidak boleh kosong!")
                    else:
                        new_menu_row = {
                            "Kode_Menu": new_code.strip(),
                            "Kategori_Pesanan": new_cat,
                            "Nama_Menu": new_name.strip(),
                            "Harga_Satuan": int(new_price),
                            "Status": "Tersedia"
                        }
                        updated_menu = pd.concat([df_master_menu, pd.DataFrame([new_menu_row])], ignore_index=True)
                        save_master_menu(updated_menu)
                        st.success(f"✅ Menu **{new_name}** ({new_cat}) berhasil ditambahkan!")
                        st.cache_data.clear()
                        st.rerun()
                        
        with m_col2:
            st.markdown("##### Hapus Menu dari Katalog")
            with st.form("form_hapus_menu"):
                menu_to_delete = st.selectbox("Pilih Menu yang Ingin Dihapus:", options=df_master_menu["Nama_Menu"].tolist())
                submit_del_menu = st.form_submit_button("🗑️ Hapus Menu Terpilih")
                if submit_del_menu:
                    updated_menu = df_master_menu[df_master_menu["Nama_Menu"] != menu_to_delete].copy()
                    save_master_menu(updated_menu)
                    st.warning(f"🗑️ Menu **{menu_to_delete}** berhasil dihapus!")
                    st.cache_data.clear()
                    st.rerun()

    # --------------------------------------------------------------------------
    # SUB TAB 3: INTEGRASI CLOUD (GOOGLE APPS SCRIPT)
    # --------------------------------------------------------------------------
    with sub_tab3:
        st.markdown("#### Integrasi Google Apps Script")
        st.write("Hubungkan formulir dashboard langsung ke Google Sheets secara real-time.")
        
        current_script_url = user_cfg.get("script_url", "")
        if current_script_url:
            st.success(f"🟢 **Status Integrasi Cloud: AKTIF** (`{current_script_url[:50]}...`)")
        else:
            st.warning("⚪ **Status Integrasi Cloud: Belum Dihubungkan** (Pesanan yang diinput saat ini baru tersimpan di database lokal).")
            
        with st.form("form_save_script_url"):
            input_tab_script_url = st.text_input(
                "🔗 Tempelkan URL Web App Google Apps Script Anda:",
                value=current_script_url,
                placeholder="https://script.google.com/macros/s/.../exec",
                help="Dapatkan URL ini setelah menerapkan (deploy) script di Google Sheets."
            )
            save_script_btn = st.form_submit_button("💾 Simpan Pengaturan Webhook Cloud")
            if save_script_btn:
                user_cfg["script_url"] = input_tab_script_url.strip()
                save_user_settings(user_cfg)
                st.success("✅ Pengaturan URL Google Apps Script berhasil disimpan!")
                st.cache_data.clear()
                st.rerun()
                
        st.divider()
        st.markdown("##### 📋 Panduan 3 Langkah Pemasangan di Google Sheets (Hanya 1 Menit):")
        sheet_link = user_cfg.get('sheet_url', '#')
        st.markdown(f"""
        1. **Buka Spreadsheet Google Sheets Nabila Catering Anda:** [Buka Spreadsheet Sekarang ↗]({sheet_link})
        2. Di menu atas Google Sheets, klik **Extensions (Ekstensi)** ➡️ **Apps Script**.
        3. Hapus seluruh isi kode bawaan di halaman editor tersebut, lalu salin (*copy*) dan tempel (*paste*) kode di bawah ini:
        """)
        
        apps_script_code = '''function doPost(e) {
  try {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sheet = ss.getActiveSheet();
    var data = JSON.parse(e.postData.contents);
    
    var id = String(data.ID_Pesanan || "").trim();
    var values = sheet.getDataRange().getValues();
    var headers = values[0];
    
    var idColIdx = 0;
    for (var j = 0; j < headers.length; j++) {
      if (String(headers[j]).trim().toLowerCase() === "id_pesanan") {
        idColIdx = j;
        break;
      }
    }
    
    var matchRow = -1;
    for (var i = 1; i < values.length; i++) {
      if (String(values[i][idColIdx]).trim() === id) {
        matchRow = i + 1;
        break;
      }
    }
    
    var rowData = [
      data.ID_Pesanan || "",
      data.Nama_Pemesan || "",
      data.Tanggal_Pesanan || "",
      data.Tanggal_Selesai || "",
      data.Kode_Menu || "",
      data.Kategori_Pesanan || "",
      data.Nama_Menu || "",
      Number(data.Jumlah_Pesanan || 0),
      Number(data.Harga_Satuan || 0),
      Number(data.Total_Penjualan || 0),
      data.Status_Pesanan || "Diproses"
    ];
    
    if (matchRow > 1) {
      sheet.getRange(matchRow, 1, 1, rowData.length).setValues([rowData]);
      return ContentService.createTextOutput(JSON.stringify({status: "success", action: "updated", id: id})).setMimeType(ContentService.MimeType.JSON);
    } else {
      sheet.appendRow(rowData);
      return ContentService.createTextOutput(JSON.stringify({status: "success", action: "inserted", id: id})).setMimeType(ContentService.MimeType.JSON);
    }
  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({status: "error", message: err.toString()})).setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet(e) {
  return ContentService.createTextOutput(JSON.stringify({status: "online", message: "Webhook Nabila Catering Aktif!"})).setMimeType(ContentService.MimeType.JSON);
}'''
        st.code(apps_script_code, language="javascript")
        
        st.markdown("""
        4. Klik tombol **Deploy (Terapkan)** di pojok kanan atas ➡️ pilih **New deployment (Penerapan baru)**.
        5. Klik ikon gerigi ⚙️ di sebelah *Select type* ➡️ pilih **Web app**.
        6. Atur konfigurasi:
           * **Description:** Webhook Kasir Nabila Catering
           * **Execute as:** *Me (email akun Google Anda)*
           * **Who has access:** *Anyone (Siapa saja)*
        7. Klik **Deploy** ➡️ Berikan izin akses (*Authorize access*) jika diminta ➡️ Salin **Web app URL** yang berakhiran `/exec` ➡️ Tempelkan ke formulir di atas!
        """)

# ------------------------------------------------------------------------------
# TAB 6: PANDUAN SISTEM & BANTUAN
# ------------------------------------------------------------------------------
with tab6:
    st.subheader("Panduan Sistem")
    st.markdown("""
    **1. Sumber Data (Hybrid Mode):**
    * **Google Sheets:** Membaca data langsung dari spreadsheet secara online.
    * **Lokal (CSV):** Menggunakan file data lokal di komputer untuk operasional offline.
    
    **2. Modul Dashboard:**
    * **Ringkasan Finansial:** Total omzet, realisasi pendapatan, tren bulanan, dan komposisi status pesanan.
    * **Analisis Menu:** Peringkat menu terlaris dan matriks musiman porsi pesanan.
    * **Antrean Dapur:** Pemantauan pesanan yang sedang diproses dan unduh lembar kerja dapur.
    * **Segmentasi Pelanggan:** Pengelompokan pelanggan institusi dan ritel berdasarkan frekuensi dan nilai transaksi.
    * **Input Pesanan:** Formulir pencatatan transaksi masuk dan pengelolaan katalog menu.
    """)
