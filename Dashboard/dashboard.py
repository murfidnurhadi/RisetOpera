import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from scipy.optimize import linear_sum_assignment
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Konfigurasi Halaman
st.set_page_config(page_title="Sentiment & Assignment", layout="wide")

# Header Utama
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>📊 Dashboard Analisis Sentimen & Model Penugasan</h1>", unsafe_allow_html=True)
st.write("---")

# Sidebar Menu
menu = st.sidebar.radio("📌 Pilih Modul:", ["Analisis Sentimen", "Model Penugasan"])

# =========================
# ✅ MODUL ANALISIS SENTIMEN
# =========================
if menu == "Analisis Sentimen":
    st.subheader("🔍 Analisis Sentimen Amazon (Sample 10 Data)")

    @st.cache_data
    def load_data():
        url = "https://drive.google.com/uc?id=1MfpNbWOrLkclRtkZXEd3xA43tw_9jckN"
        df = pd.read_csv(url)
        return df.sample(10, random_state=42)  # Ambil 10 data saja

    df = load_data()
    st.success("Data berhasil dimuat! (Sample 10 Baris)")
    st.dataframe(df)

    col1, col2 = st.columns(2)
    with col1:
        text_col = st.selectbox("Kolom Teks:", df.columns)
    with col2:
        target_col = st.selectbox("Kolom Target:", df.columns)

    model_choice = st.radio("Pilih Algoritma:", ["Logistic Regression", "Random Forest", "Naive Bayes"], horizontal=True)

    if st.button("🚀 Train Model", use_container_width=True):
        if text_col == target_col:
            st.error("Kolom teks dan target tidak boleh sama!")
        else:
            with st.spinner("Training model..."):
                # Preprocessing
                df = df.dropna(subset=[text_col, target_col])
                X = df[text_col].astype(str)
                y = df[target_col]

                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

                vectorizer = TfidfVectorizer(max_features=500)
                X_train_tf = vectorizer.fit_transform(X_train)
                X_test_tf = vectorizer.transform(X_test)

                # Model
                if model_choice == "Logistic Regression":
                    model = LogisticRegression(max_iter=1000)
                elif model_choice == "Random Forest":
                    model = RandomForestClassifier(n_estimators=100)
                else:
                    model = MultinomialNB()

                model.fit(X_train_tf, y_train)
                y_pred = model.predict(X_test_tf)

                acc = accuracy_score(y_test, y_pred)
                st.success(f"Akurasi Model: {acc:.4f}")
                st.text("Classification Report:")
                st.text(classification_report(y_test, y_pred))

                # Grafik distribusi target
                st.subheader("📊 Distribusi Target")
                fig = px.bar(y.value_counts(), x=y.value_counts().index, y=y.value_counts().values,
                             title="Distribusi Label", labels={"x": "Label", "y": "Jumlah"}, template="plotly_dark",
                             color=y.value_counts().index)
                st.plotly_chart(fig, use_container_width=True)

                # Confusion Matrix
                st.subheader("📌 Confusion Matrix")
                cm = confusion_matrix(y_test, y_pred)
                cm_fig = px.imshow(cm, text_auto=True, color_continuous_scale="Blues",
                                   title="Confusion Matrix", labels={"x": "Predicted", "y": "Actual"})
                st.plotly_chart(cm_fig)

# =========================
# ✅ MODUL MODEL PENUGASAN
# =========================
elif menu == "Model Penugasan":
    st.subheader("📌 Model Penugasan (Metode Hungarian)")
    st.write("**Asumsi:** Jumlah agen = jumlah tujuan. Jika tidak, tambahkan dummy agar seimbang.")

    # Pilih tipe masalah
    mode = st.radio("Pilih Jenis Masalah:", ["Minimasi Biaya", "Maksimisasi Keuntungan"], horizontal=True)

    # Input ukuran matriks
    n = st.number_input("Jumlah Agen/Tujuan:", min_value=2, max_value=8, value=4)

    st.markdown("### Masukkan Matriks:")
    st.caption("Contoh baris: 10,20,30,40")
    cost_matrix = []
    for i in range(n):
        row = st.text_input(f"Baris {i + 1}:", value="10,20,30,40")
        cost_matrix.append([int(x) for x in row.split(",")])

    if st.button("✅ Hitung Penugasan Optimal", use_container_width=True):
        cost = np.array(cost_matrix)

        # Jika mode maksimisasi → ubah ke minimisasi
        if mode == "Maksimisasi Keuntungan":
            max_val = cost.max()
            cost_converted = max_val - cost
        else:
            cost_converted = cost

        row_ind, col_ind = linear_sum_assignment(cost_converted)
        total_cost = cost[row_ind, col_ind].sum()

        st.success(f"Total {'Keuntungan Maksimum' if mode=='Maksimisasi Keuntungan' else 'Biaya Minimum'}: {total_cost}")

        st.write("📌 **Penugasan Optimal:**")
        for i in range(len(row_ind)):
            st.write(f"Agen {row_ind[i] + 1} → Tujuan {col_ind[i] + 1} (Nilai: {cost[row_ind[i], col_ind[i]]})")

        # Heatmap Matriks
        st.subheader("📊 Visualisasi Matriks")
        fig = px.imshow(cost, text_auto=True, color_continuous_scale="Blues",
                        title="Matriks Biaya/Keuntungan", labels={"x": "Tujuan", "y": "Agen"})
        st.plotly_chart(fig)
