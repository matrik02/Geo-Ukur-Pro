import streamlit as st

# 1. Konfigurasi Halaman
st.set_page_config(
    page_title="Sistem Pengurusan Maklumat Tanah", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# 2. CSS UNTUK HIDE IKON KANAN & KEKALKAN BUTANG SIDEBAR
hide_st_style = """
    <style>
    /* Sembunyikan footer */
    footer {visibility: hidden !important;}

    /* Sembunyikan Toolbar Header (Share, Star, GitHub, Edit) */
    div[data-testid="stToolbar"] {
        display: none !important;
    }

    /* Sembunyikan butang Deploy */
    .stAppDeployButton {display:none !important;}
    
    /* Sembunyikan menu tiga titik */
    #MainMenu {visibility: hidden !important;}

    /* Pastikan header lutsinar supaya butang sidebar nampak */
    header[data-testid="stHeader"] {
        background-color: rgba(0,0,0,0) !important;
    }

    /* Pastikan butang buka sidebar (>) di kiri atas kekal ada */
    button[data-testid="stBaseButton-headerNoPadding"] {
        visibility: visible !important;
        z-index: 999 !important;
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
    st.title("🔒 SISTEM PENGURUSAN MAKLUMAT TANAH")
    st.text_input("Kata Laluan", type="password", key="input_password", on_change=semak_login)
    st.button("Masuk", on_click=semak_login)
else:
    # Paparan Sistem Utama
    try:
        import polygonsatelite
        polygonsatelite.main() 
    except Exception as e:
        st.error(f"Ralat: {e}")
    
    if st.sidebar.button("Log Keluar"):
        st.session_state['login_berjaya'] = False
        st.rerun()
