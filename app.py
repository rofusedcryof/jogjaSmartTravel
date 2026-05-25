# import streamlit as st
# import pandas as pd
# import numpy as np
# import plotly.express as px
# from sklearn.metrics.pairwise import cosine_similarity
# from sklearn.feature_extraction.text import TfidfVectorizer
# import time

# # --- 1. SETTING & STYLE ---
# st.set_page_config(
#     page_title="JogjaSmart Travel | AI Recommendation System",
#     page_icon="🕌",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Custom CSS untuk tampilan premium
# st.markdown("""
#     <style>
#     .main { background-color: #f8f9fa; }
#     .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
#     .recom-card { 
#         background: white; padding: 20px; border-radius: 15px; 
#         border-left: 5px solid #FF4B4B; margin-bottom: 20px;
#         box-shadow: 0 4px 6px rgba(0,0,0,0.1);
#     }
#     </style>
#     """, unsafe_allow_html=True)

# # --- 2. DATA ENGINE (MOCK REAL DATASET) ---
# @st.cache_data
# def get_dataset():
#     # Simulasi Dataset Destinasi
#     destinasi = pd.DataFrame({
#         'id': range(1, 11),
#         'nama': ['Candi Borobudur', 'Pantai Parangtritis', 'Jalan Malioboro', 'Taman Sari', 
#                  'Candi Prambanan', 'Gunung Merapi', 'Goa Jomblang', 'HeHa Ocean View', 
#                  'Hutan Pinus Mangunan', 'Keraton Yogyakarta'],
#         'kategori': ['Budaya', 'Alam', 'Belanja', 'Budaya', 'Budaya', 'Alam', 'Petualangan', 'Modern', 'Alam', 'Budaya'],
#         'harga': [50000, 15000, 0, 15000, 50000, 30000, 450000, 25000, 10000, 15000],
#         'rating_avg': [4.8, 4.5, 4.7, 4.6, 4.8, 4.7, 4.9, 4.4, 4.5, 4.6],
#         'lat': [-7.607, -8.025, -7.792, -7.809, -7.752, -7.540, -7.928, -8.051, -7.934, -7.805],
#         'lon': [110.203, 110.329, 110.365, 110.359, 110.491, 110.446, 110.638, 110.505, 110.435, 110.363],
#         'deskripsi': 'Wisata ikonik Yogyakarta dengan nilai sejarah dan estetika tinggi.'
#     })
    
#     # Simulasi Dataset Rating (User-Item Interaction)
#     ratings = pd.DataFrame(np.random.randint(3, 6, size=(50, 10)), columns=destinasi['nama'])
#     ratings.insert(0, 'user_id', [f'user_{i}' for i in range(1, 51)])
    
#     return destinasi, ratings

# # --- 3. HYBRID RECOMMENDATION LOGIC ---
# class HybridRecommender:
#     def __init__(self, destinasi_df, ratings_df):
#         self.destinasi = destinasi_df
#         self.ratings = ratings_df

#     def get_content_scores(self, user_categories):
#         # Sederhana: Score 1 jika kategori cocok, 0 jika tidak
#         return self.destinasi['kategori'].apply(lambda x: 1 if x in user_categories else 0.2).values

#     def get_collaborative_scores(self, user_id):
#         # Mock Collaborative: Jika user baru (Cold Start), gunakan popularitas (rating_avg)
#         # Jika user lama, kita hitung similarity (disederhanakan untuk demo)
#         return self.destinasi['rating_avg'].values / 5.0

#     def recommend(self, user_id, categories, max_budget, weight_content=0.6):
#         # 1. Content Scores
#         c_scores = self.get_content_scores(categories)
        
#         # 2. Collaborative Scores
#         col_scores = self.get_collaborative_scores(user_id)
        
#         # 3. Hybrid Calculation
#         final_scores = (c_scores * weight_content) + (col_scores * (1 - weight_content))
        
#         # 4. Filter Budget & Merge
#         results = self.destinasi.copy()
#         results['match_score'] = np.round(final_scores * 100, 2)
        
