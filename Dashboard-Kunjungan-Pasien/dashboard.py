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

# Mapping data: Bisa lebih dari 1 dataset per menu (gunakan list)
data_sources = {
    "Data Kunjungan Pasien": [
        {
            "file": "Data_Kunjungan_Pasien.csv",
            "gdrive": "https://drive.google.com/file/d/1GUHcM1xVSjU4aEIuH2QmRYFGYo0cCDEH/view?usp=sharing"
        }
    ],
    "Data Train": [
        {
            "file": "DataTrain.csv",
            "gdrive": "https://drive.google.com/file/d/11tgNQ2GqMSIM97DH2U9HNTbIh4CceuiF/view?usp=sharing"
        }
    ],
    "Kota Cirebon": [
        {
            "file": "DataTrainKotaCirebon.csv",
            "gdrive": "https://drive.google.com/file/d/1t6K62d26MLv2C709xNPvd25wYXC0K2Ty/view?usp=drive_link"
        },
        {
            "file": "DataIntervalKotaCirebon.csv",
            "gdrive": "https://drive.google.com/file/d/1yuGJiVLxJCZJIH7_A7Jvr56BeulSnPZg/view?usp=drive_link"
        }
    ],
    "Kab Cirebon": [
        {
            "file": "DataTrainKabCirebon.csv",
            "gdrive": "https://drive.google.com/file/d/1m96_N5VCPjpga2NWr7SebxZcX3zrd_ou/view?usp=drive_link"
        },
        {
            "file": "DataIntervalKabCirebon.csv",
            "gdrive": "https://drive.google.com/file/d/1bqhfLiYPlsjYOhxxEspamSkoyhuJaLxe/view?usp=drive_link"
        }
    ],
    "Kuningan": [
        {
            "file": "DataTrainKuningan.csv",
            "gdrive": "https://drive.google.com/file/d/1Ta7DHwTtOUTuPUpTF6s25aUopK702phA/view?usp=drive_link"
        },
        {
            "file": "DataIntervalKuningan.csv",
            "gdrive": "https://drive.google.com/file/d/1XgwbODFSE8G1Vz6jojBsWevlc46w2kBy/view?usp=drive_link"
        }
    ],
    "Indramayu": [
        {
            "file": "DataTrainIndramayu.csv",
            "gdrive": "https://drive.google.com/file/d/1lYKdQPV_XFk4AAwuw6jbbzXqpsGvUCS3/view?usp=drive_link"
        },
        {
            "file": "DataIntervalIndramayu.csv",
            "gdrive": "https://drive.google.com/file/d/17g4yKK03ysNUyvPzsWxO0fMjOOQq5sA-/view?usp=drive_link"
        }
    ],
    "Majalengka": [
        {
            "file": "DataTrainMajalengka.csv",
            "gdrive": "https://drive.google.com/file/d/1xFZTTWn5QMLPMjwATtu-qMBlGOliUoiJ/view?usp=drive_link"
        },
        {
            "file": "DataIntervalMajalengka.csv",
            "gdrive": "https://drive.google.com/file/d/1PCpfJUWGhiOvLxCTdtr31zifIg7MOtu7/view?usp=drive_link"
        }
    ],
        "Lain2": [
        {
            "file": "DataTrainLain2.csv",
            "gdrive": "https://drive.google.com/file/d/1GPDnwgWwcnjBz_CHSrXXpbFVF1uLjmaK/view?usp=drive_link"
        },
        {
            "file": "DataIntervalLain2.csv",
            "gdrive": "https://drive.google.com/file/d/1I5zXYOJAhZf04LvlMkIdA8ceIXbc9exm/view?usp=drive_link"
        }
    ],
        "RNG LCG": [
        {
            "file": "RNG.csv",
            "gdrive": "https://drive.google.com/file/d/1fBZgfx9rYpBv29trUKkR1h9KT36g7udD/view?usp=sharing"
        },
        {
            "file": "LCG.csv",
            "gdrive": "https://drive.google.com/file/d/1MJMALE9054J2F6c1w-HYNRe9sftk2JGP/view?usp=sharing"
        }
    ],
    "Simulasi": [
        {
            "file": "Simulasi_Monte_Carlo.csv",
            "gdrive": "https://drive.google.com/file/d/1sbZlQXUjU7Km5pQrCcM4e1gmOL0mAzzX/view?usp=sharing"
        }
    ]
}

# Fungsi konversi link Google Drive
def convert_gdrive_link(link):
    if "/d/" in link:
        file_id = link.split("/d/")[1].split("/")[0]
        return f"https://drive.google.com/uc?id={file_id}"
    return link

# Fungsi load data (lokal/drive)
@st.cache_data
def load_data(local_path, gdrive_url):
    try:
        if os.path.exists(local_path):
            try:
                df = pd.read_csv(local_path, encoding="utf-8")
            except UnicodeDecodeError:
                df = pd.read_csv(local_path, encoding="ISO-8859-1")
        else:
            st.info(f"📥 File {os.path.basename(local_path)} tidak ditemukan, mencoba download dari Drive...")
            download_url = convert_gdrive_link(gdrive_url)
            gdown.download(download_url, local_path, quiet=False)
            try:
                df = pd.read_csv(local_path, encoding="utf-8")
            except UnicodeDecodeError:
                df = pd.read_csv(local_path, encoding="ISO-8859-1")

        if df.shape[1] == 1:  # delimiter mungkin salah
            try:
                df = pd.read_csv(local_path, delimiter=";", encoding="utf-8")
            except UnicodeDecodeError:
                df = pd.read_csv(local_path, delimiter=";", encoding="ISO-8859-1")

        return df
    except Exception as e:
        st.error(f"Gagal memuat data: {e}")
        return pd.DataFrame()

# Fungsi untuk menampilkan banyak dataset dalam satu menu
def show_multiple_datasets(menu, source_option, uploaded_file=None):
    datasets = data_sources.get(menu, [])
    base_path = os.getcwd()  # gunakan cwd agar kompatibel di Streamlit Cloud/Local

    for idx, info in enumerate(datasets):
        st.subheader(f"📄 {menu} - Dataset {idx+1}")
        file_path = os.path.join(base_path, info["file"])

        if source_option == "Otomatis (Lokal/Drive)":
            df = load_data(file_path, info["gdrive"])
        elif uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file, encoding="utf-8")
            except UnicodeDecodeError:
                df = pd.read_csv(uploaded_file, encoding="ISO-8859-1")
        else:
            df = pd.DataFrame()

        if not df.empty:
            st.dataframe(df, use_container_width=True)
            st.markdown(f"**Jumlah Data:** {len(df)} baris")
        else:
            st.warning(f"⚠ Tidak ada data untuk {menu} - Dataset {idx+1}.")

# Upload Manual jika dipilih
uploaded_file = None
if source_option == "Upload Manual":
    uploaded_file = st.file_uploader("Unggah file CSV", type=["csv"])

# Jalankan tampilan
if menu in data_sources:
    show_multiple_datasets(menu, source_option, uploaded_file)
else:
    st.warning("⚠ Dataset belum tersedia.")
