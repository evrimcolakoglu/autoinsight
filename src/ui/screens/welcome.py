"""
AutoInsight — Ana Sayfa (Welcome) Ekranı
Vitrin, hero bölümü, özellik kartları ve istatistik paneli.
"""
import streamlit as st

from src.ui.icons import IC, LOGO_FULL_SVG
from src.ui.components import raw_html, go_to


def render_welcome() -> None:
    """Ana sayfa ekranını render eder."""

    # Live Radar Ticker
    raw_html('''
    <div class="radar-ticker">
        <div class="radar-dot"></div>
        <span>Canlı Piyasa Radarı &middot; 81 İl Analizi &middot; 53.514 Gerçek İlan Aktif</span>
    </div>
    ''')

    # Premium Navbar
    raw_html(f'''
    <div class="nav">
        <div class="nlo">
            {LOGO_FULL_SVG}
        </div>
        <div class="lbg">
            <div class="radar-dot"></div>
            <span>Canlı Piyasa Motoru</span>
        </div>
    </div>
    ''')

    # Hero
    raw_html('''
    <div class="hero">
        <h1 class="hh">Aracınızın Gerçek<br><span class="g">Piyasa Değerini</span> Bilin.</h1>
        <p class="hp">53.000'den fazla güncel piyasa verisini analiz ederek saniyeler içinde hassas değer tahmini, güven aralığı ve emsal piyasa raporu sunar.</p>
    </div>
    ''')

    # Feature Cards (Vitrin Modülleri)
    col1, col2 = st.columns(2, gap="large")

    with col1:
        raw_html(f'''
        <div class="fc">
            <div class="fcl"></div>
            <div>
                <div class="fc-top-row">
                    <div class="fci">
                        {IC["valuation_card"]}
                    </div>
                    <span class="fc-badge">Hızlı Değerleme</span>
                </div>
                <div class="fct">Piyasa Değerleme</div>
                <div class="fcd">Marka, model, yıl, kilometre ve donanım verilerini girin; sistemimiz aracınızın güncel piyasa değer aralığını ve emsal konumunu anında hesaplasın.</div>
            </div>
            <div class="chips">
                <span class="chip">{IC["bolt"]} Anlık Değerleme</span>
                <span class="chip">{IC["target"]} Yüksek Hassasiyet</span>
                <span class="chip">{IC["chart"]} Fiyat Aralığı</span>
                <span class="chip">{IC["search_sm"]} Emsal Analiz</span>
            </div>
        </div>''')
        st.button("Değerleme Başlat →", key="btn_start_valuation", type="primary",
                  use_container_width=True, on_click=go_to, args=("seller",))

    with col2:
        raw_html(f'''
        <div class="fc">
            <div class="fcl"></div>
            <div>
                <div class="fc-top-row">
                    <div class="fci">
                        {IC["discovery_card"]}
                    </div>
                    <span class="fc-badge">Akıllı Filtre</span>
                </div>
                <div class="fct">Akıllı Araç Keşfi</div>
                <div class="fcd">Bütçenizi ve tercihlerinizi belirleyin; akıllı filtreleme algoritmamız kriterlerinize ve bütçenize en uygun araçları piyasa değerleriyle listelesin.</div>
            </div>
            <div class="chips">
                <span class="chip">{IC["sparkles"]} Akıllı Eşleşme</span>
                <span class="chip">{IC["star"]} Kriter Filtresi</span>
                <span class="chip">{IC["wallet"]} Fiyat Analizi</span>
                <span class="chip">{IC["flame"]} Avantajlı Araçlar</span>
            </div>
        </div>''')
        st.button("Araçları Keşfet →", key="btn_start_search", type="primary",
                  use_container_width=True, on_click=go_to, args=("buyer",))

    # Stats Bento Bar
    raw_html('''
    <div class="stats">
        <div class="sc">
            <div class="sn em">%94.0</div>
            <div class="sl">Piyasa Doğruluğu</div>
            <div class="ss">Yüksek Güvenilirlik</div>
        </div>
        <div class="sc">
            <div class="sn">53.514</div>
            <div class="sl">İncelenen İlan</div>
            <div class="ss">Türkiye Geneli Veri</div>
        </div>
        <div class="sc">
            <div class="sn em">&lt;15ms</div>
            <div class="sl">Hesaplama Süresi</div>
            <div class="ss">Anlık Değerleme</div>
        </div>
        <div class="sc">
            <div class="sn">1.100+</div>
            <div class="sl">Araç Modeli</div>
            <div class="ss">Geniş Marka Havuzu</div>
        </div>
    </div>
    <div class="hdiv"></div>
    ''')

    # Neden AutoInsight? (Bento Grid)
    raw_html(f'''
    <div class="shead">
        <div class="slbl">{IC["spark_diamond"]} NEDEN AUTOINSIGHT?</div>
        <div class="stitle">Veriye Dayalı Rasyonel Karar Avantajı</div>
    </div>
    <div class="bento-grid">
        <div class="bento-item">
            <div class="bento-icon-box">{IC["shield_bento"]}</div>
            <div>
                <div class="bento-title">Objektif &amp; Şeffaf Fiyat Aralığı</div>
                <div class="bento-desc">Spekülatif ve değişken fiyatlar yerine, binlerce gerçek ilan verisiyle filtrelenmiş tutarlı bir piyasa değer koridoru elde edin.</div>
            </div>
        </div>
        <div class="bento-item">
            <div class="bento-icon-box">{IC["bolt_bento"]}</div>
            <div>
                <div class="bento-title">Akıllı Fırsat İlan Tespiti</div>
                <div class="bento-desc">Piyasa ortalamasının altında kalan avantajlı araçları anında tespit ederek bütçeniz için en karlı seçeneği bulun.</div>
            </div>
        </div>
        <div class="bento-item">
            <div class="bento-icon-box">{IC["map_bento"]}</div>
            <div>
                <div class="bento-title">Bölgesel ve Donanımsal Esneklik</div>
                <div class="bento-desc">İl bazlı pazar dinamikleri, kasa, vites ve yakıt kombinasyonlarına göre özelleştirilmiş analiz sonuçları.</div>
            </div>
        </div>
        <div class="bento-item">
            <div class="bento-icon-box">{IC["chart_bento"]}</div>
            <div>
                <div class="bento-title">Emsal Pazar Karşılaştırması</div>
                <div class="bento-desc">Aracınızın benzer ilanlar içerisindeki fiyat yüzdeliğini ve piyasadaki rekabet konumunu görsel olarak izleyin.</div>
            </div>
        </div>
    </div>
    <div class="hdiv"></div>
    ''')

    # Nasıl Çalışır? (3 Adım)
    raw_html(f'''
    <div class="shead">
        <div class="slbl">{IC["spark_diamond"]} MİMARİ &amp; SÜREÇ</div>
        <div class="stitle">Üç Adımda Akıllı Değerleme</div>
    </div>
    <div class="hiw">
        <div class="hc">
            <span class="hn-pill">Adım 01</span>
            <div class="hi-box">{IC["step_params"]}</div>
            <div class="ht">Parametreleri Girin</div>
            <div class="hd">Marka, seri, model, yıl, kilometre, yakıt, vites ve kasa bilgilerini dinamik form aracılığıyla aktarın.</div>
        </div>
        <div class="hc">
            <span class="hn-pill">Adım 02</span>
            <div class="hi-box">{IC["step_ai"]}</div>
            <div class="ht">Yapay Zeka Analizi</div>
            <div class="hd">Gelişmiş veri analitiği motorumuz aracın piyasa değerini, güven aralığını ve varyansını anında hesaplar.</div>
        </div>
        <div class="hc">
            <span class="hn-pill">Adım 03</span>
            <div class="hi-box">{IC["step_report"]}</div>
            <div class="ht">Piyasa Raporu</div>
            <div class="hd">Güven aralığı, emsal karşılaştırması ve piyasa yüzdelik konum analiziyle objektif değerleme raporunuzu alın.</div>
        </div>
    </div>

    <div class="trust">
        <div class="ti">{IC["check_disc"]}<span>Gerçek Piyasa Verisi</span></div>
        <div class="ti">{IC["bolt_disc"]}<span>Anlık Hesaplama</span></div>
        <div class="ti">{IC["lock_disc"]}<span>Veri Gizliliği</span></div>
        <div class="ti">{IC["target_disc"]}<span>Yüksek Doğruluk Oranı</span></div>
        <div class="ti">{IC["trend_disc"]}<span>Sürekli Güncellenen Model</span></div>
    </div>

    <div class="footer-wrap">
        <div class="footer-links">
            <span>AutoInsight v2.4</span>
            <span>&bull;</span>
            <span>53.514 Gerçek İlan Analitiği</span>
            <span>&bull;</span>
            <span>Python &amp; Streamlit Platformu</span>
        </div>
        <div>&copy; 2026 AutoInsight — Tüm Hakları Saklıdır.</div>
    </div>
    ''')
