import streamlit as st
import yfinance as yf
import google.generativeai as genai

# ARAYÜZ AYARLARI
st.set_page_config(page_title="Jarvis AI", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    h1 { color: #00d4ff; text-align: center; font-family: sans-serif; text-shadow: 2px 2px #000; }
    .stMetric { border: 1px solid #00d4ff; padding: 10px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("JARVIS CORE v1.0")

# YENİ API ANAHTARINIZ (Tam ve Boşluksuz)
GEMINI_KEY = 'AIzaSyCjy_mRLq4H0RqnrFu4hckIjuKtq4w3jZU'

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-pro')

# BORSA VERİSİ
try:
    asels = yf.Ticker("ASELS.IS").history(period="1d")
    fiyat = round(asels['Close'].iloc[-1], 2)
    st.metric(label="ASELSAN HİSSE DEĞERİ", value=f"{fiyat} TL")
except:
    fiyat = "Bilinmiyor"
    st.warning("Borsa verisine ulaşılamadı.")

# SİSTEMİ ATEŞLE
if st.button("SİSTEMİ ATEŞLE"):
    with st.spinner('Jarvis protokolleri başlatıyor...'):
        try:
            # Analiz mesajı
            prompt = f"Sen JARVIS'sin. Aselsan fiyatı {fiyat} TL. Iron Man'e havalı, kısa ve Türkçe bir rapor ver. Özel karakter kullanma."
            response = model.generate_content(prompt)
            rapor = response.text.replace("'", "")
            
            st.info(f"JARVIS: {rapor}")
            
            # SESLENDİRME (iPad Uyumlu)
            st.components.v1.html(f"""
                <script>
                var msg = new SpeechSynthesisUtterance("{rapor}");
                msg.lang = "tr-TR";
                window.speechSynthesis.speak(msg);
                </script>
                """, height=0)
                
        except Exception as e:
            st.error(f"Sistem Hatası: {e}")
            st.write("Not: Yeni anahtarların aktifleşmesi bazen 2-3 dakika sürebilir.")
