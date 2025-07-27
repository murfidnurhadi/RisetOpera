import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# --- Config ---
st.set_page_config(page_title="Sentiment Analysis & Assignment Model", layout="wide")
st.title("📊 Analisis Sentimen Amazon & Model Penugasan")

menu = st.sidebar.selectbox("Pilih Modul:", ["Sentiment Analysis", "Model Penugasan"])

# ======================
# 📌 SENTIMENT ANALYSIS
# ======================
if menu == "Sentiment Analysis":
    st.header("📌 Analisis Sentimen")
    
    # ✅ Data langsung terbaca tanpa tombol
    @st.cache_data
    def load_data():
        url = "https://drive.google.com/uc?id=1MfpNbWOrLkclRtkZXEd3xA43tw_9jckN"
        return pd.read_csv(url)
    
    df = load_data()
    st.success(f"Data berhasil dimuat! ({df.shape[0]} baris, {df.shape[1]} kolom)")
    st.dataframe(df.head())

    # Pilih kolom
    text_col = st.selectbox("Kolom Teks:", df.columns)
    target_col = st.selectbox("Kolom Target:", df.columns)
    
    model_choice = st.radio("Pilih Algoritma:", ["Logistic Regression", "Random Forest", "Naive Bayes"])
    
    # ✅ Training langsung dijalankan saat tombol ditekan, tanpa refresh
    if st.button("🚀 Train Model"):
        if text_col == target_col:
            st.error("Kolom Teks dan Target tidak boleh sama!")
        else:
            with st.spinner("Training model..."):
                # Preprocessing
                df = df.dropna(subset=[text_col, target_col])
                X = df[text_col].astype(str)
                y = df[target_col]
                
                # Split data
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
                
                # TF-IDF
                vectorizer = TfidfVectorizer(max_features=5000)
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
                
                # ✅ Tambah Grafik Batang Distribusi Target
                st.subheader("📊 Distribusi Target")
                fig = px.bar(y.value_counts(), x=y.value_counts().index, y=y.value_counts().values,
                             title="Distribusi Target", labels={"x":"Label", "y":"Jumlah"}, template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)
                
                # Confusion Matrix
                st.subheader("📌 Confusion Matrix")
                cm = confusion_matrix(y_test, y_pred)
                cm_fig = px.imshow(cm, text_auto=True, color_continuous_scale="Blues",
                                    title="Confusion Matrix", labels={"x":"Predicted", "y":"Actual"})
                st.plotly_chart(cm_fig)
