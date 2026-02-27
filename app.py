import streamlit as st

# 1. Konfigurasi Halaman (Mesti baris pertama)
st.set_page_config(
    page_title="Sistem Geo-Ukur Selamat", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# --- KOD CSS KHAS: HAPUS IKON KANAN, KEKALKAN BUTANG SIDEBAR (>) ---
hide_st_style = """
            <style>
            /* 1. Sembunyikan Footer & Menu Tiga Titik */
            footer {visibility: hidden !important;}
            #MainMenu {visibility: hidden !important;}

            /* 2. Sembunyikan Toolbar Kanan (Share, Star, GitHub, Edit) */
            /* Kita guna display:none pada data-testid stToolbar supaya ikon hilang terus */
            div[data-testid="stToolbar"] {
                display: none !important;
            }

            /* 3. Sembunyikan butang Deploy */
            .stAppDeployButton {
                display: none !important;
            }

            /* 4. KEKALKAN BUTANG SIDEBAR (>) */
            /* Kita pastikan header tidak disembunyikan, cuma toolbar sahaja */
            header[data-testid="stHeader"] {
                background-color: rgba(0,0,0,0) !important;
                color: black !important;
            }
            
            /* Memastikan butang > jelas kelihatan dengan latar belakang putih sedikit */
            button[data-testid="stBaseButton-headerNoPadding"] {
                visibility: visible !important;
                background-color: white !important;
                border: 1px solid #ddd !important;
                border-radius: 50% !important;
                z-index: 9999 !important;
            }
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# 1. Tetapkan Kata Laluan
KATA_LALUAN_BETUL = "admin123"

# 2. Inisialisasi Session State
if 'login_berjaya' not in st.session_state:
    st.session_state['login_berjaya'] = False

# Fungsi untuk proses login
def semak_login():
    if st.session_state["input_password"] == KATA_LALUAN_BETUL:
        st.session_state['login_berjaya'] = True
    else:
        st.error("Kata laluan salah! Sila cuba lagi.")

# 3. Logik Paparan Halaman
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
        # Tambah tajuk kecil di sidebar supaya butang > berfungsi dengan baik
        st.sidebar.title("Menu Tetapan")
        polygonsatelite.main() 
    except Exception as e:
        st.error(f"Gagal memuatkan sistem utama: {e}")
    
    # Butang Logout di Sidebar
    st.sidebar.markdown("---")
    if st.sidebar.button("Log Keluar (Logout)"):
        st.session_state['login_berjaya'] = False
        st.rerun()
