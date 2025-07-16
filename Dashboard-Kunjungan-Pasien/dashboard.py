import streamlit as st
import pandas as pd
import gdown
import os

# Konfigurasi halaman
st.set_page_config(page_title="Dashboard Simulasi Monte Carlo", layout="wide")

# Judul Dashboard
st.title("📊 Dashboard Simulasi Monte Carlo")

# Sidebar Menu
st.sidebar.header("Menu Navigasi")
menu = st.sidebar.radio("Pilih Data:", [
    "Data Kunjungan Pasien",
    "Data Train",
    "Kota Cirebon",
    "Kab Cirebon",
    "Kuningan",
    "Indramayu",
    "Majalengka",
    "Lain2",
    "RNG LCG",
    "Simulasi"
])

# Mapping file CSV & Link Google Drive
data_sources = {
    "Data Kunjungan Pasien": {
        "file": "Data_Kunjungan_Pasien.csv",
        "gdrive": "https://drive.google.com/uc?id=YOUR_ID_HERE"
    },
    "Data Train": {
        "file": "DataTrain.csv",
        "gdrive": "https://drive.google.com/uc?id=YOUR_ID_HERE"
    },
    "Kota Cirebon": {
        "file": "DataKotaCirebon.csv",
        "gdrive": "https://drive.google.com/uc?id=YOUR_ID_HERE"
    },
    "Kab Cirebon": {
        "file": "DataKabCirebon.csv",
        "gdrive": "https://drive.google.com/uc?id=YOUR_ID_HERE"
    },
    "Kuningan": {
        "file": "DataKabKuningan.csv",
        "gdrive": "https://drive.google.com/uc?id=YOUR_ID_HERE"
    },
    "Indramayu": {
        "file": "DataKotaIndramayu.csv",
        "gdrive": "https://drive.google.com/uc?id=YOUR_ID_HERE"
    },
    "Majalengka": {
        "file": "DataKotaMajalengka.csv",
        "gdrive": "https://drive.google.com/uc?id=YOUR_ID_HERE"
    },
    "Lain2": {
        "file": "DataKotaLain2.csv",
        "gdrive": "https://drive.google.com/uc?id=YOUR_ID_HERE"
    },
    "RNG LCG": {
        "file": "rng_LCG.csv",
        "gdrive": "https://drive.google.com/uc?id=YOUR_ID_HERE"
    },
    "Simulasi": {
        "file": "Simulasi.csv",
        "gdrive": "https://drive.google.com/uc?id=YOUR_ID_HERE"
    }
}

# Pilihan cara akses data
st.sidebar.subheader("Pilih Sumber Data")
source_option = st.sidebar.radio("Ambil data dari:", ["Lokal (CSV)", "Google Drive Link"])

# Pilih data sesuai menu
file_info = data_sources[menu]
file_path = file_info["file"]
gdrive_link = file_info["gdrive"]

# Load Data
st.subheader(f"📄 {menu}")

try:
    if source_option == "Lokal (CSV)":
        # Baca file dari lokal
        df = pd.read_csv(file_path)
    else:
        # Download dari Google Drive & baca
        output_file = file_path
        if not os.path.exists(output_file):
            gdown.download(gdrive_link, output_file, quiet=False)
        df = pd.read_csv(output_file)

    # Tampilkan data
    st.dataframe(df, use_container_width=True)
    st.markdown(f"**Jumlah Data:** {len(df)} baris")
except Exception as e:
    st.error(f"Terjadi kesalahan: {e}")
