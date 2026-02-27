import streamlit as st

# 1. Konfigurasi Halaman
st.set_page_config(
    page_title="Sistem Geo-Ukur Selamat", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# --- CSS TINGKAT TINGGI: PENGASINGAN BUTANG SIDEBAR & IKON DEPLOY/SHARE ---
hide_st_style = """
            <style>
            /* 1. Sembunyikan Footer & Menu Tiga Titik */
            footer {visibility: hidden !important;}
            #MainMenu {visibility: hidden !important;}

            /* 2. SEMBUNYIKAN BAHAGIAN KANAN HEADER SAHAJA (Share, Star, GitHub, Deploy) */
            /* Kita sasarkan container aksi header di sebelah kanan */
            header div[data-testid="stHeaderActionElements"],
            header .stAppDeployButton,
            header div[data-testid="stStatusWidget"] {
                display: none !important;
                visibility: hidden !important;
            }

            /* 3. KEKALKAN & ASINGKAN BUTANG SIDEBAR (>>) */
            /* Kita pastikan butang di sebelah kiri tidak terkesan */
            header[data-testid="stHeader"] {
                background-color: rgba(0,0,0,0) !important;
                display: flex !important;
                justify-content: flex-start !important; /* Paksa elemen ke kiri */
            }

            /* Paksa butang buka sidebar muncul dengan jelas */
            button[data-testid="stBaseButton-headerNoPadding"],
            [data-testid="stSidebarCollapseIcon"],
            button[aria-label="Open sidebar"] {
                visibility: visible !important;
                display: flex !important;
                background-color: #f0f2f6 !important;
                border-radius: 50% !important;
                margin-left: 10px !important;
                z-index: 99999 !important;
            }

            /* Menghapuskan elemen-elemen hantu yang mungkin muncul di kanan */
            .st-emotion-cache-h5rgaw, .st-emotion-cache-1647z97 {
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