#         # Filtering
#         results = results[results['harga'] <= max_budget]
#         return results.sort_values(by='match_score', ascending=False).head(5)

# # --- 4. MAIN APP INTERFACE ---
# def main():
#     destinasi, ratings = get_dataset()
#     recommender = HybridRecommender(destinasi, ratings)

#     # SIDEBAR PRO
#     with st.sidebar:
#         st.image("https://cdn-icons-png.flaticon.com/512/826/826070.png", width=80)
#         st.title("User Profile")
#         user_id = st.text_input("Login ID", value="Guest_01")
#         st.divider()
#         st.subheader("Filter Preferensi")
#         selected_cats = st.multiselect("Minat Wisata", destinasi['kategori'].unique(), default=["Budaya"])
#         budget = st.slider("Budget Maksimal (IDR)", 0, 500000, 100000, step=10000)
        
#         st.info("Algoritma Hybrid menggabungkan AI Content-based (Minat) & Collaborative (Rating Orang Lain).")

#     # MAIN CONTENT AREA
#     st.title("")
#     st.caption("Sistem Rekomendasi Wisata Pintar Berbasis Hybrid Filtering")

#     # Tab System untuk profesionalitas
#     tab_rec, tab_map, tab_analytics = st.tabs(["🎯 Rekomendasi", "🗺️ Eksplorasi Peta", "📊 Analisis Data"])

#     with tab_rec:
#         col_left, col_right = st.columns([2, 1])
        
#         with col_left:
#             st.subheader("Destinasi Pilihan Untuk Anda")
#             if st.button("Generate Rekomendasi ✨", type="primary"):
#                 with st.spinner("AI sedang menghitung kecocokan destinasi..."):
#                     time.sleep(1.5) # Simulasi komputasi berat
#                     recommendations = recommender.recommend(user_id, selected_cats, budget)
                    
#                     if not recommendations.empty:
#                         for _, row in recommendations.iterrows():
#                             st.markdown(f"""
#                             <div class="recom-card">
#                                 <h3>{row['nama']} <span style='float:right; color:#FF4B4B;'>{row['match_score']}% Match</span></h3>
#                                 <p><b>Kategori:</b> {row['kategori']} | <b>Estimasi Tiket:</b> Rp {row['harga']:,}</p>
#                                 <p style='font-size: 0.9em; color: #666;'>{row['deskripsi']}</p>
#                             </div>
#                             """, unsafe_allow_html=True)
#                     else:
#                         st.error("Maaf, tidak ada destinasi yang cocok dengan budget Anda.")
#             else:
#                 st.write("Klik tombol di atas untuk melihat rekomendasi personal Anda.")

#         with col_right:
#             st.subheader("Statistik Pencarian")
#             st.metric("Total Destinasi Tersedia", len(destinasi))
#             st.metric("Rata-rata Harga", f"IDR {int(destinasi['harga'].mean()):,}")
            
#             # Chart Kecil
#             fig_pie = px.pie(destinasi, names='kategori', title='Distribusi Kategori Wisata')
#             fig_pie.update_layout(showlegend=False, height=250, margin=dict(t=30, b=0, l=0, r=0))
#             st.plotly_chart(fig_pie, use_container_width=True)

#     with tab_map:
#         st.subheader("Sebaran Lokasi Wisata Yogyakarta")
#         # Menampilkan peta berdasarkan data lat/lon
#         st.map(destinasi[['lat', 'lon']])
#         st.caption("Peta menunjukkan titik koordinat destinasi wisata di area Jogja.")

#     with tab_analytics:
#         st.subheader("Deep Data Analysis")
#         col_a, col_b = st.columns(2)
        
#         with col_a:
#             fig_bar = px.bar(destinasi, x='nama', y='harga', color='kategori', title="Komparasi Harga Tiket")
#             st.plotly_chart(fig_bar, use_container_width=True)
            
