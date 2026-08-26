import os
import joblib
import pandas as pd
import numpy as np
import streamlit as st

from src.config import (
    DATA_RAW_PATH, MODEL_SAVE_PATH,
    NUMERIC_FEATURES, CATEGORICAL_FEATURES,
    MODEL_MAPE
)
from src.recommender.engine import VehicleRecommender

# ─────────────────────────────────────────────
# Sayfa Yapılandırması
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="AutoInsight — Akıllı Otomotiv Karar Platformu",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────
# Vektörel SVG İkonlar
# ─────────────────────────────────────────────
ICON_CAR_PULSE = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#C77D1F" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9C18.7 10.6 16 10 16 10s-1.3-1.4-2.2-2.3c-.5-.4-1.1-.7-1.8-.7H5c-.6 0-1.1.4-1.4.9l-1.4 2.9A3.7 3.7 0 0 0 1 14v2c0 .6.4 1 1 1h2"/><circle cx="7" cy="17" r="2"/><path d="M9 17h6"/><circle cx="17" cy="17" r="2"/></svg>'
ICON_VALUATION = '<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#C77D1F" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M16 8h-6a2 2 0 1 0 0 4h4a2 2 0 1 1 0 4H8"/><path d="M12 18V6"/></svg>'
ICON_SEARCH = '<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#C77D1F" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>'
ICON_CHART = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#C77D1F" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/></svg>'
ICON_CHECK = '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>'

# ─────────────────────────────────────────────
# Yardımcı Fonksiyonlar
# ─────────────────────────────────────────────
def format_price(value: float) -> str:
    return f"{int(round(value)):,}".replace(",", ".") + " TL"

def format_km(value: float) -> str:
    return f"{int(round(value)):,}".replace(",", ".") + " km"

