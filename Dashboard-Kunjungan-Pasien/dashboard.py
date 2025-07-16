import streamlit as st
import pandas as pd
import gdown
import os

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
        "gdrive": "https://drive.google.com/file/d/1GUHcM1xVSjU4aEIuH2QmRYFGYo0cCDEH/view?usp=sharing"
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

base_path = os.path.dirname(__file__)

# Fungsi konversi link Google Drive
def convert_gdrive_link(link):
    if "/d/" in link:
        file_id = link.split("/d/")[1].split("/")[0]
        return f"https://drive.google.com/uc?id={file_id}"
    return link

# Fungsi untuk memuat data
@st.cache_data
def load_data(local_path, gdrive_url):
    try:
        if os.path.exists(local_path):
            try:
                df = pd.read_csv(local_path, encoding="utf-8")
            except UnicodeDecodeError:
                df = pd.read_csv(local_path, encoding="ISO-8859-1")
        else:
            st.info(f"📥 File lokal {os.path.basename(local_path)} tidak ditemukan, mencoba unduh dari Google Drive...")
            download_url = convert_gdrive_link(gdrive_url)
            gdown.download(download_url, local_path, quiet=False)
            try:
                df = pd.read_csv(local_path, encoding="utf-8")
            except UnicodeDecodeError:
                df = pd.read_csv(local_path, encoding="ISO-8859-1")

        if df.shape[1] == 1:
            try:
                df = pd.read_csv(local_path, delimiter=";", encoding="utf-8")
            except UnicodeDecodeError:
                df = pd.read_csv(local_path, delimiter=";", encoding="ISO-8859-1")

        return df
    except Exception as e:
        st.error(f"Gagal memuat data: {e}")
        return pd.DataFrame()

# Fungsi menampilkan dataset
def show_dataset(name, source, upload_file=None):
    st.subheader(f"📄 {name}")
    info = data_sources[name]
    file_path = os.path.join(base_path, info["file"])

    if source == "Otomatis (Lokal/Drive)":
        df = load_data(file_path, info["gdrive"])
    elif upload_file is not None:
        try:
            df = pd.read_csv(upload_file, encoding="utf-8")
        except UnicodeDecodeError:
            df = pd.read_csv(upload_file, encoding="ISO-8859-1")
    else:
        df = pd.DataFrame()

    if not df.empty:
        st.dataframe(df, use_container_width=True)
        st.markdown(f"**Jumlah Data:** {len(df)} baris")
    else:
        st.warning(f"⚠ Tidak ada data yang ditampilkan untuk {name}.")

# Upload manual (jika dipilih)
uploaded_file = None
if source_option == "Upload Manual":
    uploaded_file = st.file_uploader("Unggah file CSV", type=["csv"])

# === Logika tampilkan data ===

multiple_dataset_menu = {
    "Kota Cirebon": ["Kota Cirebon", "Data Kunjungan Pasien"],
    "Kab Cirebon": ["Kab Cirebon", "Data Kunjungan Pasien"],
    "Kuningan": ["Kuningan", "Data Kunjungan Pasien"],
    "Indramayu": ["Indramayu", "Data Kunjungan Pasien"],
    "Majalengka": ["Majalengka", "Data Kunjungan Pasien"],
    "Lain2": ["Lain2", "Data Kunjungan Pasien"],
    "RNG LCG": ["RNG LCG", "Data Train"]
}

if menu in multiple_dataset_menu:
    for dataset in multiple_dataset_menu[menu]:
        show_dataset(dataset, source_option, uploaded_file)
else:
    show_dataset(menu, source_option, uploaded_file)
