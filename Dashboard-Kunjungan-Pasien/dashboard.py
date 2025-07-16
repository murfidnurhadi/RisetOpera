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
        "gdrive": "https://drive.google.com/file/d/1AgGhdLZiPDIBxUcVkipYN2GAy2tAIM9z/view?usp=drive_link"
    },
    "Data Train": {
        "file": "DataTrain.csv",
        "gdrive": "https://drive.google.com/file/d/11tgNQ2GqMSIM97DH2U9HNTbIh4CceuiF/view?usp=drive_link"
    },
    "Kota Cirebon": {
        "file": "DataKotaCirebon.csv",
        "gdrive": "https://drive.google.com/file/d/19ae9zMmGu8xc79VPCK9mPVXTkUu27tJI/view?usp=drive_link"
    },
    "Kab Cirebon": {
        "file": "DataKabCirebon.csv",
        "gdrive": "https://drive.google.com/file/d/1qwDqsL9D71Id7js4isF9Azcit-gaOAaT/view?usp=drive_link"
    },
    "Kuningan": {
        "file": "DataKabKuningan.csv",
        "gdrive": "https://drive.google.com/file/d/1A3nd6dqBKeRzOo3Cpdd4BWl2g6qNxwVY/view?usp=drive_link"
    },
    "Indramayu": {
        "file": "DataKotaIndramayu.csv",
        "gdrive": "https://drive.google.com/file/d/1a_t5kUyDzSrI0WILSqyPTy3LVKdBUwjU/view?usp=drive_link"
    },
    "Majalengka": {
        "file": "DataKotaMajalengka.csv",
        "gdrive": "https://drive.google.com/file/d/1Ef4Gnl4o-5xDyX5Wu9OnQ0LRNRIb_grb/view?usp=drive_link"
    },
    "Lain2": {
        "file": "DataKotaLain2.csv",
        "gdrive": "https://drive.google.com/file/d/1-2jsT3vhWqFDIdmGep40PCUv1lhKxE6N/view?usp=drive_link"
    },
    "RNG LCG": {
        "file": "rng_LCG.csv",
        "gdrive": "https://drive.google.com/file/d/1lWjneuxb7ecQZainm_igSmB24BXYmrmb/view?usp=drive_link"
    },
    "Simulasi": {
        "file": "Simulasi_Monte_Carlo.csv",
        "gdrive": "https://drive.google.com/file/d/1sbZlQXUjU7Km5pQrCcM4e1gmOL0mAzzX/view?usp=drive_link"
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
