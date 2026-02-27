# --- KOD CSS TERKINI: HAPUS IKON KANAN SECARA TOTAL, KEKALKAN BUTANG SIDEBAR (>) ---
hide_st_style = """
            <style>
            /* 1. Sembunyikan Footer & Menu Tiga Titik sepenuhnya */
            footer {visibility: hidden !important;}
            #MainMenu {visibility: hidden !important;}

            /* 2. Sembunyikan Toolbar Kanan (Share, Star, GitHub, Edit) */
            /* Kita sasarkan semua elemen status dan aksi di header */
            [data-testid="stHeaderActionElements"], 
            [data-testid="stStatusWidget"],
            header .st-emotion-cache-1647z97, 
            header .st-emotion-cache-12fmjuu {
                display: none !important;
            }

            /* 3. Sembunyikan butang Deploy */
            .stAppDeployButton {
                display: none !important;
            }

            /* 4. PASTIKAN BUTANG SIDEBAR (>) KEKAL ADA */
            header[data-testid="stHeader"] {
                background-color: rgba(0,0,0,0) !important;
            }
            
            /* Paksa butang sidebar (ikon >) untuk muncul */
            /* Kita sasarkan butang itu sendiri secara spesifik */
            [data-testid="stSidebarCollapseIcon"],
            button[aria-label="Open sidebar"] {
                visibility: visible !important;
                display: flex !important;
                background-color: #f0f2f6 !important;
                border-radius: 50% !important;
                z-index: 99999 !important;
            }
            
            /* Menghilangkan garisan putih nipis di header yang mungkin mengganggu */
            header {
                border-bottom: none !important;
            }
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
