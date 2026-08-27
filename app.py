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
# Vektörel SVG İkonlar & Logolar
# ─────────────────────────────────────────────
LOGO_FULL_SVG = """
<div style="display: flex; align-items: center; gap: 14px;">
  <div class="logo-box">
    <div class="lb lb1"></div>
    <div class="lb lb2"></div>
    <div class="lb lb3"></div>
  </div>
  <div style="display: flex; flex-direction: column; justify-content: center;">
    <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1.5rem; font-weight: 800; color: #FFFFFF; letter-spacing: -0.03em; line-height: 1.1;">
      Auto<span style="color: #00FFB3; text-shadow: 0 0 16px rgba(0,255,179,0.4);">Insight</span>
    </div>
    <div style="font-family: 'Space Grotesk', sans-serif; font-size: 0.6rem; font-weight: 700; color: #7A8CA5; letter-spacing: 0.26em; text-transform: uppercase; margin-top: 2px;">
      Akıllı Otomotiv Platformu
    </div>
  </div>
</div>
"""

ICON_CAR = '<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#00C48C" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9C18.7 10.6 16 10 16 10s-1.3-1.4-2.2-2.3c-.5-.4-1.1-.7-1.8-.7H5c-.6 0-1.1.4-1.4.9l-1.4 2.9A3.7 3.7 0 0 0 1 14v2c0 .6.4 1 1 1h2"/><circle cx="7" cy="17" r="2"/><path d="M9 17h6"/><circle cx="17" cy="17" r="2"/></svg>'
ICON_VALUATION = '<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#00FFB3" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"></line><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg>'
ICON_SEARCH = '<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#00FFB3" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line><line x1="11" y1="8" x2="11" y2="14"></line><line x1="8" y1="11" x2="14" y2="11"></line></svg>'
ICON_CHART = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#00FFB3" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/></svg>'
ICON_CHECK = '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#00FFB3" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>'
ICON_SHIELD = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#00FFB3" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>'

# ─────────────────────────────────────────────
# Yardımcı Formatlama Fonksiyonları
# ─────────────────────────────────────────────
def format_price(value: float) -> str:
    return f"{int(round(value)):,}".replace(",", ".") + " TL"

def format_km(value: float) -> str:
    return f"{int(round(value)):,}".replace(",", ".") + " km"

# ─────────────────────────────────────────────
# Üst Düzey Obsidian & Emerald Tasarım Sistemi
# ─────────────────────────────────────────────
def inject_premium_autoinsight_css():
    st.html("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');

:root {
  --ink: #040812;
  --ink2: #08101E;
  --ink3: #0E182A;
  --ink4: #152238;
  --glass: rgba(10, 18, 32, 0.76);
  --glass-card: rgba(13, 23, 42, 0.72);
  --em: #00C48C;
  --emb: #00FFB3;
  --emd: rgba(0, 196, 140, 0.12);
  --emg: rgba(0, 255, 179, 0.35);
  --blu: rgba(56, 189, 248, 0.12);
  --bor: rgba(255, 255, 255, 0.075);
  --bore: rgba(0, 196, 140, 0.42);
  --t1: #F8FAFC;
  --t2: #94A3B8;
  --t3: #586982;
  --f: 'Plus Jakarta Sans', 'Inter', -apple-system, sans-serif;
  --fd: 'Plus Jakarta Sans', sans-serif;
  --fm: 'Space Grotesk', monospace;
  --r1: 10px;
  --r2: 16px;
  --r3: 24px;
  --r4: 32px;
}

#MainMenu, footer, header { visibility: hidden !important; }
[data-testid="stSidebar"] { display: none !important; }
html, body, [class*="css"] { font-family: var(--f) !important; }

.stApp {
  background: var(--ink) !important;
  color: var(--t1) !important;
  min-height: 100vh;
  overflow-x: hidden;
}

.block-container {
  padding-top: 0 !important;
  padding-bottom: 6rem !important;
  max-width: 1200px !important;
  position: relative;
  z-index: 2;
}

/* ── ANIMATED BACKGROUND ── */
#ai-bg {
  position: fixed;
  inset: 0;
  z-index: 0;
  pointer-events: none;
  overflow: hidden;
}

.orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(110px);
  animation: orbf 24s ease-in-out infinite;
}

.o1 {
  width: 700px;
  height: 700px;
  background: radial-gradient(circle, rgba(0, 196, 140, 0.18), transparent 70%);
  top: -200px;
  left: -200px;
  animation-duration: 26s;
}

.o2 {
  width: 600px;
  height: 600px;
  background: radial-gradient(circle, rgba(56, 189, 248, 0.14), transparent 70%);
  top: -100px;
  right: -150px;
  animation-delay: -9s;
  animation-duration: 21s;
}

.o3 {
  width: 520px;
  height: 520px;
  background: radial-gradient(circle, rgba(139, 92, 246, 0.11), transparent 70%);
  bottom: -80px;
  right: 60px;
  animation-delay: -16s;
  animation-duration: 28s;
}

.o4 {
  width: 450px;
  height: 450px;
  background: radial-gradient(circle, rgba(0, 255, 179, 0.12), transparent 70%);
  bottom: 150px;
  left: 40px;
  animation-delay: -6s;
  animation-duration: 22s;
}

@keyframes orbf {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(45px, -35px) scale(1.08); }
  66% { transform: translate(-30px, 25px) scale(0.92); }
}

.gbg {
  position: absolute;
  inset: 0;
  background-image: 
    linear-gradient(rgba(148, 163, 184, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(148, 163, 184, 0.03) 1px, transparent 1px);
  background-size: 54px 54px;
}

/* ── TOP LIVE RADAR TICKER ── */
.radar-ticker {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 0.5rem 1.4rem;
  background: rgba(0, 196, 140, 0.06);
  border: 1px solid rgba(0, 196, 140, 0.2);
  border-radius: 100px;
  margin: 1rem auto 0;
  max-width: fit-content;
  font-size: 0.78rem;
  font-weight: 600;
  color: #A7F3D0;
  letter-spacing: 0.02em;
  box-shadow: 0 0 20px rgba(0, 196, 140, 0.08);
}
.radar-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--emb);
  box-shadow: 0 0 10px var(--emb);
  animation: radarPulse 1.8s infinite;
}
@keyframes radarPulse {
  0%, 100% { opacity: 0.4; transform: scale(0.85); }
  50% { opacity: 1; transform: scale(1.35); box-shadow: 0 0 14px var(--emb); }
}

