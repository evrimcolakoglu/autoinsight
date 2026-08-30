"""
AutoInsight — Ana Sayfa (Welcome) Ekranı
Apple Pro Tasarım Dili & Dinamik Hareketli Otomotiv Kokpit Mimarisi.
"""
import os
import streamlit as st

from src.ui.icons import IC, LOGO_FULL_SVG
from src.ui.components import raw_html, go_to, get_image_base64


def render_welcome() -> None:
    """Apple Pro sinematik, hareketli ve dinamik ana sayfa ekranını render eder."""

    hero_img_src = get_image_base64("assets/valuation_lab_hero.jpg")
    cockpit_img_src = get_image_base64("assets/market_intelligence_hub.jpg")

    # ─────────────────────────────────────────────
    # 1. Live Radar & Navbar
    # ─────────────────────────────────────────────
    raw_html('''
    <div class="radar-ticker ap-reveal">
        <div class="radar-dot"></div>
        <span>Canlı Piyasa Radarı &middot; 81 İl Analizi &middot; 53.514 Gerçek İlan Aktif</span>
    </div>
    ''')

    raw_html(f'''
    <div class="nav ap-reveal">
        <div class="nlo">
            {LOGO_FULL_SVG}
        </div>
        <div class="lbg">
            <div class="radar-dot"></div>
            <span>Canlı Piyasa Motoru</span>
        </div>
    </div>
    ''')

    # ─────────────────────────────────────────────
    # 2. Apple Pro Sinematik Hero Başlığı
    # ─────────────────────────────────────────────
    raw_html(f'''
    <div class="hero ap-reveal" style="padding-top: 1.8rem; padding-bottom: 1.2rem;">
        <div class="ap-eyebrow">
            {IC["spark_diamond"]} YAPAY ZEKA &amp; OTOMOTİV TELEMETRİSİ
        </div>
        <h1 class="ap-super-headline">
            <span class="ap-titanium-text">Otomotiv Zekâsının.</span><br>
            <span class="ap-emerald-text">En İleri Seviyesi.</span>
        </h1>
        <p class="ap-hero-sub">
            53.000'den fazla güncel pazar verisi, anlık varyans analizleri ve makine öğrenmesi boru hattıyla aracınızın gerçek piyasa değerini ve en avantajlı fırsatları saniyeler içinde keşfedin.
        </p>
    </div>
    ''')

    # ─────────────────────────────────────────────
    # 3. Dinamik Sinematik Araç Sahnesi (Canlı HUD & Lazer)
    # ─────────────────────────────────────────────
    if hero_img_src:
        raw_html(f'''
        <div class="ap-cinema-stage ap-reveal">
            <div class="ap-laser-scanner"></div>
            <div class="ap-cinema-img-wrap">
                <img src="{hero_img_src}" alt="AutoInsight Yapay Zeka Araç Değerleme Laboratuvarı" class="ap-cinema-img" />
                <div class="ap-cinema-overlay">
                    <div style="font-family: var(--fd); font-size: 1.6rem; font-weight: 800; color: #FFFFFF; letter-spacing: -0.02em;">
                        Yapay Zeka Destekli Hassas Değerleme Laboratuvarı
                    </div>
                    <div style="font-size: 0.94rem; color: #CBD5E1; margin-top: 0.35rem; max-width: 680px;">
                        Gelişmiş Random Forest algoritmamız; kilometre amortismanı, pazar talebi ve emsal fiyat varyasyonlarını anlık olarak tarar.
                    </div>
                    <div class="ap-telemetry-hud-float">
                        <div class="ap-hud-stat-chip">
                            <span class="lbl">Hesaplama Motoru:</span>
                            <span class="val">&lt;15ms</span>
                        </div>
                        <div class="ap-hud-stat-chip">
                            <span class="lbl">Pazar Doğruluğu:</span>
                            <span class="val">%94.0 R²</span>
                        </div>
                        <div class="ap-hud-stat-chip">
                            <span class="lbl">Hata Payı:</span>
                            <span class="val">%11.09 MAPE</span>
                        </div>
                        <div class="ap-hud-stat-chip">
                            <span class="lbl">Durum:</span>
                            <span class="val">AKTİF PİYASA RADARI</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        ''')

    # ─────────────────────────────────────────────
    # 4. Apple Pro Showcase Kartları (Vitrin Modülleri)
    # ─────────────────────────────────────────────
    col1, col2 = st.columns(2, gap="large")

    with col1:
        raw_html(f'''
        <div class="ap-showcase-card ap-reveal ap-delay-1">
            <div>
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1.2rem;">
                    <div class="fci">
                        {IC["valuation_card"]}
                    </div>
                    <span class="ap-card-tag">Hızlı Değerleme</span>
                </div>
                <div class="ap-card-title">Piyasa Değerleme</div>
                <div class="ap-card-desc">
                    Marka, model, yıl, kilometre ve donanım parametrelerini girin; yapay zeka modelimiz aracınızın piyasa değer koridorunu, güven aralığını ve emsal rekabet konumunu anında hesaplasın.
                </div>
            </div>
            <div class="chips" style="margin-bottom: 0.5rem;">
                <span class="chip">{IC["bolt"]} Anlık Değerleme</span>
                <span class="chip">{IC["target"]} %94 Doğruluk</span>
                <span class="chip">{IC["chart"]} Fiyat Koridoru</span>
                <span class="chip">{IC["search_sm"]} Emsal Analizi</span>
            </div>
        </div>''')
        st.button("Değerleme Başlat →", key="btn_start_valuation", type="primary",
                  use_container_width=True, on_click=go_to, args=("seller",))

    with col2:
        raw_html(f'''
        <div class="ap-showcase-card ap-reveal ap-delay-2">
            <div>
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1.2rem;">
                    <div class="fci">
                        {IC["discovery_card"]}
                    </div>
                    <span class="ap-card-tag">Akıllı Keşif</span>
                </div>
                <div class="ap-card-title">Akıllı Araç Keşfi</div>
                <div class="ap-card-desc">
                    Bütçenizi veya donanım tercihlerinizi belirleyin; bütçe-ağırlıklı akıllı algoritma kriterlerinize en uygun fırsat ilanlarını 3-4 cümlelik yapay zeka pazar gerekçeleriyle listelesin.
                </div>
            </div>
            <div class="chips" style="margin-bottom: 0.5rem;">
                <span class="chip">{IC["sparkles"]} Akıllı Eşleşme</span>
                <span class="chip">{IC["star"]} Bütçe Optimizasyonu</span>
                <span class="chip">{IC["wallet"]} Esnek Arama</span>
                <span class="chip">{IC["flame"]} AI Pazar Gerekçesi</span>
            </div>
        </div>''')
        st.button("Araçları Keşfet →", key="btn_start_search", type="primary",
                  use_container_width=True, on_click=go_to, args=("buyer",))

    # ─────────────────────────────────────────────
    # 5. Apple Pro Telemetri & İstatistik Barı
    # ─────────────────────────────────────────────
    raw_html('''
    <div class="ap-metrics-bar ap-reveal">
        <div class="ap-metric-box">
            <div class="ap-metric-val glow">%94.0</div>
            <div class="ap-metric-label">R² Pazar Doğruluğu</div>
            <div class="ap-metric-sub">Yüksek Varyans Açıklama</div>
        </div>
        <div class="ap-metric-box">
            <div class="ap-metric-val">53.514</div>
            <div class="ap-metric-label">İncelenen İlan</div>
            <div class="ap-metric-sub">Türkiye Geneli Canlı Veri</div>
        </div>
        <div class="ap-metric-box">
            <div class="ap-metric-val glow">&lt;15ms</div>
            <div class="ap-metric-label">Hesaplama Hızı</div>
            <div class="ap-metric-sub">Anlık Yerel Çıkarım</div>
        </div>
        <div class="ap-metric-box">
            <div class="ap-metric-val">46 Marka</div>
            <div class="ap-metric-label">1.100+ Model</div>
            <div class="ap-metric-sub">Geniş Segment Havuzu</div>
        </div>
    </div>
    ''')

    # ─────────────────────────────────────────────
    # 6. Canlı Kokpit & Akıllı Telemetri Merkezi
    # ─────────────────────────────────────────────
    if cockpit_img_src:
        raw_html(f'''
        <div class="ap-cockpit-grid ap-reveal">
            <div class="ap-cockpit-frame">
                <img src="{cockpit_img_src}" alt="AutoInsight Otomotiv Pazar İstihbarat Merkezi" />
            </div>
            <div class="ap-cockpit-details">
                <div class="ap-eyebrow" style="margin-bottom:0.2rem;">
                    {IC["spark_diamond"]} PAZAR İSTİHBARAT MERKEZİ
                </div>
                <div style="font-family: var(--fd); font-size: 1.8rem; font-weight: 800; color: #FFFFFF; letter-spacing: -0.03em;">
                    Canlı Pazar Hacmi &amp; İkinci El Fiyat Dağılımları
                </div>
                <div style="font-size: 0.94rem; line-height: 1.65; color: #94A3B8;">
                    53.514 gerçek ilan verisiyle beslenen yapay zeka analiz merkezimiz, 81 ildeki bölgesel fiyat dalgalanmalarını ve segment fırsatlarını anlık olarak haritalandırır.
                </div>
                <div style="display: flex; flex-direction: column; gap: 0.65rem; margin-top: 0.4rem;">
                    <div class="ap-live-telemetry-row">
                        <div class="k"><div class="radar-dot"></div><span>İstanbul İkinci El Pazar Hacmi</span></div>
                        <div class="v">18.420 İlan</div>
                    </div>
                    <div class="ap-live-telemetry-row">
                        <div class="k"><div class="radar-dot"></div><span>Ankara &amp; İzmir Pazar Dağılımı</span></div>
                        <div class="v">14.150 İlan</div>
                    </div>
                    <div class="ap-live-telemetry-row">
                        <div class="k"><div class="radar-dot"></div><span>Çıkarım Modeli &amp; RAG</span></div>
                        <div class="v">Lokal / Çevrimdışı</div>
                    </div>
                </div>
            </div>
        </div>
        ''')

    # ─────────────────────────────────────────────
    # 7. Apple Pro Deep-Dive Bento Grid
    # ─────────────────────────────────────────────
    raw_html(f'''
    <div class="ap-bento-section ap-reveal">
        <div class="ap-section-header">
            <div class="ap-eyebrow">{IC["spark_diamond"]} MÜHENDİSLİK &amp; MİMARİ</div>
            <div class="ap-section-title">Veriye Dayalı Rasyonel Karar Avantajı</div>
        </div>
        <div class="ap-bento-grid-4">
            <div class="ap-bento-cell ap-reveal ap-delay-1">
                <div class="ap-bento-icon">{IC["shield_bento"]}</div>
                <div>
                    <div class="ap-bento-head">Random Forest Regresyon Modeli</div>
                    <div class="ap-bento-para">Spekülatif ve değişken fiyatlar yerine, binlerce gerçek ilan verisiyle eğitilmiş Target Encoding ve Random Forest boru hattı sayesinde objektif bir değer koridoru elde edin.</div>
                </div>
            </div>
            <div class="ap-bento-cell ap-reveal ap-delay-2">
                <div class="ap-bento-icon">{IC["bolt_bento"]}</div>
                <div>
                    <div class="ap-bento-head">Bütçe-Ağırlıklı Akıllı Eşleştirme</div>
                    <div class="ap-bento-para">Bütçenizi atıl bırakmayan, bütçe sınırına en yakın ve en avantajlı araçları kilometre, yıl ve donanım skorlamasıyla öne çıkaran akıllı keşif motoru.</div>
                </div>
            </div>
            <div class="ap-bento-cell ap-reveal ap-delay-3">
                <div class="ap-bento-icon">{IC["map_bento"]}</div>
                <div>
                    <div class="ap-bento-head">81 İl Bölgesel Pazar Dinamikleri</div>
                    <div class="ap-bento-para">İl bazlı pazar talebi, karoser formu, yakıt ve vites kombinasyonlarının yarattığı bölgesel fiyat değişimlerini hassas şekilde hesaba katan derinlikli mimari.</div>
                </div>
            </div>
            <div class="ap-bento-cell ap-reveal ap-delay-4">
                <div class="ap-bento-icon">{IC["chart_bento"]}</div>
                <div>
                    <div class="ap-bento-head">Yerel Yapay Zeka Pazar İçgörüsü</div>
                    <div class="ap-bento-para">Her araç için fiyat seviyesinin nedenlerini (düşük km avantajı, pazar talebi, segment konumu) açıklayan 3-4 cümlelik yerel ve güvenilir doğal dil sentezi.</div>
                </div>
            </div>
        </div>
    </div>
    ''')

    # ─────────────────────────────────────────────
    # 8. Nasıl Çalışır? (3 Aşamalı Pro Timeline)
    # ─────────────────────────────────────────────
    raw_html(f'''
    <div class="ap-bento-section ap-reveal">
        <div class="ap-section-header">
            <div class="ap-eyebrow">{IC["spark_diamond"]} İŞLEM AKIŞI</div>
            <div class="ap-section-title">Üç Adımda Akıllı Değerleme</div>
        </div>
        <div class="ap-timeline-grid">
            <div class="ap-step-card ap-reveal ap-delay-1">
                <span class="ap-step-num">Adım 01</span>
                <div class="hi-box">{IC["step_params"]}</div>
                <div class="ht">Parametreleri Belirleyin</div>
                <div class="hd">Marka, seri, model, yıl, kilometre, yakıt, vites ve kasa bilgilerini dinamik akıllı form üzerinden aktarın.</div>
            </div>
            <div class="ap-step-card ap-reveal ap-delay-2">
                <span class="ap-step-num">Adım 02</span>
                <div class="hi-box">{IC["step_ai"]}</div>
                <div class="ht">Yapay Zeka Telemetrisi</div>
                <div class="hd">Gelişmiş analitik motorumuz aracın piyasa değerini, %11.09 MAPE güven aralığını ve emsal pazar konumunu anında hesaplar.</div>
            </div>
            <div class="ap-step-card ap-reveal ap-delay-3">
                <span class="ap-step-num">Adım 03</span>
                <div class="hi-box">{IC["step_report"]}</div>
                <div class="ht">Gerekçeli Piyasa Raporu</div>
                <div class="hd">Güven koridoru, emsal ilan yüzdelik konumu ve 3-4 cümlelik yapay zeka pazar analiziyle objektif değerleme raporunuzu alın.</div>
            </div>
        </div>
    </div>
    ''')

    # ─────────────────────────────────────────────
    # 9. Güven & Güvenlik Rozetleri + Footer
    # ─────────────────────────────────────────────
    raw_html(f'''
    <div class="trust ap-reveal">
        <div class="ti">{IC["check_disc"]}<span>Gerçek Piyasa Verisi</span></div>
        <div class="ti">{IC["bolt_disc"]}<span>Yerel &amp; Ücretsiz Çıkarım</span></div>
        <div class="ti">{IC["lock_disc"]}<span>Sıfır Veri Sızıntısı</span></div>
        <div class="ti">{IC["target_disc"]}<span>Yüksek Doğruluk Oranı</span></div>
        <div class="ti">{IC["trend_disc"]}<span>Sürekli Güncellenen Model</span></div>
    </div>

    <div class="footer-wrap ap-reveal">
        <div class="footer-links">
            <span>AutoInsight v2.5</span>
            <span>&bull;</span>
            <span>53.514 Gerçek İlan Analitiği</span>
            <span>&bull;</span>
            <span>Dinamik Scrollytelling Mimarisi</span>
        </div>
        <div>&copy; 2026 AutoInsight — Tüm Hakları Saklıdır.</div>
    </div>
    ''')
