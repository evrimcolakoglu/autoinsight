"""
AutoInsight — Alıcı (Buyer) Ekranı
Akıllı araç keşif formu ve öneri sonuçları.
"""
import pandas as pd
import streamlit as st

from src.config import NUMERIC_FEATURES, CATEGORICAL_FEATURES, MODEL_MAPE
from src.insights.explainer import MarketInsightExplainer
from src.ui.icons import IC, LOGO_FULL_SVG
from src.ui.components import raw_html, format_price, format_km, go_home


def render_buyer(df: pd.DataFrame, pipeline, recommender) -> None:
    """Alıcı / akıllı araç keşfi ekranını render eder."""
    raw_html(f'''
    <div class="nav">
        <div class="nlo">
            {LOGO_FULL_SVG}
        </div>
        <div class="lbg">
            <div class="radar-dot"></div>
            <span>Akıllı Keşif Modülü</span>
        </div>
    </div>
    ''')
    nav_col1, nav_col2 = st.columns([1, 5])
    with nav_col1:
        st.button("← Ana Sayfa", key="buyer_back", on_click=go_home, type="secondary")
    with nav_col2:
        raw_html('<div style="text-align:right;padding-top:.3rem"><span class="lbg">Akıllı Araç Keşfi</span></div>')

    if "buyer_result" in st.session_state:
        _render_buyer_result(st.session_state.buyer_result)
        return

    raw_html('<div class="ph"><h2>Bütçenize En Uygun Araçları Bulun</h2><p>Kriterleri ve tercihlerinizi belirleyin — akıllı benzerlik algoritmamız fiyat/performans açısından en avantajlı ilanları listelesin.</p></div>')

    # ── 1. Bütçe ve Arama Modu ───────────────────────────────
    with st.container(border=True):
        raw_html(f'''
        <div class="form-group-title">
            <span>{IC["hdr_wallet"]} 1. Bütçe ve Arama Yaklaşımı</span>
            <span class="form-step-badge">Fiyat Sınırı</span>
        </div>
        ''')
        col_budget, col_flex = st.columns([2, 1])
        with col_budget:
            budget = st.number_input("Maksimum Bütçe Tutarı (TL)", min_value=0, value=1350000,
                                     step=50000, key="b_budget")
        with col_flex:
            raw_html("<div style='height: 28px;'></div>")
            flexible = st.checkbox("Bütçesiz Esnek Arama (Kriter Odaklı)", key="b_flexible")

    # ── 2. Araç Filtreleri ───────────────────────────────────
    with st.container(border=True):
        raw_html(f'''
        <div class="form-group-title">
            <span>{IC["hdr_filter"]} 2. Donanım Tercihleri ve Filtreler</span>
            <span class="form-step-badge">Araç Filtreleri</span>
        </div>
        ''')
        f_col1, f_col2, f_col3 = st.columns(3)

        with f_col1:
            b_brand_options = ["Tümü"] + sorted(df['marka'].dropna().unique().tolist())
            b_brand = st.selectbox("Marka Tercihi", options=b_brand_options, key="b_brand")
            fuel_options = ["Tümü"] + sorted(df['yakit_tipi'].dropna().unique().tolist())
            b_fuel = st.selectbox("Yakıt Tipi", options=fuel_options, key="b_fuel")

        with f_col2:
            trans_options = ["Tümü"] + sorted(df['vites_tipi'].dropna().unique().tolist())
            b_trans = st.selectbox("Vites Tipi", options=trans_options, key="b_trans")
            body_options = ["Tümü"] + sorted(df['kasa_tipi'].dropna().unique().tolist())
            b_body = st.selectbox("Kasa Tipi", options=body_options, key="b_body")

        with f_col3:
            b_max_km = st.number_input(
                "Maksimum Kilometre Sınırı (Opsiyonel)", min_value=0, value=0,
                step=10000, key="b_max_km",
                help="0 bırakılırsa kilometre sınırı uygulanmaz."
            )
            year_min_options = sorted(df['yil'].dropna().unique().astype(int))
            b_min_year = st.selectbox(
                "En Düşük Model Yılı", options=[None] + year_min_options,
                key="b_min_year", format_func=lambda x: "Fark etmez" if x is None else str(x)
            )

    # ── Validasyon ───────────────────────────────────────────
    optional_filled = sum([
        b_brand != "Tümü",
        b_fuel != "Tümü",
        b_trans != "Tümü",
        b_body != "Tümü",
        b_max_km is not None and b_max_km > 0,
        b_min_year is not None,
    ])

    has_budget = budget is not None and budget > 0
    if flexible:
        can_search = optional_filled >= 2
        hint = "" if can_search else "Esnek bütçeli arama için lütfen en az 2 filtre seçin."
    else:
        can_search = has_budget
        hint = "" if can_search else "Arama yapmak için lütfen bir maksimum bütçe tutarı girin."

    raw_html("<div style='height: 14px;'></div>")
    clicked = st.button("Avantajlı Araçları Keşfet →", key="b_submit", type="primary",
                        use_container_width=True, disabled=not can_search)

    if hint:
        raw_html(f'<div style="text-align:center; color:#00FFB3; font-size:0.88rem; font-weight:600; margin-top:0.6rem;">{hint}</div>')

    if clicked:
        with st.spinner("Piyasa taranıyor ve en avantajlı araçlar puanlanıyor..."):
            recs = recommender.recommend_by_preferences(
                preferred_brand=b_brand if b_brand != "Tümü" else None,
                max_budget=budget if (has_budget and not flexible) else None,
                preferred_fuel=b_fuel if b_fuel != "Tümü" else None,
                preferred_transmission=b_trans if b_trans != "Tümü" else None,
                preferred_kasa=b_body if b_body != "Tümü" else None,
                max_km=b_max_km if b_max_km and b_max_km > 0 else None,
                min_year=b_min_year if b_min_year else None,
                top_n=20,
            )

            if recs.empty:
                st.warning("Kriterlerinize uygun araç bulunamadı. Lütfen filtrelerinizi genişletmeyi deneyin.")
                return

            results = []
            available_num = [c for c in NUMERIC_FEATURES if c in df.columns]
            available_cat = [c for c in CATEGORICAL_FEATURES if c in df.columns]

            for _, row in recs.iterrows():
                market_value = None
                if pipeline is not None:
                    car_full = df[
                        (df['marka'] == row['marka']) &
                        (df['model'] == row['model']) &
                        (df['yil'] == row['yil']) &
                        (df['kilometre'] == row['kilometre'])
                    ]
                    if not car_full.empty:
                        input_row = car_full.iloc[0][available_num + available_cat].to_frame().T
                        try:
                            market_value = float(pipeline.predict(input_row)[0])
                        except Exception:
                            market_value = None

                car_dict = {
                    "marka": row['marka'],
                    "seri": row.get('seri', ''),
                    "model": row['model'],
                    "yil": int(row['yil']),
                    "km": float(row['kilometre']),
                    "vites": row.get('vites_tipi', ''),
                    "yakit": row.get('yakit_tipi', ''),
                    "kasa": row.get('kasa_tipi', ''),
                    "market_value": market_value,
                }

                car_dict["explanation"] = MarketInsightExplainer.generate_buyer_explanation(
                    df=df,
                    car_dict=car_dict,
                    market_value=market_value
                )

                results.append(car_dict)

            st.session_state.buyer_result = results
            st.rerun()