/* ── NAVBAR ── */
.nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.95rem 1.6rem;
  background: rgba(8, 15, 28, 0.68);
  backdrop-filter: blur(28px) saturate(170%);
  -webkit-backdrop-filter: blur(28px) saturate(170%);
  border: 1px solid var(--bor);
  border-radius: var(--r4);
  margin: 1rem 0 1.8rem;
  position: sticky;
  top: 14px;
  z-index: 100;
  box-shadow: 0 12px 36px rgba(0, 0, 0, 0.55), inset 0 1px 0 rgba(255, 255, 255, 0.06);
}
.nlo { display: flex; align-items: center; gap: 12px; }
.logo-box {
  width: 42px;
  height: 42px;
  border-radius: 12px;
  background: linear-gradient(135deg, #091C14, #08182D);
  border: 1px solid rgba(0, 196, 140, 0.35);
  display: flex;
  align-items: flex-end;
  justify-content: center;
  gap: 4px;
  padding: 8px 9px;
  box-shadow: 0 0 20px rgba(0, 196, 140, 0.2);
}
.lb { width: 5px; border-radius: 3px; background: var(--emb); }
.lb1 { height: 10px; opacity: 0.5; }
.lb2 { height: 16px; opacity: 0.75; }
.lb3 { height: 22px; }

.lbg {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 0.4rem 0.95rem;
  background: var(--emd);
  border: 1px solid var(--bore);
  border-radius: 100px;
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--emb);
  letter-spacing: 0.03em;
  box-shadow: 0 0 15px rgba(0, 196, 140, 0.12);
}

/* ── HERO ── */
.hero {
  text-align: center;
  padding: 2.8rem 1rem 1.8rem;
  max-width: 940px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.hh {
  font-family: var(--fd);
  font-size: clamp(2.5rem, 5vw, 4.3rem);
  font-weight: 800;
  letter-spacing: -0.035em;
  line-height: 1.12;
  color: var(--t1);
  text-align: center;
  margin: 0 auto 1.3rem;
  animation: fiu 0.6s ease both;
}
.hh .g {
  background: linear-gradient(110deg, #00FFB3 0%, #00C48C 45%, #38BDF8 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 0 35px rgba(0, 196, 140, 0.25);
}
.hp {
  font-size: 1.06rem;
  line-height: 1.74;
  color: var(--t2);
  max-width: 650px;
  text-align: center;
  margin: 0 auto 2.5rem;
  animation: fiu 0.6s 0.1s ease both;
}
@keyframes fiu {
  from { opacity: 0; transform: translateY(18px); }
  to { opacity: 1; transform: translateY(0); }
}

/* ── FEATURE CARDS (VITRIN MODULLERI) ── */
.fc {
  background: var(--glass-card);
  backdrop-filter: blur(26px);
  -webkit-backdrop-filter: blur(26px);
  border: 1px solid var(--bor);
  border-radius: var(--r3);
  padding: 2.3rem 2.1rem;
  min-height: 335px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
  position: relative;
  overflow: hidden;
  box-shadow: 0 16px 45px rgba(0, 0, 0, 0.45);
}
.fc::before {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at top right, rgba(0, 196, 140, 0.12), transparent 60%);
  opacity: 0;
  transition: opacity 0.4s ease;
  border-radius: inherit;
}
.fc:hover {
  transform: translateY(-7px);
  border-color: rgba(0, 255, 179, 0.55);
  box-shadow: 0 28px 70px rgba(0, 0, 0, 0.6), 0 0 45px rgba(0, 196, 140, 0.15), inset 0 1px 0 rgba(0, 255, 179, 0.25);
}
.fc:hover::before { opacity: 1; }

.fcl {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, transparent, #00FFB3, transparent);
  opacity: 0;
  transition: opacity 0.4s ease;
}
.fc:hover .fcl { opacity: 1; }

.fc-top-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.1rem;
}
.fci {
  width: 58px;
  height: 58px;
  border-radius: 16px;
  background: linear-gradient(135deg, rgba(0, 196, 140, 0.2), rgba(8, 24, 18, 0.75));
  border: 1.5px solid rgba(0, 255, 179, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #00FFB3;
  flex-shrink: 0;
  box-shadow: 0 0 25px rgba(0, 196, 140, 0.22);
  transition: all 0.35s ease;
}
.fc:hover .fci {
  background: linear-gradient(135deg, rgba(0, 255, 179, 0.32), rgba(0, 196, 140, 0.22));
  border-color: rgba(0, 255, 179, 0.8);
  box-shadow: 0 0 35px rgba(0, 196, 140, 0.42);
  transform: scale(1.06);
}

.fc-badge {
  font-size: 0.72rem;
  font-weight: 700;
  padding: 0.32rem 0.78rem;
  border-radius: 100px;
  background: rgba(0, 196, 140, 0.1);
  border: 1px solid rgba(0, 196, 140, 0.3);
  color: #00FFB3;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.fct {
  font-family: var(--fd);
  font-size: 1.45rem;
  font-weight: 800;
  letter-spacing: -0.025em;
  color: var(--t1);
  margin-bottom: 0.55rem;
}
.fcd {
  font-size: 0.94rem;
  line-height: 1.68;
  color: var(--t2);
  margin-bottom: 1.2rem;
  flex: 1;
}

.chips { display: flex; flex-wrap: wrap; gap: 8px; margin-top: auto; }
.chip {
  padding: 0.34rem 0.8rem;
  border-radius: 8px;
  font-size: 0.76rem;
  font-weight: 600;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.08);
  color: #CBD5E1;
  transition: all 0.2s ease;
}
.fc:hover .chip {
  background: rgba(0, 196, 140, 0.08);
  border-color: rgba(0, 196, 140, 0.22);
  color: #E2E8F0;
}

/* ── STATS BENTO BAR ── */
.stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1px;
  background: var(--bor);
  border: 1px solid var(--bor);
  border-radius: var(--r3);
  overflow: hidden;
  margin: 3.2rem 0 1rem;
  box-shadow: 0 20px 55px rgba(0, 0, 0, 0.4);
}
.sc {
  background: var(--ink2);
  padding: 1.9rem 1.4rem;
  text-align: center;
  transition: all 0.3s ease;
  position: relative;
}
.sc:hover { background: var(--ink4); }
.sc::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 20%;
  right: 20%;
  height: 2px;
  background: linear-gradient(90deg, transparent, #00FFB3, transparent);
  opacity: 0;
  transition: opacity 0.3s ease;
}
.sc:hover::after { opacity: 1; }
.sn {
  font-family: var(--fm);
  font-size: 2.25rem;
  font-weight: 800;
  letter-spacing: -0.04em;
  color: var(--t1);
  line-height: 1;
  margin-bottom: 0.45rem;
}
.sn.em {
  color: #00FFB3;
  text-shadow: 0 0 26px rgba(0, 255, 179, 0.45);
}
.sl {
  font-size: 0.76rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--t2);
  margin-bottom: 0.25rem;
}
.ss {
  font-size: 0.72rem;
  color: var(--t3);
  font-weight: 500;
}

/* ── SECTION HEADINGS ── */
.shead {
  text-align: center;
  margin: 3.5rem 0 1.8rem;
}
.slbl {
  font-size: 0.74rem;
  font-weight: 800;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: #00FFB3;
  margin-bottom: 0.45rem;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}
.stitle {
  font-family: var(--fd);
  font-size: 2rem;
  font-weight: 800;
  letter-spacing: -0.03em;
  color: var(--t1);
}

