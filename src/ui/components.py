"""
AutoInsight — Paylaşılan UI Yardımcı Fonksiyonlar
format_price, format_km, raw_html ve navigasyon yardımcıları burada tanımlanır.
"""
import streamlit as st


def format_price(value: float) -> str:
    """Fiyatı Türkçe formatında gösterir: 1.234.567 TL"""
    return f"{int(round(value)):,}".replace(",", ".") + " TL"


def format_km(value: float) -> str:
    """Kilometreyi Türkçe formatında gösterir: 12.345 km"""
    return f"{int(round(value)):,}".replace(",", ".") + " km"


def raw_html(html_str: str) -> None:
    """
    Ham HTML içeriğini Streamlit'e güvenli biçimde enjekte eder.
    CommonMark'ın 4-boşluk code block yorumlamasını önlemek için
    her satır başındaki beyaz boşluklar temizlenir.
    """
    cleaned = "\n".join(line.strip() for line in html_str.strip().splitlines())
    st.markdown(cleaned, unsafe_allow_html=True)


def go_to(screen_name: str) -> None:
    """Belirtilen ekrana geçiş yapar."""
    st.session_state.screen = screen_name


def go_home() -> None:
    """Ana sayfaya döner ve mevcut sonuçları temizler."""
    for key in ["seller_result", "buyer_result"]:
        if key in st.session_state:
            del st.session_state[key]
    st.session_state.screen = "welcome"
