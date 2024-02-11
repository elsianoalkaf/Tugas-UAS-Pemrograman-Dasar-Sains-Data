import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu


st.cache_data
def load_data(url) :
    df = pd.read_csv(url)
    return df

def lama_pengiriman(df_data_order):
    #Cek apakah ada missing value atau tidak
    df_data_order_null = df_data_order.isnull().values.any()
    df_data_order.isnull().sum()

    #Cek apakah ada data duplikat atau tidak
    df_data_order_duplicate = df_data_order.duplicated().values.any()

    #Cleaning data products_dataset.csv
    df_data_order.dropna(subset=['order_approved_at','order_delivered_carrier_date','order_delivered_customer_date'], axis=0, inplace=True)
    df_data_order.reset_index(drop=True, inplace=True)

    #Mengubah kolom 'order_purchase_timestamp' dan 'order_delivered_customer_date' menjadi tipe data datetime
    df_data_order['order_purchase_timestamp'] = pd.to_datetime(df_data_order['order_purchase_timestamp'])
    df_data_order['order_delivered_customer_date'] = pd.to_datetime(df_data_order['order_delivered_customer_date'])
    
    #Menghitung berapa lama pembeli menerima barang setelah memesannya
    df_data_order['lama_pengiriman'] = (df_data_order['order_delivered_customer_date'] - df_data_order['order_purchase_timestamp']).dt.days

    #Menampilkan DataFrame dengan kolom tambahan 'lama_pengiriman'
    st.write("Tabel hasil perhitungan lama pengiriman :")
    df_data_beli = df_data_order['order_delivered_customer_date']
    df_data_sampai = df_data_order['order_purchase_timestamp']
    lama_kirim = df_data_order['lama_pengiriman']

    tabel_hasil = pd.DataFrame({
        'Tanggal pembelian' : df_data_beli,
        'Tanggal sampai' : df_data_sampai,
        'Lama Pengiriman' : lama_kirim
    })

    #Mengambil data lama pengiriman barang
    waktu_pengiriman = df_data_order['lama_pengiriman'].values

    #Mengambil jumlah barang dengan waktu pengiriman kurang dari 30 hari
    waktu_U30 = waktu_pengiriman[(waktu_pengiriman >= 1) & (waktu_pengiriman < 30)]
    jumlah_waktu_U30 = len(waktu_U30)

    #Mengambil jumlah barang dengan waktu pengiriman lebih dari sama dengan 30 hari
    waktu_A30 = waktu_pengiriman[(waktu_pengiriman >= 30)]
    jumlah_waktu_A30 = len(waktu_A30)

    #Memvisualisasikan data lama pengiriman
    fig, ax = plt.subplots()
    ax.hist(df_data_order['lama_pengiriman'], bins=30, color='lightgreen', edgecolor='black')
    ax.set_title('Histogram Lama Pengiriman')
    ax.set_xlabel('Lama Pengiriman (hari)')
    ax.set_ylabel('Frekuensi')
    ax.set_xlim(0, 80)

    #menampilkan tabel hasil perhitungan
    st.dataframe(tabel_hasil)

    #menampilkan hasil visualisasi data lama pengiriman
    st.write('Diagram Lama Pengiriman Paket Kepada Pelanggan')
    st.pyplot(fig)    

    #Banyak barang yang waktu pengirimannya kurang dari 30 hari dan lebih dari sama dengan 30 hari
    st.write('Banyak barang yang waktu pengirimannya lebih 30 hari =', jumlah_waktu_U30)
    st.write('Banyak barang yang waktu pengirimannya lebih dari sama dengan 30 hari =', jumlah_waktu_A30)

    with st.expander("Conclusion dari pertanyaan kedua") :
        st.write(
            """
            - Conclution pertanyaan 2 \n
                Berdasarkan histogram di atas dapat diketahui bahwa 
                banyak barang yang waktu sampainya kurang dari 30 hari lebih banyak 
                dibandingkan dengan barang yang waktu sampainya lebih dari 30 hari. 
                Dengan jumlah barang yang waktu sampainya kurang dari 30 hari adalah 91896, 
                sedangkan barang yang waktu sampainya lebih dari 30 hari adalah 4552. 
                Dengan demikian perusahaan tetap bisa memakai jasa ekspedisi yang sekarang digunakan 
                karena waktu pengirimannya masih dalam batas wajar.
            """
        )



#dataset yang digunakan    
df_data_order = pd.read_csv('orders_dataset.csv')

with st.sidebar :
    selected = option_menu('Menu',['Dashboard','About'],
    icons =["easel2", "info-circle"],
    menu_icon="cast",
    default_index=0)
    
if (selected == 'Dashboard') :
    st.title(f"DASHBOARD LAMA PENGIRIMAN BARANG")
    st.write('<hr>', unsafe_allow_html=True)
    lama_pengiriman(df_data_order)
else :
    if (selected == 'About') :
        st.title("Profile Mahasiswa")
        st.write('<hr>', unsafe_allow_html=True)
        st.write("NIM    : 10122237")
        st.write("NAMA   : Muhammad Elsiano Gibran Alkaf")
        st.write("KELAS  : IF-7")
        st.write("UAS Pemrograman Dasar Sains Data")
    
