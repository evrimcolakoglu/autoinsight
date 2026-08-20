import os
import joblib
import pandas as pd
import streamlit as st

from src.config import DATA_RAW_PATH, MODEL_SAVE_PATH, NUMERIC_FEATURES, CATEGORICAL_FEATURES
from src.recommender.engine import VehicleRecommender
from src.rag.retriever import LocalRAGRetriever

# Sayfa Yapılandırması
st.set_page_config(
    page_title="AutoInsight AI",
    page_icon="🚗",
    layout="wide"
)

# Cache ile Veri ve Model Yükleme
@st.cache_resource
def load_resources():
    df = pd.read_csv(DATA_RAW_PATH)
    pipeline = joblib.load(MODEL_SAVE_PATH) if os.path.exists(MODEL_SAVE_PATH) else None
    recommender = VehicleRecommender(DATA_RAW_PATH)
    retriever = LocalRAGRetriever()
    return df, pipeline, recommender, retriever

df, pipeline, recommender, retriever = load_resources()

# Başlık
st.title("🚗 AutoInsight: Akıllı Araç Değerleme & Asistan")
st.caption("Yerel Makine Öğrenmesi, Öneri Algoritmaları ve Çevrimdışı RAG Mimarisi")

tab1, tab2, tab3 = st.tabs(["💰 Fiyat Tahmini (ML)", "🎯 Akıllı Araç Tavsiyesi", "📖 RAG Teknik Asistan"])

# ==========================================
# SEKME 1: MAKİNE ÖĞRENMESİ İLE FİYAT TAHMİNİ
# ==========================================
with tab1:
    st.subheader("İkinci El Araç Değerleme Modeli")
    st.write("Aracın teknik ve hasar bilgilerini girerek piyasa değerini tahmin edin.")

    col1, col2, col3 = st.columns(3)

    with col1:
        brand = st.selectbox("Marka", options=sorted(df['marka'].dropna().unique()))
        series_options = sorted(df[df['marka'] == brand]['seri'].dropna().unique())
        series = st.selectbox("Seri", options=series_options)
        model_options = sorted(df[(df['marka'] == brand) & (df['seri'] == series)]['model'].dropna().unique())
        model_name = st.selectbox("Model / Paket", options=model_options)
        city = st.selectbox("Konum (İl)", options=sorted(df['konum'].dropna().unique()))

    with col2:
        year = st.slider("Model Yılı", min_value=int(df['yil'].min()), max_value=int(df['yil'].max()), value=2020)
        km = st.number_input("Kilometre", min_value=0, max_value=1000000, value=80000, step=5000)
        fuel = st.selectbox("Yakıt Tipi", options=sorted(df['yakit_tipi'].dropna().unique()))
        transmission = st.selectbox("Vites Tipi", options=sorted(df['vites_tipi'].dropna().unique()))
        body = st.selectbox("Kasa Tipi", options=sorted(df['kasa_tipi'].dropna().unique()))

    with col3:
        engine_cc = st.number_input("Motor Hacmi (cc)", min_value=500.0, max_value=6000.0, value=1498.0, step=100.0)
        hp = st.number_input("Motor Gücü (HP)", min_value=40.0, max_value=600.0, value=150.0, step=10.0)
        drive = st.selectbox("Çekiş", options=sorted(df['cekis'].dropna().unique()))
        consumption = st.number_input("Ort. Yakıt Tüketimi (L/100km)", min_value=1.0, max_value=25.0, value=5.0, step=0.1)
        tank = st.number_input("Yakıt Deposu (L)", min_value=30.0, max_value=100.0, value=50.0, step=1.0)
        tramer = st.number_input("Tramer / Hasar Kaydı (TL)", min_value=0.0, value=0.0, step=1000.0)
        changed = st.number_input("Değişen Parça Sayısı", min_value=0, max_value=15, value=0)
        painted = st.number_input("Boyalı Parça Sayısı", min_value=0, max_value=15, value=0)

    if st.button("Fiyatı Tahmin Et", type="primary"):
        if pipeline is None:
            st.error("Eğitilmiş model dosyası bulunamadı. Lütfen önce `pipeline.py` dosyasını çalıştırın.")
        else:
            input_data = pd.DataFrame([{
                "marka": brand, "seri": series, "model": model_name, "konum": city,
                "yil": year, "kilometre": float(km), "yakit_tipi": fuel, "vites_tipi": transmission,
                "kasa_tipi": body, "motor_hacmi": engine_cc, "motor_gucu": hp, "cekis": drive,
                "ortalama_yakit_tuketimi": consumption, "yakit_deposu": tank, "tramer": tramer,
                "degisen": changed, "boyali": painted
            }])
            
            estimated_price = pipeline.predict(input_data)[0]
            st.success(f"### Tahmini Piyasa Değeri: **{estimated_price:,.2f} TL**")

# ==========================================
# SEKME 2: AKILLI ARAÇ TAVSİYE MOTORU
# ==========================================
with tab2:
    st.subheader("Bütçe ve Tercihe Dayalı Eşleştirme")
    
    r_col1, r_col2, r_col3 = st.columns(3)
    with r_col1:
        budget = st.number_input("Maksimum Bütçe (TL)", min_value=0, value=1500000, step=50000)
    with r_col2:
        fuel_pref = st.selectbox("Yakıt Tercihi", options=["Tümü"] + list(df['yakit_tipi'].dropna().unique()))
    with r_col3:
        trans_pref = st.selectbox("Vites Tercihi", options=["Tümü"] + list(df['vites_tipi'].dropna().unique()))

    if st.button("En Uygun Araçları Bul"):
        recs = recommender.recommend_by_preferences(
            max_budget=budget if budget > 0 else None,
            preferred_fuel=fuel_pref,
            preferred_transmission=trans_pref,
            top_n=5
        )
        if recs.empty:
            st.warning("Kriterlerinize uygun araç bulunamadı.")
        else:
            st.dataframe(
                recs.rename(columns={
                    "marka": "Marka", "seri": "Seri", "model": "Model", "yil": "Yıl",
                    "kilometre": "KM", "fiyat": "Fiyat (TL)", "match_score": "Uyum Skoru (%)"
                }),
                use_container_width=True
            )

# ==========================================
# SEKME 3: ÇEVRİMDIŞI RAG VE TEKNİK ASİSTAN
# ==========================================
with tab3:
    st.subheader("Kılavuz ve Bakım Dokümanları Asistanı (RAG)")
    st.write("Veritabanına kaydedilen araç bakım bültenlerinden bilgi çekin (Harici API gerektirmez).")

    user_query = st.text_input(
        "Teknik veya bakım sorusu sorun:",
        placeholder="Örn: Toyota Corolla Hybrid modelinde soğutma sıvısı ne zaman değişir?"
    )

    if st.button("Dokümanlarda Ara"):
        if user_query.strip():
            with st.spinner("Vektör veritabanında taranıyor..."):
                retrieved_chunks = retriever.retrieve_context(user_query, top_k=1)
                st.info(f"**Dokümandan Çıkarılan Bilgi:**\n\n{retrieved_chunks[0]}")
        else:
            st.warning("Lütfen bir soru girin.")