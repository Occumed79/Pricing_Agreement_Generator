from __future__ import annotations

from pathlib import Path
from typing import List, Tuple

import streamlit as st

BASE_DIR = Path(__file__).parent
LOGO_B64_PATH = BASE_DIR / "assets" / "om-logo.b64"


def logo_data_uri() -> str:
    try:
        data = LOGO_B64_PATH.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        return ""
    if not data:
        return ""
    return f"data:image/png;base64,{data}"


def apply_luminous_ui() -> None:
    st.markdown(
        """
        <style>
        :root {
          --om-blue: #1B4079;
          --om-air: #4D7C8A;
          --om-cambridge: #7F9C96;
          --om-cambridge-2: #8FAD88;
          --om-mindaro: #CBDF90;
          --om-charcoal: #1C282E;
          --om-slate: #547C86;
          --om-mist: #ACC8C9;
          --om-sage: #A0B894;
          --om-olive: #94A85F;
        }

        .stApp {
          color: #f5f8fb;
          background:
            radial-gradient(circle at 10% 10%, rgba(77,124,138,.34), transparent 32%),
            radial-gradient(circle at 88% 4%, rgba(203,223,144,.12), transparent 30%),
            radial-gradient(circle at 52% 100%, rgba(27,64,121,.34), transparent 44%),
            linear-gradient(135deg, #1C282E 0%, #08111E 50%, #05070D 100%);
        }

        .stApp::before {
          content: "";
          position: fixed;
          inset: -30% -12%;
          pointer-events: none;
          z-index: 0;
          opacity: .72;
          filter: blur(34px);
          mix-blend-mode: screen;
          background:
            linear-gradient(110deg, transparent 18%, rgba(77,124,138,.26) 36%, rgba(172,200,201,.16) 44%, rgba(203,223,144,.11) 52%, transparent 72%),
            linear-gradient(245deg, transparent 20%, rgba(27,64,121,.30) 41%, rgba(143,173,136,.16) 56%, transparent 76%);
          animation: omRibbonSweep 20s ease-in-out infinite alternate;
        }

        .stApp::after {
          content: "";
          position: fixed;
          inset: 0;
          pointer-events: none;
          z-index: 0;
          opacity: .13;
          background-image: linear-gradient(rgba(255,255,255,.04) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,.025) 1px, transparent 1px);
          background-size: 48px 48px;
        }

        @keyframes omRibbonSweep {
          0% { transform: translate3d(-8%, -4%, 0) rotate(-7deg) scale(1.02); }
          50% { transform: translate3d(4%, 2%, 0) rotate(4deg) scale(1.08); }
          100% { transform: translate3d(11%, -2%, 0) rotate(10deg) scale(1.03); }
        }

        @keyframes sheetFloat {
          0%, 100% { transform: translate3d(0, 0, 0) rotate(var(--r)); opacity: .72; }
          50% { transform: translate3d(var(--dx), var(--dy), 0) rotate(calc(var(--r) + 2deg)); opacity: .96; }
        }

        @keyframes lineGlow {
          0%, 18% { opacity: .24; text-shadow: none; }
          38%, 70% { opacity: 1; text-shadow: 0 0 10px rgba(203,223,144,.62), 0 0 20px rgba(77,124,138,.42); }
          100% { opacity: .30; text-shadow: none; }
        }

        @keyframes haloPulse {
          0%, 100% { transform: scale(.94); opacity: .32; }
          50% { transform: scale(1.08); opacity: .72; }
        }

        [data-testid="stHeader"], [data-testid="stToolbar"] { background: transparent; }
        .block-container { position: relative; z-index: 1; max-width: 1180px; padding-top: 2.25rem; }

        .hero,
        .status-box,
        div[data-testid="stForm"],
        div[data-testid="stFileUploader"] section {
          position: relative;
          border: 1px solid rgba(172,200,201,.26) !important;
          border-radius: 28px !important;
          background: linear-gradient(135deg, rgba(172,200,201,.16), rgba(27,64,121,.18) 42%, rgba(28,40,46,.50)) !important;
          box-shadow: 0 24px 80px rgba(0,0,0,.42), inset 0 1px 0 rgba(255,255,255,.12) !important;
          backdrop-filter: blur(22px) saturate(155%);
          -webkit-backdrop-filter: blur(22px) saturate(155%);
        }

        .hero::after,
        .status-box::after,
        div[data-testid="stForm"]::after,
        div[data-testid="stFileUploader"] section::after {
          content: "";
          position: absolute;
          inset: 10px;
          border: 1px solid rgba(255,255,255,.09);
          border-radius: 20px;
          pointer-events: none;
          box-shadow: inset 0 0 0 1px rgba(0,0,0,.18);
        }

        .hero { padding: 36px 40px; margin-bottom: 22px; }
        .hero h1 { margin: 0 0 10px 0; font-size: clamp(2rem, 4vw, 3.25rem); letter-spacing: -.055em; color: #f8fbff; }
        .hero p { color: rgba(245,248,251,.82); font-size: 1.05rem; line-height: 1.65; max-width: 920px; }
        .status-box { padding: 16px 18px; margin: 12px 0 20px; color: rgba(245,248,251,.88); }

        .stTabs [data-baseweb="tab-list"] { gap: 12px; }
        .stTabs [data-baseweb="tab"] {
          border-radius: 999px;
          border: 1px solid rgba(172,200,201,.20);
          background: rgba(255,255,255,.055);
          padding: 10px 18px;
        }

        .stButton > button, .stDownloadButton > button {
          border-radius: 16px !important;
          border: 1px solid rgba(203,223,144,.36) !important;
          color: #f8fbff !important;
          background: linear-gradient(135deg, rgba(77,124,138,.80), rgba(27,64,121,.72)) !important;
          box-shadow: 0 0 30px rgba(77,124,138,.22) !important;
          font-weight: 800 !important;
        }

        .landing-stage { min-height: calc(100vh - 32px); display: grid; place-items: center; position: relative; overflow: hidden; margin: -1.5rem -1rem 0; }
        .landing-click {
          display: block;
          position: relative;
          width: min(1180px, 96vw);
          min-height: 760px;
          text-decoration: none !important;
          color: inherit !important;
          border-radius: 42px;
          overflow: hidden;
          border: 1px solid rgba(172,200,201,.18);
          background: radial-gradient(circle at 50% 48%, rgba(77,124,138,.28), transparent 34%), radial-gradient(circle at 18% 54%, rgba(27,64,121,.38), transparent 35%), linear-gradient(135deg, rgba(28,40,46,.86), rgba(6,12,22,.96));
          box-shadow: 0 34px 120px rgba(0,0,0,.50), inset 0 1px 0 rgba(255,255,255,.10);
        }
        .landing-click::before { content: ""; position: absolute; inset: -18%; background: linear-gradient(115deg, transparent 22%, rgba(77,124,138,.32) 42%, rgba(203,223,144,.14) 50%, transparent 66%), radial-gradient(ellipse at center, rgba(27,64,121,.34), transparent 58%); filter: blur(18px); animation: omRibbonSweep 18s ease-in-out infinite alternate; }
        .landing-click::after { content: ""; position: absolute; inset: 18px; border: 1px solid rgba(255,255,255,.09); border-radius: 30px; pointer-events: none; }
        .landing-logo-wrap { position: absolute; inset: 0; display: grid; place-items: center; z-index: 5; pointer-events: none; }
        .landing-logo-halo { position: absolute; width: min(550px, 64vw); height: min(330px, 40vw); border-radius: 50%; background: radial-gradient(ellipse at center, rgba(172,200,201,.28), rgba(77,124,138,.14) 38%, transparent 68%); filter: blur(16px); animation: haloPulse 7s ease-in-out infinite; }
        .landing-logo { width: min(420px, 58vw); height: auto; position: relative; z-index: 2; filter: drop-shadow(0 0 24px rgba(172,200,201,.45)) drop-shadow(0 0 50px rgba(27,64,121,.50)); }
        .fallback-logo { font-size: clamp(2.5rem, 7vw, 5.2rem); letter-spacing: .16em; font-weight: 900; position: relative; z-index: 2; }

        .price-sheet { position: absolute; z-index: 2; width: 235px; min-height: 285px; padding: 24px 22px; border: 1px solid rgba(172,200,201,.26); border-radius: 8px; background: linear-gradient(160deg, rgba(27,64,121,.34), rgba(28,40,46,.72)); box-shadow: 0 20px 50px rgba(0,0,0,.42), inset 0 1px 0 rgba(255,255,255,.10), 0 0 28px rgba(77,124,138,.12); backdrop-filter: blur(8px); animation: sheetFloat 9s ease-in-out infinite; --dx: 12px; --dy: -16px; --r: -7deg; }
        .price-sheet::after { content: ""; position: absolute; inset: 8px; border: 1px solid rgba(255,255,255,.07); border-radius: 5px; pointer-events: none; }
        .price-title { text-align: center; font-weight: 900; letter-spacing: .12em; font-size: .78rem; color: #f7fbff; margin-bottom: 16px; text-transform: uppercase; }
        .line { display: grid; grid-template-columns: 1fr auto; gap: 14px; align-items: center; padding: 8px 0; border-bottom: 1px solid rgba(172,200,201,.18); color: rgba(245,248,251,.86); font-size: .82rem; animation: lineGlow 6.4s ease-in-out infinite; animation-delay: var(--delay); }
        .line span:last-child { color: #f2ffe0; }
        .s1 { left: 3%; top: 16%; --r: -7deg; --dx: 16px; --dy: -18px; }
        .s2 { left: 29%; top: 6%; transform: scale(.72); --r: -4deg; --dx: -10px; --dy: 18px; animation-duration: 11s; }
        .s3 { right: 7%; top: 12%; --r: 8deg; --dx: -18px; --dy: -12px; animation-duration: 10s; }
        .s4 { left: 21%; bottom: 9%; transform: scale(.74); --r: -6deg; --dx: 18px; --dy: 15px; animation-duration: 12s; }
        .s5 { right: 26%; bottom: 11%; transform: scale(.78); --r: 7deg; --dx: -10px; --dy: 12px; animation-duration: 9.5s; }
        .s6 { right: 12%; bottom: 26%; transform: scale(.82); --r: 11deg; --dx: 12px; --dy: -12px; animation-duration: 13s; }
        .s7 { left: 44%; top: 2%; transform: scale(.66); --r: -5deg; --dx: 8px; --dy: 20px; animation-duration: 14s; opacity: .58; }
        .enter-copy { position: absolute; left: 50%; bottom: 34px; transform: translateX(-50%); z-index: 8; color: rgba(245,248,251,.70); font-size: .92rem; letter-spacing: .12em; text-transform: uppercase; }

        @media (max-width: 820px) {
          .landing-click { min-height: 680px; }
          .price-sheet { width: 190px; min-height: 235px; padding: 18px; opacity: .68; }
          .s2, .s5, .s7 { display: none; }
          .block-container { padding-left: 1rem; padding-right: 1rem; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _landing_sheet(sheet_class: str, rows: List[Tuple[str, str]]) -> str:
    lines = []
    for idx, (service, price) in enumerate(rows):
        delay = f"{idx * 0.55:.2f}s"
        lines.append(f"<div class='line' style='--delay:{delay}'><span>{service}</span><span>{price}</span></div>")
    return f"<div class='price-sheet {sheet_class}'><div class='price-title'>Pricing Agreement</div>{''.join(lines)}</div>"


def render_landing_page() -> None:
    logo_uri = logo_data_uri()
    logo_html = f"<img class='landing-logo' src='{logo_uri}' alt='Occu-Med logo'>" if logo_uri else "<div class='fallback-logo'>OCCU-MED</div>"
    services = [
        ("General Physical Exam", "$125.00"),
        ("Audiogram", "$45.00"),
        ("Chest X-Ray", "$75.00"),
        ("Resting EKG", "$65.00"),
        ("Treadmill Stress Test", "$210.00"),
        ("Pulmonary Function Test", "$85.00"),
        ("Dental Evaluation", "$60.00"),
        ("Bitewing Radiographs", "$35.00"),
    ]
    alt_services = [
        ("Exam Packet Review", "$40.00"),
        ("Venipuncture", "$22.00"),
        ("Drug Screen Collection", "$30.00"),
        ("Respirator Fit Test", "$55.00"),
        ("Vision Screening", "$25.00"),
        ("Vaccine Admin", "$35.00"),
    ]
    sheets = "\n".join([
        _landing_sheet("s1", services),
        _landing_sheet("s2", alt_services),
        _landing_sheet("s3", services[:6]),
        _landing_sheet("s4", services[1:7]),
        _landing_sheet("s5", alt_services),
        _landing_sheet("s6", services[2:]),
        _landing_sheet("s7", services[:5]),
    ])
    html = """
    <div class="landing-stage">
      <a class="landing-click" href="?view=app" aria-label="Open pricing agreement generator">
        __SHEETS__
        <div class="landing-logo-wrap">
          <div class="landing-logo-halo"></div>
          __LOGO__
        </div>
        <div class="enter-copy">Click anywhere to enter</div>
      </a>
    </div>
    """
    st.markdown(html.replace("__SHEETS__", sheets).replace("__LOGO__", logo_html), unsafe_allow_html=True)
    st.stop()