# ─────────────────────────────────────────────
# Apple / Modern Tasarım Tipografi ve Stil CSS'i
# ─────────────────────────────────────────────
def inject_premium_apple_css():
    st.html("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');

    :root {
        --c-ana: #1A1F26;
        --c-ikincil: #4B5563;
        --c-muted: #6B7280;
        --c-vurgu: #C77D1F;
        --c-vurgu-hover: #AA6512;
        --c-vurgu-soft: rgba(199, 125, 31, 0.10);
        --c-vurgu-border: rgba(199, 125, 31, 0.32);
        --c-zemin: #F5F2EC;
        --c-kart: #FFFFFF;
        --c-kart-trans: rgba(255, 255, 255, 0.90);
        --c-border: #E2DDD5;
        --c-border-subtle: rgba(226, 221, 213, 0.85);
        --font-main: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        --font-display: 'Space Grotesk', 'Plus Jakarta Sans', sans-serif;
        --shadow-soft: 0 4px 20px rgba(26, 31, 38, 0.04);
        --shadow-hover: 0 12px 32px rgba(26, 31, 38, 0.08);
        --shadow-glow: 0 0 24px rgba(199, 125, 31, 0.16);
    }

    #MainMenu, footer, header { visibility: hidden !important; }
    [data-testid="stSidebar"] { display: none !important; }
    
    html, body, [class*="css"] {
        font-family: var(--font-main) !important;
    }

    .stApp {
        background-color: var(--c-zemin) !important;
        font-family: var(--font-main) !important;
        color: var(--c-ana) !important;
    }

    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 5rem !important;
        max-width: 1120px !important;
        position: relative;
        z-index: 2;
    }

    /* Ambient Arka Plan */
    .apple-ambient-canvas {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: 0;
        pointer-events: none;
        background: 
            radial-gradient(circle at 8% 12%, rgba(199, 125, 31, 0.11) 0%, transparent 40%),
            radial-gradient(circle at 92% 18%, rgba(75, 85, 99, 0.07) 0%, transparent 45%),
            radial-gradient(circle at 50% 50%, rgba(199, 125, 31, 0.05) 0%, transparent 50%),
            radial-gradient(circle at 12% 88%, rgba(26, 31, 38, 0.04) 0%, transparent 45%),
            radial-gradient(circle at 88% 92%, rgba(199, 125, 31, 0.09) 0%, transparent 40%);
        background-attachment: fixed;
    }

    .apple-grid-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: 1;
        pointer-events: none;
        background-image: radial-gradient(rgba(75, 85, 99, 0.11) 1px, transparent 1px);
        background-size: 28px 28px;
        opacity: 0.55;
    }

    /* Rozetler */
    .brand-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.6rem;
        background: var(--c-kart-trans);
        backdrop-filter: blur(16px);
        border: 1px solid var(--c-border);
        border-radius: 100px;
        padding: 0.45rem 1.1rem;
        font-size: 0.82rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: var(--c-ikincil);
        box-shadow: var(--shadow-soft);
    }

    .screen-tag-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.35rem 0.9rem;
        background: var(--c-vurgu-soft);
        border: 1px solid var(--c-vurgu-border);
        border-radius: 100px;
        color: var(--c-vurgu);
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    /* Hero */
    .hero-wrap {
        text-align: center;
        padding: 2.2rem 1rem 2.5rem;
    }

    .hero-title-text {
        font-family: var(--font-main);
        font-size: clamp(2.4rem, 5vw, 3.6rem);
        font-weight: 800;
        letter-spacing: -0.035em;
        line-height: 1.15;
        color: var(--c-ana);
        margin-bottom: 1.1rem;
    }

    .hero-title-text .accent-gold {
        color: var(--c-vurgu);
        background: linear-gradient(135deg, #C77D1F 0%, #E69D35 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-lead-desc {
        font-size: 1.12rem;
        line-height: 1.65;
        color: var(--c-ikincil);
        max-width: 620px;
        margin: 0 auto 1.5rem;
    }

    /* Bento Kartları */
    .bento-action-card {
        background: var(--c-kart-trans);
        backdrop-filter: blur(20px);
        border: 1px solid var(--c-border);
        border-radius: 24px;
        padding: 2.2rem 2rem 1.6rem;
        box-shadow: var(--shadow-soft);
        transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
        position: relative;
        min-height: 250px;
        margin-bottom: 0.8rem;
    }

    .bento-action-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-hover), var(--shadow-glow);
        border-color: var(--c-vurgu-border);
    }

    .card-icon-box {
        width: 56px;
        height: 56px;
        border-radius: 16px;
        background: var(--c-vurgu-soft);
        border: 1px solid var(--c-vurgu-border);
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 1.2rem;
    }

    .card-heading {
        font-size: 1.35rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin-bottom: 0.5rem;
        color: var(--c-ana);
    }

    .card-body-text {
        font-size: 0.92rem;
        line-height: 1.55;
        color: var(--c-ikincil);
    }

    /* Bento Stats */
    .bento-stats-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin: 2.6rem 0 3rem;
    }

    @media (max-width: 768px) {
        .bento-stats-grid { grid-template-columns: repeat(2, 1fr); }
    }

    .stat-tile {
        background: var(--c-kart-trans);
        backdrop-filter: blur(16px);
        border: 1px solid var(--c-border-subtle);
        border-radius: 18px;
        padding: 1.4rem 1.2rem;
        text-align: center;
        box-shadow: var(--shadow-soft);
        transition: transform 0.3s ease;
    }

    .stat-tile:hover {
        transform: translateY(-2px);
    }

    .stat-big-num {
        font-family: var(--font-display);
        font-size: 2.1rem;
        font-weight: 700;
        color: var(--c-vurgu);
        line-height: 1.1;
        margin-bottom: 0.3rem;
    }

    .stat-label-text {
        font-size: 0.78rem;
        font-weight: 600;
        color: var(--c-ikincil);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* 3 Adım Akış Kartları */
    .section-tag {
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: var(--c-vurgu);
        margin-bottom: 0.4rem;
        display: block;
    }

    .section-headline {
        font-size: 1.75rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        margin-bottom: 1.4rem;
        color: var(--c-ana);
    }

    .feature-step-card {
        background: var(--c-kart-trans);
        backdrop-filter: blur(16px);
        border: 1px solid var(--c-border-subtle);
        border-radius: 20px;
        padding: 1.6rem 1.4rem;
        box-shadow: var(--shadow-soft);
        height: 100%;
        transition: transform 0.3s ease;
    }

    .feature-step-card:hover {
        transform: translateY(-3px);
        border-color: var(--c-vurgu-border);
    }

    .feature-step-num {
        font-family: var(--font-display);
        font-size: 1.1rem;
        font-weight: 700;
        color: var(--c-vurgu);
        margin-bottom: 0.6rem;
    }

    .feature-step-title {
        font-size: 1.05rem;
        font-weight: 700;
        margin-bottom: 0.4rem;
        color: var(--c-ana);
    }

    .feature-step-desc {
        font-size: 0.88rem;
        line-height: 1.5;
        color: var(--c-ikincil);
    }

    /* Native Container Border Styling */
    div[data-testid="stVerticalBlockBorderWrapper"] > div {
        background: var(--c-kart-trans) !important;
        backdrop-filter: blur(16px) !important;
        border: 1px solid var(--c-border) !important;
        border-radius: 20px !important;
        padding: 1.4rem 1.6rem !important;
        box-shadow: var(--shadow-soft) !important;
        margin-bottom: 1rem !important;
    }

    .form-group-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: var(--c-ana);
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* Streamlit Butonlar */
    .stButton > button {
        border-radius: 14px !important;
        font-family: var(--font-main) !important;
        font-weight: 700 !important;
        padding: 0.65rem 1.8rem !important;
        font-size: 0.95rem !important;
        transition: all 0.25s ease !important;
    }

    .stButton > button[kind="primary"],
    .stButton > button[data-testid="baseButton-primary"] {
        background: #1A1F26 !important;
        color: #FFFFFF !important;
        border: 1px solid #1A1F26 !important;
        box-shadow: 0 4px 14px rgba(26, 31, 38, 0.16) !important;
    }

    .stButton > button[kind="primary"]:hover,
    .stButton > button[data-testid="baseButton-primary"]:hover {
        background: #2D333B !important;
        border-color: var(--c-vurgu) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(26, 31, 38, 0.22), 0 0 12px rgba(199, 125, 31, 0.2) !important;
    }

    .stButton > button[kind="primary"]:disabled,
    .stButton > button[data-testid="baseButton-primary"]:disabled {
        background: #D1D5DB !important;
        color: #9CA3AF !important;
        border-color: #D1D5DB !important;
        cursor: not-allowed !important;
        transform: none !important;
        box-shadow: none !important;
    }

    .stButton > button[kind="secondary"],
    .stButton > button[data-testid="baseButton-secondary"] {
        background: #FFFFFF !important;
        color: var(--c-ana) !important;
        border: 1px solid var(--c-border) !important;
        box-shadow: var(--shadow-soft) !important;
    }

    .stButton > button[kind="secondary"]:hover,
    .stButton > button[data-testid="baseButton-secondary"]:hover {
        background: #FAF9F6 !important;
        border-color: var(--c-vurgu) !important;
        color: var(--c-vurgu) !important;
        transform: translateY(-1px) !important;
    }

    /* Form Etiketleri & Inputları */
    label[data-testid="stWidgetLabel"] p {
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        color: var(--c-ana) !important;
        margin-bottom: 0.35rem !important;
    }

    .stSelectbox div[data-baseweb="select"] > div,
    .stNumberInput div[data-baseweb="input"] > div,
    .stTextInput div[data-baseweb="input"] > div {
        background-color: #FFFFFF !important;
        border: 1.5px solid var(--c-border) !important;
        border-radius: 12px !important;
        color: var(--c-ana) !important;
        font-weight: 500 !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
    }

    .stSelectbox div[data-baseweb="select"] > div:hover,
    .stNumberInput div[data-baseweb="input"] > div:hover {
        border-color: #B5AFA6 !important;
    }

    .stSelectbox div[data-baseweb="select"] > div:focus-within,
    .stNumberInput div[data-baseweb="input"] > div:focus-within {
        border-color: var(--c-vurgu) !important;
        box-shadow: 0 0 0 3px var(--c-vurgu-soft) !important;
    }

    /* Dropdown Menü Popover */
    div[data-baseweb="popover"],
    ul[data-baseweb="menu"] {
        background-color: #FFFFFF !important;
        border-radius: 14px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.12), 0 0 1px rgba(0,0,0,0.1) !important;
        border: 1px solid var(--c-border) !important;
        overflow: hidden !important;
    }

    li[role="option"] {
        color: var(--c-ana) !important;
        font-family: var(--font-main) !important;
        font-weight: 500 !important;
        padding: 0.6rem 1rem !important;
        transition: background-color 0.15s ease !important;
    }

    li[role="option"]:hover,
    li[role="option"][aria-selected="true"] {
        background-color: var(--c-vurgu-soft) !important;
        color: var(--c-vurgu-hover) !important;
        font-weight: 700 !important;
    }

    .stNumberInput button {
        background-color: #F5F2EC !important;
        border-color: transparent !important;
        color: var(--c-ana) !important;
    }

    .stNumberInput button:hover {
        background-color: var(--c-vurgu-soft) !important;
        color: var(--c-vurgu) !important;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background: #FFFFFF !important;
        border: 1px solid var(--c-border) !important;
        border-radius: 14px !important;
        font-weight: 700 !important;
        color: var(--c-ana) !important;
        padding: 0.9rem 1.2rem !important;
    }

    div[data-testid="stExpander"] {
        border: none !important;
        margin-top: 0.5rem;
    }

    div[data-testid="stExpander"] > div[role="region"] {
        background: rgba(255, 255, 255, 0.6) !important;
        border: 1px solid var(--c-border-subtle) !important;
        border-top: none !important;
        border-radius: 0 0 14px 14px !important;
        padding: 1.2rem 1.2rem 0.5rem !important;
    }

    /* Titanium Değerleme Kartı */
    .titanium-price-box {
        background: linear-gradient(145deg, #1A1F26 0%, #111418 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 2.8rem 2rem;
        text-align: center;
        margin: 1.5rem 0 1.8rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 20px 50px rgba(26, 31, 38, 0.25);
    }

    .titanium-price-box::before {
        content: '';
        position: absolute;
        top: -40%;
        left: 50%;
        transform: translateX(-50%);
        width: 500px;
        height: 280px;
        background: radial-gradient(ellipse, rgba(199, 125, 31, 0.25) 0%, transparent 70%);
        pointer-events: none;
    }

    .titanium-label {
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        color: #E69D35 !important;
        margin-bottom: 1rem;
    }

    .titanium-price-range {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 1rem;
        flex-wrap: wrap;
    }

    .titanium-price-val {
        font-family: var(--font-display);
        font-size: clamp(2rem, 4.2vw, 3rem);
        font-weight: 700;
        letter-spacing: -0.02em;
        line-height: 1.1;
        color: #FFFFFF !important;
    }

    .titanium-dash {
        color: #E69D35 !important;
        font-size: 1.8rem;
        font-weight: 300;
    }

    .titanium-sub {
        font-size: 0.84rem;
        color: rgba(255, 255, 255, 0.65) !important;
        margin-top: 1.2rem;
        font-weight: 500;
    }

    /* Emsal Paneli */
    .market-comp-panel {
        background: var(--c-kart);
        border: 1px solid var(--c-border);
        border-radius: 20px;
        padding: 1.6rem 1.8rem;
        box-shadow: var(--shadow-soft);
        margin-top: 1.5rem;
    }

    .comp-header {
        font-size: 1.15rem;
        font-weight: 800;
        color: var(--c-ana);
        margin-bottom: 1.1rem;
        display: flex;
        align-items: center;
        gap: 0.6rem;
    }

    .comp-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.8rem 0;
        border-bottom: 1px solid var(--c-border-subtle);
    }

    .comp-row:last-of-type { border-bottom: none; }

    .comp-kpi { font-size: 0.92rem; font-weight: 500; color: var(--c-ikincil); }
    .comp-val { font-size: 0.98rem; font-weight: 700; color: var(--c-ana); }

    .comp-narrative {
        background: var(--c-vurgu-soft);
        border-left: 4px solid var(--c-vurgu);
        border-radius: 0 12px 12px 0;
        padding: 1rem 1.2rem;
        font-size: 0.92rem;
        color: var(--c-ana);
        line-height: 1.55;
        margin-top: 1.2rem;
        font-weight: 500;
    }

    /* Araç İlan Kartı (Buyer) */
    .vehicle-listing-card {
        background: var(--c-kart);
        border: 1px solid var(--c-border);
        border-radius: 20px;
        padding: 1.6rem 1.8rem;
        margin-bottom: 1.2rem;
        box-shadow: var(--shadow-soft);
        transition: all 0.3s ease;
    }

    .vehicle-listing-card:hover {
        transform: translateY(-3px);
        box-shadow: var(--shadow-hover);
        border-color: var(--c-vurgu-border);
    }

    .vlc-top-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 1rem;
        margin-bottom: 0.6rem;
    }

    .vlc-title {
        font-size: 1.22rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        color: var(--c-ana);
    }

    .vlc-badge-match {
        background: #ECFDF5;
        border: 1px solid #A7F3D0;
        color: #065F46;
        padding: 0.3rem 0.75rem;
        border-radius: 100px;
        font-size: 0.78rem;
        font-weight: 700;
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        white-space: nowrap;
    }

    .vlc-specs-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-bottom: 1.1rem;
    }

    .spec-pill {
        background: #F3F0E8;
        border-radius: 8px;
        padding: 0.25rem 0.65rem;
        font-size: 0.82rem;
        font-weight: 600;
        color: var(--c-ikincil);
    }

    .vlc-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1.2rem;
        padding-top: 1rem;
        border-top: 1px solid var(--c-border-subtle);
    }

    @media (max-width: 600px) {
        .vlc-grid { grid-template-columns: 1fr; }
    }

    .vlc-box .label {
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.07em;
        color: var(--c-muted);
        margin-bottom: 0.25rem;
    }

    .vlc-box .value {
        font-family: var(--font-display);
        font-size: 1.22rem;
        font-weight: 700;
        color: var(--c-ana);
    }

    .vlc-box .value.gold {
        color: var(--c-vurgu);
    }
    </style>
    """)

# ─────────────────────────────────────────────
# Veri ve Model Yükleme
# ─────────────────────────────────────────────
@st.cache_resource
def load_app_resources():
    df = pd.read_csv(DATA_RAW_PATH)
    pipeline = joblib.load(MODEL_SAVE_PATH) if os.path.exists(MODEL_SAVE_PATH) else None
    recommender = VehicleRecommender(DATA_RAW_PATH)
    return df, pipeline, recommender

df, pipeline, recommender = load_app_resources()

# ─────────────────────────────────────────────
# Navigasyon Yönetimi
# ─────────────────────────────────────────────
if "screen" not in st.session_state:
    st.session_state.screen = "welcome"

def go_to(screen_name: str):
    st.session_state.screen = screen_name

def go_home():
    for key in ["seller_result", "buyer_result"]:
        if key in st.session_state:
            del st.session_state[key]
    st.session_state.screen = "welcome"

# ─────────────────────────────────────────────
# CSS ve Arka Plan Enjeksiyonu
# ─────────────────────────────────────────────
inject_premium_apple_css()
st.html('<div class="apple-ambient-canvas"></div><div class="apple-grid-overlay"></div>')

# ═════════════════════════════════════════════
# EKRAN 1 — APPLE TARZI VİTRİN VE HİKAYE AKIŞI
# ═════════════════════════════════════════════
def render_welcome():
    # 1. Hero Alanı
    st.html(f"""
    <div class="hero-wrap">
        <div class="brand-pill" style="margin-bottom: 1.5rem;">
            <span>{ICON_CAR_PULSE}</span>
            <span>AutoInsight Intelligence</span>
        </div>
        <h1 class="hero-title-text">
            Aracını <span class="accent-gold">değerle</span>.<br>
            Doğru araca ulaş.
        </h1>
        <p class="hero-lead-desc">
            Makine öğrenmesi destekli dinamik değerleme ve hibrit benzerlik algoritmalarıyla ikinci el pazarında güvenli ve şeffaf kararlar alın.
        </p>
    </div>
    """)

    # 2. İki Ana Modül Bento Kartları
    col1, col2 = st.columns(2, gap="medium")

    with col1:
        st.html(f"""
        <div class="bento-action-card">
            <div>
                <div class="card-icon-box">{ICON_VALUATION}</div>
                <div class="card-heading">Piyasa Değerleme</div>
                <div class="card-body-text">
                    Aracınızın marka, model, km ve hasar geçmişini Random Forest modeliyle analiz edin; güncel piyasa güven aralığını anında öğrenin.
                </div>
            </div>
        </div>
        """)
        st.button("Değerleme Başlat  →", key="btn_start_valuation", type="primary",
                  use_container_width=True, on_click=go_to, args=("seller",))

    with col2:
        st.html(f"""
        <div class="bento-action-card">
            <div>
                <div class="card-icon-box">{ICON_SEARCH}</div>
                <div class="card-heading">Akıllı Araç Arama</div>
                <div class="card-body-text">
                    Bütçenize ve kullanım tercihlerinize en uygun ilanları akıllı puanlama ile bulun; gerçek ilan fiyatlarını yapay zeka piyasa değeriyle karşılaştırın.
                </div>
            </div>
        </div>
        """)
        st.button("Araçları Keşfet  →", key="btn_start_search", type="primary",
                  use_container_width=True, on_click=go_to, args=("buyer",))

    # 3. Canlı Metrik ve İstatistik Barı
    st.html("""
    <div class="bento-stats-grid">
        <div class="stat-tile">
            <div class="stat-big-num">%95</div>
            <div class="stat-label-text">Model Doğruluğu (R²)</div>
        </div>
        <div class="stat-tile">
            <div class="stat-big-num">&lt; 50ms</div>
            <div class="stat-label-text">Vektör Tabanlı Arama</div>
        </div>
        <div class="stat-tile">
            <div class="stat-big-num">53.000+</div>
            <div class="stat-label-text">Gerçek İlan Havuzu</div>
        </div>
        <div class="stat-tile">
            <div class="stat-big-num">%100</div>
            <div class="stat-label-text">Güvenli Lokal Hesaplama</div>
        </div>
    </div>
    """)

    # 4. 3 Adımda Rasyonel Otomotiv Kararı
    st.html("""
    <div>
        <span class="section-tag">Nasıl Çalışır</span>
        <div class="section-headline">Üç adımda rasyonel otomotiv kararı</div>
    </div>
    """)

    s_col1, s_col2, s_col3 = st.columns(3, gap="medium")

    with s_col1:
        st.html("""
        <div class="feature-step-card">
            <div class="feature-step-num">01</div>
            <div class="feature-step-title">Teknik Veri Girişi</div>
            <div class="feature-step-desc">
                Marka, model, yıl, km ve ekspertiz/hasar durumu gibi kritik değişkenleri sisteme aktarın.
            </div>
        </div>
        """)

    with s_col2:
        st.html("""
        <div class="feature-step-card">
            <div class="feature-step-num">02</div>
            <div class="feature-step-title">Yapay Zeka Analizi</div>
            <div class="feature-step-desc">
                Target Encoder ve Random Forest regresyon hattı aracın değer varyansını belirler.
            </div>
        </div>
        """)

    with s_col3:
        st.html("""
        <div class="feature-step-card">
            <div class="feature-step-num">03</div>
            <div class="feature-step-title">Piyasa & Emsal Raporu</div>
            <div class="feature-step-desc">
                Model güven aralığı ve pazar emsal verileriyle şeffaf değerleme çıktısı elde edin.
            </div>
        </div>
        """)

# ═════════════════════════════════════════════
# EKRAN 2 — SATICI AKIŞI (ARAÇ DEĞERLEME)
# ═════════════════════════════════════════════
def render_seller():
    # Üst Navigasyon Barı
    nav_col1, nav_col2 = st.columns([1, 4])
    with nav_col1:
        st.button("← Ana Sayfa", key="seller_back", on_click=go_home, type="secondary")
    with nav_col2:
        st.html(f"""
        <div style="text-align: right; padding-top: 0.3rem;">
            <span class="screen-tag-badge">{ICON_VALUATION} &nbsp;Piyasa Değerleme Stüdyosu</span>
        </div>
        """)

    if "seller_result" in st.session_state:
        _render_seller_result(st.session_state.seller_result)
        return

    st.html("""
    <div style="margin: 1.2rem 0 1.6rem;">
        <h2 style="font-size: 1.9rem; font-weight: 800; letter-spacing: -0.03em; margin: 0 0 0.4rem; color: var(--c-ana);">
            Aracınızın Piyasa Değerini Hesaplayın
        </h2>
        <p style="color: var(--c-ikincil); font-size: 0.96rem; margin: 0;">
            Zorunlu ve opsiyonel teknik değişkenleri girerek Random Forest modeliyle anlık piyasa değer aralığını analiz edin.
        </p>
    </div>
    """)

    # 1. Temel Araç Bilgileri
    with st.container(border=True):
        st.html('<div class="form-group-title">🚗 Temel Araç Bilgileri</div>')
        col1, col2, col3 = st.columns(3)
        with col1:
            brand = st.selectbox("Marka *", options=sorted(df['marka'].dropna().unique()), key="s_brand")
            model_options = sorted(df[df['marka'] == brand]['model'].dropna().unique())
            model_name = st.selectbox("Model *", options=model_options, key="s_model")

        with col2:
            year_options = sorted(df['yil'].dropna().unique().astype(int), reverse=True)
            year = st.selectbox("Model Yılı *", options=year_options, key="s_year")
            km = st.number_input("Kilometre *", min_value=0, max_value=1_000_000, value=85000,
                                 step=5000, key="s_km")

        with col3:
            fuel = st.selectbox("Yakıt Tipi *", options=sorted(df['yakit_tipi'].dropna().unique()), key="s_fuel")
            transmission = st.selectbox("Vites Tipi *", options=sorted(df['vites_tipi'].dropna().unique()), key="s_trans")

    # 2. Ekspertiz ve Hasar Durumu
    with st.container(border=True):
        st.html('<div class="form-group-title">🛡️ Ekspertiz ve Hasar Kayıtları</div>')
        e_col1, e_col2, e_col3 = st.columns(3)
        with e_col1:
            tramer = st.number_input("Tramer Hasar Kaydı (TL)", min_value=0.0, value=0.0, step=1000.0, key="s_tramer")
        with e_col2:
            changed = st.number_input("Değişen Parça Sayısı", min_value=0, max_value=15, value=0, key="s_changed")
        with e_col3:
            painted = st.number_input("Boyalı Parça Sayısı", min_value=0, max_value=15, value=0, key="s_painted")

    # 3. Gelişmiş Opsiyonel Parametreler
    with st.expander("⚙️ Gelişmiş Değişkenler (Model Hassasiyetini Artırır)"):
        o_col1, o_col2, o_col3 = st.columns(3)
        with o_col1:
            series_options = sorted(df[df['marka'] == brand]['seri'].dropna().unique())
            series = st.selectbox("Seri", options=[""] + series_options, key="s_series")
            city_options = sorted(df['konum'].dropna().unique())
            city = st.selectbox("Konum (İl)", options=[""] + city_options, key="s_city")

        with o_col2:
            body_options = sorted(df['kasa_tipi'].dropna().unique())
            body = st.selectbox("Kasa Tipi", options=[""] + body_options, key="s_body")
            drive_options = sorted(df['cekis'].dropna().unique())
            drive = st.selectbox("Çekiş Tipi", options=[""] + drive_options, key="s_drive")

        with o_col3:
            engine_cc = st.number_input("Motor Hacmi (cc)", min_value=0.0, max_value=6000.0,
                                        value=None, step=100.0, key="s_engine", placeholder="Örn: 1598")
            hp = st.number_input("Motor Gücü (HP)", min_value=0.0, max_value=600.0,
                                 value=None, step=10.0, key="s_hp", placeholder="Örn: 120")

        o2_col1, o2_col2 = st.columns(2)
        with o2_col1:
            consumption = st.number_input("Ortalama Yakıt Tüketimi (L/100km)", min_value=0.0,
                                          max_value=25.0, value=None, step=0.1, key="s_consumption", placeholder="Örn: 5.4")
        with o2_col2:
            tank = st.number_input("Yakıt Deposu (Litre)", min_value=0.0, max_value=100.0,
                                   value=None, step=1.0, key="s_tank", placeholder="Örn: 50")

    required_ok = all([brand, model_name, year, km is not None and km >= 0, fuel, transmission])

    st.html("<div style='height: 12px;'></div>")
    clicked = st.button("Piyasa Değerini Hesapla  →", key="s_submit", type="primary",
                        use_container_width=True, disabled=not required_ok)

    if not required_ok:
        st.html(
            '<div style="text-align:center; color:var(--c-vurgu); font-size:0.88rem; font-weight:600; margin-top:0.6rem;">'
            'Lütfen zorunlu alanları doldurun: Marka, Model, Yıl, Kilometre, Yakıt ve Vites.'
            '</div>'
        )

    if clicked:
        if pipeline is None:
            st.error("Eğitilmiş model dosyası bulunamadı. Lütfen önce 'pipeline.py' dosyasını çalıştırın.")
            return

        with st.spinner("Piyasa varyansı ve emsal veriler hesaplanıyor..."):
            brand_data = df[df['marka'] == brand]
            defaults = {
                'motor_hacmi': brand_data['motor_hacmi'].median(),
                'motor_gucu': brand_data['motor_gucu'].median(),
                'ortalama_yakit_tuketimi': brand_data['ortalama_yakit_tuketimi'].median(),
                'yakit_deposu': brand_data['yakit_deposu'].median(),
            }

            input_data = pd.DataFrame([{
                "marka": brand,
                "seri": series if series else (brand_data['seri'].mode().iloc[0] if not brand_data['seri'].mode().empty else "missing"),
                "model": model_name,
                "konum": city if city else (brand_data['konum'].mode().iloc[0] if not brand_data['konum'].mode().empty else "missing"),
                "yil": int(year),
                "kilometre": float(km),
                "yakit_tipi": fuel,
                "vites_tipi": transmission,
                "kasa_tipi": body if body else (brand_data['kasa_tipi'].mode().iloc[0] if not brand_data['kasa_tipi'].mode().empty else "missing"),
                "motor_hacmi": engine_cc if engine_cc and engine_cc > 0 else defaults['motor_hacmi'],
                "motor_gucu": hp if hp and hp > 0 else defaults['motor_gucu'],
                "cekis": drive if drive else (brand_data['cekis'].mode().iloc[0] if not brand_data['cekis'].mode().empty else "missing"),
                "ortalama_yakit_tuketimi": consumption if consumption and consumption > 0 else defaults['ortalama_yakit_tuketimi'],
                "yakit_deposu": tank if tank and tank > 0 else defaults['yakit_deposu'],
                "tramer": float(tramer),
                "degisen": int(changed),
                "boyali": int(painted)
            }])

            predicted = float(pipeline.predict(input_data)[0])
            price_low = predicted * (1 - MODEL_MAPE)
            price_high = predicted * (1 + MODEL_MAPE)

            comparison = recommender.find_comparable_listings(
                marka=brand,
                model=model_name,
                yil=int(year),
                km=float(km),
                predicted_price=predicted,
                degisen=int(changed)
            )

            st.session_state.seller_result = {
                "predicted": predicted,
                "price_low": price_low,
                "price_high": price_high,
                "comparison": comparison,
                "brand": brand,
                "model": model_name,
                "year": year
            }
            st.rerun()

def _render_seller_result(result):
    st.html(f"""
    <div style="margin-top: 0.5rem;">
        <span class="section-tag">Değerleme Raporu</span>
        <h2 style="font-size: 1.85rem; font-weight: 800; color: var(--c-ana); margin: 0 0 0.5rem;">
            {result["brand"]} {result["model"]} ({result["year"]})
        </h2>
    </div>
    """)

    st.html(f"""
    <div class="titanium-price-box">
        <div class="titanium-label">Tahmini Piyasa Değer Aralığı</div>
        <div class="titanium-price-range">
            <div class="titanium-price-val">{format_price(result["price_low"])}</div>
            <div class="titanium-dash">&mdash;</div>
            <div class="titanium-price-val">{format_price(result["price_high"])}</div>
        </div>
        <div class="titanium-sub">Model Güven Aralığı (MAPE: %{MODEL_MAPE*100:.1f} &nbsp;&middot;&nbsp; Makine Öğrenmesi Tahmini: {format_price(result["predicted"])})</div>
    </div>
    """)

    comp = result["comparison"]
    if comp["sufficient"]:
        st.html(f"""
        <div class="market-comp-panel">
            <div class="comp-header">
                <span>{ICON_CHART}</span>
                <span>Piyasa Emsal İlan Karşılaştırması</span>
            </div>
            <div class="comp-row">
                <span class="comp-kpi">Eşleşen Emsal İlan Sayısı</span>
                <span class="comp-val">{comp["count"]} Adet</span>
            </div>
            <div class="comp-row">
                <span class="comp-kpi">Pazardaki Benzer Araçların Ortalama Fiyatı</span>
                <span class="comp-val">{format_price(comp["avg_price"])}</span>
            </div>
            <div class="comp-row">
                <span class="comp-kpi">Piyasa Yüzdelik Konumu</span>
                <span class="comp-val">İlanların %{comp["percentile"]:.0f} diliminden yüksek</span>
            </div>
            <div class="comp-narrative">
                <strong>Piyasa Özeti:</strong> {comp["comment"]}
            </div>
        </div>
        """)
    else:
        st.info(f"Emsal karşılaştırması için yeterli hacim bulunamadı (Bulunan: {comp['count']} ilan, minimum 10 gereklidir).")

    st.html("<div style='height: 16px;'></div>")
    res_col1, res_col2 = st.columns([1, 1])
    with res_col1:
        st.button("Yeni Bir Araç Değerle", key="sr_reset", on_click=_clear_seller_result, type="primary", use_container_width=True)
    with res_col2:
        st.button("İlanları Keşfet (Alıcı Ekranı) →", key="sr_to_buyer", on_click=go_to, args=("buyer",), type="secondary", use_container_width=True)

def _clear_seller_result():
    if "seller_result" in st.session_state:
        del st.session_state["seller_result"]

# ═════════════════════════════════════════════
# EKRAN 3 — ALICI AKIŞI (AKILLI ARAÇ ARAMA)
# ═════════════════════════════════════════════
def render_buyer():
    # Üst Navigasyon Barı
    nav_col1, nav_col2 = st.columns([1, 4])
    with nav_col1:
        st.button("← Ana Sayfa", key="buyer_back", on_click=go_home, type="secondary")
    with nav_col2:
        st.html(f"""
        <div style="text-align: right; padding-top: 0.3rem;">
            <span class="screen-tag-badge">{ICON_SEARCH} &nbsp;Akıllı Araç Keşif Stüdyosu</span>
        </div>
        """)

    if "buyer_result" in st.session_state:
        _render_buyer_result(st.session_state.buyer_result)
        return

    st.html("""
    <div style="margin: 1.2rem 0 1.6rem;">
        <h2 style="font-size: 1.9rem; font-weight: 800; letter-spacing: -0.03em; margin: 0 0 0.4rem; color: var(--c-ana);">
            Bütçenize En Uygun Araçları Bulun
        </h2>
        <p style="color: var(--c-ikincil); font-size: 0.96rem; margin: 0;">
            Bütçe ve donanım kriterlerinizi belirleyin; hibrit benzerlik algoritmasıyla fiyat/performans açısından en avantajlı seçenekleri listeleyin.
        </p>
    </div>
    """)

    # 1. Bütçe ve Arama Modu
    with st.container(border=True):
        st.html('<div class="form-group-title">💰 Bütçe ve Arama Yaklaşımı</div>')
        col_budget, col_flex = st.columns([2, 1])
        with col_budget:
            budget = st.number_input("Maksimum Bütçe Tutarı (TL)", min_value=0, value=1350000,
                                     step=50000, key="b_budget")
        with col_flex:
            st.html("<div style='height: 28px;'></div>")
            flexible = st.checkbox("Bütçesiz Esnek Arama (Kriter Odaklı)", key="b_flexible")

    # 2. Araç Filtreleri
    with st.container(border=True):
        st.html('<div class="form-group-title">🔍 Tercihler ve Filtreler</div>')
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
            b_max_km = st.number_input("Maksimum Kilometre Sınırı", min_value=0, value=120000,
                                        step=10000, key="b_max_km")
            year_min_options = sorted(df['yil'].dropna().unique().astype(int))
            b_min_year = st.selectbox("En Düşük Model Yılı", options=[None] + year_min_options,
                                       key="b_min_year", format_func=lambda x: "Fark etmez" if x is None else str(x))

    optional_filled = sum([
        b_brand != "Tümü",
        b_fuel != "Tümü",
        b_trans != "Tümü",
        b_body != "Tümü",
        b_max_km is not None and b_max_km > 0,
        b_min_year is not None
    ])

    has_budget = budget is not None and budget > 0
    if flexible:
        can_search = optional_filled >= 2
        hint = "" if can_search else "Esnek bütçeli arama için lütfen en az 2 filtre seçin."
    else:
        can_search = has_budget
        hint = "" if can_search else "Arama yapmak için lütfen bir maksimum bütçe tutarı girin."

    st.html("<div style='height: 12px;'></div>")
    clicked = st.button("Avantajlı Araçları Keşfet  →", key="b_submit", type="primary",
                        use_container_width=True, disabled=not can_search)

    if hint:
        st.html(f'<div style="text-align:center; color:var(--c-vurgu); font-size:0.88rem; font-weight:600; margin-top:0.6rem;">{hint}</div>')

    if clicked:
        with st.spinner("Piyasa taranıyor ve en avantajlı araçlar puanlanıyor..."):
            recs = recommender.recommend_by_preferences(
                max_budget=budget if (has_budget and not flexible) else None,
                preferred_fuel=b_fuel if b_fuel != "Tümü" else None,
                preferred_transmission=b_trans if b_trans != "Tümü" else None,
                preferred_kasa=b_body if b_body != "Tümü" else None,
                max_km=b_max_km if b_max_km and b_max_km > 0 else None,
                min_year=b_min_year if b_min_year else None,
                top_n=20
            )

            if b_brand != "Tümü" and not recs.empty:
                recs = recs[recs['marka'] == b_brand]

            if recs.empty:
                st.warning("Kriterlerinize uygun araç bulunamadı. Lütfen filtrelerinizi genişletmeyi deneyin.")
                return

            results = []
            if pipeline is not None:
                for _, row in recs.iterrows():
                    car_full = df[(df['marka'] == row['marka']) &
                                 (df['model'] == row['model']) &
                                 (df['yil'] == row['yil']) &
                                 (df['kilometre'] == row['kilometre'])]

                    if not car_full.empty:
                        car_data = car_full.iloc[0]
                        available_num = [c for c in NUMERIC_FEATURES if c in df.columns]
                        available_cat = [c for c in CATEGORICAL_FEATURES if c in df.columns]
                        input_row = car_data[available_num + available_cat].to_frame().T
                        try:
                            market_value = float(pipeline.predict(input_row)[0])
                        except Exception:
                            market_value = None
                    else:
                        market_value = None

                    results.append({
                        "marka": row['marka'],
                        "seri": row.get('seri', ''),
                        "model": row['model'],
                        "yil": int(row['yil']),
                        "km": float(row['kilometre']),
                        "vites": row.get('vites_tipi', ''),
                        "yakit": row.get('yakit_tipi', ''),
                        "kasa": row.get('kasa_tipi', ''),
                        "ilan_fiyat": float(row['fiyat']),
                        "market_value": market_value,
                        "match_score": float(row.get('match_score', 0))
                    })
            else:
                for _, row in recs.iterrows():
                    results.append({
                        "marka": row['marka'],
                        "seri": row.get('seri', ''),
                        "model": row['model'],
                        "yil": int(row['yil']),
                        "km": float(row['kilometre']),
                        "vites": row.get('vites_tipi', ''),
                        "yakit": row.get('yakit_tipi', ''),
                        "kasa": row.get('kasa_tipi', ''),
                        "ilan_fiyat": float(row['fiyat']),
                        "market_value": None,
                        "match_score": float(row.get('match_score', 0))
                    })

            st.session_state.buyer_result = results
            st.rerun()

def _render_buyer_result(results):
    res_header_col1, res_header_col2 = st.columns([3, 1])
    with res_header_col1:
        st.html(f"""
        <div style="margin: 0.5rem 0 1.5rem;">
            <span class="section-tag">Arama Sonuçları</span>
            <h2 style="font-size: 1.85rem; font-weight: 800; color: var(--c-ana); margin: 0;">
                {len(results)} Avantajlı Araç Eşleşti
            </h2>
        </div>
        """)
    with res_header_col2:
        st.button("Filtreleri Değiştir", key="br_reset_top", on_click=_clear_buyer_result, type="secondary", use_container_width=True)

    for car in results:
        title = f"{car['marka']} {car['model']} ({car['yil']})"
        
        match_badge = ""
        if car.get('match_score', 0) > 0:
            match_badge = f'<div class="vlc-badge-match">{ICON_CHECK} <span>Uyum: %{car["match_score"]:.0f}</span></div>'

        market_html = ""
        if car['market_value'] is not None:
            mv_low = car['market_value'] * (1 - MODEL_MAPE)
            mv_high = car['market_value'] * (1 + MODEL_MAPE)
            
            deal_note = ""
            if car["ilan_fiyat"] < mv_low:
                deal_note = '<span style="color:#16a34a; font-size:0.8rem; font-weight:700; display:block; margin-top:3px;">✦ Piyasa Altı Fırsat</span>'
            elif car["ilan_fiyat"] <= mv_high:
                deal_note = '<span style="color:var(--c-vurgu); font-size:0.8rem; font-weight:600; display:block; margin-top:3px;">✓ Piyasa Değerinde</span>'

            market_html = f'<div class="vlc-box"><div class="label">Yapay Zeka Tahmini Piyasa Değeri</div><div class="value gold">{format_price(mv_low)} &mdash; {format_price(mv_high)}</div>{deal_note}</div>'

        kasa_pill = f'<span class="spec-pill">{car["kasa"]}</span>' if car.get("kasa") else ""
        seri_pill = f'<span class="spec-pill">{car["seri"]}</span>' if car.get("seri") else ""

        card_html = f"""
        <div class="vehicle-listing-card">
            <div class="vlc-top-row">
                <div class="vlc-title">{title}</div>
                {match_badge}
            </div>
            <div class="vlc-specs-row">
                <span class="spec-pill">{format_km(car['km'])}</span>
                <span class="spec-pill">{car['vites']}</span>
                <span class="spec-pill">{car['yakit']}</span>
                {kasa_pill}
                {seri_pill}
            </div>
            <div class="vlc-grid">
                <div class="vlc-box">
                    <div class="label">İlan Satış Fiyatı</div>
                    <div class="value">{format_price(car["ilan_fiyat"])}</div>
                </div>
                {market_html}
            </div>
        </div>
        """

        st.html(card_html)

    st.html("<div style='height: 16px;'></div>")
    st.button("Yeni Arama Yap", key="br_reset_bottom", on_click=_clear_buyer_result, type="primary", use_container_width=True)

def _clear_buyer_result():
    if "buyer_result" in st.session_state:
        del st.session_state["buyer_result"]

# ═════════════════════════════════════════════
# ANA ROUTER
# ═════════════════════════════════════════════
screen = st.session_state.screen

if screen == "welcome":
    render_welcome()
elif screen == "seller":
    render_seller()
elif screen == "buyer":
    render_buyer()
else:
    st.session_state.screen = "welcome"
    st.rerun()