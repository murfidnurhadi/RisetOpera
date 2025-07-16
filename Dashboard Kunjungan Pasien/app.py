import streamlit as st
import pandas as pd
import plotly.express as px

# Konfigurasi halaman
st.set_page_config(layout="wide", page_title="Dashboard Kunjungan Pasien", page_icon="🏥")

# Fungsi untuk memuat data
@st.cache_data
def load_data():
    file_path = "Data_Kujungan_Pasien.csv"  # Pastikan file ada di repo GitHub Anda
    # Skip baris awal yang bukan data
    df = pd.read_csv(file_path, skiprows=2)
    
    # Ambil kolom penting
    df = df[["tahun", "bulan", "Angka Acak", "Kota Cirebon", "Kab. Cirebon",
             "Kuningan", "Indramayu", "Majalengka", "Lain-lain"]]

    # Hilangkan baris kosong
    df = df.dropna(subset=["tahun", "bulan"])
    
    # Ubah format tahun menjadi int
    df["tahun"] = df["tahun"].astype(int)

    # Ubah ke format long agar mudah visualisasi
    df_melted = df.melt(id_vars=["tahun", "bulan", "Angka Acak"], 
                        var_name="Wilayah", value_name="Jumlah Pasien")
    df_melted["Jumlah Pasien"] = pd.to_numeric(df_melted["Jumlah Pasien"], errors="coerce").fillna(0)
    return df_melted

# Load data
df = load_data()

# Sidebar Filter
with st.sidebar:
    st.title("🏥 Filter Data")
    tahun_list = sorted(df["tahun"].unique())
    selected_tahun = st.multiselect("Pilih Tahun", tahun_list, default=tahun_list)
    
    wilayah_list = df["Wilayah"].unique()
    selected_wilayah = st.multiselect("Pilih Wilayah", wilayah_list, default=wilayah_list)

# Filter data sesuai pilihan
filtered_df = df[(df["tahun"].isin(selected_tahun)) & (df["Wilayah"].isin(selected_wilayah))]

# Tampilan Utama
st.title("📊 Dashboard Kunjungan Pasien Rawat Inap")
st.markdown("### Rumah Sakit Gunung Jati - Kota Cirebon")

# KPI: Total Kunjungan
total_kunjungan = int(filtered_df["Jumlah Pasien"].sum())
col1, col2 = st.columns(2)
col1.metric("Total Kunjungan", f"{total_kunjungan:,}")
col2.metric("Jumlah Wilayah", len(selected_wilayah))

# Grafik Tren per Bulan
st.subheader("📈 Tren Kunjungan per Bulan")
fig_trend = px.line(filtered_df, x="bulan", y="Jumlah Pasien", color="Wilayah",
                    title="Tren Kunjungan Pasien per Wilayah",
                    markers=True)
st.plotly_chart(fig_trend, use_container_width=True)

# Distribusi per Wilayah (Bar)
st.subheader("📊 Distribusi Total Kunjungan per Wilayah")
wilayah_total = filtered_df.groupby("Wilayah")["Jumlah Pasien"].sum().reset_index()
fig_bar = px.bar(wilayah_total, x="Wilayah", y="Jumlah Pasien", color="Wilayah",
                 title="Distribusi Kunjungan", text="Jumlah Pasien")
st.plotly_chart(fig_bar, use_container_width=True)

# Pie Chart
st.subheader("🍩 Proporsi Kunjungan per Wilayah")
fig_pie = px.pie(wilayah_total, names="Wilayah", values="Jumlah Pasien",
                 hole=0.4, title="Proporsi Kunjungan")
st.plotly_chart(fig_pie, use_container_width=True)

# Tabel Data
st.subheader("📄 Data Detail")
st.dataframe(filtered_df)

# Footer
st.markdown("---")
st.markdown("📌 **Dashboard ini dibuat oleh Kelompok 6 | UNIKOM**")
