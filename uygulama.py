import streamlit as st
from google import genai
from PIL import Image

# --- 1. ŞIK VE PROFESYONEL ARAYÜZ YAPILANDIRMASI ---
st.set_page_config(page_title="X Analiz Ajani", page_icon="👁️", layout="centered")

st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stButton>button {
    width: 100%; 
    border-radius: 8px; 
    font-weight: bold; 
    background-color: #1DA1F2; 
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.title("👁️ X Profil Analiz Ajani")
st.markdown("X (Twitter) profillerini yapay zeka ile derinlemesine inceleyin.")

# --- API ANAHTARI ---
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

# --- 2. SEKME (TAB) YAPISI ---
sekme1, sekme2 = st.tabs(["🚀 Kendi Profilimi Büyüt", "🕵️‍♂️ Başkasını İncele (Karakter Analizi)"])

# ==========================================
# SEKME 1: BÜYÜME VE TAKİPÇİ ARTIRMA
# ==========================================
with sekme1:
    st.info("Bu bölüm, kendi hesabınızı büyütmek ve etkileşiminizi artırmak için 30 günlük stratejiler sunar.")
    
    kullanici_1 = st.text_input("Sizin X Kullanıcı Adınız:", key="kullanici_1")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        yuklenen_dosyalar_1 = st.file_uploader("📸 Ekran Görüntüleri", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key="dosya_1")
    with col2:
        manuel_tweetler_1 = st.text_area("📝 Metin Yapıştır", height=100, key="metin_1")
    with col3:
        arsiv_dosyasi_1 = st.file_uploader("📁 X Arşivi", type=["csv", "txt", "json"], key="arsiv_1")

    if st.button("🚀 Büyüme Analizini Başlat", key="btn_1"):
        if not kullanici_1:
            st.warning("Lütfen X kullanıcı adınızı girin.")
        elif not yuklenen_dosyalar_1 and not manuel_tweetler_1 and not arsiv_dosyasi_1:
            st.warning("Analiz için en az bir veri yüklemelisiniz.")
        else:
            with st.spinner("Büyüme reçeteniz yazılıyor..."):
                try:
                    client = genai.Client(api_key=GEMINI_API_KEY)
                    icerikler = []
                    
                    arsiv_metni = ""
                    if arsiv_dosyasi_1:
                        arsiv_metni = arsiv_dosyasi_1.getvalue().decode("utf-8")[:100000]
                    
                    prompt_1 = f"Görev: @{kullanici_1} adlı kullanıcı için büyüme danışmanlığı yap.\n"
                    prompt_1 += "Raporun %80'i DOĞRUDAN uygulanabilir tavsiyeler olmalı.\n"
                    if manuel_tweetler_1: prompt_1 += f"Tweetler:\n{manuel_tweetler_1}\n"
                    if arsiv_metni: prompt_1 += f"Arşiv:\n{arsiv_metni}\n"
                    
                    prompt_1 += "Format:\n🎯 1. Mevcut Durum\n💡 2. İçerik Reçetesi (3 örnek tweet ile)\n🚀 3. 30 Günlük Büyüme Stratejisi"
                    icerikler.append(prompt_1)
                    
                    if yuklenen_dosyalar_1:
                        for dosya in yuklenen_dosyalar_1: icerikler.append(Image.open(dosya))
                            
                    res = client.models.generate_content(model='gemini-2.5-flash', contents=icerikler)
                    st.success("Büyüme Raporu Hazır!")
                    st.write(res.text)
                except Exception as e:
                    st.error(f"Hata: {e}")

# ==========================================
# SEKME 2: KARAKTER VE İK ANALİZİ
# ==========================================
with sekme2:
    st.info("Bu bölüm; işe alacağınız bir adayın, yeni tanıştığınız birinin veya rakiplerinizin X profilini psikolojik ve profesyonel açıdan analiz eder.")
    
    kullanici_2 = st.text_input("İncelenecek Kişinin X Kullanıcı Adı:", key="kullanici_2")
    
    col4, col5 = st.columns(2)
    with col4:
        yuklenen_dosyalar_2 = st.file_uploader("📸 Profil/Tweet Görüntüleri", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key="dosya_2")
    with col5:
        manuel_tweetler_2 = st.text_area("📝 Kopyalanan Tweet Metinleri", height=100, key="metin_2")

    if st.button("🕵️‍♂️ Karakter Analizini Başlat", key="btn_2"):
        if not kullanici_2:
            st.warning("Lütfen incelenecek kişinin kullanıcı adını girin.")
        elif not yuklenen_dosyalar_2 and not manuel_tweetler_2:
            st.warning("Analiz için kişiye ait en az bir ekran görüntüsü veya metin girmelisiniz.")
        else:
            with st.spinner("Yapay zeka profilin psikolojik ve profesyonel röntgenini çekiyor..."):
                try:
                    client = genai.Client(api_key=GEMINI_API_KEY)
                    icerikler_2 = []
                    
                    prompt_2 = f"Görev: @{kullanici_2} adlı X kullanıcısının psikolojik, profesyonel ve sosyal eğilimlerini analiz et. Sen uzman bir İnsan Kaynakları profesyoneli ve davranış bilimcisisin.\n\n"
                    if manuel_tweetler_2: prompt_2 += f"İncelenecek Tweetler:\n{manuel_tweetler_2}\n\n"
                    
                    prompt_2 += """
                    Lütfen şu başlıklarda tarafsız, net ve içgörü dolu bir rapor sun:
                    
                    🧠 1. Kişilik Çıkarımı ve İlgi Alanları
                    - Bu kişi nasıl bir karaktere sahip? (Örn: Agresif, mizahi, analitik, tartışmacı, sakin)
                    - En çok hangi konulara (teknoloji, siyaset, sanat, vb.) ilgi duyuyor?
                    
                    🗣️ 2. İletişim Tonu ve Üslup
                    - İnsanlarla iletişim kurarken nasıl bir dil kullanıyor?
                    
                    ⚠️ 3. Profesyonel Değerlendirme & Kırmızı Bayraklar (Red Flags)
                    - Bir işveren olsanız, bu profili nasıl değerlendirirsiniz?
                    - Ekip çalışmasına uygun mu, yoksa toksik/kutuplaştırıcı eğilimleri var mı?
                    """
                    icerikler_2.append(prompt_2)
                    
                    if yuklenen_dosyalar_2:
                        for dosya in yuklenen_dosyalar_2: icerikler_2.append(Image.open(dosya))
                            
                    res_2 = client.models.generate_content(model='gemini-2.5-flash', contents=icerikler_2)
                    st.success("Karakter Analizi Tamamlandı!")
                    st.markdown("### 🕵️‍♂️ Kişilik ve Eğilim Raporu")
                    st.write(res_2.text)
                except Exception as e:
                    st.error(f"Hata: {e}")