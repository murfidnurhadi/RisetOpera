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
source_option = st.sidebar.radio("Ambil data dari:", ["Otomatis (Lokal/Drive)", "Upload Manual"])

# Mapping file CSV & Link Google Drive
data_sources = {
    "Data Kunjungan Pasien": {
        "file": "Data_Kunjungan_Pasien.csv",
        "gdrive": "https://drive.google.com/file/d/1cvmZN48OFsZz4-Gy6cVoQXoU9qFkzD9a/view?usp=sharing"
    },
    "Data Train": {
        "file": "DataTrain.csv",
        "gdrive": "https://drive.google.com/file/d/1vLyXjeN5tYDAgUFiXbHi-W32GfKm3eXx/view?usp=sharing"
    },
    "Kota Cirebon": {
        "file": "DataKotaCirebon.csv",
        "gdrive": "https://drive.google.com/file/d/18Xieo21oEz364MyTN4Mylbqi7Vz8VNaI/view?usp=sharing"
    },
    "Kab Cirebon": {
        "file": "DataKabCirebon.csv",
        "gdrive": "https://drive.google.com/file/d/1-5uMWGJ-9dSQwGPo8TOKFAig3U44Gyue/view?usp=sharing"
    },
    "Kuningan": {
        "file": "DataKotaKuningan.csv",
        "gdrive": "https://drive.google.com/file/d/1_qilfpMwNz0jZ83L-Rk9WIDIURSvFptK/view?usp=sharing"
    },
    "Indramayu": {
        "file": "DataKotaIndramayu.csv",
        "gdrive": "https://drive.google.com/file/d/11NbPohAAUxyXXIb3bJNsM0436Owb777Z/view?usp=sharing"
    },
    "Majalengka": {
        "file": "DataKotaMajalengka.csv",
        "gdrive": "https://drive.google.com/file/d/1l6DpYU44tkY7cauoH9a11OG_wV0KxC9R/view?usp=sharing"
    },
    "Lain2": {
        "file": "DataKotaLain2.csv",
        "gdrive": "https://drive.google.com/file/d/1-9G0yXDxknArbNVI_wLvF8PW8OPnqkuv/view?usp=sharing"
    },
    "RNG LCG": {
        "file": "RNG_LCG.csv",
        "gdrive": "https://drive.google.com/file/d/1DQI43a9-DEnP3FD1Rrl3WaWSS9XPTD9p/view?usp=sharing"
    },
    "Simulasi": {
        "file": "Simulasi_Monte_Carlo.csv",
        "gdrive": "https://drive.google.com/file/d/1vWcvlQb3N-C-SWmqbGN0uoSgngWQUDmP/view?usp=sharing"
    }
}

file_info = data_sources[menu]
base_path = os.path.dirname(__file__)
file_path = os.path.join(base_path, file_info["file"])
gdrive_link = file_info["gdrive"]

# Fungsi untuk konversi link Google Drive
def convert_gdrive_link(link):
    if "/d/" in link:
        file_id = link.split("/d/")[1].split("/")[0]
        return f"https://drive.google.com/uc?id={file_id}"
    return link

# Fungsi untuk memuat data dengan cache
@st.cache_data
def load_data_automatic(local_path, gdrive_url):
    try:
        if os.path.exists(local_path):
            df = pd.read_csv(local_path)
        else:
            st.info("📥 File lokal tidak ditemukan, mencoba unduh dari Google Drive...")
            download_url = convert_gdrive_link(gdrive_url)
            gdown.download(download_url, local_path, quiet=False)
            df = pd.read_csv(local_path)

        if df.shape[1] == 1:  # Fallback jika delimiter salah
            df = pd.read_csv(local_path, delimiter=";")
        return df
    except Exception as e:
        st.error(f"Gagal memuat data: {e}")
        return pd.DataFrame()

# Pilihan Upload Manual
uploaded_file = None
if source_option == "Upload Manual":
    uploaded_file = st.file_uploader("Unggah file CSV", type=["csv"])

# Load data sesuai pilihan
if source_option == "Otomatis (Lokal/Drive)":
    df = load_data_automatic(file_path, gdrive_link)
elif uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    df = pd.DataFrame()

# Tampilkan data
st.subheader(f"📄 {menu}")
if not df.empty:
    st.dataframe(df, use_container_width=True)
    st.markdown(f"**Jumlah Data:** {len(df)} baris")

    # Ringkasan statistik
    st.subheader("📊 Ringkasan Statistik")
    st.write(df.describe(include="all"))

    # Visualisasi jika ada kolom numerik
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    if len(numeric_cols) > 0:
        st.subheader("📈 Visualisasi Data")
        col_x = st.selectbox("Pilih X-axis", options=numeric_cols)
        col_y = st.selectbox("Pilih Y-axis", options=numeric_cols)
        fig = px.scatter(df, x=col_x, y=col_y, title=f"Scatter Plot {col_x} vs {col_y}")
        st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("⚠ Tidak ada data yang ditampilkan. Pastikan Anda memilih sumber data yang benar.")
