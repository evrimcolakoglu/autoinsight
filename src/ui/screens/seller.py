"""
AutoInsight — Satıcı (Seller) Ekranı
Araç değerleme formu ve sonuç raporu.
"""
import pandas as pd
import streamlit as st

from src.config import MODEL_MAPE
from src.ui.icons import IC, LOGO_FULL_SVG
from src.ui.components import raw_html, format_price, go_to, go_home


def render_seller(df: pd.DataFrame, pipeline, recommender) -> None:
    """Satıcı / araç değerleme ekranını render eder."""
    raw_html(f'''
    <div class="nav">
        <div class="nlo">
            {LOGO_FULL_SVG}
        </div>
        <div class="lbg">
            <div class="radar-dot"></div>
            <span>Piyasa Değerleme Modülü</span>
        </div>
    </div>
    ''')
    nav_col1, nav_col2 = st.columns([1, 5])
    with nav_col1:
        st.button("← Ana Sayfa", key="seller_back", on_click=go_home, type="secondary")
    with nav_col2:
        raw_html('<div style="text-align:right;padding-top:.3rem"><span class="lbg">Piyasa Değerleme</span></div>')

    if "seller_result" in st.session_state:
        _render_seller_result(st.session_state.seller_result, recommender)
        return

    raw_html('<div class="ph"><h2>Aracınızın Piyasa Değerini Hesaplayın</h2><p>Araç bilgilerinizi girin — 53.000+ güncel piyasa verisiyle sistemimiz anlık değer aralığını saniyeler içinde hesaplasın.</p></div>')

    # ── Araç Bilgileri Formu ──────────────────────────────────
    with st.container(border=True):
        raw_html(f'''
        <div class="form-group-title">
            <span>{IC["hdr_car"]} 1. Temel Araç Bilgileri</span>
            <span class="form-step-badge">Zorunlu Alanlar</span>
        </div>
        ''')

        # 1. Satır: Marka → Seri → Model
        col1, col2, col3 = st.columns(3)
        with col1:
            brand_list = sorted(df['marka'].dropna().unique().tolist())
            brand = st.selectbox("Marka", options=["Seçiniz..."] + brand_list, index=0, key="s_brand")
            selected_brand = brand if brand != "Seçiniz..." else None

        with col2:
            if selected_brand:
                series_list = sorted(df[df['marka'] == selected_brand]['seri'].dropna().unique().tolist())
                series = st.selectbox("Seri", options=["Seçiniz..."] + series_list, index=0,
                                      key=f"s_series_{selected_brand}")
                selected_series = series if series != "Seçiniz..." else None
            else:
                st.selectbox("Seri", options=["Önce marka seçiniz"], disabled=True, key="s_series_disabled")
                selected_series = None

        with col3:
            if selected_brand and selected_series:
                model_list = sorted(
                    df[(df['marka'] == selected_brand) & (df['seri'] == selected_series)]['model']
                    .dropna().unique().tolist()
                )
                model_name = st.selectbox("Model", options=["Seçiniz..."] + model_list, index=0,
                                          key=f"s_model_{selected_brand}_{selected_series}")
                selected_model = model_name if model_name != "Seçiniz..." else None
            else:
                st.selectbox("Model", options=["Önce marka ve seri seçiniz"], disabled=True,
                             key="s_model_disabled")
                selected_model = None

        # Seçilen araca göre filtrelenmiş alt veri havuzu
        sub_df = df.copy()
        if selected_brand:
            sub_df = sub_df[sub_df['marka'] == selected_brand]
        if selected_series:
            sub_df = sub_df[sub_df['seri'] == selected_series]
        if selected_model:
            sub_df = sub_df[sub_df['model'] == selected_model]

    # ── Donanım ve Teknik Bilgiler ────────────────────────────
    with st.container(border=True):
        raw_html(f'''
        <div class="form-group-title">
            <span>{IC["hdr_gear"]} 2. Donanım, Kilometre ve Konum</span>
            <span class="form-step-badge">Teknik Parametreler</span>
        </div>
        ''')

        r2_col1, r2_col2, r2_col3 = st.columns(3)
        with r2_col1:
            available_years = sorted(sub_df['yil'].dropna().unique().astype(int).tolist(), reverse=True)
            if not available_years:
                available_years = sorted(df['yil'].dropna().unique().astype(int).tolist(), reverse=True)
            year = st.selectbox("Model Yılı", options=available_years, key="s_year")

        with r2_col2:
            km = st.number_input("Kilometre", min_value=0, max_value=1_000_000, value=85000,
                                 step=5000, key="s_km")

        with r2_col3:
            available_bodies = sorted(sub_df['kasa_tipi'].dropna().unique().tolist())
            if not available_bodies:
                available_bodies = sorted(df['kasa_tipi'].dropna().unique().tolist())
            body = st.selectbox("Kasa Tipi", options=["Seçiniz..."] + available_bodies, key="s_body")
            selected_body = body if body != "Seçiniz..." else None

        r3_col1, r3_col2, r3_col3 = st.columns(3)
        with r3_col1:
            available_fuels = sorted(sub_df['yakit_tipi'].dropna().unique().tolist())
            if not available_fuels:
                available_fuels = sorted(df['yakit_tipi'].dropna().unique().tolist())
            fuel = st.selectbox("Yakıt Tipi", options=["Seçiniz..."] + available_fuels, key="s_fuel")
            selected_fuel = fuel if fuel != "Seçiniz..." else None

        with r3_col2:
            available_trans = sorted(sub_df['vites_tipi'].dropna().unique().tolist())
            if not available_trans:
                available_trans = sorted(df['vites_tipi'].dropna().unique().tolist())
            transmission = st.selectbox("Vites Tipi", options=["Seçiniz..."] + available_trans, key="s_trans")
            selected_trans = transmission if transmission != "Seçiniz..." else None

        with r3_col3:
            city_options = ["Tüm Türkiye (Genel)"] + sorted(df['konum'].dropna().unique().tolist())
            city = st.selectbox("Konum (İl) — Opsiyonel", options=city_options, key="s_city")

    # ── Validasyon ve Submit ──────────────────────────────────
    required_ok = all([
        selected_brand is not None,
        selected_series is not None,
        selected_model is not None,
        year is not None,
        km is not None and km >= 0,
        selected_fuel is not None,
        selected_trans is not None,
        selected_body is not None,
    ])

    raw_html("<div style='height: 14px;'></div>")
    clicked = st.button("Piyasa Değerini Hesapla →", key="s_submit", type="primary",
                        use_container_width=True, disabled=not required_ok)

    if clicked:
        if pipeline is None:
            st.error("Eğitilmiş model dosyası bulunamadı. Lütfen önce model eğitimini çalıştırın.")
            return

        with st.spinner("Piyasa varyansı ve emsal veriler analiz ediliyor..."):
            chosen_city = city if (city and city != "Tüm Türkiye (Genel)") \
                else (df['konum'].mode().iloc[0] if not df['konum'].mode().empty else "missing")

            input_data = pd.DataFrame([{
                "marka": selected_brand,
                "seri": selected_series,
                "model": selected_model,
                "konum": chosen_city,
                "yil": int(year),
                "kilometre": float(km),
                "yakit_tipi": selected_fuel,
                "vites_tipi": selected_trans,
                "kasa_tipi": selected_body,
            }])

            predicted = float(pipeline.predict(input_data)[0])

            st.session_state.seller_result = {
                "predicted": predicted,
                "price_low": predicted * (1 - MODEL_MAPE),
                "price_high": predicted * (1 + MODEL_MAPE),
                "comparison": recommender.find_comparable_listings(
                    marka=selected_brand,
                    model=selected_model,
                    yil=int(year),
                    km=float(km),
                    predicted_price=predicted,
                ),
                "brand": selected_brand,
                "model": selected_model,
                "year": year,
            }
            st.rerun()


