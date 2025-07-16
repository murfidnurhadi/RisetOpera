import streamlit as st
import pandas as pd
import gdown
import os
import plotly.express as px

# Konfigurasi halaman
st.set_page_config(page_title="Dashboard Simulasi Monte Carlo", layout="wide")

st.title("📊 Dashboard Simulasi Monte Carlo")

# Sidebar menu navigasi
st.sidebar.header("Menu Navigasi")
menu = st.sidebar.radio("Pilih Dataset:", [
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

# Pilihan sumber data
st.sidebar.subheader("Pilih Sumber Data")
source_option = st.sidebar.radio("Ambil data dari:", ["Lokal (CSV)", "Google Drive Link", "Upload Manual"])

# Mapping file CSV & Link Google Drive
data_sources = {
    "Data Kunjungan Pasien": {"file": "Data_Kunjungan_Pasien.csv", "gdrive": "https://drive.google.com/uc?id=1AgGhdLZiPDIBxUcVkipYN2GAy2tAIM9z"},
    "Data Train": {"file": "DataTrain.csv", "gdrive": "https://drive.google.com/uc?id=11tgNQ2GqMSIM97DH2U9HNTbIh4CceuiF"},
    "Kota Cirebon": {"file": "DataKotaCirebon.csv", "gdrive": "https://drive.google.com/uc?id=FILE_ID"},
    "Kab Cirebon": {"file": "DataKabCirebon.csv", "gdrive": "https://drive.google.com/uc?id=FILE_ID"},
    "Kuningan": {"file": "DataKabKuningan.csv", "gdrive": "https://drive.google.com/uc?id=FILE_ID"},
    "Indramayu": {"file": "DataKotaIndramayu.csv", "gdrive": "https://drive.google.com/uc?id=FILE_ID"},
    "Majalengka": {"file": "DataKotaMajalengka.csv", "gdrive": "https://drive.google.com/uc?id=FILE_ID"},
    "Lain2": {"file": "DataKotaLain2.csv", "gdrive": "https://drive.google.com/uc?id=FILE_ID"},
    "RNG LCG": {"file": "rng_LCG.csv", "gdrive": "https://drive.google.com/uc?id=FILE_ID"},
    "Simulasi": {"file": "Simulasi_Monte_Carlo.csv", "gdrive": "https://drive.google.com/uc?id=FILE_ID"}
}

file_info = data_sources[menu]
file_path = file_info["file"]
gdrive_link = file_info["gdrive"]

# Fungsi untuk memuat data dengan cache
@st.cache_data
def load_data(source, local_path, gdrive_url, uploaded_file):
    try:
        if source == "Lokal (CSV)":
            df = pd.read_csv(local_path)
        elif source == "Google Drive Link":
            if not os.path.exists(local_path):
                gdown.download(gdrive_url, local_path, quiet=False)
            df = pd.read_csv(local_path)
        elif source == "Upload Manual" and uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
        else:
            return pd.DataFrame()

        # Fallback jika delimiter salah
        if df.shape[1] == 1:
            df = pd.read_csv(local_path, delimiter=";")

        return df
    except Exception as e:
        st.error(f"Gagal memuat data: {e}")
        return pd.DataFrame()

# Jika pilih upload manual
uploaded_file = None
if source_option == "Upload Manual":
    uploaded_file = st.file_uploader("Unggah file CSV", type=["csv"])

# Load data
df = load_data(source_option, file_path, gdrive_link, uploaded_file)

# Tampilkan data
st.subheader(f"📄 {menu}")
if not df.empty:
    st.dataframe(df, use_container_width=True)
    st.markdown(f"**Jumlah Data:** {len(df)} baris")

    # Ringkasan statistik
    st.subheader("📊 Ringkasan Statistik")
    st.write(df.describe(include="all"))

    # Visualisasi (jika ada kolom numerik)
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    if len(numeric_cols) > 0:
        st.subheader("📈 Visualisasi Data")
        col_x = st.selectbox("Pilih X-axis", options=numeric_cols)
        col_y = st.selectbox("Pilih Y-axis", options=numeric_cols)
        fig = px.scatter(df, x=col_x, y=col_y, title=f"Scatter Plot {col_x} vs {col_y}")
        st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Tidak ada data yang ditampilkan. Pastikan Anda memilih sumber data yang benar.")
