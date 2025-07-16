import streamlit as st
import pandas as pd
import gdown
import os
import plotly.express as px

st.set_page_config(page_title="Dashboard Simulasi Monte Carlo", layout="wide")
st.title("📊 Dashboard Simulasi Monte Carlo")

# Sidebar
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

source_option = st.sidebar.radio("Ambil data dari:", ["Otomatis (Lokal/Drive)", "Upload Manual"])

data_sources = {
    "Data Kunjungan Pasien": [
        {"file": "Data_Kunjungan_Pasien.csv", "gdrive": "https://drive.google.com/file/d/1GUHcM1xVSjU4aEIuH2QmRYFGYo0cCDEH/view?usp=sharing", "judul": "Data Kunjungan Pasien"}
    ],
    "Data Train": [
        {"file": "DataTrain.csv", "gdrive": "https://drive.google.com/file/d/11tgNQ2GqMSIM97DH2U9HNTbIh4CceuiF/view?usp=sharing", "judul": "Data Train Gabungan"}
    ]
}

def convert_gdrive_link(link):
    if "/d/" in link:
        file_id = link.split("/d/")[1].split("/")[0]
        return f"https://drive.google.com/uc?id={file_id}"
    return link

@st.cache_data
def load_data(local_path, gdrive_url):
    try:
        if os.path.exists(local_path):
            df = pd.read_csv(local_path, low_memory=False)
        else:
            st.info(f"📥 Mengunduh {os.path.basename(local_path)} dari Google Drive...")
            gdown.download(convert_gdrive_link(gdrive_url), local_path, quiet=False)
            df = pd.read_csv(local_path, low_memory=False)

        if df.shape[1] == 1:  # Jika salah delimiter
            df = pd.read_csv(local_path, delimiter=";", low_memory=False)

        return df
    except Exception as e:
        st.error(f"Gagal memuat data: {e}")
        return pd.DataFrame()

uploaded_file = None
if source_option == "Upload Manual":
    uploaded_file = st.file_uploader("Unggah file CSV", type=["csv"])

datasets = data_sources.get(menu, [])
if not datasets:
    st.warning("⚠ Dataset belum tersedia.")
else:
    for idx, info in enumerate(datasets):
        st.subheader(f"📄 {info['judul']}")
        file_path = os.path.join(os.getcwd(), info["file"])

        if source_option == "Otomatis (Lokal/Drive)":
            df = load_data(file_path, info["gdrive"])
        elif uploaded_file:
            df = pd.read_csv(uploaded_file, low_memory=False)
        else:
            df = pd.DataFrame()

        if df.empty:
            st.warning("⚠ Tidak ada data untuk ditampilkan.")
            continue

        st.dataframe(df, use_container_width=True)
        st.markdown(f"**Jumlah Data:** {len(df)} baris")

        # ✅ Filter Dinamis
        with st.expander("🔍 Filter Data"):
            df_filtered = df.copy()
            for col in df.columns:
                if df[col].dtype == "object":
                    options = st.multiselect(f"Filter {col}", df[col].dropna().unique())
                    if options:
                        df_filtered = df_filtered[df_filtered[col].isin(options)]
                else:
                    try:
                        min_val = float(df[col].min())
                        max_val = float(df[col].max())
                        if min_val != max_val:  # ✅ Cek agar slider tidak error
                            min_slider, max_slider = st.slider(f"Rentang {col}", min_val, max_val, (min_val, max_val))
                            df_filtered = df_filtered[(df_filtered[col] >= min_slider) & (df_filtered[col] <= max_slider)]
                    except:
                        pass

            st.dataframe(df_filtered)

        # ✅ Visualisasi
        if len(df_filtered.columns) >= 2:
            st.subheader("📈 Visualisasi Data")
            chart_type = st.radio("Pilih Grafik", ["Bar", "Line", "Pie"], horizontal=True)
            col_x = st.selectbox("Kolom X", df_filtered.columns)
            col_y = st.selectbox("Kolom Y", df_filtered.columns)

            try:
                if chart_type == "Bar":
                    fig = px.bar(df_filtered, x=col_x, y=col_y, title="Bar Chart")
                elif chart_type == "Line":
                    fig = px.line(df_filtered, x=col_x, y=col_y, title="Line Chart")
                else:
                    fig = px.pie(df_filtered, names=col_x, values=col_y, title="Pie Chart")
                st.plotly_chart(fig, use_container_width=True)
            except:
                st.warning("⚠ Tidak bisa membuat grafik. Pastikan kolom numerik untuk Y.")

        # ✅ Download
        csv = df_filtered.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Data (CSV)", csv, file_name="filtered_data.csv", mime="text/csv")