def _render_seller_result(result: dict, recommender) -> None:
    """Hesaplama sonucunu / değerleme raporunu render eder."""
    raw_html(f'''
    <div style="margin-top: 0.5rem;">
        <span class="rpill"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#00FFB3" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" style="display:inline-block;vertical-align:-1px;margin-right:4px;"><polyline points="20 6 9 17 4 12"/></svg> Değerleme Raporu</span>
        <h2 style="font-size: 2.1rem; font-weight: 800; color: #FFFFFF; margin: 0.6rem 0 0.5rem;">
            {result["brand"]} {result["model"]} ({result["year"]})
        </h2>
    </div>
    ''')

    # Digital Cockpit HUD
    raw_html(f'''
    <div class="phud">
        <div class="phey">Tahmini Piyasa Değer Aralığı</div>
        <div class="prange">
            <div class="pval">{format_price(result["price_low"])}</div>
            <div class="pdash">&mdash;</div>
            <div class="pval">{format_price(result["price_high"])}</div>
        </div>
        <div class="hud-visual-bar">
            <div class="hud-track">
                <div class="hud-fill"></div>
            </div>
            <div class="hud-markers">
                <span>Düşük Fiyat Koridoru</span>
                <span style="color:#00FFB3;font-weight:700;">Ortanca Değer</span>
                <span>Yüksek Fiyat Koridoru</span>
            </div>
        </div>
        <div class="pmeta">Tahmini Piyasa Fiyat Aralığı &nbsp;&middot;&nbsp; Tahmini Ortanca Değer: <span class="pt">{format_price(result["predicted"])}</span></div>
    </div>
    ''')

    comp = result["comparison"]
    if comp["sufficient"]:
        percentile_val = int(round(comp["percentile"]))
        raw_html(f'''
        <div class="mkt">
            <div class="mkth">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#00FFB3" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>
                <span>Piyasa Emsal İlan Karşılaştırması</span>
            </div>
            <div class="mktr">
                <span class="mktk">Eşleşen Emsal İlan Sayısı</span>
                <span class="mktv">{comp["count"]} Adet İlan</span>
            </div>
            <div class="mktr">
                <span class="mktk">Pazardaki Benzer Araçların Ortalama Fiyatı</span>
                <span class="mktv">{format_price(comp["avg_price"])}</span>
            </div>
            <div class="mktr">
                <span class="mktk">Piyasa Yüzdelik Konumu</span>
                <span class="mktv">Benzer ilanların %{percentile_val} diliminden yüksek</span>
            </div>
            <div class="mkti">
                <strong>Piyasa Özeti:</strong> {comp["comment"]}
            </div>
        </div>
        ''')
    else:
        st.info(f"Emsal karşılaştırması için yeterli hacim bulunamadı (Bulunan: {comp['count']} ilan, minimum 10 gereklidir).")

    raw_html("<div style='height: 18px;'></div>")
    res_col1, res_col2 = st.columns([1, 1])
    with res_col1:
        st.button("Yeni Bir Araç Değerle", key="sr_reset", on_click=_clear_seller_result,
                  type="primary", use_container_width=True)
    with res_col2:
        st.button("İlanları Keşfet (Alıcı Ekranı) →", key="sr_to_buyer",
                  on_click=go_to, args=("buyer",), type="secondary", use_container_width=True)


def _clear_seller_result() -> None:
    """Satıcı sonuç verisini session_state'den temizler."""
    if "seller_result" in st.session_state:
        del st.session_state["seller_result"]
