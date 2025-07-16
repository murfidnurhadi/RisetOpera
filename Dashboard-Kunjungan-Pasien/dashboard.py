import streamlit as st
import pandas as pd
import gdown
import os
import plotly.express as px

# Konfigurasi halaman
st.set_page_config(page_title="Dashboard Simulasi Monte Carlo", layout="wide")
st.title("📊 Dashboard Simulasi Monte Carlo")

# Sidebar navigasi
st.sidebar.header("📌 Menu Navigasi")
menu = st.sidebar.selectbox("Pilih Dataset:", [
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
source_option = st.sidebar.radio("Ambil data dari:", ["Otomatis (Lokal/Drive)", "Upload Manual"])

# Mapping dataset
data_sources = {
    "Kota Cirebon": [
        {"file": "DataTrainKotaCirebon.csv",
         "gdrive": "https://drive.google.com/file/d/1t6K62d26MLv2C709xNPvd25wYXC0K2Ty/view?usp=drive_link",
         "judul": "Data Train Kota Cirebon"},
        {"file": "DataIntervalKotaCirebon.csv",
         "gdrive": "https://drive.google.com/file/d/1yuGJiVLxJCZJIH7_A7Jvr56BeulSnPZg/view?usp=drive_link",
         "judul": "Data Interval Kota Cirebon"}
    ],
    "Kab Cirebon": [
        {"file": "DataTrainKabCirebon.csv",
         "gdrive": "https://drive.google.com/file/d/1m96_N5VCPjpga2NWr7SebxZcX3zrd_ou/view?usp=drive_link",
         "judul": "Data Train Kab Cirebon"},
        {"file": "DataIntervalKabCirebon.csv",
         "gdrive": "https://drive.google.com/file/d/1bqhfLiYPlsjYOhxxEspamSkoyhuJaLxe/view?usp=drive_link",
         "judul": "Data Interval Kab Cirebon"}
    ],
    "Data Kunjungan Pasien": [
        {"file": "Data_Kunjungan_Pasien.csv",
         "gdrive": "https://drive.google.com/file/d/1GUHcM1xVSjU4aEIuH2QmRYFGYo0cCDEH/view?usp=sharing",
         "judul": "Data Kunjungan Pasien"}
    ]
}

# Fungsi konversi link Google Drive
def convert_gdrive_link(link):
    if "/d/" in link:
        file_id = link.split("/d/")[1].split("/")[0]
        return f"https://drive.google.com/uc?id={file_id}"
    return link

# Fungsi load data
@st.cache_data
def load_data(local_path, gdrive_url):
    try:
        if os.path.exists(local_path):
            df = pd.read_csv(local_path)
        else:
            st.info(f"📥 Mengunduh {os.path.basename(local_path)} dari Drive...")
            gdown.download(convert_gdrive_link(gdrive_url), local_path, quiet=False)
            df = pd.read_csv(local_path)
        return df
    except Exception as e:
        st.error(f"Gagal memuat data: {e}")
        return pd.DataFrame()

# Upload manual
uploaded_file = None
if source_option == "Upload Manual":
    uploaded_file = st.file_uploader("Unggah file CSV", type=["csv"])

# Tampilkan dataset
datasets = data_sources.get(menu, [])
if not datasets:
    st.warning("⚠ Dataset belum tersedia.")
else:
    for idx, info in enumerate(datasets):
        judul = info.get("judul", f"{menu} - Dataset {idx+1}")
        st.subheader(f"📄 {judul}")
        file_path = os.path.join(os.getcwd(), info["file"])

        if source_option == "Otomatis (Lokal/Drive)":
            df = load_data(file_path, info["gdrive"])
        elif uploaded_file:
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.DataFrame()

        if df.empty:
            st.warning(f"⚠ Tidak ada data untuk {judul}.")
        else:
            # ✅ Tampilkan data
            st.dataframe(df, use_container_width=True)
            st.markdown(f"**Jumlah Data:** {len(df)} baris")

            # ✅ Filter dinamis
            with st.expander("🔍 Filter Data"):
                for col in df.columns:
                    if df[col].dtype == "object":
                        options = st.multiselect(f"Filter {col}", df[col].unique())
                        if options:
                            df = df[df[col].isin(options)]
                    else:
                        min_val, max_val = st.slider(f"Rentang {col}", float(df[col].min()), float(df[col].max()),
                                                     (float(df[col].min()), float(df[col].max())))
                        df = df[(df[col] >= min_val) & (df[col] <= max_val)]

                st.dataframe(df)

            # ✅ Pilih kolom untuk grafik
            if len(df.columns) >= 2:
                st.subheader("📈 Visualisasi Data")
                chart_type = st.radio("Pilih Jenis Grafik", ["Bar", "Line", "Pie"], horizontal=True)
                col_x = st.selectbox("Kolom X", df.columns)
                col_y = st.selectbox("Kolom Y", df.columns)

                if chart_type == "Bar":
                    fig = px.bar(df, x=col_x, y=col_y, title="Bar Chart")
                elif chart_type == "Line":
                    fig = px.line(df, x=col_x, y=col_y, title="Line Chart")
                else:
                    fig = px.pie(df, names=col_x, values=col_y, title="Pie Chart")
                st.plotly_chart(fig, use_container_width=True)

            # ✅ Tombol download data hasil filter
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(label="📥 Download Data (CSV)", data=csv, file_name="filtered_data.csv",
                               mime="text/csv")
