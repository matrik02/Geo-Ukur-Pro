import os

# ========================================================
# UBAT UNTUK RALAT POSTGRESQL / PROJ:
# Buang gangguan environment variable dari perisian lain
# ========================================================
if 'PROJ_LIB' in os.environ:
    del os.environ['PROJ_LIB']

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Polygon
import numpy as np
import contextily as cx  # <-- LIBRARY UNTUK SATELIT

st.set_page_config(page_title="Geo-Ukur Pro v3.1", layout="wide")
st.title("🗺️ Visualisasi Poligon (Label Stesen Rapat & Di Luar)")

# ==========================================
# MENU TETAPAN (SIDEBAR)
# ==========================================
st.sidebar.header("⚙️ Tetapan Peta")

papar_satelit = st.sidebar.checkbox("🌍 Buka Layer Satelit (On/Off)", value=False)

if papar_satelit:
    st.sidebar.info("Sistem perlukan Kod EPSG untuk tahu lokasi sebenar di atas muka bumi.")
    kod_epsg = st.sidebar.text_input("Kod EPSG (Cth: 4390, 3386, 3168):", value="4390")

# SLIDER UNTUK ZOOM OUT (MARGIN)
margin_peta = st.sidebar.slider("🔍 Zum Keluar Peta (Margin dalam Meter)", min_value=5, max_value=200, value=20)

st.sidebar.markdown("---")

# ==========================================
# MENU TETAPAN LABEL
# ==========================================
st.sidebar.header("🏷️ Tetapan Label")
papar_label_stesen = st.sidebar.checkbox("Papar Label Stesen (STN)", value=True)
papar_label_garisan = st.sidebar.checkbox("Papar Bearing & Jarak", value=True)
papar_label_luas = st.sidebar.checkbox("Papar Label Luas", value=True)

uploaded_file = st.file_uploader("Upload fail CSV anda", type=['csv'])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    if 'E' in df.columns and 'N' in df.columns:
        coords = list(zip(df['E'], df['N']))
        poly_geom = Polygon(coords)
        gdf = gpd.GeoDataFrame(index=[0], geometry=[poly_geom])
        centroid = poly_geom.centroid
        
        luas = poly_geom.area
        perimeter = poly_geom.length
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Luas", f"{luas:.2f} m²")
        col2.metric("Perimeter", f"{perimeter:.2f} m")
        col3.metric("Bilangan Stesen", len(df))

        # Saiz Rajah 5x5
        fig, ax = plt.subplots(figsize=(5, 5))
        
        warna_garisan = 'cyan' if papar_satelit else 'black'
        
        gdf.plot(ax=ax, facecolor='none', edgecolor=warna_garisan, linewidth=1.5, zorder=1)
        ax.scatter(df['E'], df['N'], color='red', s=30, zorder=5)

        num_points = len(df)
        for i in range(num_points):
            p1 = df.iloc[i]
            p2 = df.iloc[(i + 1) % num_points]

            # PENGIRAAN BEARING & JARAK
            de = p2['E'] - p1['E']
            dn = p2['N'] - p1['N']
            jarak = np.sqrt(de**2 + dn**2)
            angle_deg = np.degrees(np.arctan2(de, dn)) % 360
            
            d = int(angle_deg)
            m = int((angle_deg - d) * 60)
            s = int(round(((angle_deg - d) * 60 - m) * 60))
            if s == 60: m += 1; s = 0
            if m == 60: d += 1; m = 0
            bearing_text = f"{d}°{m:02d}'{s:02d}\""

            txt_angle_deg = np.degrees(np.arctan2(dn, de))
            if txt_angle_deg > 90: txt_angle_deg -= 180
            if txt_angle_deg < -90: txt_angle_deg += 180

            mid_e, mid_n = (p1['E'] + p2['E']) / 2, (p1['N'] + p2['N']) / 2

            # LOGIK ON/OFF: BEARING & JARAK
            if papar_label_garisan:
                ax.text(mid_e, mid_n, f"{bearing_text}\n{jarak:.2f}m", 
                        fontsize=7, color='darkred', fontweight='bold',
                        ha='center', va='center', rotation=txt_angle_deg,
                        bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=0.5))

            # LOGIK LABEL STESEN
            vec_e = p1['E'] - centroid.x
            vec_n = p1['N'] - centroid.y
            dist_from_center = np.sqrt(vec_e**2 + vec_n**2)
            
            if dist_from_center == 0: dist_from_center = 1
            
            offset_dist = 0.5  
            label_e = p1['E'] + (vec_e / dist_from_center) * offset_dist
            label_n = p1['N'] + (vec_n / dist_from_center) * offset_dist

            warna_stn = 'yellow' if papar_satelit else 'blue'
            latar_belakang_stn = dict(facecolor='black', alpha=0.4, edgecolor='none', pad=0.1) if papar_satelit else None

            # LOGIK ON/OFF: LABEL STESEN
            if papar_label_stesen:
                ax.text(label_e, label_n, str(p1['STN']), 
                        fontsize=8, color=warna_stn, fontweight='bold',
                        ha='center', va='center', bbox=latar_belakang_stn)

        # LOGIK ON/OFF: LUAS DI TENGAH
        if papar_label_luas:
            ax.text(centroid.x, centroid.y, f"LUAS\n{luas:.2f} m²", 
                    ha='center', va='center', fontsize=9, fontweight='bold', color='darkgreen',
                    bbox=dict(facecolor='white', alpha=0.8, edgecolor='green', boxstyle='round,pad=0.3'))

        # =================================================================
        # FUNGSI ZOOM OUT DILAKSANAKAN DI SINI
        # =================================================================
        minx, miny, maxx, maxy = gdf.total_bounds
        
        # Tambahkan nilai 'margin_peta' dari slider ke sempadan tersebut
        ax.set_xlim(minx - margin_peta, maxx + margin_peta)
        ax.set_ylim(miny - margin_peta, maxy + margin_peta)

        ax.set_aspect('equal')
        
        warna_grid = 'white' if papar_satelit else 'black'
        ax.grid(True, linestyle=':', alpha=0.3, color=warna_grid)
        ax.tick_params(axis='both', which='major', labelsize=7)

        # =================================================================
        # 5. MENAMBAH LAYER SATELIT JIKA DIHIDUPKAN (ON)
        # =================================================================
        if papar_satelit:
            try:
                gdf = gdf.set_crs(epsg=int(kod_epsg))
                
                # Gunakan URL Tile Google Maps Satelit
                url_google_satelit = "https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}"
                
                # Biarkan zoom pada 19 supaya gambar kekal tajam
                cx.add_basemap(ax, crs=gdf.crs.to_string(), 
                               source=url_google_satelit, 
                               zoom=19,
                               attribution="© Google Maps")
            except Exception as e:
                st.error(f"Gagal memuatkan imej satelit. Sila pastikan Kod EPSG sah. Info ralat: {e}")

        # HALANG STREAMLIT MEMBESARKAN GAMBAR
        st.pyplot(fig, use_container_width=False)
        
    else:
        st.error("Ralat: Kolum 'E' dan 'N' diperlukan.")