import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import calendar

# Konfigurasi halaman
st.set_page_config(
    page_title="Dashboard Pertanian Jawa Timur",
    page_icon="🌾",
    layout="wide"
)

# Custom CSS sederhana
st.markdown("""
<style>
    /* Warna utama */
    .green-bg { 
        background: linear-gradient(135deg, #2d6a4f, #1b4332);
        color: white; 
        padding: 25px; 
        border-radius: 10px; 
        margin-bottom: 20px;
    }
    
    .card { 
        background: white; 
        padding: 20px; 
        border-radius: 10px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.1); 
        margin: 10px 0; 
        border-left: 4px solid #2d6a4f;
    }
    
    .metric-card { 
        background: white; 
        padding: 15px; 
        border-radius: 10px; 
        box-shadow: 0 3px 10px rgba(0,0,0,0.08);
        border-top: 4px solid #2d6a4f;
        text-align: center;
    }
    
    /* Tombol */
    .stButton > button {
        background: linear-gradient(135deg, #2d6a4f, #40916c) !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        transition: all 0.3s !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 15px rgba(45, 106, 79, 0.3) !important;
    }
    
    /* Tab */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background-color: #f8f9fa;
        padding: 5px;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 500;
        color: #1b4332;
        border: 1px solid #dee2e6;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #2d6a4f !important;
        color: white !important;
        border-color: #2d6a4f !important;
    }
    
    /* Improved stat cards */
    .komoditas-stat {
        background: white;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid;
        margin-bottom: 12px;
        box-shadow: 0 3px 8px rgba(0,0,0,0.08);
        transition: transform 0.2s;
        height: 160px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    
    .komoditas-stat:hover {
        transform: translateY(-3px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    /* Warna border berbeda untuk urutan */
    .rank-1 { border-left-color: #ff6b6b !important; }
    .rank-2 { border-left-color: #ffa94d !important; }
    .rank-3 { border-left-color: #ffd166 !important; }
    .rank-4 { border-left-color: #06d6a0 !important; }
    .rank-5 { border-left-color: #118ab2 !important; }
    .rank-6 { border-left-color: #7b68ee !important; }
    .rank-7 { border-left-color: #9d4edd !important; }
    .rank-8 { border-left-color: #4361ee !important; }
    .rank-9 { border-left-color: #4cc9f0 !important; }
    .rank-10 { border-left-color: #7209b7 !important; }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="green-bg">
    <h1 style="margin: 0; font-size: 32px; font-weight: 700;">🌾 DASHBOARD PERTANIAN JAWA TIMUR</h1>
    <p style="margin: 10px 0 0 0; font-size: 18px; opacity: 0.9;">
    Analisis Harga & Produksi Komoditas Pertanian 2020
    </p>
    <div style="background: rgba(255,255,255,0.15); padding: 12px; border-radius: 8px; margin-top: 15px; border-left: 4px solid #95d5b2;">
        <strong>📊 SISTEM MONITORING REAL-TIME</strong> | Visualisasi Data Interaktif
    </div>
</div>
""", unsafe_allow_html=True)

# Generate data sederhana
@st.cache_data
def generate_data():
    komoditas_list = ['Padi', 'Jagung', 'Kedelai', 'Cabe Merah', 'Bawang Merah', 'Tomat', 'Kentang', 'Pisang', 'Mangga', 'Jeruk']
    kabupaten_list = ['Surabaya', 'Malang', 'Sidoarjo', 'Kediri', 'Jember', 'Banyuwangi', 'Madiun', 'Pasuruan', 'Blitar']
    
    data = []
    for bulan in range(1, 13):
        for komoditas in komoditas_list:
            for kabupaten in kabupaten_list:
                # Harga berdasarkan jenis komoditas
                if komoditas in ['Padi', 'Jagung', 'Kedelai']:
                    harga_dasar = np.random.randint(5000, 15000)
                elif komoditas in ['Cabe Merah', 'Bawang Merah']:
                    harga_dasar = np.random.randint(20000, 50000)
                elif komoditas in ['Tomat', 'Kentang']:
                    harga_dasar = np.random.randint(8000, 20000)
                else:  # Buah-buahan
                    harga_dasar = np.random.randint(10000, 30000)
                
                # Variasi harga dengan trend musiman
                if bulan in [6, 7, 8]:  # Musim kemarau
                    harga = harga_dasar * np.random.uniform(1.1, 1.3)
                elif bulan in [11, 12, 1]:  # Musim hujan
                    harga = harga_dasar * np.random.uniform(0.8, 1.0)
                else:
                    harga = harga_dasar
                
                # Trend harga
                if harga > harga_dasar * 1.15:
                    trend = 'Naik'
                elif harga < harga_dasar * 0.85:
                    trend = 'Turun'
                else:
                    trend = 'Stabil'
                
                data.append({
                    'Bulan': bulan,
                    'Nama_Bulan': calendar.month_name[bulan],
                    'Komoditas': komoditas,
                    'Kabupaten': kabupaten,
                    'Harga': round(harga),
                    'Produksi': np.random.randint(500, 10000),
                    'Trend': trend
                })
    
    return pd.DataFrame(data)