/* ── HOW IT WORKS (3 ADIMDA SUREC) ── */
.hiw {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.1rem;
  margin-top: 1.4rem;
}
.hc {
  background: var(--ink2);
  border: 1px solid var(--bor);
  border-radius: var(--r2);
  padding: 1.9rem 1.6rem;
  transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
  position: relative;
  overflow: hidden;
}
.hc::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, transparent, #00FFB3, transparent);
  opacity: 0;
  transition: opacity 0.35s ease;
}
.hc:hover {
  border-color: rgba(0, 196, 140, 0.45);
  transform: translateY(-5px);
  box-shadow: 0 20px 48px rgba(0, 0, 0, 0.5), 0 0 30px rgba(0, 196, 140, 0.12);
}
.hc:hover::before { opacity: 1; }

.hn-pill {
  display: inline-block;
  font-family: var(--fm);
  font-size: 0.72rem;
  font-weight: 800;
  letter-spacing: 0.12em;
  color: #00FFB3;
  background: rgba(0, 196, 140, 0.12);
  border: 1px solid rgba(0, 196, 140, 0.3);
  padding: 0.25rem 0.65rem;
  border-radius: 6px;
  margin-bottom: 1.1rem;
  text-transform: uppercase;
}
.hi-box {
  font-size: 1.9rem;
  margin-bottom: 0.8rem;
  display: block;
}
.ht {
  font-family: var(--fd);
  font-weight: 700;
  font-size: 1.08rem;
  color: var(--t1);
  margin-bottom: 0.45rem;
  letter-spacing: -0.01em;
}
.hd {
  font-size: 0.88rem;
  line-height: 1.65;
  color: var(--t2);
}

/* ── BENTO PLATFORM AVANTAJLARI ── */
.bento-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.1rem;
  margin-top: 1.4rem;
}
.bento-item {
  background: var(--ink2);
  border: 1px solid var(--bor);
  border-radius: var(--r2);
  padding: 1.8rem 1.6rem;
  display: flex;
  gap: 1.1rem;
  align-items: flex-start;
  transition: all 0.3s ease;
}
.bento-item:hover {
  border-color: rgba(0, 196, 140, 0.4);
  background: var(--ink3);
  transform: translateY(-3px);
  box-shadow: 0 16px 40px rgba(0,0,0,0.4);
}
.bento-icon {
  font-size: 1.8rem;
  line-height: 1;
  padding: 0.7rem;
  background: rgba(0, 196, 140, 0.1);
  border: 1px solid rgba(0, 196, 140, 0.25);
  border-radius: 12px;
  flex-shrink: 0;
}
.bento-title {
  font-family: var(--fd);
  font-weight: 700;
  font-size: 1.05rem;
  color: var(--t1);
  margin-bottom: 0.35rem;
}
.bento-desc {
  font-size: 0.88rem;
  line-height: 1.62;
  color: var(--t2);
}

/* ── TRUST STRIP ── */
.trust {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 2rem;
  padding: 1.2rem 2rem;
  background: var(--ink2);
  border: 1px solid var(--bor);
  border-radius: var(--r2);
  margin-top: 2.8rem;
  flex-wrap: wrap;
  box-shadow: 0 12px 35px rgba(0, 0, 0, 0.35);
}
.ti {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.84rem;
  font-weight: 600;
  color: #CBD5E1;
}
.tic {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: var(--emd);
  border: 1px solid var(--bore);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.7rem;
  color: #00FFB3;
}

/* ── FOOTER ── */
.footer-wrap {
  text-align: center;
  padding: 3rem 1rem 1rem;
  color: var(--t3);
  font-size: 0.82rem;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
  margin-top: 4rem;
}
.footer-links {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
  margin-bottom: 0.8rem;
}
.footer-links span {
  color: var(--t2);
  font-weight: 600;
}

/* ── PAGE HEADER ── */
.ph {
  padding: 1.4rem 0 1.8rem;
}
.ph h2 {
  font-family: var(--fd);
  font-size: 2.1rem;
  font-weight: 800;
  letter-spacing: -0.035em;
  color: var(--t1);
  margin: 0 0 0.4rem;
}
.ph p {
  color: var(--t2);
  font-size: 0.96rem;
  margin: 0;
  line-height: 1.62;
}

/* ── FORM PANELS (GLASS) ── */
div[data-testid="stVerticalBlock"] > div[data-testid="stContainer"]:has(.form-group-title),
div[data-testid="stVerticalBlock"] > div[data-testid="stContainer"]:has(div.form-group-title),
div[data-testid="stForm"],
div[data-testid="stContainer"]:has(div[data-testid="stSelectbox"]) {
  background: rgba(10, 18, 34, 0.8) !important;
  backdrop-filter: blur(28px) !important;
  -webkit-backdrop-filter: blur(28px) !important;
  border: 1px solid rgba(255, 255, 255, 0.085) !important;
  border-radius: var(--r4) !important;
  padding: 2.2rem 2.4rem 2.4rem !important;
  margin-bottom: 1.6rem !important;
  box-shadow: 0 26px 70px rgba(0, 0, 0, 0.55), inset 0 1px 0 rgba(255, 255, 255, 0.05) !important;
}

.form-group-title {
  font-family: var(--fd) !important;
  font-size: 1.18rem !important;
  font-weight: 700 !important;
  color: #F1F5F9 !important;
  margin-bottom: 1.4rem !important;
  padding-bottom: 0.85rem !important;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06) !important;
  letter-spacing: -0.015em !important;
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
}
.form-step-badge {
  font-size: 0.72rem !important;
  font-weight: 700 !important;
  padding: 0.25rem 0.65rem !important;
  border-radius: 6px !important;
  background: rgba(0, 196, 140, 0.12) !important;
  border: 1px solid rgba(0, 196, 140, 0.3) !important;
  color: #00FFB3 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.06em !important;
}

/* ── STREAMLIT FORM CONTROLS (DARK OBSIDIAN) ── */
label[data-testid="stWidgetLabel"] p {
  font-family: var(--f) !important;
  font-weight: 600 !important;
  font-size: 0.81rem !important;
  color: #8B9AB5 !important;
  margin-bottom: 0.38rem !important;
  text-transform: uppercase !important;
  letter-spacing: 0.07em !important;
}

/* Selectbox & NumberInput Base Styles */
div[data-testid="stSelectbox"] > div,
div[data-testid="stSelectbox"] div[data-baseweb="select"],
div[data-testid="stSelectbox"] div[data-baseweb="select"] > div,
div[data-testid="stSelectbox"] div[data-baseweb="select"] * {
  background-color: transparent;
}

div[data-testid="stSelectbox"] div[data-baseweb="select"] > div,
div[data-testid="stNumberInput"] div[data-baseweb="input"],
div[data-testid="stNumberInput"] div[data-baseweb="base-input"],
div[data-testid="stNumberInputContainer"],
div[data-baseweb="input"],
div[data-baseweb="base-input"] {
  background: #091220 !important;
  background-color: #091220 !important;
  border: 1.5px solid rgba(255, 255, 255, 0.11) !important;
  border-radius: 12px !important;
  color: #F1F5F9 !important;
  min-height: 48px !important;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.4) !important;
  transition: all 0.25s ease !important;
}

div[data-testid="stSelectbox"] span,
div[data-testid="stSelectbox"] div,
div[data-testid="stSelectbox"] p {
  color: #F1F5F9 !important;
  font-family: var(--f) !important;
  font-weight: 500 !important;
  font-size: 0.93rem !important;
}

