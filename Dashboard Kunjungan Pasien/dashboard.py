import pandas as pd
import matplotlib.pyplot as plt

# Nama file Excel
file_excel = "Data Kunjungan Pasien.csv"

# Daftar sheet dan header row
sheet_headers = {
    'Data': 0,
    'Data Training': 2,
    'Probabilitas': 2,
    'Interval': 2,
    'RNG LCG': 2,
    'Simulasi': 2,
}

# Fungsi membaca sheet
def baca_sheet_dengan_header(file, sheet_name, header_row=0):
    try:
        df = pd.read_excel(file, sheet_name=sheet_name, header=header_row)
        df = df.dropna(how='all')  # Hapus baris yang semua kolomnya kosong
        return df
    except Exception as e:
        print(f"Gagal membaca sheet '{sheet_name}': {e}")
        return None

# Fungsi menampilkan grafik
def tampilkan_grafik(df, judul=''):
    try:
        df_num = df.select_dtypes(include='number')
        if df_num.empty:
            print("Tidak ada kolom numerik untuk divisualisasikan.")
            return

        label_col = df.columns[0]

        # Grafik garis
        df.plot(x=label_col, kind='line', title=f"{judul} - Garis")
        plt.grid()
        plt.show()

        # Grafik batang
        df.plot(x=label_col, kind='bar', title=f"{judul} - Batang")
        plt.grid()
        plt.show()

        # Grafik lingkaran (pie)
        if len(df.columns) > 2:
            pie_data = df.drop(columns=label_col).sum(numeric_only=True)
            pie_data.plot(kind='pie', autopct='%1.1f%%', title=f"{judul} - Pie")
            plt.ylabel('')
            plt.show()
    except Exception as e:
        print(f"Gagal menampilkan grafik: {e}")

# Fungsi menampilkan sheet dan grafik
def tampilkan_sheet(sheet_index):
    sheet_names = list(sheet_headers.keys())
    if 1 <= sheet_index <= len(sheet_names):
        sheet_name = sheet_names[sheet_index - 1]
        df = baca_sheet_dengan_header(file_excel, sheet_name, header_row=sheet_headers[sheet_name])
        if df is not None:
            print(f"\n--- {sheet_name} ---\n")
            print(df.head(12))
            tampilkan_grafik(df, judul=sheet_name)
    else:
        print("Pilihan tidak valid.")

# Menu utama
def menu():
    while True:
        print("\n=== MENU SIMULASI KUNJUNGAN PASIEN ===")
        for i, name in enumerate(sheet_headers.keys(), 1):
            print(f"{i}. {name}")
        print("0. Keluar")

        pilihan = input("Pilih menu [0-6]: ")
        if pilihan == '0':
            print("Selesai.")
            break
        elif pilihan.isdigit() and 1 <= int(pilihan) <= len(sheet_headers):
            tampilkan_sheet(int(pilihan))
        else:
            print("Pilihan tidak valid.")

menu()
