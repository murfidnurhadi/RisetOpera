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

# Streamlit Config
st.set_page_config(page_title="Amazon Reviews & Assignment Model", layout="wide")
st.title("📊 Analisis Amazon Reviews & Model Penugasan")

menu = st.sidebar.selectbox("Pilih Modul:", ["Sentiment Analysis", "Model Penugasan"])

# =====================
# 📌 MODUL SENTIMENT ANALYSIS
# =====================
if menu == "Sentiment Analysis":
    st.header("📌 Modul Analisis Sentimen")
    data_source = st.radio("Sumber Data:", ("Google Drive", "Upload CSV"))
    
    @st.cache_data
    def load_data_gdrive():
        url = "https://drive.google.com/uc?id=1MfpNbWOrLkclRtkZXEd3xA43tw_9jckN"
        return pd.read_csv(url)
    
    if data_source == "Google Drive":
        if st.button("Load Data"):
            df = load_data_gdrive()
            st.success(f"Data dimuat! Baris: {df.shape[0]}, Kolom: {df.shape[1]}")
            st.dataframe(df.head())
    else:
        file = st.file_uploader("Upload CSV", type="csv")
        if file:
            df = pd.read_csv(file)
            st.success(f"File berhasil diupload! ({df.shape[0]} baris)")
            st.dataframe(df.head())
    
    if 'df' in locals():
        st.subheader("Model Training")
        text_col = st.selectbox("Kolom Teks:", df.columns)
        target_col = st.selectbox("Kolom Target:", df.columns)
        model_choice = st.radio("Pilih Algoritma:", ["Logistic Regression", "Random Forest", "Naive Bayes"])
        
        if st.button("Train Model"):
            df = df.dropna(subset=[text_col, target_col])
            X = df[text_col].astype(str)
            y = df[target_col]
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            vec = TfidfVectorizer(max_features=5000)
            X_train_tf = vec.fit_transform(X_train)
            X_test_tf = vec.transform(X_test)
            
            if model_choice == "Logistic Regression":
                model = LogisticRegression(max_iter=1000)
            elif model_choice == "Random Forest":
                model = RandomForestClassifier(n_estimators=100)
            else:
                model = MultinomialNB()
            
            model.fit(X_train_tf, y_train)
            y_pred = model.predict(X_test_tf)
            acc = accuracy_score(y_test, y_pred)
            st.success(f"Akurasi: {acc:.4f}")
            st.text(classification_report(y_test, y_pred))
            
            cm = confusion_matrix(y_test, y_pred)
            st.write("Confusion Matrix:")
            st.write(cm)

# =====================
# 📌 MODUL MODEL PENUGASAN
# =====================
elif menu == "Model Penugasan":
    st.header("📌 Model Penugasan (Assignment Problem)")
    st.write("""
    **Asumsi:**
    - Jumlah agen = jumlah tujuan.
    - Tujuan: meminimalkan total biaya penugasan.
    """)
    
    source = st.radio("Pilih sumber data:", ["Input Manual", "Upload CSV"])
    
    if source == "Input Manual":
        n = st.number_input("Masukkan jumlah Agen/Tujuan:", min_value=2, max_value=10, value=3)
        st.write("Masukkan Matriks Biaya:")
        
        cost_matrix = []
        for i in range(n):
            row = st.text_input(f"Baris {i+1} (pisahkan dengan koma):", value="10,20,30")
            cost_matrix.append([int(x) for x in row.split(",")])
        
        if st.button("Hitung Penugasan Optimal"):
            cost = np.array(cost_matrix)
            row_ind, col_ind = linear_sum_assignment(cost)
            total_cost = cost[row_ind, col_ind].sum()
            st.success(f"Total Biaya Minimum: {total_cost}")
            st.write("Penugasan Optimal:")
            for i in range(len(row_ind)):
                st.write(f"Agen {row_ind[i]+1} → Tujuan {col_ind[i]+1} (Biaya: {cost[row_ind[i], col_ind[i]]})")
    
    else:
        file = st.file_uploader("Upload CSV Matriks Biaya", type="csv")
        if file:
            df_cost = pd.read_csv(file, index_col=0)
            st.write("Matriks Biaya:")
            st.dataframe(df_cost)
            
            if st.button("Hitung Penugasan Optimal"):
                cost = df_cost.to_numpy()
                row_ind, col_ind = linear_sum_assignment(cost)
                total_cost = cost[row_ind, col_ind].sum()
                st.success(f"Total Biaya Minimum: {total_cost}")
                st.write("Penugasan Optimal:")
                for i in range(len(row_ind)):
                    st.write(f"Agen {row_ind[i]+1} → Tujuan {col_ind[i]+1} (Biaya: {cost[row_ind[i], col_ind[i]]})")
