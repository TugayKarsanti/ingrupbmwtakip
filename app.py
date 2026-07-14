import streamlit as st
import pandas as pd
import uuid
from datetime import datetime, timedelta

# Sayfa Yapılandırması
st.set_page_config(page_title="İnciroğlu Otomotiv | Müşteri Takip Sistemi", layout="wide")

# Kurumsal Başlık
st.markdown("<h1 style='text-align: center; color: #000000; font-family: sans-serif;'>İnciroğlu Otomotiv Müşteri Takip Sistemi</h1>", unsafe_allow_html=True)

# Hafıza Yönetimi
if 'musteriler' not in st.session_state:
    st.session_state.musteriler = pd.DataFrame(columns=[
        "ID", "Tarih", "İsim", "Telefon", "Model", "Danışman", "Durum", "Test Sürüşü", "Özet"
    ])

# 1. Kayıt Formu
with st.form("yeni_kayit", clear_on_submit=True):
    col1, col2, col3 = st.columns(3)
    isim = col1.text_input("Müşteri Adı Soyadı")
    telefon = col2.text_input("Telefon Numarası")
    
    tum_modeller = [
        "BMW 1 Serisi", "BMW 2 Serisi", "BMW 3 Serisi", "BMW 4 Serisi", "BMW 5 Serisi", 
        "BMW 7 Serisi", "BMW i4", "BMW i5", "BMW iX3 50 xDrive", "BMW iX", "BMW i7",
        "BMW X1", "BMW X2", "BMW X3", "BMW X5", "BMW X7",
        "MINI COUNTRYMAN E", "MINI 3 KAPI", "MINI COUNTRYMAN C", 
        "MINI COUNTRYMAN JCW ALL4", "MINI JCW", "MINI CABRIO"
    ]
    model = col3.selectbox("Model", tum_modeller)
    
    col4, col5, col6 = st.columns(3)
    danismanlar = ["Çavuş Karakaya", "Furkan Benli", "Raife Karakız", "M.Tugay Karsantı", "Arif Yüksel", "Osman Sami Özkes"]
    danisman = col4.selectbox("Danışman", danismanlar)
    durum = col5.selectbox("Durum", ["Beklemede", "Satış Gerçekleşti", "Kaybedildi"])
    test_surusu = col6.radio("Test Sürüşü", ["Yapıldı", "Yapılmadı"], horizontal=True)
    
    ozet = st.text_input("Görüşme Özeti")
    
    if st.form_submit_button("➕ Müşteriyi Kaydet"):
        yeni_id = str(uuid.uuid4())[:8].upper()
        tarih = datetime.now().strftime("%Y-%m-%d")
        yeni_kayit = pd.DataFrame([[yeni_id, tarih, isim, telefon, model, danisman, durum, test_surusu, ozet]], 
                                 columns=st.session_state.musteriler.columns)
        st.session_state.musteriler = pd.concat([st.session_state.musteriler, yeni_kayit], ignore_index=True)
        st.success(f"Kayıt oluşturuldu! ID: {yeni_id}")

# 2. Arama ve Düzenleme (Veri Düzenleyici)
st.markdown("---")
arama = st.text_input("🔍 Müşteri Adı, Telefon veya Model ile Ara:")
df = st.session_state.musteriler

if arama:
    df = df[df.apply(lambda row: arama.lower() in str(row['İsim']).lower() or 
                                 arama.lower() in str(row['Telefon']).lower() or 
                                 arama.lower() in str(row['Model']).lower(), axis=1)]

# Durum Güncelleme için Data Editor
st.subheader("Müşteri Listesini Düzenle")
edited_df = st.data_editor(df, use_container_width=True, hide_index=True)
st.session_state.musteriler.update(edited_df)

# 3. Hatırlatma Algoritması (3 Gün)
st.markdown("---")
st.subheader("⏰ 3 Günlük Takip Hatırlatıcısı")
bugun = datetime.now()
hatirlatma_listesi = []

for idx, row in st.session_state.musteriler.iterrows():
    kayit_tarihi = datetime.strptime(row['Tarih'], "%Y-%m-%d")
    if row['Durum'] == "Beklemede" and (bugun - kayit_tarihi).days >= 3:
        hatirlatma_listesi.append(row)

if hatirlatma_listesi:
    hatirlatma_df = pd.DataFrame(hatirlatma_listesi)
    st.warning("⚠️ Takip Süresi Dolan Müşteriler:")
    st.dataframe(hatirlatma_df[['İsim', 'Telefon', 'Danışman', 'Özet']])
else:
    st.info("Takip süresi dolan bekleyen müşteriniz bulunmuyor.")