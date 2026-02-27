import streamlit as st

# 1. Konfigurasi Halaman (Mesti baris pertama)
st.set_page_config(
    page_title="Sistem Pengurusan Maklumat Tanah", 
    layout="wide", 
    initial_sidebar_state="collapsed" # Sidebar tertutup secara lalai untuk ruang luas
)

# 2. CSS UNTUK HIDE IKON HEADER KANAN SAHAJA (BUTANG SIDEBAR KEKAL)
hide_st_style = """
    <style>
    /* Sembunyikan footer (Made with Streamlit) */
    footer {visibility: hidden !important;}

    /* Sembunyikan Toolbar Header sebelah kanan (Share, Star, GitHub, Edit) */
    div[data-testid="stToolbar"] {
        display: none !important;
    }

    /* Sembunyikan butang Deploy yang mengganggu */
    .stAppDeployButton {display:none !important;}

    /* Sembunyikan menu tiga titik (MainMenu) */
    #MainMenu {visibility: hidden !important;}

    /* PASTIKAN HEADER LUTSINAR: 
       Supaya butang sidebar (>) di kiri atas nampak, 
       tapi bar putih tidak menghalang peta. */
    header[data-testid="stHeader"] {
        background-color: rgba(0,0,0,0) !important;
        color: white !important;
    }

    /* Pastikan butang buka sidebar (>) kekal nampak dan boleh diklik */
    button[data-testid="stBaseButton-headerNoPadding"] {
        visibility: visible !important;
        z-index: 999 !important;
    }
    </style>
    """
st.markdown(hide_st_style, unsafe_allow_html=True)

# 3. Tetapan Kata Laluan
KATA_LALUAN_BETUL = "admin123"

# 4. Inisialisasi Session State
if 'login_berjaya' not in st.session_state:
    st.session_state['login_berjaya'] = False

# Fungsi Proses Login
def semak_login():
    if st.session_state["input_password"] == KATA_LALUAN_BETUL:
        st.session_state['login_berjaya'] = True
    else:
        st.error("Kata laluan salah! Sila cuba lagi.")

# 5. Logik Paparan Halaman
if not st.session_state['login_berjaya']:
    # --- HALAMAN 1: LOGIN ---
    col_logo, col_tajuk = st.columns([1, 4])
    
    with col_logo:
        try:
            st.image("logo.jpg", width=250) 
        except:
            st.warning("Fail logo.jpg tidak dijumpai")

    with col_tajuk:
        st.title("SISTEM PENGURUSAN MAKLUMAT TANAH")
    
    st.markdown("---")
    st.subheader("🔒 Akses Terhad")
    st.info("Sila masukkan kata laluan untuk menggunakan sistem")
    
    st.text_input("Kata Laluan", type="password", key="input_password", on_change=semak_login)
    st.button("Masuk", on_click=semak_login)

else:
    # --- HALAMAN 2: SISTEM UTAMA ---
    try:
        import polygonsatelite
        # Tambah logo di Sidebar supaya nampak pro
        st.sidebar.image("logo.jpg", use_container_width=True)
        st.sidebar.markdown("---")
        
        # Panggil fungsi utama dari fail polygonsatelite.py
        polygonsatelite.main() 
    except Exception as e:
        st.error(f"Gagal memuatkan sistem utama: {e}")
    
    # Butang Logout di bawah sidebar
    st.sidebar.markdown("---")
    if st.sidebar.button("Log Keluar (Logout)"):
        st.session_state['login_berjaya'] = False
        st.rerun()