# Load data
df = generate_data()

# Sidebar untuk filter
with st.sidebar:
    st.markdown("### 🔍 FILTER DATA")
    
    # Filter komoditas
    komoditas_options = ['Semua Komoditas'] + list(df['Komoditas'].unique())
    selected_komoditas = st.selectbox('Komoditas', komoditas_options)
    
    # Filter kabupaten
    kabupaten_options = ['Semua Kabupaten'] + list(df['Kabupaten'].unique())
    selected_kabupaten = st.selectbox('Kabupaten/Kota', kabupaten_options)
    
    # Filter bulan
    bulan_options = ['Semua Bulan'] + [f'{calendar.month_name[i]}' for i in range(1, 13)]
    selected_bulan = st.selectbox('Bulan', bulan_options)
    
    # Filter trend
    trend_options = ['Semua Trend'] + list(df['Trend'].unique())
    selected_trend = st.selectbox('Trend Harga', trend_options)
    
    st.markdown("---")
    
    # Quick stats
    st.markdown("### 📊 INFO DATA")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Data", f"{len(df):,}")
    with col2:
        st.metric("Jenis Komoditas", df['Komoditas'].nunique())
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Kabupaten", df['Kabupaten'].nunique())
    with col2:
        st.metric("Bulan", df['Bulan'].nunique())
    
    st.markdown("---")
    
    # Download semua data
    if st.button("📥 Download Semua Data (CSV)", use_container_width=True):
        csv = df.to_csv(index=False)
        st.download_button(
            label="Klik untuk Download",
            data=csv,
            file_name="data_pertanian_jatim_2020.csv",
            mime="text/csv"
        )

# Filter data berdasarkan pilihan
filtered_df = df.copy()

if selected_komoditas != 'Semua Komoditas':
    filtered_df = filtered_df[filtered_df['Komoditas'] == selected_komoditas]

if selected_kabupaten != 'Semua Kabupaten':
    filtered_df = filtered_df[filtered_df['Kabupaten'] == selected_kabupaten]

if selected_bulan != 'Semua Bulan':
    bulan_num = list(calendar.month_name).index(selected_bulan)
    filtered_df = filtered_df[filtered_df['Bulan'] == bulan_num]

if selected_trend != 'Semua Trend':
    filtered_df = filtered_df[filtered_df['Trend'] == selected_trend]

# METRICS UTAMA
st.subheader("📊 METRIK UTAMA")

col1, col2, col3, col4 = st.columns(4)

