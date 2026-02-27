import streamlit as st

# 1. Konfigurasi Halaman
st.set_page_config(
    page_title="Sistem Pengurusan Maklumat Tanah", 
    layout="wide", 
    initial_sidebar_state="collapsed" # Sidebar akan tertutup pada mulanya
)

# 2. CSS TERBARU: Hapus Ikon Kanan, Kekalkan Butang Sidebar di Kiri
hide_st_style = """
    <style>
    /* 1. Sembunyikan footer & menu tiga titik */
    footer {visibility: hidden !important;}
    #MainMenu {visibility: hidden !important;}

    /* 2. Sembunyikan Toolbar Header sebelah kanan (Share, Star, GitHub, Edit) */
    div[data-testid="stToolbar"] {
        display: none !important;
    }

    /* 3. Sembunyikan butang Deploy */
    .stAppDeployButton {display:none !important;}

    /* 4. PEMBETULAN HEADER: Jangan sorok header, cuma buat lutsinar */
    header[data-testid="stHeader"] {
        background-color: rgba(0,0,0,0) !important;
    }

    /* 5. PEMBETULAN SIDEBAR TOGGLE: Pastikan butang '>' nampak jelas */
    button[data-testid="stBaseButton-headerNoPadding"] {
        visibility: visible !important;
        background-color: #f0f2f6 !important; /* Beri warna latar sikit supaya nampak */
        border-radius: 50% !important;
        z-index: 999999 !important;
    }
    </style>
    """
st.markdown(hide_st_style, unsafe_allow_html=True)

# 3. Logik Login
KATA_LALUAN_BETUL = "admin123"

if 'login_berjaya' not in st.session_state:
    st.session_state['login_berjaya'] = False

def semak_login():
    if st.session_state["input_password"] == KATA_LALUAN_BETUL:
        st.session_state['login_berjaya'] = True
    else:
        st.error("Kata laluan salah!")

if not st.session_state['login_berjaya']:
    # --- HALAMAN LOGIN ---
    st.title("🔒 SISTEM PENGURUSAN MAKLUMAT TANAH")
    st.text_input("Kata Laluan", type="password", key="input_password", on_change=semak_login)
    st.button("Masuk", on_click=semak_login)
else:
    # --- HALAMAN UTAMA ---
    try:
        import polygonsatelite
        # Pastikan sidebar ada kandungan supaya tidak nampak kosong bila dibuka
        st.sidebar.title("Menu Utama")
        polygonsatelite.main() 
    except Exception as e:
        st.error(f"Ralat: {e}")
    
    # Butang Logout
    st.sidebar.markdown("---")
    if st.sidebar.button("Log Keluar"):
        st.session_state['login_berjaya'] = False
        st.rerun()
