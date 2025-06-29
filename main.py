import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

# ========== KONFIGURASI HALAMAN ==========
st.set_page_config(
    page_title="Dashboard Makanan",
    page_icon="🍽️",
    layout="centered"  # Tidak terlalu lebar, nyaman dilihat
)

# ========== NAVIGASI HORIZONTAL ==========
selected = option_menu(
    menu_title=None,
    options=["Beranda", "Tabel Data", "Visualisasi", "Tentang Metode", "Kesimpulan"],
    icons=["house", "table", "bar-chart-line", "info-circle", "check-circle"],
    orientation="horizontal"
)

# ========== BACA DATA ==========
df = pd.read_csv("hasil_clustering_kmeans.csv")

# ========== LOGIKA TIAP HALAMAN ==========
if selected == "Beranda":
    st.markdown("<h1 style='text-align:center; color:#4CAF50;'>🍽️ Dashboard Data Makanan </h1>", unsafe_allow_html=True)

    image = Image.open("makanan.jpg")
    st.image(image, caption="Makanan", use_container_width=True)

    st.write("<p style='text-align:center;'>Selamat datang! Website ini menampilkan data makanan berdasarkan kandungan nutrisinya dan gambarnya.</p>", unsafe_allow_html=True)

elif selected == "Tabel Data":
    st.markdown("<h2 style='color:#4CAF50;'>📊 Tabel Data Makanan</h2>", unsafe_allow_html=True)

    search = st.text_input("Cari nama makanan")
    if search:
        filtered_df = df[df['name'].str.contains(search, case=False)].copy()
    else:
        filtered_df = df.copy()

    sort_col = st.selectbox("Urutkan berdasarkan", ["name", "calories", "proteins", "fat", "carbohydrate", "Cluster"], index=0)
    sort_order = st.radio("Urutan", ["Naik", "Turun"], horizontal=True)
    filtered_df = filtered_df.sort_values(by=sort_col, ascending=(sort_order == "Naik"))

    rows_per_page = 5
    total_rows = len(filtered_df)
    total_pages = (total_rows - 1) // rows_per_page + 1
    page_number = st.number_input("Halaman", min_value=1, max_value=total_pages, value=1)
    start_idx = (page_number - 1) * rows_per_page
    end_idx = start_idx + rows_per_page
    paginated_df = filtered_df.iloc[start_idx:end_idx]

    for idx, row in paginated_df.iterrows():
        with st.container():
            col_gambar, col_nutrisi, col_cluster = st.columns([1, 2, 1])

            with col_gambar:
                st.write("")
                st.image(row["image"], width=130)

            with col_nutrisi:
                st.markdown(f"<h4 style='margin-bottom: 5px;'>{row['name']}</h4>", unsafe_allow_html=True)
                st.markdown(
                    f"""
                    <div style='font-size: 14px; line-height: 1.8; color: black !important;'>
                    <b>Kalori:</b> {row['calories']} kcal<br>
                    <b>Karbohidrat:</b> {row['carbohydrate']} g<br>
                    <b>Protein:</b> {row['proteins']} g<br>
                    <b>Lemak:</b> {row['fat']} g
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with col_cluster:
                st.markdown("<h5 style='color:black;'>Cluster</h5>", unsafe_allow_html=True)
                st.markdown(
                    f"""
                    <div style='font-size: 20px; text-align: center; font-weight: bold; color: black;'>
                    {row['Cluster']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        st.markdown("<hr style='border:0.5px solid #ccc;'>", unsafe_allow_html=True)

elif selected == "Visualisasi":
    st.markdown("<h2 style='color:#4CAF50;'>📈 Visualisasi Data</h2>", unsafe_allow_html=True)

    # Visualisasi K-Means
    st.subheader("🔹 K-Means Clustering")

    st.markdown("**Metode Elbow**")
    st.image("elbow.jpg", use_container_width=True)
    st.markdown("""
    Grafik di atas merupakan hasil dari **Metode Elbow** pada algoritma K-Means untuk menentukan jumlah klaster optimal.

    - **Sumbu X (Jumlah Cluster):** menunjukkan jumlah klaster yang diuji, dari 1 hingga 10.
    - **Sumbu Y (Within-Cluster Sum of Squares / WCSS):** menunjukkan total jarak kuadrat antar data dan pusat klasternya (semakin kecil, semakin baik).

    Pada grafik ini, terlihat adanya penurunan tajam pada jumlah klaster 3. Setelah titik ini, penurunan nilai WCSS mulai melambat.  
    **Titik 'tekukan' (elbow)** tersebut mengindikasikan jumlah klaster optimal, yaitu **3 cluster**.
    """)

    st.markdown("**Hasil Clustering K-Means**")
    st.image("Scatter plot k-means.jpg", use_container_width=True)
    st.markdown("""
    Plot ini menunjukkan hasil akhir pengelompokan K-Means dengan 3 klaster berdasarkan variabel gizi makanan.  
    Setiap warna mewakili satu klaster dengan pola distribusi yang cukup jelas.
    """)

    # Visualisasi DBSCAN
    st.subheader("🔸 DBSCAN Clustering")

    st.markdown("**K-Distance Plot (Menentukan Epsilon)**")
    st.image("k-distance.jpg", use_container_width=True)
    st.markdown("""
    Grafik ini digunakan untuk membantu menentukan nilai **epsilon (ε)** optimal pada DBSCAN.  
    Titik tekukan pada kurva mengindikasikan nilai epsilon terbaik untuk pemisahan klaster secara alami.
    """)

    st.markdown("**Hasil Clustering DBSCAN**")
    st.image("dbscan.jpg", use_container_width=True)
    st.markdown("""
    Visualisasi ini menunjukkan hasil akhir dari metode DBSCAN.  
    Setiap warna menandakan klaster yang terdeteksi, sedangkan titik berwarna abu-abu atau hitam merupakan **data noise** yang tidak termasuk dalam klaster manapun.
    """)


elif selected == "Tentang Metode":
    st.markdown("<h2 style='color:#4CAF50;'>🔍 Metode Klastering yang Digunakan</h2>", unsafe_allow_html=True)

    st.markdown("<div style='background-color:#e6fff0;padding:10px;border-left:5px solid #4CAF50;'>"
                "Analisis klaster dilakukan menggunakan metode <strong>K-Means Clustering</strong>."
                "</div><br>", unsafe_allow_html=True)

    with st.container():
        st.markdown("### 📌 K-Means Clustering")
        st.markdown("""
        Metode K-Means digunakan untuk mengelompokkan data responden ke dalam beberapa klaster berdasarkan kesamaan karakteristik.
        Metode ini efektif untuk segmentasi data karena mampu mengelompokkan data berdasarkan jarak antar titik dalam ruang multidimensi.
        """)

    with st.container():
        st.markdown("### 🧪 Langkah-langkah Analisis")
        st.markdown("""
        1. **Preprocessing data** (membersihkan dan menormalisasi data)  
        2. **Menentukan jumlah klaster optimal** (menggunakan Elbow & Silhouette Score)  
        3. **Menerapkan algoritma K-Means** untuk membentuk klaster  
        4. **Visualisasi hasil** dan interpretasi klaster  
        """)

    with st.container():
        st.markdown("### 📊 Evaluasi Model")
        st.markdown("""
        Model dievaluasi menggunakan **Silhouette Score**, **Calinski-Harabasz Index**, dan **Davies-Bouldin Index**
        untuk memastikan kualitas pengelompokan yang optimal.
        """)

    st.markdown("<div style='background-color:#fff3cd;padding:15px;border-left:5px solid #ffc107;border-radius:8px;'>"
                "<h5>⚠️ Catatan Penting:</h5>"
                "<ul>"
                "<li>🔑 Pemilihan jumlah klaster sangat krusial agar hasil pengelompokan bermakna.</li>"
                "<li>📈 Visualisasi seperti Elbow Curve dan PCA membantu memahami struktur data.</li>"
                "<li>✅ Evaluasi model dilakukan untuk memastikan pembagian klaster efektif dan valid.</li>"
                "</ul>"
                "</div>", unsafe_allow_html=True)


elif selected == "Kesimpulan":
    st.markdown("<h2 style='color:#4CAF50;'>📌 Kesimpulan</h2>", unsafe_allow_html=True)

    st.markdown("""
    ### 🟢 Cluster 0 – Rendah Kalori dan Gizi Berat  
    - Jumlah Data: 769 item  
    - Kalori: 93,02 kkal | Protein: 6,07 g | Lemak: 2,36 g | Karbohidrat: 12,19 g  
    Kelompok ini terdiri dari makanan rendah kalori, protein, dan lemak, dengan karbohidrat sedang ke rendah.  
    Cocok untuk diet rendah kalori, penderita diabetes, atau pasien dengan gangguan ginjal.
    """)

    st.markdown("""
    ### 🟡 Cluster 1 – Tinggi Karbohidrat dan Kalori  
    - Jumlah Data: 273 item  
    - Kalori: 343,35 kkal | Protein: 7,27 g | Lemak: 5,94 g | Karbohidrat: 67,15 g  
    Makanan dalam kelompok ini tinggi karbohidrat dan kalori, namun rendah hingga sedang dalam protein dan lemak.  
    Perlu dibatasi untuk individu dengan kebutuhan pengendalian karbohidrat.
    """)

    st.markdown("""
    ### 🔴 Cluster 2 – Tinggi Protein dan Lemak  
    - Jumlah Data: 179 item  
    - Kalori: 347,80 kkal | Protein: 23,12 g | Lemak: 22,33 g | Karbohidrat: 14,55 g  
    Klaster ini berisi makanan tinggi protein dan lemak serta rendah karbohidrat.  
    Cocok untuk kebutuhan protein tinggi, namun perlu perhatian bagi penderita kolesterol tinggi atau gangguan ginjal.
    """)

    st.info("""
    Aplikasi ini menyajikan hasil pengelompokan makanan berdasarkan kandungan gizi. 
    Informasi ini dapat digunakan untuk analisis gizi atau perencanaan pola makan sehat yang disesuaikan dengan kondisi kesehatan dan tujuan diet masing-masing individu.
    """)


# ========== FOOTER ==========
st.markdown("""
    <hr style="margin-top: 3rem; margin-bottom: 1rem;">
    <div style='text-align: center; color: black; font-size: 16px;'>
        © 2025 Muhammad Ilham Juardi - Dashboard Data Makanan
    </div>
""", unsafe_allow_html=True)