with col1:
    avg_price = filtered_df['Harga'].mean()
    st.markdown(f"""
    <div class="metric-card">
        <div style="font-size: 14px; color: #666; margin-bottom: 5px;">💰 Rata-rata Harga</div>
        <div style="font-size: 26px; font-weight: bold; color: #2d6a4f;">Rp {avg_price:,.0f}</div>
        <div style="font-size: 12px; color: #888; margin-top: 5px;">per kg</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    total_prod = filtered_df['Produksi'].sum()
    st.markdown(f"""
    <div class="metric-card">
        <div style="font-size: 14px; color: #666; margin-bottom: 5px;">📦 Total Produksi</div>
        <div style="font-size: 26px; font-weight: bold; color: #2d6a4f;">{total_prod:,.0f}</div>
        <div style="font-size: 12px; color: #888; margin-top: 5px;">ton</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    jenis_komoditas = filtered_df['Komoditas'].nunique()
    st.markdown(f"""
    <div class="metric-card">
        <div style="font-size: 14px; color: #666; margin-bottom: 5px;">🌱 Jenis Komoditas</div>
        <div style="font-size: 26px; font-weight: bold; color: #2d6a4f;">{jenis_komoditas}</div>
        <div style="font-size: 12px; color: #888; margin-top: 5px;">aktif</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    wilayah = filtered_df['Kabupaten'].nunique()
    st.markdown(f"""
    <div class="metric-card">
        <div style="font-size: 14px; color: #666; margin-bottom: 5px;">📍 Wilayah Terdata</div>
        <div style="font-size: 26px; font-weight: bold; color: #2d6a4f;">{wilayah}</div>
        <div style="font-size: 12px; color: #888; margin-top: 5px;">kabupaten/kota</div>
    </div>
    """, unsafe_allow_html=True)


# Tab untuk berbagai analisis
st.markdown("## 📊 Analisis Data")

tab1, tab2, tab3 = st.tabs(["📊 Visualisasi Diagram", "🗺️ Wilayah", "📋 Data Detail"])

with tab1:
    st.subheader("📈 Analisis Tren dan Perbandingan Harga")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Grafik trend harga per bulan
        monthly_price = filtered_df.groupby('Nama_Bulan')['Harga'].mean().reset_index()
        monthly_price['Nama_Bulan'] = pd.Categorical(monthly_price['Nama_Bulan'], 
                                                    categories=list(calendar.month_name[1:]), 
                                                    ordered=True)
        monthly_price = monthly_price.sort_values('Nama_Bulan')
        
        fig1 = px.line(monthly_price, x='Nama_Bulan', y='Harga', 
                      title='Trend Harga per Bulan',
                      markers=True,
                      line_shape='spline')
        fig1.update_traces(line_color='#2d6a4f', line_width=3, marker_color='#40916c', marker_size=8)
        fig1.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            hovermode='x unified'
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Grafik komoditas terpopuler
        if selected_komoditas == 'Semua Komoditas':
            top_komoditas = filtered_df.groupby('Komoditas')['Harga'].mean().nlargest(8).reset_index()
            fig2 = px.bar(top_komoditas, x='Komoditas', y='Harga',
                         title='Komoditas dengan Harga Tertinggi',
                         color='Harga',
                         color_continuous_scale=['#95d5b2', '#2d6a4f'])
            fig2.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white'
            )
            st.plotly_chart(fig2, use_container_width=True)
        else:
            # Grafik harga di berbagai kabupaten
            kabupaten_price = filtered_df.groupby('Kabupaten')['Harga'].mean().reset_index().sort_values('Harga', ascending=True)
            fig2 = px.bar(kabupaten_price, x='Harga', y='Kabupaten', orientation='h',
                         title=f'Harga {selected_komoditas} per Kabupaten',
                         color='Harga',
                         color_continuous_scale=['#e9c46a', '#f4a261'])
            fig2.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                height=400
            )
            st.plotly_chart(fig2, use_container_width=True)
    
    st.subheader("📊 Analisis Hubungan Antar Variabel")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Scatter plot harga vs produksi
        scatter_data = filtered_df.groupby('Komoditas').agg({
            'Harga': 'mean',
            'Produksi': 'sum'
        }).reset_index()
        
        fig3 = px.scatter(scatter_data, x='Produksi', y='Harga',
                         size='Produksi', color='Komoditas',
                         title='Hubungan Produksi vs Harga',
                         hover_name='Komoditas',
                         size_max=40)
        fig3.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        # Pie chart distribusi trend
        trend_counts = filtered_df['Trend'].value_counts().reset_index()
        fig4 = px.pie(trend_counts, values='count', names='Trend',
                     title='Distribusi Trend Harga',
                     color='Trend',
                     color_discrete_map={'Naik': '#e76f51', 'Turun': '#52b788', 'Stabil': '#a2d2ff'})
        fig4.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig4, use_container_width=True)
    
    st.markdown("---")
    st.subheader("📊 Analisis Distribusi dan Pola Data")
    
    # Pilihan diagram lanjutan
    col1, col2 = st.columns(2)
    with col1:
        diagram_option = st.selectbox(
            "Pilih Jenis Visualisasi:",
            ["Histogram", "Heatmap", "Boxplot"]
        )
    with col2:
        # Pilihan variabel (harga atau produksi)
        col_type = st.radio(
            "Pilih Variabel:",
            ["Harga", "Produksi"],
            horizontal=True
        )
    
    if diagram_option == "Histogram":
        col1, col2 = st.columns(2)
        
        with col1:
            # Histogram
            if col_type == "Harga":
                fig_hist = px.histogram(
                    filtered_df,
                    x='Harga',
                    nbins=30,
                    title=f'Histogram Distribusi {col_type}',
                    color_discrete_sequence=['#2d6a4f'],
                    opacity=0.8
                )
                
                avg_value = filtered_df['Harga'].mean()
                fig_hist.add_vline(
                    x=avg_value,
                    line_dash="dash",
                    line_color="#e76f51",
                    annotation_text=f"Rata-rata: Rp {avg_value:,.0f}",
                    annotation_position="top right"
                )
                
                fig_hist.update_layout(
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    xaxis_title="Harga (Rp)",
                    yaxis_title="Frekuensi"
                )
                st.plotly_chart(fig_hist, use_container_width=True)
                
            else:  # Produksi
                fig_hist = px.histogram(
                    filtered_df,
                    x='Produksi',
                    nbins=30,
                    title=f'Histogram Distribusi {col_type}',
                    color_discrete_sequence=['#40916c'],
                    opacity=0.8
                )
                
                avg_value = filtered_df['Produksi'].mean()
                fig_hist.add_vline(
                    x=avg_value,
                    line_dash="dash",
                    line_color="#f4a261",
                    annotation_text=f"Rata-rata: {avg_value:,.0f} ton",
                    annotation_position="top right"
                )
                
                fig_hist.update_layout(
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    xaxis_title="Produksi (ton)",
                    yaxis_title="Frekuensi"
                )
                st.plotly_chart(fig_hist, use_container_width=True)
        
        with col2:
            # Statistik histogram
            st.markdown("##### 📊 Statistik Distribusi")
            if col_type == "Harga":
                st.write(f"**Rata-rata:** Rp {filtered_df['Harga'].mean():,.0f}")
                st.write(f"**Median:** Rp {filtered_df['Harga'].median():,.0f}")
                st.write(f"**Modus:** Rp {filtered_df['Harga'].mode()[0]:,.0f}")
                st.write(f"**Standar Deviasi:** Rp {filtered_df['Harga'].std():,.0f}")
                st.write(f"**Rentang:** Rp {filtered_df['Harga'].min():,.0f} - Rp {filtered_df['Harga'].max():,.0f}")
            else:
                st.write(f"**Rata-rata:** {filtered_df['Produksi'].mean():,.0f} ton")
                st.write(f"**Median:** {filtered_df['Produksi'].median():,.0f} ton")
                st.write(f"**Modus:** {filtered_df['Produksi'].mode()[0]:,.0f} ton")
                st.write(f"**Standar Deviasi:** {filtered_df['Produksi'].std():,.0f} ton")
                st.write(f"**Rentang:** {filtered_df['Produksi'].min():,.0f} - {filtered_df['Produksi'].max():,.0f} ton")
    
    elif diagram_option == "Heatmap":
        # Persiapan data untuk heatmap
        if col_type == "Harga":
            heatmap_data = filtered_df.pivot_table(
                index='Kabupaten',
                columns='Bulan',
                values='Harga',
                aggfunc='mean'
            ).fillna(0).round(0)
            
            title_text = 'Heatmap: Rata-rata Harga per Kabupaten & Bulan'
            color_scale = ['#95d5b2', '#2d6a4f', '#1b4332']
            label_text = "Harga (Rp)"
            
            # Interpretasi
            max_value = heatmap_data.max().max()
            min_value = heatmap_data.min().min()
            avg_value = filtered_df['Harga'].mean()
            
        else:  # Produksi
            heatmap_data = filtered_df.pivot_table(
                index='Kabupaten',
                columns='Bulan',
                values='Produksi',
                aggfunc='mean'
            ).fillna(0).round(0)
            
            title_text = 'Heatmap: Rata-rata Produksi per Kabupaten & Bulan'
            color_scale = ['#e9c46a', '#f4a261', '#e76f51']
            label_text = "Produksi (ton)"
            
            # Interpretasi
            max_value = heatmap_data.max().max()
            min_value = heatmap_data.min().min()
            avg_value = filtered_df['Produksi'].mean()
        
        # Konversi bulan angka ke nama bulan
        heatmap_data.columns = [calendar.month_name[i] for i in heatmap_data.columns]
        
        fig_heatmap = px.imshow(
            heatmap_data,
            title=title_text,
            color_continuous_scale=color_scale,
            aspect="auto",
            labels=dict(color=label_text)
        )
        
        fig_heatmap.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=500
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)
        
        # Interpretasi heatmap
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(f"{col_type} Tertinggi", f"{max_value:,.0f}" + (" Rp" if col_type == "Harga" else " ton"))
        with col2:
            st.metric(f"{col_type} Terendah", f"{min_value:,.0f}" + (" Rp" if col_type == "Harga" else " ton"))
        with col3:
            st.metric(f"Rata-rata {col_type}", f"{avg_value:,.0f}" + (" Rp" if col_type == "Harga" else " ton"))
    
    elif diagram_option == "Boxplot":
        # Boxplot memenuhi lebar penuh
        st.markdown("##### 📦 Boxplot: Sebaran Data per Komoditas")
        
        if col_type == "Harga":
            fig_box = px.box(
                filtered_df,
                x='Komoditas',
                y='Harga',
                title=f'Boxplot: Sebaran {col_type} per Komoditas',
                color='Komoditas',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            
            fig_box.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                xaxis_title="Komoditas",
                yaxis_title=f"{col_type} (Rp)",
                showlegend=False,
                height=500
            )
            st.plotly_chart(fig_box, use_container_width=True)
            
        else:  # Produksi
            fig_box = px.box(
                filtered_df,
                x='Komoditas',
                y='Produksi',
                title=f'Boxplot: Sebaran {col_type} per Komoditas',
                color='Komoditas',
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            
            fig_box.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                xaxis_title="Komoditas",
                yaxis_title=f"{col_type} (ton)",
                showlegend=False,
                height=500
            )
            st.plotly_chart(fig_box, use_container_width=True)
        
        # Statistik boxplot ditempatkan di bawah dalam grid yang rapat
        st.markdown("##### 📊 STATISTIK LENGKAP 10 KOMODITAS")
        
        if col_type == "Harga":
            box_stats = filtered_df.groupby('Komoditas')['Harga'].agg(['mean', 'min', 'max', 'std']).round(0)
            box_stats = box_stats.sort_values('mean', ascending=False)
            
            # Tampilkan dalam 2 baris dengan 5 kolom per baris
            st.markdown("**🎯 5 Komoditas Tertinggi**")
            col1, col2, col3, col4, col5 = st.columns(5)
            columns_row1 = [col1, col2, col3, col4, col5]
            
            # Tampilkan 5 komoditas pertama
            for idx, ((komoditas, row), col) in enumerate(zip(box_stats.head(5).iterrows(), columns_row1), 1):
                with col:
                    st.markdown(f"""
                    <div class="komoditas-stat rank-{idx}">
                        <div style="font-weight: bold; color: #333; font-size: 16px; margin-bottom: 8px;">
                            #{idx} {komoditas}
                        </div>
                        <div style="background: rgba(45, 106, 79, 0.1); padding: 5px 8px; border-radius: 6px; margin: 5px 0;">
                            <div style="font-size: 12px; color: #666; margin-bottom: 2px;">Rata-rata Harga</div>
                            <div style="font-size: 18px; font-weight: bold; color: #2d6a4f;">Rp {row['mean']:,.0f}</div>
                        </div>
                        <div style="font-size: 11px; color: #666; margin-top: 5px;">
                            <span style="color: #e76f51;">Min:</span> Rp {row['min']:,.0f}<br>
                            <span style="color: #52b788;">Max:</span> Rp {row['max']:,.0f}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("**📊 5 Komoditas Berikutnya**")
            col6, col7, col8, col9, col10 = st.columns(5)
            columns_row2 = [col6, col7, col8, col9, col10]
            
            # Tampilkan 5 komoditas berikutnya
            for idx, ((komoditas, row), col) in enumerate(zip(box_stats.tail(5).iterrows(), columns_row2), 6):
                with col:
                    st.markdown(f"""
                    <div class="komoditas-stat rank-{idx}">
                        <div style="font-weight: bold; color: #333; font-size: 16px; margin-bottom: 8px;">
                            #{idx} {komoditas}
                        </div>
                        <div style="background: rgba(45, 106, 79, 0.1); padding: 5px 8px; border-radius: 6px; margin: 5px 0;">
                            <div style="font-size: 12px; color: #666; margin-bottom: 2px;">Rata-rata Harga</div>
                            <div style="font-size: 18px; font-weight: bold; color: #2d6a4f;">Rp {row['mean']:,.0f}</div>
                        </div>
                        <div style="font-size: 11px; color: #666; margin-top: 5px;">
                            <span style="color: #e76f51;">Min:</span> Rp {row['min']:,.0f}<br>
                            <span style="color: #52b788;">Max:</span> Rp {row['max']:,.0f}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
        else:  # Produksi
            box_stats = filtered_df.groupby('Komoditas')['Produksi'].agg(['mean', 'min', 'max', 'std']).round(0)
            box_stats = box_stats.sort_values('mean', ascending=False)
            
            # Tampilkan dalam 2 baris dengan 5 kolom per baris
            st.markdown("**🎯 5 Komoditas Tertinggi**")
            col1, col2, col3, col4, col5 = st.columns(5)
            columns_row1 = [col1, col2, col3, col4, col5]
            
            # Tampilkan 5 komoditas pertama
            for idx, ((komoditas, row), col) in enumerate(zip(box_stats.head(5).iterrows(), columns_row1), 1):
                with col:
                    st.markdown(f"""
                    <div class="komoditas-stat rank-{idx}">
                        <div style="font-weight: bold; color: #333; font-size: 16px; margin-bottom: 8px;">
                            #{idx} {komoditas}
                        </div>
                        <div style="background: rgba(64, 145, 108, 0.1); padding: 5px 8px; border-radius: 6px; margin: 5px 0;">
                            <div style="font-size: 12px; color: #666; margin-bottom: 2px;">Rata-rata Produksi</div>
                            <div style="font-size: 18px; font-weight: bold; color: #40916c;">{row['mean']:,.0f} ton</div>
                        </div>
                        <div style="font-size: 11px; color: #666; margin-top: 5px;">
                            <span style="color: #e76f51;">Min:</span> {row['min']:,.0f} ton<br>
                            <span style="color: #52b788;">Max:</span> {row['max']:,.0f} ton
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("**📊 5 Komoditas Berikutnya**")
            col6, col7, col8, col9, col10 = st.columns(5)
            columns_row2 = [col6, col7, col8, col9, col10]
            
            # Tampilkan 5 komoditas berikutnya
            for idx, ((komoditas, row), col) in enumerate(zip(box_stats.tail(5).iterrows(), columns_row2), 6):
                with col:
                    st.markdown(f"""
                    <div class="komoditas-stat rank-{idx}">
                        <div style="font-weight: bold; color: #333; font-size: 16px; margin-bottom: 8px;">
                            #{idx} {komoditas}
                        </div>
                        <div style="background: rgba(64, 145, 108, 0.1); padding: 5px 8px; border-radius: 6px; margin: 5px 0;">
                            <div style="font-size: 12px; color: #666; margin-bottom: 2px;">Rata-rata Produksi</div>
                            <div style="font-size: 18px; font-weight: bold; color: #40916c;">{row['mean']:,.0f} ton</div>
                        </div>
                        <div style="font-size: 11px; color: #666; margin-top: 5px;">
                            <span style="color: #e76f51;">Min:</span> {row['min']:,.0f} ton<br>
                            <span style="color: #52b788;">Max:</span> {row['max']:,.0f} ton
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

with tab2:
    st.subheader("Analisis Per Wilayah")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # Data agregat per wilayah
        region_data = filtered_df.groupby('Kabupaten').agg({
            'Harga': 'mean',
            'Produksi': 'sum',
            'Komoditas': 'nunique'
        }).reset_index()
        
        region_data.columns = ['Kabupaten', 'Harga_Rata2', 'Total_Produksi', 'Jenis_Komoditas']
        region_data['Harga_Rata2'] = region_data['Harga_Rata2'].round(0)
        region_data['Total_Produksi'] = region_data['Total_Produksi'].round(0)
        
        # Buat heatmap dengan bar chart
        fig_region = px.bar(region_data.sort_values('Harga_Rata2', ascending=False).head(10),
                          x='Kabupaten', y='Harga_Rata2',
                          title='10 Wilayah dengan Harga Tertinggi',
                          color='Total_Produksi',
                          color_continuous_scale=['#95d5b2', '#2d6a4f'])
        fig_region.update_layout(height=500)
        st.plotly_chart(fig_region, use_container_width=True)
    
    with col2:
        st.markdown("### 📊 Ranking Wilayah")
        
        # Tabel ranking
        ranking_data = region_data.copy()
        
        # Sort by harga
        ranking_data = ranking_data.sort_values('Harga_Rata2', ascending=False)
        ranking_data['Rank'] = range(1, len(ranking_data) + 1)
        
        # Tampilkan tabel
        st.dataframe(
            ranking_data[['Rank', 'Kabupaten', 'Harga_Rata2', 'Total_Produksi', 'Jenis_Komoditas']].head(8),
            use_container_width=True,
            height=350
        )
        
        # Statistik cepat
        st.markdown("### 📈 Statistik Cepat")
        st.write(f"**Harga Tertinggi:** Rp {ranking_data['Harga_Rata2'].max():,.0f}")
        st.write(f"**Harga Terendah:** Rp {ranking_data['Harga_Rata2'].min():,.0f}")
        st.write(f"**Produksi Total:** {ranking_data['Total_Produksi'].sum():,.0f} ton")

with tab3:
    st.subheader("Data Lengkap & Ekspor")
    
    # Tampilkan data dengan pagination
    st.markdown(f"**Menampilkan {len(filtered_df)} dari {len(df)} records**")
    
    # Tampilkan data
    st.dataframe(
        filtered_df,
        use_container_width=True,
        height=400,
        column_config={
            'Harga': st.column_config.NumberColumn(format="Rp %d"),
            'Produksi': st.column_config.NumberColumn(format="%d ton")
        }
    )
    
    # Statistik detail
    st.subheader("📊 Statistik Detail")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### 📈 Statistik Harga")
        harga_stats = filtered_df['Harga'].describe()
        
        stats_df = pd.DataFrame({
            'Statistik': ['Rata-rata', 'Minimum', 'Maksimum', 'Standar Deviasi', 'Q1 (25%)', 'Median', 'Q3 (75%)'],
            'Nilai': [
                f"Rp {harga_stats['mean']:,.0f}",
                f"Rp {harga_stats['min']:,.0f}",
                f"Rp {harga_stats['max']:,.0f}",
                f"Rp {harga_stats['std']:,.0f}",
                f"Rp {harga_stats['25%']:,.0f}",
                f"Rp {harga_stats['50%']:,.0f}",
                f"Rp {harga_stats['75%']:,.0f}"
            ]
        })
        
        st.dataframe(stats_df, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("##### 📦 Statistik Produksi")
        prod_stats = filtered_df['Produksi'].describe()
        
        stats_df = pd.DataFrame({
            'Statistik': ['Total', 'Rata-rata', 'Minimum', 'Maksimum', 'Q1 (25%)', 'Median', 'Q3 (75%)'],
            'Nilai': [
                f"{prod_stats['count'] * prod_stats['mean']:,.0f} ton",
                f"{prod_stats['mean']:,.0f} ton",
                f"{prod_stats['min']:,.0f} ton",
                f"{prod_stats['max']:,.0f} ton",
                f"{prod_stats['25%']:,.0f} ton",
                f"{prod_stats['50%']:,.0f} ton",
                f"{prod_stats['75%']:,.0f} ton"
            ]
        })
        
        st.dataframe(stats_df, use_container_width=True, hide_index=True)
    
    # Download data yang difilter
    st.markdown("---")
    st.markdown("### 📥 Download Data")
    
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="📄 Download Data Filtered (CSV)",
        data=csv,
        file_name=f"data_filtered_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv",
        use_container_width=True
    )

# Footer Kekinian (Samaran)
st.markdown("---")
current_time = datetime.now().strftime("%d %B %Y · %H:%M")

st.markdown(f"""
<div style="text-align: center; padding: 20px; font-size: 14px; color: #555;">
    <div style="font-weight: 600; margin-bottom: 6px;">
        🌾 Dashboard Pertanian Jawa Timur · 2020
    </div>
    <div style="font-size: 13px; margin-bottom: 6px;">
        Built by <strong>0110222222</strong> · STT Terpadu Nurul Fikri
    </div>
    <div style="font-size: 12px; color: #888;">
        Data: Jan–Dec 2020 · Last update: {current_time}
    </div>
</div>
""", unsafe_allow_html=True)
