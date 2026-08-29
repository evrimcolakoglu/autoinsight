"""
AutoInsight — Icon & Logo Library
Tüm SVG ikonlar ve logo bileşenleri bu modülde merkezi olarak tanımlanır.
"""

# ─────────────────────────────────────────────
# AutoInsight Özel Vektörel İkon Kütüphanesi
# ─────────────────────────────────────────────
IC: dict[str, str] = {
    "logo_bars": '<div class="logo-box"><div class="lb lb1"></div><div class="lb lb2"></div><div class="lb lb3"></div></div>',

    "valuation_card": '<svg width="34" height="34" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="3" y="13" width="4" height="8" rx="1.5" fill="#00C48C" opacity="0.65"/><rect x="10" y="8" width="4" height="13" rx="1.5" fill="#00FFB3"/><rect x="17" y="3" width="4" height="18" rx="1.5" fill="#38BDF8"/><path d="M4 9L11 4.5L18 7.5" stroke="#00FFB3" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>',

    "discovery_card": '<svg width="34" height="34" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="11" cy="11" r="7.5" stroke="#00FFB3" stroke-width="2.2"/><path d="M16.5 16.5L21.5 21.5" stroke="#00FFB3" stroke-width="2.4" stroke-linecap="round"/><circle cx="11" cy="11" r="3.5" fill="rgba(0,255,179,0.25)"/><path d="M11 7.5V14.5M7.5 11H14.5" stroke="#38BDF8" stroke-width="1.6" stroke-linecap="round"/></svg>',

    "bolt": '<svg class="ai-chip-ic" viewBox="0 0 24 24" fill="none" stroke="#00FFB3" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>',
    "target": '<svg class="ai-chip-ic" viewBox="0 0 24 24" fill="none" stroke="#00FFB3" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>',
    "chart": '<svg class="ai-chip-ic" viewBox="0 0 24 24" fill="none" stroke="#00FFB3" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>',
    "sparkles": '<svg class="ai-chip-ic" viewBox="0 0 24 24" fill="none" stroke="#00FFB3" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/></svg>',
    "star": '<svg class="ai-chip-ic" viewBox="0 0 24 24" fill="none" stroke="#00FFB3" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>',
    "wallet": '<svg class="ai-chip-ic" viewBox="0 0 24 24" fill="none" stroke="#00FFB3" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="14" x="2" y="5" rx="2"/><line x1="2" y1="10" x2="22" y2="10"/><path d="M16 14h.01"/></svg>',
    "flame": '<svg class="ai-chip-ic" viewBox="0 0 24 24" fill="none" stroke="#00FFB3" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 0 0 2.5 2.5z"/></svg>',
    "search_sm": '<svg class="ai-chip-ic" viewBox="0 0 24 24" fill="none" stroke="#00FFB3" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>',

    "shield_bento": '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#00FFB3" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/></svg>',
    "bolt_bento": '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#00FFB3" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>',
    "map_bento": '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#00FFB3" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>',
    "chart_bento": '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#00FFB3" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>',

    "step_params": '<svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="#00FFB3" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="3"/><path d="m9 12 2 2 4-4"/><line x1="3" y1="8" x2="21" y2="8"/></svg>',
    "step_ai": '<svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="#00FFB3" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2a4 4 0 0 0-4 4v1H7a3 3 0 0 0-3 3v2a3 3 0 0 0 3 3h1v1a4 4 0 0 0 8 0v-1h1a3 3 0 0 0 3-3v-2a3 3 0 0 0-3-3h-1V6a4 4 0 0 0-4-4Z"/><path d="M9 10h.01M15 10h.01M10 14h4"/></svg>',
    "step_report": '<svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="#00FFB3" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>',

    "hdr_car": '<svg class="ai-hdr-ic" viewBox="0 0 24 24" fill="none" stroke="#00FFB3" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9C18.7 10.6 16 10 16 10s-1.3-1.4-2.2-2.3c-.5-.4-1.1-.7-1.8-.7H5c-.6 0-1.1.4-1.4.9l-1.4 2.9A3.7 3.7 0 0 0 1 14v2c0 .6.4 1 1 1h2"/><circle cx="7" cy="17" r="2"/><path d="M9 17h6"/><circle cx="17" cy="17" r="2"/></svg>',
    "hdr_gear": '<svg class="ai-hdr-ic" viewBox="0 0 24 24" fill="none" stroke="#00FFB3" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><line x1="4" y1="21" x2="4" y2="14"></line><line x1="4" y1="10" x2="4" y2="3"></line><line x1="12" y1="21" x2="12" y2="12"></line><line x1="12" y1="8" x2="12" y2="3"></line><line x1="20" y1="21" x2="20" y2="16"></line><line x1="20" y1="12" x2="20" y2="3"></line><line x1="1" y1="14" x2="7" y2="14"></line><line x1="9" y1="8" x2="15" y2="8"></line><line x1="17" y1="16" x2="23" y2="16"></line></svg>',
    "hdr_wallet": '<svg class="ai-hdr-ic" viewBox="0 0 24 24" fill="none" stroke="#00FFB3" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="14" x="2" y="5" rx="2"/><line x1="2" y1="10" x2="22" y2="10"/><path d="M16 14h.01"/></svg>',
    "hdr_filter": '<svg class="ai-hdr-ic" viewBox="0 0 24 24" fill="none" stroke="#00FFB3" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon></svg>',

    "check_disc": '<div class="tic"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#00FFB3" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg></div>',
    "bolt_disc": '<div class="tic"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#00FFB3" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg></div>',
    "lock_disc": '<div class="tic"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#00FFB3" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="11" x="3" y="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg></div>',
    "target_disc": '<div class="tic"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#00FFB3" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="3"/></svg></div>',
    "trend_disc": '<div class="tic"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#00FFB3" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg></div>',

    "spark_diamond": '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#00FFB3" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 22 12 12 22 2 12 12 2"/></svg>',
}

LOGO_FULL_SVG: str = f'''
<div style="display: flex; align-items: center; gap: 14px;">
  {IC["logo_bars"]}
  <div style="display: flex; flex-direction: column; justify-content: center;">
    <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1.5rem; font-weight: 800; color: #FFFFFF; letter-spacing: -0.03em; line-height: 1.1;">
      Auto<span style="color: #00FFB3; text-shadow: 0 0 16px rgba(0,255,179,0.4);">Insight</span>
    </div>
    <div style="font-family: 'Space Grotesk', sans-serif; font-size: 0.6rem; font-weight: 700; color: #7A8CA5; letter-spacing: 0.26em; text-transform: uppercase; margin-top: 2px;">
      Akıllı Otomotiv Platformu
    </div>
  </div>
</div>
'''
