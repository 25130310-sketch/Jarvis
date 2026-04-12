import streamlit as st
import yfinance as yf
import google.generativeai as genai

# ARAYÜZ AYARLARI
st.set_page_config(page_title="Jarvis AI", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    h1 { color: #00d4ff; text-align: center; font-family: 'Courier New', Courier, monospace; }
    .stMetric { background-color: #1a1c23; padding: 15px; border-radius: 10px; border: 1px solid #00d4ff; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>JARVIS CORE v1.0</h1>", unsafe_allow_html=True)

# API ANAHTARINIZ YERLEŞTİRİLDİ
GEMINI_KEY = 'AIzaSyCZxwv408UVf3xtjxWI8oxQt_2giVGkc3A' 

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-pro')

# BORSA VERİSİ (ASELSAN)
try:
    asels = yf.Ticker("ASELS.IS").history(period="1d")
    fiyat = round(asels['Close'].iloc[-1], 2)
    st.metric(label="ASELSAN GÜNCEL VERİ", value=f"{fiyat} TL")
except Exception as e:
    fiyat = "Bilinmiyor"
    st.error("Borsa verisi şu an çekilemedi.")

# ANA İŞLEM BUTONU
if st.button("SİSTEMİ ATEŞLE"):
    with st.spinner('Bağlantı kuruluyor...'):
        try:
            # Jarvis'e özel komut
            prompt = f"Sen JARVIS'sin. Aselsan hisse fiyatı {fiyat} TL. Bu durumu Iron Man'e rapor verir gibi havalı ve kısa bir şekilde Türkçe anlat. Özel karakter kullanma."
            
            response = model.generate_content(prompt)
            rapor = response.text.replace("'", "") # Seslendirme hatası olmaması için
            
            st.info(f"JARVIS: {rapor}")
            
            # SESLENDİRME KOMUTU (IPAD VE SAFARI UYUMLU)
            st.components.v1.html(f"""
                <script>
                var msg = new SpeechSynthesisUtterance("{rapor}");
                msg.lang = "tr-TR";
                msg.pitch = 1;
                msg.rate = 1;
                window.speechSynthesis.speak(msg);
                </script>
                """, height=0)
        except Exception as e:
            st.error(f"Bir hata oluştu: {e}")
