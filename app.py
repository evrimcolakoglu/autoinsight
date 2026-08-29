"""
AutoInsight — Akıllı Otomotiv Karar Platformu
Ana Giriş ve Router Modülü (Streamlit Entrypoint)
"""
import streamlit as st

from src.config import DATA_RAW_PATH
from src.recommender.engine import VehicleRecommender
from src.ui.styles import inject_premium_autoinsight_css
from src.ui.components import raw_html
from src.ui.data_loader import load_app_data, load_app_model
from src.ui.screens.welcome import render_welcome
from src.ui.screens.seller import render_seller
from src.ui.screens.buyer import render_buyer

# ─────────────────────────────────────────────
# 1. Sayfa Yapılandırması
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="AutoInsight — Akıllı Otomotiv Karar Platformu",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────
# 2. Tema & Görsel Katmanlar
# ─────────────────────────────────────────────
inject_premium_autoinsight_css()
raw_html(
    '<div id="ai-bg">'
    '<div class="gbg"></div>'
    '<div class="orb o1"></div>'
    '<div class="orb o2"></div>'
    '<div class="orb o3"></div>'
    '<div class="orb o4"></div>'
    '</div>'
)

# ─────────────────────────────────────────────
# 3. Kaynakların Yüklenmesi
# ─────────────────────────────────────────────
df = load_app_data()
pipeline = load_app_model()
recommender = VehicleRecommender(DATA_RAW_PATH)

# ─────────────────────────────────────────────
# 4. Navigasyon & Router
# ─────────────────────────────────────────────
if "screen" not in st.session_state:
    st.session_state.screen = "welcome"

screen = st.session_state.screen

if screen == "welcome":
    render_welcome()
elif screen == "seller":
    render_seller(df, pipeline, recommender)
elif screen == "buyer":
    render_buyer(df, pipeline, recommender)
else:
    st.session_state.screen = "welcome"
    st.rerun()
