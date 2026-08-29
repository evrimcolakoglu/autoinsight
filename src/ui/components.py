"""
AutoInsight — Paylaşılan UI Yardımcı Fonksiyonlar
format_price, format_km, raw_html, get_image_base64 ve navigasyon yardımcıları burada tanımlanır.
"""
import os
import base64
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


@st.cache_data
def get_image_base64(file_path: str) -> str:
    """Yerel görsel dosyasını base64 formatına çevirir (HTML içi hızlı kullanım)."""
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
            ext = os.path.splitext(file_path)[1].lstrip(".").lower()
            mime = "image/jpeg" if ext in ["jpg", "jpeg"] else f"image/{ext}"
            return f"data:{mime};base64,{encoded}"
    return ""


def go_to(screen_name: str) -> None:
    """Belirtilen ekrana geçiş yapar."""
    st.session_state.screen = screen_name


def go_home() -> None:
    """Ana sayfaya döner ve mevcut sonuçları temizler."""
    for key in ["seller_result", "buyer_result"]:
        if key in st.session_state:
            del st.session_state[key]
    st.session_state.screen = "welcome"
