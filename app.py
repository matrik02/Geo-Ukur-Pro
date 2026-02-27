import streamlit as st

# 1. Konfigurasi Halaman (Mesti baris pertama)
st.set_page_config(
    page_title="Sistem Geo-Ukur Selamat", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# --- KOD CSS TERKINI: HAPUS IKON KANAN, PAKSA BUTANG SIDEBAR (>) MUNCUL ---
hide_st_style = """
            <style>
            /* 1. Sembunyikan Footer & Menu Tiga Titik sepenuhnya */
            footer {visibility: hidden !important;}
            #MainMenu {visibility: hidden !important;}

            /* 2. Sembunyikan Toolbar Kanan (Share, Star, GitHub, Edit) secara total */
            [data-testid="stHeaderActionElements"] {
                display: none !important;
            }

            /* 3. Sembunyikan butang Deploy */
            .stAppDeployButton {
                display: none !important;
            }

            /* 4. PASTIKAN BUTANG SIDEBAR (>) KEKAL ADA */
            /* Kita buat header lutsinar supaya tidak menutup butang */
            header[data-testid="stHeader"] {
                background-color: rgba(0,0,0,0) !important;
            }
            
            /* Paksa butang sidebar (ikon >) untuk muncul dan boleh diklik */
            /* Kita beri warna latar belakang kelabu cerah supaya butang nampak jelas */
            [data-testid="stSidebarCollapseIcon"] {
                visibility: visible !important;
                display: block !important;
                background-color: #f0f2f6 !important;
                border-radius: 50% !important;
                padding: 5px !important;
                z-index: 99999 !important;
            }

            /* Jika menggunakan butang header standard Streamlit */
            button[aria-label="Open sidebar"] {
                visibility: visible !important;
                display: block !important;
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
        # Sidebar akan muncul bila butang > diklik
        st.sidebar.title("Menu Tetapan")
        polygonsatelite.main() 
    except Exception as e:
        st.error(f"Gagal memuatkan sistem utama: {e}")
    
    # Butang Logout di Sidebar
    st.sidebar.markdown("---")
    if st.sidebar.button("Log Keluar (Logout)"):
        st.session_state['login_berjaya'] = False
        st.rerun()
