import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# --- Streamlit Config ---
st.set_page_config(page_title="Amazon Review Analysis", layout="wide")

# --- Header ---
st.title("📊 Amazon Reviews Sentiment Analysis & ML Dashboard")

# --- Source Selector ---
st.sidebar.header("⚙️ Pilih Sumber Data")
data_source = st.sidebar.radio("Sumber Data:", ("Google Drive", "Upload File"))

# --- Load Data ---
@st.cache_data
def load_data_from_gdrive():
    url = "https://drive.google.com/uc?id=1MfpNbWOrLkclRtkZXEd3xA43tw_9jckN"
    return pd.read_csv(url)

if data_source == "Google Drive":
    st.subheader("📂 Load Dataset dari Google Drive")
    if st.button("Load Data dari GDrive"):
        df = load_data_from_gdrive()
        st.success(f"Data berhasil dimuat! ({df.shape[0]} baris, {df.shape[1]} kolom)")
        st.dataframe(df.head())
else:
    st.subheader("📂 Upload CSV Manual")
    uploaded_file = st.file_uploader("Upload file CSV", type="csv")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.success(f"File berhasil diupload! ({df.shape[0]} baris, {df.shape[1]} kolom)")
        st.dataframe(df.head())

# Pastikan df ada
if 'df' in locals():
    # --- EDA Section ---
    st.subheader("📊 Exploratory Data Analysis")
    
    st.write("**Info Kolom:**")
    st.write(df.info())
    
    st.write("**Statistik Deskriptif:**")
    st.write(df.describe())
    
    # Missing values
    st.write("**Missing Values:**")
    st.write(df.isnull().sum())
    
    # Distribusi target
    st.subheader("📈 Distribusi Target")
    target_col = st.selectbox("Pilih kolom target (label/sentimen):", df.columns)
    fig = px.histogram(df, x=target_col, color=target_col, title="Distribusi Target", template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)
    
    # Numeric columns distribution
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    if numeric_cols:
        st.subheader("📊 Distribusi Kolom Numerik")
        num_col = st.selectbox("Pilih kolom numerik:", numeric_cols)
        fig = px.histogram(df, x=num_col, nbins=30, title=f"Distribusi {num_col}", template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)
    
    # --- ML Section ---
    st.subheader("🤖 Machine Learning Model")
    text_col = st.selectbox("Pilih kolom teks:", df.columns)
    
    model_choice = st.radio("Pilih Algoritma ML:", ("Logistic Regression", "Random Forest", "Naive Bayes"))
    
    if st.button("🚀 Train Model"):
        df = df.dropna(subset=[text_col, target_col])
        X = df[text_col].astype(str)
        y = df[target_col]
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        vectorizer = TfidfVectorizer(max_features=5000)
        X_train_tfidf = vectorizer.fit_transform(X_train)
        X_test_tfidf = vectorizer.transform(X_test)
        
        if model_choice == "Logistic Regression":
            model = LogisticRegression(max_iter=1000)
        elif model_choice == "Random Forest":
            model = RandomForestClassifier(n_estimators=100, random_state=42)
        else:
            model = MultinomialNB()
        
        model.fit(X_train_tfidf, y_train)
        y_pred = model.predict(X_test_tfidf)
        
        acc = accuracy_score(y_test, y_pred)
        st.success(f"✅ Model {model_choice} dilatih! Akurasi: {acc:.4f}")
        
        st.text("Classification Report:")
        st.text(classification_report(y_test, y_pred))
        
        # Confusion Matrix
        cm = confusion_matrix(y_test, y_pred)
        fig_cm = px.imshow(cm, text_auto=True, color_continuous_scale="Blues",
                           title="Confusion Matrix")
        st.plotly_chart(fig_cm, use_container_width=True)
        
        # Predict user input
        st.subheader("🔮 Prediksi Sentimen Manual")
        user_input = st.text_area("Masukkan teks review:")
        if st.button("Prediksi"):
            if user_input.strip():
                user_vec = vectorizer.transform([user_input])
                pred = model.predict(user_vec)[0]
                st.success(f"Hasil Prediksi: **{pred}**")
            else:
                st.warning("Masukkan teks terlebih dahulu!")
