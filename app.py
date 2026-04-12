import streamlit as st
import yfinance as yf
import google.generativeai as genai

# ARAYÜZ AYARLARI
st.set_page_config(page_title="Jarvis AI", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    h1 { color: #00d4ff; text-align: center; font-family: sans-serif; }
    </style>
    """, unsafe_allow_html=True)

st.title("JARVIS CORE v1.0")

# API ANAHTARI (Lütfen başında veya sonunda boşluk kalmadığından emin olun)
GEMINI_KEY = 'AIzaSyCZxwv408UVf3xtjxWI8oxQt_2giVGkc3A' 

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-pro')

try:
    asels = yf.Ticker("ASELS.IS").history(period="1d")
    fiyat = round(asels['Close'].iloc[-1], 2)
    st.success(f"ASELSAN GÜNCEL FİYAT: {fiyat} TL")
except:
    fiyat = "Bilinmiyor"

if st.button("SİSTEMİ ATEŞLE"):
    try:
        query = f"You are JARVIS. Aselsan price is {fiyat}. Give a short, cool tactical report in Turkish. No special characters."
        response = model.generate_content(query)
        rapor = response.text.replace("'", "")
        st.info(f"JARVIS: {rapor}")
        
        st.components.v1.html(f"""
            <script>
            var msg = new SpeechSynthesisUtterance("{rapor}");
            msg.lang = "tr-TR";
            window.speechSynthesis.speak(msg);
            </script>
            """, height=0)
    except Exception as e:
        st.error(f"Anahtar hatası: {e}")