div[data-testid="stNumberInput"] input,
input[type="number"],
input[type="text"],
div[data-baseweb="input"] input {
  background: transparent !important;
  background-color: transparent !important;
  color: #F1F5F9 !important;
  font-family: var(--f) !important;
  font-weight: 600 !important;
  font-size: 0.96rem !important;
  padding-left: 0.9rem !important;
}

div[data-baseweb="select"] svg,
div[data-testid="stSelectbox"] svg {
  fill: #00C48C !important;
  color: #00C48C !important;
  stroke: #00C48C !important;
}

div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:hover,
div[data-testid="stNumberInput"] div[data-baseweb="input"]:hover,
div[data-testid="stNumberInputContainer"]:hover {
  border-color: rgba(0, 196, 140, 0.5) !important;
  background: #0E1A2C !important;
  background-color: #0E1A2C !important;
}

div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:focus-within,
div[data-testid="stNumberInput"] div[data-baseweb="input"]:focus-within,
div[data-testid="stNumberInputContainer"]:focus-within {
  border-color: #00FFB3 !important;
  background: #0E1A2C !important;
  background-color: #0E1A2C !important;
  box-shadow: 0 0 0 3px rgba(0, 196, 140, 0.22), 0 0 22px rgba(0, 196, 140, 0.16) !important;
}

div[data-testid="stNumberInput"] button,
button[data-testid="stNumberInputStepDownButton"],
button[data-testid="stNumberInputStepUpButton"] {
  background-color: #142238 !important;
  border: 1px solid rgba(255, 255, 255, 0.08) !important;
  color: #00FFB3 !important;
  border-radius: 8px !important;
  margin: 3px !important;
  transition: all 0.2s ease !important;
}
div[data-testid="stNumberInput"] button:hover,
button[data-testid="stNumberInputStepDownButton"]:hover,
button[data-testid="stNumberInputStepUpButton"]:hover {
  background-color: rgba(0, 196, 140, 0.28) !important;
  border-color: #00C48C !important;
  color: #FFFFFF !important;
}

/* Disabled Selectbox */
div[data-testid="stSelectbox"]:has(input:disabled) div[data-baseweb="select"] > div,
div[data-testid="stSelectbox"] input:disabled ~ div,
div[aria-disabled="true"] {
  background-color: #070D18 !important;
  border-color: rgba(255, 255, 255, 0.05) !important;
  opacity: 0.65 !important;
  cursor: not-allowed !important;
}
div[data-testid="stSelectbox"]:has(input:disabled) span,
div[data-testid="stSelectbox"]:has(input:disabled) div {
  color: #56647A !important;
}

/* ── UNFILLED MANDATORY FIELDS (GLOWING PULSE) ── */
@keyframes mandatoryFieldPulse {
  0%, 100% {
    border-color: rgba(0, 196, 140, 0.45) !important;
    box-shadow: 0 0 0 1.5px rgba(0, 196, 140, 0.18), 0 2px 10px rgba(0, 0, 0, 0.4) !important;
  }
  50% {
    border-color: rgba(0, 255, 179, 0.95) !important;
    box-shadow: 0 0 0 3.5px rgba(0, 196, 140, 0.38), 0 0 24px rgba(0, 255, 179, 0.32) !important;
  }
}