#         with col_b:
#             fig_scatter = px.scatter(destinasi, x='harga', y='rating_avg', size='harga', color='kategori', 
#                                     hover_name='nama', title="Korelasi Harga vs Rating")
#             st.plotly_chart(fig_scatter, use_container_width=True)

#     # FOOTER
#     st.divider()
#     st.markdown("<center>JogjaSmart Travel v2.0 © 2023 - Backend Powered by Python (Hybrid AI Engine)</center>", unsafe_allow_html=True)

# if __name__ == "__main__":
#     main()

#new prog
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.metrics.pairwise import cosine_similarity
import time

# 1. SETTING & STYLE
st.set_page_config(
    page_title="SISTEM REKOMENDASI PAKET PERJALANAN WISATA AREA JOGJA ",
    page_icon="icon.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk tampilan premium (Mendukung Dark & Light Mode)
# st.markdown("""
#     <style>
#     /* Menyesuaikan warna teks di dalam metrik agar selalu terbaca */
#     [data-testid="stMetricValue"], [data-testid="stMetricLabel"] { 
#         color: #1f1f1f !important; 
#     }
#     div[data-testid="metric-container"] { 
#         background-color: #ffffff; padding: 15px; border-radius: 10px; 
#     }
    
#     /* Style untuk Kartu Rekomendasi dengan Gambar */
#     .recom-card { 
#         background: white; padding: 20px; border-radius: 15px; 
#         border-left: 5px solid #FF4B4B; margin-bottom: 20px;
#         box-shadow: 0 4px 6px rgba(0,0,0,0.1);
#         color: #1f1f1f !important; 
#         display: flex; gap: 20px; align-items: center;
#     }
#     .recom-card h3 { color: #1f1f1f !important; margin-top: 0; margin-bottom: 5px;}
#     .recom-card p { color: #444444 !important; margin-bottom: 5px;}
#     .recom-card b { color: #1f1f1f !important; }
#     .badge {
#         background-color: #ffe4e4; color: #FF4B4B; 
#         padding: 4px 8px; border-radius: 5px; font-weight: bold; font-size: 0.8em;
#     }
#     .recom-img {
#         width: 180px; height: 120px; object-fit: cover; 
#         border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);
#     }
#     </style>
#     """, unsafe_allow_html=True)

st.markdown("""
    <style>
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    /* 1. BAGIAN KOTAK METRIK (STATISTIK PENCARIAN) */
    [data-testid="stMetricValue"], [data-testid="stMetricLabel"] { 
        color: #1E3A8A !important; /* Warna teks angka dan label (Biru Gelap) */
    }
    div[data-testid="metric-container"] { 
        background-color: #ffffff; /* Background kotak statistik (Putih) */
        padding: 15px; border-radius: 10px; 
    }
    
    /* 2. BAGIAN KARTU REKOMENDASI (DESTINASI) */
    .recom-card { 
        background: white; padding: 20px; border-radius: 15px; 
        border-left: 5px solid #FF4B4B; margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        color: #333333 !important; /* Warna teks dasar di dalam kartu */
        display: flex; gap: 20px; align-items: center;
    }
    .recom-card h3 { 
        color: #1E3A8A !important; /* Warna Judul Destinasi (Biru Gelap) */
        margin-top: 0; margin-bottom: 5px;
    }
    .recom-card p { 
        color: #444444 !important; /* Warna teks deskripsi (Abu-abu Gelap) */
        margin-bottom: 5px;
    }
    .recom-card b { 
        color: #1E3A8A !important; /* Warna teks tebal / bold (Biru Gelap) */
    }
    .badge {
        background-color: #ffe4e4; color: #FF4B4B; 
        padding: 4px 8px; border-radius: 5px; font-weight: bold; font-size: 0.8em;
    }
    .recom-img {
        width: 180px; height: 120px; object-fit: cover; 
        border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

#2. DATA ENGINE (INTEGRASI DATASET)
@st.cache_data
def get_dataset():
    # Load dataset asli dari CSV
    try:
        df = pd.read_csv('dataset-wisata-jogja-sekitar.csv')
    except FileNotFoundError:
        st.error("File 'dataset-wisata-jogja-sekitar.csv' tidak ditemukan. Pastikan file ada di folder yang sama.")
        return pd.DataFrame(), pd.DataFrame()

    # Mapping dan Cleaning Data agar sesuai dengan engine kita
    destinasi = pd.DataFrame()
    destinasi['id'] = df['no']
    destinasi['nama'] = df['nama']
    # Membersihkan underscore pada tipe (misal: Budaya_Dan_Sejarah -> Budaya Dan Sejarah)
    destinasi['kategori'] = df['type'].str.replace('_', ' ')
    # Menggunakan harga weekend sebagai acuan batas maksimal budget
    destinasi['harga'] = df['htm_weekend']
    destinasi['rating_avg'] = df['vote_average']
    destinasi['lat'] = df['latitude']
    destinasi['lon'] = df['longitude']
    destinasi['image_url'] = df['image']
    destinasi['deskripsi'] = df['description'].astype(str).str.capitalize()
    
    # Membuat DUMMY Simulasi Rating dari user lain (Karena belum ada dataset riwayat transaksi user)
    # Di dunia nyata, ini diambil dari tabel riwayat klik/rating di database
    np.random.seed(42) # Agar randomnya tetap
    ratings = pd.DataFrame(np.random.randint(3, 6, size=(50, len(destinasi))), columns=destinasi['nama'])
    ratings.insert(0, 'user_id', [f'user_{i}' for i in range(1, 51)])
    
    return destinasi, ratings

# 3. HYBRID RECOMMENDATION LOGIC
class HybridRecommender:
    def __init__(self, destinasi_df, ratings_df):
        self.destinasi = destinasi_df
        self.ratings = ratings_df

    def get_content_scores(self, user_categories):
        # Score 1 jika kategori cocok, 0.1 jika tidak (penalti yang lebih halus)
        return self.destinasi['kategori'].apply(lambda x: 1 if x in user_categories else 0.1).values

    def get_collaborative_scores(self, user_id):
        # Menggunakan skor popularitas murni (rating_avg) jika riwayat interaksi personal kosong (Cold Start)
        return self.destinasi['rating_avg'].values / 5.0

    def recommend(self, user_id, categories, max_budget, weight_content=0.65):
        c_scores = self.get_content_scores(categories)
        col_scores = self.get_collaborative_scores(user_id)
        
        # Kalkulasi Pembobotan Hybrid (65% Minat Kategori, 35% Rating Populer)
        final_scores = (c_scores * weight_content) + (col_scores * (1 - weight_content))
        
        results = self.destinasi.copy()
        results['match_score'] = np.round(final_scores * 100, 1)
        
        # Filter Budget
        results = results[results['harga'] <= max_budget]
        
        # Urutkan berdasarkan skor kecocokan tertinggi
        return results.sort_values(by='match_score', ascending=False).head(5)

#4. MAIN APP INTERFACE
def main():
    destinasi, ratings = get_dataset()
    
    if destinasi.empty:
        return # stop eksekusi kalo file CSV tidak ada

    recommender = HybridRecommender(destinasi, ratings)

    # SIDEBAR
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/826/826070.png", width=80)
        st.title("User Profile")
        user_id = st.text_input("Login ID", value="DIAZ")
        st.divider()
        st.subheader("Filter Preferensi")
        
        # Ambil list kategori unik dari dataset asli
        list_kategori = sorted(destinasi['kategori'].unique().tolist())
        selected_cats = st.multiselect("Minat Wisata Utama", list_kategori, default=["Alam"])
        
        # Slider budget menyesuaikan harga tertinggi di dataset (sekitar 500rb)
        budget = st.slider("Budget Maksimal (IDR)", 0, 500000, 100000, step=10000)
        
        st.info("Algoritma Hybrid menggabungkan AI Content-based (Minat) & Collaborative (Rating Orang Lain).")

    # MAIN CONTENT AREA
    st.title("🗻🗻SISTEM REKOMENDASI PAKET PERJALANAN WISATA AREA JOGJA ")
    st.caption(f"Menjelajahi {len(destinasi)} Destinasi Wisata Pintar Berbasis Hybrid Filtering")

    tab_rec, tab_map, tab_analytics = st.tabs(["🎯 Rekomendasi", "🗺️ Eksplorasi Peta", "📊 Analisis Data"])

    #TAB 1: REKOMENDASI
    with tab_rec:
        col_left, col_right = st.columns([2, 1])
        
        with col_left:
            st.subheader("Destinasi Pilihan Untuk Anda")
            if st.button("Generate Rekomendasi ✨", type="primary"):
                if not selected_cats:
                    st.warning("Mohon pilih minimal 1 minat wisata!")
                else:
                    with st.spinner("AI sedang menghitung kecocokan destinasi..."):
                        time.sleep(1) # Efek loading agar terasa sistem bekerja
                        recommendations = recommender.recommend(user_id, selected_cats, budget)
                        
                        if not recommendations.empty:
                            for _, row in recommendations.iterrows():
                                # Memotong deskripsi agar tidak terlalu panjang
                                desc = row['deskripsi'][:150] + "..." if len(str(row['deskripsi'])) > 150 else row['deskripsi']
                                
                                st.markdown(f"""
                                <div class="recom-card">
                                    <img src="{row['image_url']}" class="recom-img" onerror="this.src='https://via.placeholder.com/180x120?text=No+Image'">
                                    <div style="flex-grow: 1;">
                                        <h3>{row['nama']} <span style='float:right; color:#FF4B4B;'>{row['match_score']}% Match</span></h3>
                                        <p><span class="badge">{row['kategori']}</span> | <b>Estimasi Tiket:</b> Rp {row['harga']:,}</p>
                                        <p style='font-size: 0.9em; line-height: 1.4;'>{desc}</p>
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.error("Maaf, tidak ada destinasi yang cocok dengan kriteria dan budget Anda.")
            else:
                st.info("Atur preferensi di menu sebelah kiri dan klik tombol di atas.")

        with col_right:
            st.subheader("Statistik Pencarian")
            st.metric("Total Destinasi Tersedia", len(destinasi))
            st.metric("Rata-rata Harga Tiket", f"IDR {int(destinasi['harga'].mean()):,}")
            
            # Chart Pie Kategori (dari dataset)
            fig_pie = px.pie(destinasi, names='kategori', title='Distribusi Kategori Wisata')
            fig_pie.update_layout(showlegend=False, height=250, margin=dict(t=30, b=0, l=0, r=0))
            st.plotly_chart(fig_pie, use_container_width=True)

    # TAB 2: MAP
    with tab_map:
        st.subheader("Sebaran Lokasi Wisata Yogyakarta")
        st.write("Titik di bawah ini memetakan seluruh data koordinat (latitude & longitude) dari dataset Anda.")
        st.map(destinasi[['lat', 'lon']])

    #TAB 3: ANALISIS
    with tab_analytics:
        st.subheader("Deep Data Analysis")
        col_a, col_b = st.columns(2)
        
        with col_a:
            # Karena datasetnya ratusan (476 data), tak ambil Top 20 termahal buat Bar Chart
            top_expensive = destinasi.nlargest(20, 'harga')
            fig_bar = px.bar(top_expensive, x='nama', y='harga', color='kategori', title="Top 20 Destinasi Termahal")
            fig_bar.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_bar, use_container_width=True)
            
        with col_b:
            # Scatter Plot seluruh dataset
            fig_scatter = px.scatter(destinasi, x='harga', y='rating_avg', color='kategori', 
                                    hover_name='nama', title="Korelasi Harga vs Rating (Seluruh Data)")
            st.plotly_chart(fig_scatter, use_container_width=True)

    st.divider()
    st.markdown("<center>JogjaSmart Travel v1.0 © 2026 - Backend Powered by @cyberwarehouse.care (Hybrid AI Engine)</center>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()