import streamlit as st

# Pastikan ini baris pertama dalam kod
st.set_page_config(
    page_title="Sistem Geo-Ukur Selamat", 
    layout="wide", 
    initial_sidebar_state="collapsed" # Ini akan menyorokkan sidebar secara automatik
)
# --- KOD UNTUK HIDE MENU & FOOTER ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
# 1. Tetapkan Kata Laluan
KATA_LALUAN_BETUL = "admin123"

# 2. Inisialisasi Session State untuk status login
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
    
    # SUSUNAN LOGO DAN TAJUK BERSEBELAHAN
    col_logo, col_tajuk = st.columns([1, 4]) # Nisbah 1:4
    
    with col_logo:
        # Gantikan 'logo.png' dengan nama fail logo anda (png/jpg)
        try:
            st.image("logo.jpg", width=250) 
        except:
            st.warning("Fail logo.png tidak dijumpai")

    with col_tajuk:
        st.title("SISTEM PENGURUSAN MAKLUMAT TANAH")
    
    st.markdown("---") # Garis pemisah
    st.subheader("🔒 Akses Terhad")
    st.info("Sila masukkan kata laluan untuk menggunakan sistem")
    
    st.text_input("Kata Laluan", type="password", key="input_password", on_change=semak_login)
    st.button("Masuk", on_click=semak_login)

else:
    # --- HALAMAN 2: SISTEM UTAMA ---
    try:
        import polygonsatelite
        polygonsatelite.main() 
    except Exception as e:
        st.error(f"Gagal memuatkan sistem utama: {e}")
    
    # Butang Logout di Sidebar
    if st.sidebar.button("Log Keluar (Logout)"):
        st.session_state['login_berjaya'] = False

        st.rerun()










