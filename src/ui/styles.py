"""
AutoInsight — Premium CSS Enjeksiyonu
Tüm stillendirme ve animasyonlar bu modülde merkezi olarak yönetilir.
"""
from src.ui.components import raw_html


def inject_premium_autoinsight_css() -> None:
    """Premium AutoInsight tema CSS'ini Streamlit sayfasına enjekte eder."""
    raw_html('''
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

.ai-chip-ic {
  width: 14px;
  height: 14px;
  display: inline-block;
  vertical-align: -2px;
  margin-right: 6px;
  filter: drop-shadow(0 0 6px rgba(0, 255, 179, 0.5));
}
.ai-hdr-ic {
  width: 22px;
  height: 22px;
  display: inline-block;
  vertical-align: -4px;
  margin-right: 8px;
  filter: drop-shadow(0 0 8px rgba(0, 255, 179, 0.6));
}

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
  display: inline-flex;
  align-items: center;
}
.fc:hover .chip {
  background: rgba(0, 196, 140, 0.08);
  border-color: rgba(0, 196, 140, 0.22);
  color: #E2E8F0;
}

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
  width: 52px;
  height: 52px;
  border-radius: 14px;
  background: rgba(0, 196, 140, 0.1);
  border: 1px solid rgba(0, 196, 140, 0.25);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 0.9rem;
  box-shadow: 0 0 16px rgba(0, 196, 140, 0.1);
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
.bento-icon-box {
  width: 48px;
  height: 48px;
  background: rgba(0, 196, 140, 0.1);
  border: 1px solid rgba(0, 196, 140, 0.25);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  box-shadow: 0 0 15px rgba(0, 196, 140, 0.12);
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
  gap: 9px;
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

label[data-testid="stWidgetLabel"] p {
  font-family: var(--f) !important;
  font-weight: 600 !important;
  font-size: 0.81rem !important;
  color: #8B9AB5 !important;
  margin-bottom: 0.38rem !important;
  text-transform: uppercase !important;
  letter-spacing: 0.07em !important;
}

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
  align-items: center;
  padding: 1.3rem 1.6rem 1.1rem;
  gap: 1rem;
  border-bottom: 1px solid rgba(255,255,255,0.05);
}
.vcti {
  font-family: var(--fd);
  font-size: 1.18rem;
  font-weight: 800;
  letter-spacing: -0.025em;
  color: var(--t1);
}

/* Araç özellik grid */
.vc-specs {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(110px, 1fr));
  gap: 0;
}
.vc-spec {
  padding: 0.9rem 1.35rem;
  border-right: 1px solid rgba(255,255,255,0.04);
}
.vc-spec:last-child { border-right: none; }
.vc-spec-label {
  font-size: 0.63rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  color: #506070;
  margin-bottom: 0.32rem;
  text-transform: none;
}
.vc-spec-value {
  font-size: 0.98rem;
  font-weight: 700;
  color: #D1E0EF;
  letter-spacing: -0.01em;
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
.vcpr {
  border-top: 1px solid rgba(255, 255, 255, 0.06);
  background: linear-gradient(135deg, rgba(0, 196, 140, 0.04), rgba(0, 0, 0, 0));
}
.vcpb {
  padding: 1.25rem 1.6rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.75rem;
}
.vcpl {
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  color: #6B82A0;
  margin-bottom: 0;
}
.vcpv {
  font-family: var(--fm);
  font-size: 1.35rem;
  font-weight: 800;
  letter-spacing: -0.02em;
  color: var(--t1);
}
.vcpv.em {
  font-size: 1.55rem;
  color: #00FFB3;
  text-shadow: 0 0 28px rgba(0, 255, 179, 0.45);
  letter-spacing: -0.03em;
}

.dtag {
  display: inline-flex;
  align-items: center;
  gap: 5px;
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
''')
