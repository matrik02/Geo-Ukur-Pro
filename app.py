import streamlit as st

# 1. Konfigurasi Halaman
st.set_page_config(
    page_title="Sistem Geo-Ukur Selamat", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# --- CSS TINGKAT TINGGI: HIDE IKON KANAN, KEKALKAN BUTANG SIDEBAR ---
hide_st_style = """
            <style>
            /* 1. Sembunyikan Footer & Menu Tiga Titik sepenuhnya */
            footer {visibility: hidden !important;}
            #MainMenu {visibility: hidden !important;}

            /* 2. PADAMKAN BAHAGIAN KANAN HEADER (Share, Star, GitHub, Edit, Deploy) */
            /* Ini akan menghalang orang daripada klik ikon 'Edit' atau melihat kod */
            [data-testid="stHeaderActionElements"], 
            .stAppDeployButton, 
            header div:nth-child(2) {
                display: none !important;
                visibility: hidden !important;
            }

            /* 3. KEKALKAN BUTANG SIDEBAR (>>) DAN PASTIKAN IA BOLEH DIKLIK */
            /* Kita sasarkan butang sidebar secara spesifik */
            [data-testid="stSidebarCollapseIcon"], 
            button[aria-label="Open sidebar"],
            button[data-testid="stBaseButton-headerNoPadding"] {
                visibility: visible !important;
                display: flex !important;
                background-color: #f0f2f6 !important; /* Warna kelabu lembut supaya nampak */
                border-radius: 50% !important;
                z-index: 999999 !important;
                position: relative !important;
            }

            /* Pastikan header tidak menghalang klik (pointer-events) */
            header[data-testid="stHeader"] {
                background-color: rgba(0,0,0,0) !important;
                pointer-events: none !important;
            }
            
            /* Benarkan semula klik hanya pada butang sidebar */
            [data-testid="stSidebarCollapseIcon"], button[aria-label="Open sidebar"] {
                pointer-events: auto !important;
            }
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# --- LOGIK LOGIN ---
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
        st.error(f"Ralat: {e}")
    
    if st.sidebar.button("Log Keluar"):
        st.session_state['login_berjaya'] = False
        st.rerun()
