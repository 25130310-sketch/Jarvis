import streamlit as st
import yfinance as yf
import google.generativeai as genai

# ARAYÜZ TASARIMI
st.set_page_config(page_title="Jarvis AI", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    h1 { color: #00d4ff; text-align: center; font-family: sans-serif; }
    </style>
    """, unsafe_allow_html=True)

st.title("JARVIS CORE v1.0")

# BURAYA KENDİ API KEYİNİ YAPIŞTIR
GEMINI_KEY = 'BURAYA_KENDI_ANAHTARINI_YAZ' 

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-pro')

# VERİ ÇEKME
try:
    asels = yf.Ticker("ASELS.IS").history(period="1d")
    fiyat = round(asels['Close'].iloc[-1], 2)
    st.success(f"ASELSAN GÜNCEL FİYAT: {fiyat} TL")
except:
    fiyat = "Bilinmiyor"
    st.error("Borsa verisi şu an alınamıyor.")

# BUTON VE ANALİZ
if st.button("SİSTEMİ ATEŞLE"):
    with st.spinner('Jarvis analiz ediyor...'):
        # Hata payını sıfırlamak için İngilizce sorup Türkçe cevap alıyoruz
        query = f"You are JARVIS. Aselsan price is {fiyat}. Give a short, cool tactical report in Turkish. No special characters."
        response = model.generate_content(query)
        rapor = response.text.replace("'", "")
        
        st.info(f"JARVIS: {rapor}")
        
        # SESLENDİRME (IPAD UYUMLU)
        st.components.v1.html(f"""
            <script>
            var msg = new SpeechSynthesisUtterance("{rapor}");
            msg.lang = "tr-TR";
            window.speechSynthesis.speak(msg);
            </script>
            """, height=0)
