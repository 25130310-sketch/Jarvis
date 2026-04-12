import streamlit as st
import yfinance as yf
import google.generativeai as genai

# ARAYÜZ
st.set_page_config(page_title="Jarvis", layout="centered")
st.title("JARVIS CORE v1.0")

# API ANAHTARI - Boşlukları temizleyen özel fonksiyon
RAW_KEY = 'AIzaSyCZxwv408UVf3xtjxWI8oxQt_2giVGkc3A'
GEMINI_KEY = RAW_KEY.strip() 

try:
    genai.configure(api_key=GEMINI_KEY)
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error(f"Kurulum Hatası: {e}")

# VERİ ÇEKME
asels = yf.Ticker("ASELS.IS").history(period="1d")
fiyat = round(asels['Close'].iloc[-1], 2)
st.metric("ASELSAN", f"{fiyat} TL")

if st.button("SİSTEMİ ATEŞLE"):
    with st.spinner('Jarvis uyanıyor...'):
        try:
            # En basit sorgu
            response = model.generate_content("Merhaba Jarvis, sistemler hazır mı?")
            rapor = response.text
            st.info(f"JARVIS: {rapor}")
            
            # Seslendirme
            st.components.v1.html(f'<script>var m=new SpeechSynthesisUtterance("{rapor}");m.lang="tr-TR";window.speechSynthesis.speak(m);</script>', height=0)
        except Exception as e:
            st.error("Hala hata alıyoruz. Lütfen Google AI Studio'dan yeni bir API KEY almayı deneyin, bu anahtar kısıtlanmış olabilir.")
