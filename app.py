import streamlit as st

# 1. Konfigurasi Halaman
st.set_page_config(
    page_title="Sistem Geo-Ukur Selamat", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# --- KOD CSS MODEN: HILANGKAN IKON KANAN, KEKALKAN BUTANG SIDEBAR SAHAJA ---
hide_st_style = """
            <style>
            /* 1. Sembunyikan Footer & Menu Tiga Titik */
            footer {visibility: hidden !important;}
            #MainMenu {visibility: hidden !important;}

            /* 2. SEMBUNYIKAN SELURUH BAHAGIAN KANAN HEADER */
            /* Ini akan memadamkan Share, Star, Edit, GitHub, dan Deploy */
            [data-testid="stHeaderActionElements"], 
            .stAppDeployButton, 
            [data-testid="stStatusWidget"] {
                display: none !important;
            }

            /* 3. ASINGKAN & PAKSA BUTANG SIDEBAR (>>) UNTUK MUNCUL */
            /* Kita buat header lutsinar supaya butang di bawahnya tidak terlindung */
            header[data-testid="stHeader"] {
                background-color: rgba(0,0,0,0) !important;
                pointer-events: none; /* Supaya klik boleh tembus ke butang di bawah */
            }

            /* Aktifkan semula klik hanya untuk butang sidebar */
            [data-testid="stSidebarCollapseIcon"], 
            button[aria-label="Open sidebar"],
            button[data-testid="stBaseButton-headerNoPadding"] {
                pointer-events: auto !important;
                visibility: visible !important;
                display: flex !important;
                background-color: #f0f2f6 !important; /* Warna kelabu lembut supaya nampak */
                border-radius: 50% !important;
                margin-left: 10px !important;
                z-index: 999999 !important;
            }

            /* Menghapuskan sebarang elemen 'ghost' yang mungkin masih ada di kanan header */
            header > div:first-child > div:nth-child(2) {
                display: none !important;
            }
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# --- LOGIK LOGIN (Kekalkan yang asal) ---
KATA_LALUAN_BETUL = "admin123"
if 'login_berjaya' not in st.session_state:
    st.session_state['login_berjaya'] = False

def semak_login():
    if st.session_state["input_password"] == KATA_LALUAN_BETUL:
        st.session_state['login_berjaya'] = True
    else:
        st.error("Kata laluan salah!")

if not st.session_state['login_berjaya']:
    # Paparan Login
    col_logo, col_tajuk = st.columns([1, 4]) 
    with col_logo:
        try: st.image("logo.jpg", width=250)
        except: st.warning("Fail logo.jpg tidak dijumpai")
    with col_tajuk:
        st.title("SISTEM PENGURUSAN MAKLUMAT TANAH")
    
    st.markdown("---")
    st.text_input("Kata Laluan", type="password", key="input_password", on_change=semak_login)
    st.button("Masuk", on_click=semak_login)
else:
    # Paparan Utama
    try:
        import polygonsatelite
        st.sidebar.title("Menu Tetapan")
        polygonsatelite.main() 
    except Exception as e:
        st.error(f"Gagal memuatkan sistem utama: {e}")
    
    if st.sidebar.button("Log Keluar"):
        st.session_state['login_berjaya'] = False
        st.rerun()

