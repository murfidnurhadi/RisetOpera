import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# --- Config ---
st.set_page_config(page_title="Amazon Review Analysis", layout="wide")
CSV_URL = "https://drive.google.com/uc?id=1MfpNbWOrLkclRtkZXEd3xA43tw_9jckN"

# --- Title ---
st.title("📊 Amazon Reviews Analysis & Sentiment Classification")

# --- Load Data ---
@st.cache_data
def load_data():
    return pd.read_csv(CSV_URL)

st.subheader("Load Dataset")
if st.button("📂 Load Data"):
    df = load_data()
    st.success(f"Data berhasil dimuat! Jumlah baris: {df.shape[0]}, Kolom: {df.shape[1]}")
    st.dataframe(df.head())

    # --- Data Overview ---
    st.subheader("🔍 Informasi Data")
    st.write(df.info())
    st.write(df.describe())

    # --- Missing Values ---
    st.subheader("🚨 Missing Values")
    st.write(df.isnull().sum())

    # --- Distribusi Label ---
    if 'sentiment' in df.columns or 'label' in df.columns:
        target_col = 'sentiment' if 'sentiment' in df.columns else 'label'
        st.subheader("📊 Distribusi Sentimen")
        fig, ax = plt.subplots()
        sns.countplot(x=target_col, data=df, ax=ax, palette='viridis')
        st.pyplot(fig)
    else:
        st.warning("Kolom target (sentiment/label) tidak ditemukan.")

    # --- Numeric Distribution ---
    st.subheader("📈 Distribusi Kolom Numerik")
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    if numeric_cols:
        col = st.selectbox("Pilih Kolom Numerik:", numeric_cols)
        fig, ax = plt.subplots()
        sns.histplot(df[col], bins=30, kde=True, ax=ax, color='blue')
        st.pyplot(fig)
    else:
        st.warning("Tidak ada kolom numerik.")

    # --- Model Training ---
    st.subheader("🤖 Machine Learning Model")
    text_col = st.selectbox("Pilih kolom teks untuk analisis:", df.columns)
    label_col = st.selectbox("Pilih kolom label:", df.columns)

    if st.button("🚀 Train Model"):
        # Preprocessing
        df = df.dropna(subset=[text_col, label_col])
        X = df[text_col].astype(str)
        y = df[label_col]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        vectorizer = TfidfVectorizer(max_features=5000)
        X_train_tfidf = vectorizer.fit_transform(X_train)
        X_test_tfidf = vectorizer.transform(X_test)

        model = LogisticRegression(max_iter=1000)
        model.fit(X_train_tfidf, y_train)

        y_pred = model.predict(X_test_tfidf)
        acc = accuracy_score(y_test, y_pred)

        st.success(f"✅ Model Trained! Akurasi: {acc:.4f}")
        st.text("Classification Report:")
        st.text(classification_report(y_test, y_pred))

        # Confusion Matrix
        st.subheader("📌 Confusion Matrix")
        cm = confusion_matrix(y_test, y_pred)
        fig, ax = plt.subplots()
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax)
        st.pyplot(fig)

        # Prediksi Manual
        st.subheader("📝 Coba Prediksi Sentimen")
        user_input = st.text_area("Masukkan teks review:")
        if st.button("Prediksi"):
            if user_input.strip():
                user_vec = vectorizer.transform([user_input])
                pred = model.predict(user_vec)[0]
                st.success(f"Prediksi Sentimen: **{pred}**")
            else:
                st.warning("Masukkan teks untuk diprediksi.")
