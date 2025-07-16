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
        "gdrive": "https://drive.google.com/file/d/1AgGhdLZiPDIBxUcVkipYN2GAy2tAIM9z/view?usp=sharing"
    },
    "Data Train": {
        "file": "DataTrain.csv",
        "gdrive": "https://drive.google.com/file/d/11tgNQ2GqMSIM97DH2U9HNTbIh4CceuiF/view?usp=sharing"
    },
    "Kota Cirebon": {
        "file": "DataKotaCirebon.csv",
        "gdrive": "https://drive.google.com/file/d/19ae9zMmGu8xc79VPCK9mPVXTkUu27tJI/view?usp=sharing"
    },
    "Kab Cirebon": {
        "file": "DataKabCirebon.csv",
        "gdrive": "https://drive.google.com/file/d/1qwDqsL9D71Id7js4isF9Azcit-gaOAaT/view?usp=sharing"
    },
    "Kuningan": {
        "file": "DataKotaKuningan.csv",
        "gdrive": "https://drive.google.com/file/d/1A3nd6dqBKeRzOo3Cpdd4BWl2g6qNxwVY/view?usp=sharing"
    },
    "Indramayu": {
        "file": "DataKotaIndramayu.csv",
        "gdrive": "https://drive.google.com/file/d/1a_t5kUyDzSrI0WILSqyPTy3LVKdBUwjU/view?usp=sharing"
    },
    "Majalengka": {
        "file": "DataKotaMajalengka.csv",
        "gdrive": "https://drive.google.com/file/d/1Ef4Gnl4o-5xDyX5Wu9OnQ0LRNRIb_grb/view?usp=sharing"
    },
    "Lain2": {
        "file": "DataKotaLain2.csv",
        "gdrive": "https://drive.google.com/file/d/1-2jsT3vhWqFDIdmGep40PCUv1lhKxE6N/view?usp=sharing"
    },
    "RNG LCG": {
        "file": "RNG_LCG.csv",
        "gdrive": "https://drive.google.com/file/d/1lWjneuxb7ecQZainm_igSmB24BXYmrmb/view?usp=sharing"
    },
    "Simulasi": {
        "file": "Simulasi_Monte_Carlo.csv",
        "gdrive": "https://drive.google.com/file/d/1sbZlQXUjU7Km5pQrCcM4e1gmOL0mAzzX/view?usp=sharing"
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