def _render_buyer_result(results: list) -> None:
    """Öneri listesi sonuçlarını araç kartları olarak render eder."""
    res_header_col1, res_header_col2 = st.columns([3, 1])
    with res_header_col1:
        raw_html(f'''
        <div style="margin: 0.5rem 0 1.5rem;">
            <span class="rpill"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#00FFB3" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" style="display:inline-block;vertical-align:-1px;margin-right:4px;"><polyline points="20 6 9 17 4 12"/></svg> Arama Sonuçları</span>
            <h2 style="font-size: 2rem; font-weight: 800; color: #FFFFFF; margin: 0.6rem 0 0;">
                {len(results)} Uygun Araç Eşleşti
            </h2>
        </div>
        ''')
    with res_header_col2:
        st.button("Filtreleri Değiştir", key="br_reset_top", on_click=_clear_buyer_result,
                  type="secondary", use_container_width=True)

    for car in results:
        title = f"{car['marka']} {car['model']} ({car['yil']})"

        market_html = ""
        if car['market_value'] is not None:
            mv_low = car['market_value'] * (1 - MODEL_MAPE)
            mv_high = car['market_value'] * (1 + MODEL_MAPE)
            market_html = f'''
            <div class="vcpr">
            <div class="vcpb">
            <div class="vcpl">TAHMİNİ PİYASA DEĞERİ</div>
            <div class="vcpv em">{format_price(mv_low)} &mdash; {format_price(mv_high)}</div>
            </div>
            </div>
            '''

        # Opsiyonel özellik hücreleri
        kasa_spec = f'<div class="vc-spec"><div class="vc-spec-label">KASA TİPİ</div><div class="vc-spec-value">{car["kasa"]}</div></div>' if car.get("kasa") else ""
        seri_spec = f'<div class="vc-spec"><div class="vc-spec-label">SERİ</div><div class="vc-spec-value">{car["seri"]}</div></div>' if car.get("seri") else ""

        ai_insight_html = ""
        if car.get("explanation"):
            ai_insight_html = f'''
            <div class="ai-buyer-insight">
                <div class="ai-buyer-badge">
                    <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#00FFB3" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/></svg>
                    AI Pazar Değerlendirmesi
                </div>
                <div class="ai-buyer-text">{car["explanation"]}</div>
            </div>
            '''

        card_html = f'''
        <div class="vc">
        <div class="vct">
        <div class="vcti">{title}</div>
        </div>
        <div class="vc-specs">
        <div class="vc-spec"><div class="vc-spec-label">KİLOMETRE</div><div class="vc-spec-value">{format_km(car["km"])}</div></div>
        <div class="vc-spec"><div class="vc-spec-label">MODEL YILI</div><div class="vc-spec-value">{car["yil"]}</div></div>
        <div class="vc-spec"><div class="vc-spec-label">YAKIT</div><div class="vc-spec-value">{car["yakit"]}</div></div>
        <div class="vc-spec"><div class="vc-spec-label">VİTES</div><div class="vc-spec-value">{car["vites"]}</div></div>
        {kasa_spec}
        {seri_spec}
        </div>
        {market_html}
        {ai_insight_html}
        </div>
        '''
        raw_html(card_html)

    raw_html("<div style='height: 18px;'></div>")
    st.button("Yeni Arama Yap", key="br_reset_bottom", on_click=_clear_buyer_result,
              type="primary", use_container_width=True)


def _clear_buyer_result() -> None:
    """Alıcı sonuç verisini session_state'den temizler."""
    if "buyer_result" in st.session_state:
        del st.session_state["buyer_result"]