div[data-testid="stSelectbox"]:has(div[title*="Seçiniz"]) div[data-baseweb="select"] > div,
div[data-testid="stSelectbox"]:has(span[title*="Seçiniz"]) div[data-baseweb="select"] > div,
div[data-baseweb="select"]:has(div[title*="Seçiniz"]) > div {
  border-color: rgba(0, 255, 179, 0.72) !important;
  background: linear-gradient(135deg, rgba(0, 196, 140, 0.09), #091220) !important;
  animation: mandatoryFieldPulse 2.4s infinite ease-in-out !important;
}

div[data-testid="stSelectbox"] div[title*="Seçiniz"],
div[data-testid="stSelectbox"] span[title*="Seçiniz"] {
  color: #7193B6 !important;
  font-style: italic !important;
}

/* Checkbox */
div[data-testid="stCheckbox"] label span:first-child {
  background-color: #091220 !important;
  border: 1.5px solid rgba(255, 255, 255, 0.2) !important;
  border-radius: 6px !important;
}
div[data-testid="stCheckbox"] label p {
  color: #C4D2E4 !important;
  font-weight: 500 !important;
  font-size: 0.92rem !important;
}

/* Dropdown Menu List / Popover */
div[data-baseweb="popover"],
div[data-baseweb="popover"] > div,
ul[data-baseweb="menu"] {
  background: #091222 !important;
  background-color: #091222 !important;
  border: 1.5px solid rgba(0, 196, 140, 0.35) !important;
  border-radius: 14px !important;
  box-shadow: 0 24px 60px rgba(0, 0, 0, 0.9), 0 0 35px rgba(0, 196, 140, 0.15) !important;
  overflow: hidden !important;
}

li[role="option"] {
  background-color: transparent !important;
  color: #C4D2E4 !important;
  font-family: var(--f) !important;
  font-weight: 500 !important;
  font-size: 0.92rem !important;
  padding: 0.72rem 1.15rem !important;
  border-bottom: 1px solid rgba(255, 255, 255, 0.03) !important;
  transition: all 0.15s ease !important;
}
li[role="option"]:hover,
li[role="option"][aria-selected="true"] {
  background-color: rgba(0, 196, 140, 0.2) !important;
  color: #00FFB3 !important;
  font-weight: 700 !important;
  padding-left: 1.35rem !important;
}

/* ── BUTTONS ── */
.stButton > button[kind="primary"] {
  background: linear-gradient(135deg, #00FFB3 0%, #00C48C 45%, #009F76 100%) !important;
  color: #030C14 !important;
  font-family: var(--f) !important;
  font-weight: 800 !important;
  font-size: 0.96rem !important;
  border-radius: 12px !important;
  border: none !important;
  padding: 0.85rem 2.2rem !important;
  letter-spacing: -0.01em !important;
  box-shadow: 0 8px 28px rgba(0, 196, 140, 0.38), 0 2px 8px rgba(0, 0, 0, 0.3) !important;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
}
.stButton > button[kind="primary"]:hover {
  background: linear-gradient(135deg, #22FFA8 0%, #00FFB3 100%) !important;
  transform: translateY(-2px) !important;
  box-shadow: 0 14px 42px rgba(0, 196, 140, 0.52), 0 0 25px rgba(0, 255, 179, 0.4) !important;
}

.stButton > button[kind="secondary"] {
  background: rgba(18, 30, 52, 0.65) !important;
  color: #CBD5E1 !important;
  font-family: var(--f) !important;
  font-weight: 600 !important;
  font-size: 0.9rem !important;
  border-radius: 12px !important;
  border: 1px solid var(--bor) !important;
  padding: 0.85rem 2.2rem !important;
  transition: all 0.22s ease !important;
}
.stButton > button[kind="secondary"]:hover {
  border-color: rgba(0, 196, 140, 0.5) !important;
  color: #00FFB3 !important;
  background: rgba(0, 196, 140, 0.08) !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4) !important;
}

/* ── RESULT HEADER ── */
.rh { margin-bottom: 1.8rem; }
.rpill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 0.36rem 0.95rem;
  background: var(--emd);
  border: 1px solid var(--bore);
  border-radius: 100px;
  font-size: 0.74rem;
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #00FFB3;
  margin-bottom: 0.65rem;
}
.rtitle {
  font-family: var(--fd);
  font-size: 2.1rem;
  font-weight: 800;
  letter-spacing: -0.035em;
  color: var(--t1);
  margin: 0;
}

/* ── PRICE HUD COCKPIT ── */
.phud {
  background: linear-gradient(148deg, #0E1C36 0%, #06101E 100%);
  border: 1.5px solid rgba(0, 196, 140, 0.28);
  border-radius: var(--r4);
  padding: 3.2rem 2.5rem;
  text-align: center;
  position: relative;
  overflow: hidden;
  margin: 1.6rem 0;
  box-shadow: 0 45px 90px rgba(0, 0, 0, 0.65), 0 0 70px rgba(0, 196, 140, 0.12), inset 0 1px 0 rgba(255, 255, 255, 0.08);
}
.phud::before {
  content: '';
  position: absolute;
  top: -55%;
  left: 50%;
  transform: translateX(-50%);
  width: 750px;
  height: 440px;
  background: radial-gradient(ellipse, rgba(0, 196, 140, 0.2) 0%, transparent 64%);
  pointer-events: none;
}
.phud::after {
  content: '';
  position: absolute;
  top: 0;
  left: 8%;
  right: 8%;
  height: 2px;
  background: linear-gradient(90deg, transparent, #00FFB3, transparent);
}
.phey {
  font-size: 0.72rem;
  font-weight: 800;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: #00FFB3;
  margin-bottom: 1.2rem;
  position: relative;
  z-index: 1;
}

.prange {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1.2rem;
  flex-wrap: wrap;
  position: relative;
  z-index: 1;
}
.pval {
  font-family: var(--fm);
  font-size: clamp(2rem, 4.5vw, 3.2rem);
  font-weight: 800;
  letter-spacing: -0.03em;
  color: var(--t1);
  text-shadow: 0 0 40px rgba(255, 255, 255, 0.15);
}
.pdash {
  color: rgba(0, 255, 179, 0.65);
  font-size: 2.2rem;
  font-weight: 200;
}

/* Visual Meter Bar inside HUD */
.hud-visual-bar {
  max-width: 580px;
  margin: 1.6rem auto 1.2rem;
  position: relative;
  z-index: 1;
}
.hud-track {
  height: 8px;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 10px;
  position: relative;
  overflow: hidden;
}
.hud-fill {
  height: 100%;
  width: 60%;
  margin: 0 auto;
  background: linear-gradient(90deg, #38BDF8, #00FFB3, #00C48C);
  border-radius: 10px;
  box-shadow: 0 0 16px rgba(0, 255, 179, 0.6);
}
.hud-markers {
  display: flex;
  justify-content: space-between;
  margin-top: 0.5rem;
  font-size: 0.74rem;
  font-weight: 600;
  color: var(--t3);
}

.pmeta {
  margin-top: 1.2rem;
  font-size: 0.88rem;
  color: var(--t2);
  position: relative;
  z-index: 1;
}
.pmeta .pt {
  color: #00FFB3;
  font-weight: 700;
}

/* ── MARKET COMPARISON PANEL ── */
.mkt {
  background: var(--glass-card);
  border: 1px solid var(--bor);
  border-radius: var(--r3);
  overflow: hidden;
  margin-top: 1.4rem;
  box-shadow: 0 22px 55px rgba(0, 0, 0, 0.38);
}
.mkth {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 1.3rem 1.8rem;
  border-bottom: 1px solid var(--bor);
  font-weight: 700;
  font-size: 1rem;
  color: var(--t1);
  background: rgba(255, 255, 255, 0.02);
}
.mktr {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.8rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.04);
  transition: background 0.18s ease;
}
.mktr:last-of-type { border-bottom: none; }
.mktr:hover { background: rgba(255, 255, 255, 0.02); }
.mktk { font-size: 0.88rem; color: var(--t2); font-weight: 500; }
.mktv { font-size: 0.98rem; font-weight: 700; color: var(--t1); }
.mkti {
  margin: 0.2rem 1.8rem 1.6rem;
  padding: 1rem 1.2rem;
  background: var(--emd);
  border-left: 3.5px solid #00FFB3;
  border-radius: 0 var(--r1) var(--r1) 0;
  font-size: 0.9rem;
  line-height: 1.65;
  color: #D1FAE5;
}
.mkti strong { color: #00FFB3; }

/* ── VEHICLE CARDS (ALICI AKISI) ── */
.vc {
  background: var(--glass-card);
  border: 1px solid var(--bor);
  border-radius: var(--r3);
  overflow: hidden;
  margin-bottom: 1rem;
  transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
  box-shadow: 0 10px 32px rgba(0, 0, 0, 0.32);
}
.vc:hover {
  transform: translateY(-5px);
  border-color: rgba(0, 196, 140, 0.45);
  box-shadow: 0 22px 60px rgba(0, 0, 0, 0.52), 0 0 35px rgba(0, 196, 140, 0.1);
}
.vct {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 1.4rem 1.6rem 0.8rem;
  gap: 1rem;
}
.vcti {
  font-family: var(--fd);
  font-size: 1.18rem;
  font-weight: 800;
  letter-spacing: -0.025em;
  color: var(--t1);
}
.mbdg {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 0.32rem 0.8rem;
  background: var(--emd);
  border: 1px solid var(--bore);
  border-radius: 100px;
  font-size: 0.74rem;
  font-weight: 700;
  color: #00FFB3;
  white-space: nowrap;
  flex-shrink: 0;
  box-shadow: 0 0 12px rgba(0, 196, 140, 0.15);
}
.vcs {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  padding: 0 1.6rem 1.2rem;
}
.stg {
  padding: 0.28rem 0.68rem;
  background: rgba(255, 255, 255, 0.045);
  border: 1px solid rgba(255, 255, 255, 0.075);
  border-radius: 7px;
  font-size: 0.78rem;
  font-weight: 600;
  color: #CBD5E1;
}

.vcpr {
  display: grid;
  grid-template-columns: 1fr 1fr;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}
.vcpb {
  padding: 1.2rem 1.6rem;
}
.vcpb:first-child {
  border-right: 1px solid rgba(255, 255, 255, 0.05);
}
.vcpl {
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--t3);
  margin-bottom: 0.35rem;
}
.vcpv {
  font-family: var(--fm);
  font-size: 1.15rem;
  font-weight: 800;
  letter-spacing: -0.02em;
  color: var(--t1);
}
.vcpv.em { color: #00FFB3; }

.dtag {
  display: inline-block;
  margin-top: 4px;
  font-size: 0.72rem;
  font-weight: 700;
  padding: 0.2rem 0.58rem;
  border-radius: 6px;
}
.dtag.hot {
  background: rgba(0, 196, 140, 0.12);
  color: #00FFB3;
  border: 1px solid rgba(0, 196, 140, 0.3);
}
.dtag.fair {
  background: rgba(56, 189, 248, 0.1);
  color: #38BDF8;
  border: 1px solid rgba(56, 189, 248, 0.25);
}

/* ── MISC ── */
.hdiv {
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--bor) 28%, var(--bor) 72%, transparent);
  margin: 2.8rem 0;
}
.stSpinner > div { border-top-color: var(--em) !important; }
.stInfo {
  background: var(--blu) !important;
  border: 1px solid rgba(56, 189, 248, 0.25) !important;
  border-radius: var(--r2) !important;
  color: #BAE6FD !important;
}
.stWarning {
  background: rgba(234, 179, 8, 0.08) !important;
  border: 1px solid rgba(234, 179, 8, 0.25) !important;
  border-radius: var(--r2) !important;
  color: #FDE047 !important;
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
inject_premium_autoinsight_css()
st.html('<div id="ai-bg"><div class="gbg"></div><div class="orb o1"></div><div class="orb o2"></div><div class="orb o3"></div><div class="orb o4"></div></div>')

# ═════════════════════════════════════════════
# EKRAN 1 — ANA SAYFA (VİTRİN & HERO AKIŞI)
# ═════════════════════════════════════════════
def render_welcome():
    # Live Radar Ticker
    st.html("""
    <div class="radar-ticker">
        <div class="radar-dot"></div>
        <span>Canlı Piyasa Radarı &middot; 81 İl Analizi &middot; 53.514 Gerçek İlan Aktif</span>
    </div>
    """)

    # Premium Navbar
    st.html(f"""
    <div class="nav">
        <div class="nlo">
            {LOGO_FULL_SVG}
        </div>
        <div class="lbg">
            <div class="radar-dot"></div>
            <span>Canlı Piyasa Motoru</span>
        </div>
    </div>
    """)

    # Hero
    st.html("""
    <div class="hero">
        <h1 class="hh">Aracınızın Gerçek<br><span class="g">Piyasa Değerini</span> Bilin.</h1>
        <p class="hp">53.000'den fazla güncel piyasa verisini analiz ederek saniyeler içinde hassas değer tahmini, güven aralığı ve emsal piyasa raporu sunar.</p>
    </div>
    """)

    # Feature cards (Vitrin Modülleri)
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.html("""
        <div class="fc">
            <div class="fcl"></div>
            <div>
                <div class="fc-top-row">
                    <div class="fci">
                        <span style="font-size: 1.7rem; line-height: 1; display: flex; align-items: center; justify-content: center; filter: drop-shadow(0 0 10px rgba(0,255,179,0.7));">📊</span>
                    </div>
                    <span class="fc-badge">Hızlı Değerleme</span>
                </div>
                <div class="fct">Piyasa Değerleme</div>
                <div class="fcd">Marka, model, yıl, kilometre ve donanım verilerini girin; modelimiz aracınızın güncel piyasa değer aralığını ve emsal konumunu anında hesaplasın.</div>
            </div>
            <div class="chips">
                <span class="chip">⚡ Anlık Değerleme</span>
                <span class="chip">🎯 Yüksek Hassasiyet</span>
                <span class="chip">📈 Fiyat Aralığı</span>
                <span class="chip">🔍 Emsal Analiz</span>
            </div>
        </div>""")
        st.button("Değerleme Başlat →", key="btn_start_valuation", type="primary",
                  use_container_width=True, on_click=go_to, args=("seller",))

    with col2:
        st.html("""
        <div class="fc">
            <div class="fcl"></div>
            <div>
                <div class="fc-top-row">
                    <div class="fci">
                        <span style="font-size: 1.7rem; line-height: 1; display: flex; align-items: center; justify-content: center; filter: drop-shadow(0 0 10px rgba(0,255,179,0.7));">🔍</span>
                    </div>
                    <span class="fc-badge">Akıllı Filtre</span>
                </div>
                <div class="fct">Akıllı Araç Keşfi</div>
                <div class="fcd">Bütçenizi ve tercihlerinizi belirleyin; hibrit benzerlik algoritmamız gerçek ilanlar arasından en avantajlı araçları uyum puanıyla listelesin.</div>
            </div>
            <div class="chips">
                <span class="chip">✨ Akıllı Eşleşme</span>
                <span class="chip">⭐ Uyum Puanı</span>
                <span class="chip">💰 Fiyat Analizi</span>
                <span class="chip">🔥 Fırsat İlanlar</span>
            </div>
        </div>""")
        st.button("Araçları Keşfet →", key="btn_start_search", type="primary",
                  use_container_width=True, on_click=go_to, args=("buyer",))

    # Stats Bento Bar
    st.html("""
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
    """)

    # Neden AutoInsight? (Bento Grid)
    st.html("""
    <div class="shead">
        <div class="slbl"><span>✦</span> NEDEN AUTOINSIGHT?</div>
        <div class="stitle">Veriye Dayalı Rasyonel Karar Avantajı</div>
    </div>
    <div class="bento-grid">
        <div class="bento-item">
            <div class="bento-icon">🛡️</div>
            <div>
                <div class="bento-title">Objektif &amp; Şeffaf Fiyat Aralığı</div>
                <div class="bento-desc">Spekülatif ve değişken fiyatlar yerine, binlerce gerçek ilan verisiyle filtrelenmiş tutarlı bir piyasa değer koridoru elde edin.</div>
            </div>
        </div>
        <div class="bento-item">
            <div class="bento-icon">⚡</div>
            <div>
                <div class="bento-title">Akıllı Fırsat İlan Tespiti</div>
                <div class="bento-desc">Piyasa ortalamasının altında kalan avantajlı araçları anında tespit ederek bütçeniz için en karlı seçeneği bulun.</div>
            </div>
        </div>
        <div class="bento-item">
            <div class="bento-icon">📍</div>
            <div>
                <div class="bento-title">Bölgesel ve Donanımsal Esneklik</div>
                <div class="bento-desc">İl bazlı pazar dinamikleri, kasa, vites ve yakıt kombinasyonlarına göre özelleştirilmiş analiz sonuçları.</div>
            </div>
        </div>
        <div class="bento-item">
            <div class="bento-icon">📊</div>
            <div>
                <div class="bento-title">Emsal Pazar Karşılaştırması</div>
                <div class="bento-desc">Aracınızın benzer ilanlar içerisindeki fiyat yüzdeliğini ve piyasadaki rekabet konumunu görsel olarak izleyin.</div>
            </div>
        </div>
    </div>
    <div class="hdiv"></div>
    """)

    # Nasıl Çalışır? (3 Adım)
    st.html("""
    <div class="shead">
        <div class="slbl"><span>✦</span> MİMARİ &amp; SÜREÇ</div>
        <div class="stitle">Üç Adımda Akıllı Değerleme</div>
    </div>
    <div class="hiw">
        <div class="hc">
            <span class="hn-pill">Adım 01</span>
            <span class="hi-box">🎯</span>
            <div class="ht">Parametreleri Girin</div>
            <div class="hd">Marka, seri, model, yıl, kilometre, yakıt, vites ve kasa bilgilerini dinamik form aracılığıyla aktarın.</div>
        </div>
        <div class="hc">
            <span class="hn-pill">Adım 02</span>
            <span class="hi-box">🧠</span>
            <div class="ht">Yapay Zeka Analizi</div>
            <div class="hd">Gelişmiş veri analitiği motorumuz aracın piyasa değerini, güven aralığını ve varyansını anında hesaplar.</div>
        </div>
        <div class="hc">
            <span class="hn-pill">Adım 03</span>
            <span class="hi-box">📊</span>
            <div class="ht">Piyasa Raporu</div>
            <div class="hd">Güven aralığı, emsal karşılaştırması ve piyasa yüzdelik konum analiziyle objektif değerleme raporunuzu alın.</div>
        </div>
    </div>

    <div class="trust">
        <div class="ti"><div class="tic">✓</div><span>Gerçek Piyasa Verisi</span></div>
        <div class="ti"><div class="tic">⚡</div><span>Anlık Hesaplama</span></div>
        <div class="ti"><div class="tic">🔒</div><span>Veri Gizliliği</span></div>
        <div class="ti"><div class="tic">🎯</div><span>Yüksek Doğruluk Oranı</span></div>
        <div class="ti"><div class="tic">📈</div><span>Sürekli Güncellenen Model</span></div>
    </div>

    <div class="footer-wrap">
        <div class="footer-links">
            <span>AutoInsight v2.4</span>
            <span>&bull;</span>
            <span>53.514 Gerçek İlan Analitiği</span>
            <span>&bull;</span>
            <span>Python &amp; Streamlit Engine</span>
        </div>
        <div>&copy; 2026 AutoInsight — Tüm Hakları Saklıdır.</div>
    </div>
    """)

# ═════════════════════════════════════════════
# EKRAN 2 — SATICI AKIŞI (ARAÇ DEĞERLEME)
# ═════════════════════════════════════════════
def render_seller():
    st.html(f"""
    <div class="nav">
        <div class="nlo">
            {LOGO_FULL_SVG}
        </div>
        <div class="lbg">
            <div class="radar-dot"></div>
            <span>Piyasa Değerleme Modülü</span>
        </div>
    </div>
    """)
    nav_col1, nav_col2 = st.columns([1, 5])
    with nav_col1:
        st.button("← Ana Sayfa", key="seller_back", on_click=go_home, type="secondary")
    with nav_col2:
        st.html('<div style="text-align:right;padding-top:.3rem"><span class="lbg">Piyasa Değerleme</span></div>')

    if "seller_result" in st.session_state:
        _render_seller_result(st.session_state.seller_result)
        return

    st.html('<div class="ph"><h2>Aracınızın Piyasa Değerini Hesaplayın</h2><p>Araç bilgilerinizi girin — 53.000+ güncel piyasa verisiyle sistemimiz anlık değer aralığını saniyeler içinde hesaplasın.</p></div>')

    # Araç Bilgileri Formu (8 Zorunlu Parametre + 1 Opsiyonel Konum)
    with st.container(border=True):
        st.html("""
        <div class="form-group-title">
            <span>🚗 1. Temel Araç Bilgileri</span>
            <span class="form-step-badge">Zorunlu Alanlar</span>
        </div>
        """)

        # 1. Satır: Marka ➔ Seri ➔ Model
        col1, col2, col3 = st.columns(3)
        with col1:
            brand_list = sorted(df['marka'].dropna().unique().tolist())
            brand = st.selectbox(
                "Marka",
                options=["Seçiniz..."] + brand_list,
                index=0,
                key="s_brand"
            )
            selected_brand = brand if brand != "Seçiniz..." else None

        with col2:
            if selected_brand:
                series_list = sorted(df[df['marka'] == selected_brand]['seri'].dropna().unique().tolist())
                series = st.selectbox(
                    "Seri",
                    options=["Seçiniz..."] + series_list,
                    index=0,
                    key=f"s_series_{selected_brand}"
                )
                selected_series = series if series != "Seçiniz..." else None
            else:
                st.selectbox("Seri", options=["Önce marka seçiniz"], disabled=True, key="s_series_disabled")
                selected_series = None

        with col3:
            if selected_brand and selected_series:
                model_list = sorted(df[(df['marka'] == selected_brand) & (df['seri'] == selected_series)]['model'].dropna().unique().tolist())
                model_name = st.selectbox(
                    "Model",
                    options=["Seçiniz..."] + model_list,
                    index=0,
                    key=f"s_model_{selected_brand}_{selected_series}"
                )
                selected_model = model_name if model_name != "Seçiniz..." else None
            else:
                st.selectbox("Model", options=["Önce marka ve seri seçiniz"], disabled=True, key="s_model_disabled")
                selected_model = None

        # Seçilen araca göre filtrelenmiş alt veri havuzu
        sub_df = df.copy()
        if selected_brand:
            sub_df = sub_df[sub_df['marka'] == selected_brand]
        if selected_series:
            sub_df = sub_df[sub_df['seri'] == selected_series]
        if selected_model:
            sub_df = sub_df[sub_df['model'] == selected_model]

    # Donanım ve Teknik Bilgiler Paneli
    with st.container(border=True):
        st.html("""
        <div class="form-group-title">
            <span>⚙️ 2. Donanım, Kilometre ve Konum</span>
            <span class="form-step-badge">Teknik Parametreler</span>
        </div>
        """)

        # 2. Satır: Model Yılı, Kilometre, Kasa Tipi
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
            body_options = ["Seçiniz..."] + available_bodies
            body = st.selectbox("Kasa Tipi", options=body_options, key="s_body")
            selected_body = body if body != "Seçiniz..." else None

        # 3. Satır: Yakıt Tipi, Vites Tipi, Konum (İl)
        r3_col1, r3_col2, r3_col3 = st.columns(3)
        with r3_col1:
            available_fuels = sorted(sub_df['yakit_tipi'].dropna().unique().tolist())
            if not available_fuels:
                available_fuels = sorted(df['yakit_tipi'].dropna().unique().tolist())
            fuel_options = ["Seçiniz..."] + available_fuels
            fuel = st.selectbox("Yakıt Tipi", options=fuel_options, key="s_fuel")
            selected_fuel = fuel if fuel != "Seçiniz..." else None

        with r3_col2:
            available_trans = sorted(sub_df['vites_tipi'].dropna().unique().tolist())
            if not available_trans:
                available_trans = sorted(df['vites_tipi'].dropna().unique().tolist())
            trans_options = ["Seçiniz..."] + available_trans
            transmission = st.selectbox("Vites Tipi", options=trans_options, key="s_trans")
            selected_trans = transmission if transmission != "Seçiniz..." else None

        with r3_col3:
            city_options = ["Tüm Türkiye (Genel)"] + sorted(df['konum'].dropna().unique().tolist())
            city = st.selectbox("Konum (İl) — Opsiyonel", options=city_options, key="s_city")

    required_ok = all([
        selected_brand is not None,
        selected_series is not None,
        selected_model is not None,
        year is not None,
        km is not None and km >= 0,
        selected_fuel is not None,
        selected_trans is not None,
        selected_body is not None
    ])

    st.html("<div style='height: 14px;'></div>")
    clicked = st.button("Piyasa Değerini Hesapla →", key="s_submit", type="primary",
                        use_container_width=True, disabled=not required_ok)

    if clicked:
        if pipeline is None:
            st.error("Eğitilmiş model dosyası bulunamadı. Lütfen önce 'pipeline.py' dosyasını çalıştırın.")
            return

        with st.spinner("Piyasa varyansı ve emsal veriler analiz ediliyor..."):
            if city and city != "Tüm Türkiye (Genel)":
                chosen_city = city
            else:
                chosen_city = df['konum'].mode().iloc[0] if not df['konum'].mode().empty else "missing"

            input_data = pd.DataFrame([{
                "marka": selected_brand,
                "seri": selected_series,
                "model": selected_model,
                "konum": chosen_city,
                "yil": int(year),
                "kilometre": float(km),
                "yakit_tipi": selected_fuel,
                "vites_tipi": selected_trans,
                "kasa_tipi": selected_body
            }])

            predicted = float(pipeline.predict(input_data)[0])
            price_low = predicted * (1 - MODEL_MAPE)
            price_high = predicted * (1 + MODEL_MAPE)

            comparison = recommender.find_comparable_listings(
                marka=selected_brand,
                model=selected_model,
                yil=int(year),
                km=float(km),
                predicted_price=predicted
            )

            st.session_state.seller_result = {
                "predicted": predicted,
                "price_low": price_low,
                "price_high": price_high,
                "comparison": comparison,
                "brand": selected_brand,
                "model": selected_model,
                "year": year
            }
            st.rerun()

def _render_seller_result(result):
    st.html(f"""
    <div style="margin-top: 0.5rem;">
        <span class="rpill">{ICON_CHECK} Değerleme Raporu</span>
        <h2 style="font-size: 2.1rem; font-weight: 800; color: #FFFFFF; margin: 0.6rem 0 0.5rem;">
            {result["brand"]} {result["model"]} ({result["year"]})
        </h2>
    </div>
    """)

    # Digital Cockpit HUD
    st.html(f"""
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
    """)

    comp = result["comparison"]
    if comp["sufficient"]:
        percentile_val = int(round(comp["percentile"]))
        st.html(f"""
        <div class="mkt">
            <div class="mkth">
                <span>{ICON_CHART}</span>
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
        """)
    else:
        st.info(f"Emsal karşılaştırması için yeterli hacim bulunamadı (Bulunan: {comp['count']} ilan, minimum 10 gereklidir).")

    st.html("<div style='height: 18px;'></div>")
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
    st.html(f"""
    <div class="nav">
        <div class="nlo">
            {LOGO_FULL_SVG}
        </div>
        <div class="lbg">
            <div class="radar-dot"></div>
            <span>Akıllı Keşif Modülü</span>
        </div>
    </div>
    """)
    nav_col1, nav_col2 = st.columns([1, 5])
    with nav_col1:
        st.button("← Ana Sayfa", key="buyer_back", on_click=go_home, type="secondary")
    with nav_col2:
        st.html('<div style="text-align:right;padding-top:.3rem"><span class="lbg">Akıllı Araç Keşfi</span></div>')

    if "buyer_result" in st.session_state:
        _render_buyer_result(st.session_state.buyer_result)
        return

    st.html('<div class="ph"><h2>Bütçenize En Uygun Araçları Bulun</h2><p>Kriterleri ve tercihlerinizi belirleyin — akıllı benzerlik algoritmamız fiyat/performans açısından en avantajlı ilanları listelesin.</p></div>')

    # 1. Bütçe ve Arama Modu
    with st.container(border=True):
        st.html("""
        <div class="form-group-title">
            <span>💰 1. Bütçe ve Arama Yaklaşımı</span>
            <span class="form-step-badge">Fiyat Sınırı</span>
        </div>
        """)
        col_budget, col_flex = st.columns([2, 1])
        with col_budget:
            budget = st.number_input("Maksimum Bütçe Tutarı (TL)", min_value=0, value=1350000,
                                     step=50000, key="b_budget")
        with col_flex:
            st.html("<div style='height: 28px;'></div>")
            flexible = st.checkbox("Bütçesiz Esnek Arama (Kriter Odaklı)", key="b_flexible")

    # 2. Araç Filtreleri
    with st.container(border=True):
        st.html("""
        <div class="form-group-title">
            <span>🔍 2. Donanım Tercihleri ve Filtreler</span>
            <span class="form-step-badge">Araç Filtreleri</span>
        </div>
        """)
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

    st.html("<div style='height: 14px;'></div>")
    clicked = st.button("Avantajlı Araçları Keşfet →", key="b_submit", type="primary",
                        use_container_width=True, disabled=not can_search)

    if hint:
        st.html(f'<div style="text-align:center; color:#00FFB3; font-size:0.88rem; font-weight:600; margin-top:0.6rem;">{hint}</div>')

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
            <span class="rpill">{ICON_CHECK} Arama Sonuçları</span>
            <h2 style="font-size: 2rem; font-weight: 800; color: #FFFFFF; margin: 0.6rem 0 0;">
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
            match_badge = f'<div class="mbdg">{ICON_CHECK} <span>%{car["match_score"]:.0f} Uyum</span></div>'

        market_html = ""
        if car['market_value'] is not None:
            mv_low = car['market_value'] * (1 - MODEL_MAPE)
            mv_high = car['market_value'] * (1 + MODEL_MAPE)
            
            deal_note = ""
            if car["ilan_fiyat"] < mv_low:
                deal_note = '<span class="dtag hot">✦ Piyasa Altı Fırsat</span>'
            elif car["ilan_fiyat"] <= mv_high:
                deal_note = '<span class="dtag fair">✓ Piyasa Değerinde</span>'

            market_html = f'<div class="vcpb"><div class="vcpl">Tahmini Piyasa Değeri</div><div class="vcpv em">{format_price(mv_low)} &mdash; {format_price(mv_high)}</div>{deal_note}</div>'

        kasa_pill = f'<span class="stg">{car["kasa"]}</span>' if car.get("kasa") else ""
        seri_pill = f'<span class="stg">{car["seri"]}</span>' if car.get("seri") else ""

        card_html = f"""
        <div class="vc">
            <div class="vct">
                <div class="vcti">{title}</div>
                {match_badge}
            </div>
            <div class="vcs">
                <span class="stg">{format_km(car['km'])}</span>
                <span class="stg">{car['vites']}</span>
                <span class="stg">{car['yakit']}</span>
                {kasa_pill}
                {seri_pill}
            </div>
            <div class="vcpr">
                <div class="vcpb">
                    <div class="vcpl">İlan Satış Fiyatı</div>
                    <div class="vcpv">{format_price(car["ilan_fiyat"])}</div>
                </div>
                {market_html}
            </div>
        </div>
        """

        st.html(card_html)

    st.html("<div style='height: 18px;'></div>")
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
