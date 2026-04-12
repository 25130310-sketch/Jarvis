import streamlit as st
import yfinance as yf
import google.generativeai as genai

# ARAYÜZ TASARIMI
st.set_page_config(page_title="Jarvis AI", layout="centered")
st.markdown("<h1 style='text-align: center; color: #00d4ff;'>JARVIS CORE v1.0</h1>", unsafe_allow_html=True)

# EN SON VERDİĞİNİZ ANAHTAR
GEMINI_KEY = 'AIzaSyAVJgBwg5pqVVjxbWTHJa6O_8XP6X_B0_w'.strip()

# TEST FONKSİYONU
def sistemi_kontrol_et():
    try:
        genai.configure(api_key=GEMINI_KEY)
        model = genai.GenerativeModel('gemini-pro')
        # Küçük bir test mesajı gönderiyoruz
        response = model.generate_content("Test")
        return True, "Sistem Aktif"
    except Exception as e:
        return False, str(e)

# BORSA VERİSİ
asels = yf.Ticker("ASELS.IS").history(period="1d")
fiyat = round(asels['Close'].iloc[-1], 2)
st.metric("ASELSAN", f"{fiyat} TL")

if st.button("SİSTEMİ ATEŞLE"):
    is_ok, mesaj = sistemi_kontrol_et()
    
    if is_ok:
        st.success("Jarvis Bağlantısı Başarılı!")
        model = genai.GenerativeModel('gemini-pro')
        res = model.generate_content(f"Aselsan {fiyat} TL. Havalı bir rapor ver.")
        st.info(res.text)
    else:
        st.error(f"Bağlantı Kurulamadı: {mesaj}")
        st.warning("Eğer 'API_KEY_INVALID' yazıyorsa, Google anahtarı henüz onaylamamış demektir. Lütfen 5-10 dakika bekleyin.")
