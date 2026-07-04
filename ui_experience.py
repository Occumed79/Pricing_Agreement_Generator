from __future__ import annotations

import base64
from pathlib import Path
from typing import List, Tuple

import streamlit as st


ASSET_DIR = Path(__file__).parent / "assets"
LOGO_PATH = ASSET_DIR / "occu-med-logo.png"


def _asset_data_uri(path: Path) -> str:
    if not path.exists():
        return ""
    suffix = path.suffix.lower().lstrip(".") or "png"
    mime = "image/svg+xml" if suffix == "svg" else f"image/{suffix}"
    encoded = base64.b64encode(path.read_bytes()).decode("utf-8")
    return f"data:{mime};base64,{encoded}"


def logo_markup() -> str:
    logo_src = _asset_data_uri(LOGO_PATH)
    if logo_src:
        return f"""
        <div class="brand-logo" aria-label="Occu-Med logo">
          <img class="brand-image" src="{logo_src}" alt="Occu-Med logo" />
        </div>
        """
    return """
    <div class="brand-logo brand-logo-fallback" aria-label="Occu-Med logo">
      OCCU-MED
    </div>
    """


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
          --om-mist: #ACC8C9;
          --om-ink: #050913;
          --glass-line: rgba(172, 200, 201, .30);
          --text-main: rgba(248, 251, 255, .96);
          --text-soft: rgba(228, 238, 244, .78);
        }

        html, body, .stApp { min-height: 100%; }
        .stApp {
          color: var(--text-main);
          background:
            radial-gradient(circle at 8% 12%, rgba(77,124,138,.34), transparent 30%),
            radial-gradient(circle at 88% 4%, rgba(203,223,144,.12), transparent 28%),
            radial-gradient(circle at 50% 100%, rgba(27,64,121,.36), transparent 44%),
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
          opacity: .11;
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

        [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stStatusWidget"] { background: transparent !important; }
        [data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stStatusWidget"] { visibility: hidden !important; height: 0 !important; }
        footer { visibility: hidden !important; }
        .block-container { position: relative; z-index: 1; max-width: 1180px; padding-top: 2.25rem; }

        h1, h2, h3, h4, h5, h6,
        p, label, span, div[data-testid="stMarkdownContainer"],
        [data-testid="stWidgetLabel"], [data-testid="stWidgetLabel"] p,
        [data-testid="stWidgetLabel"] *, [data-testid="stCaptionContainer"],
        [data-testid="stCaptionContainer"] *, [data-testid="stText"],
        [data-testid="stExpander"] *, [data-testid="stForm"] label,
        [data-testid="stFileUploader"] label, [data-testid="stFileUploader"] small {
          color: var(--text-main) !important;
          opacity: 1 !important;
        }
        .stCaptionContainer, small, .stMarkdown p,
        [data-testid="stCaptionContainer"] *, [data-testid="stFileUploader"] small {
          color: var(--text-soft) !important;
        }

        .hero,
        .status-box,
        div[data-testid="stForm"],
        div[data-testid="stFileUploader"] section,
        div[data-testid="stFileUploaderDropzone"] {
          position: relative;
          border: 1px solid var(--glass-line) !important;
          border-radius: 28px !important;
          background: linear-gradient(135deg, rgba(172,200,201,.14), rgba(27,64,121,.18) 44%, rgba(28,40,46,.48)) !important;
          box-shadow: 0 24px 80px rgba(0,0,0,.42), inset 0 1px 0 rgba(255,255,255,.12) !important;
          backdrop-filter: blur(22px) saturate(155%);
          -webkit-backdrop-filter: blur(22px) saturate(155%);
        }
        .hero::after,
        .status-box::after,
        div[data-testid="stForm"]::after,
        div[data-testid="stFileUploader"] section::after,
        div[data-testid="stFileUploaderDropzone"]::after {
          content: "";
          position: absolute;
          inset: 10px;
          border: 1px solid rgba(255,255,255,.09);
          border-radius: 20px;
          pointer-events: none;
          box-shadow: inset 0 0 0 1px rgba(0,0,0,.18);
        }
        .hero { padding: 34px 40px; margin-bottom: 20px; }
        .hero h1 { margin: 0 0 10px 0; font-size: clamp(2rem, 4vw, 3.18rem); letter-spacing: -.055em; }
        .hero p { color: var(--text-soft) !important; font-size: 1.05rem; line-height: 1.65; max-width: 920px; }
        .status-box { padding: 15px 18px; margin: 12px 0 20px; }

        input, textarea,
        [data-testid="stTextInput"] input,
        [data-testid="stTextArea"] textarea,
        [data-testid="stNumberInput"] input,
        [data-testid="stDateInput"] input,
        [data-testid="stTimeInput"] input,
        [data-baseweb="select"],
        [data-baseweb="select"] > div,
        [data-baseweb="input"],
        [data-baseweb="input"] > div,
        [data-baseweb="textarea"],
        [data-baseweb="textarea"] > div {
          color: #f8fbff !important;
          background: rgba(5, 10, 18, .82) !important;
          border-color: rgba(172,200,201,.32) !important;
          border-radius: 13px !important;
          box-shadow: inset 0 1px 0 rgba(255,255,255,.07), 0 0 0 1px rgba(0,0,0,.18) !important;
        }
        input:focus, textarea:focus,
        [data-testid="stTextInput"] input:focus,
        [data-testid="stTextArea"] textarea:focus,
        [data-testid="stNumberInput"] input:focus,
        [data-baseweb="select"]:focus-within,
        [data-baseweb="input"]:focus-within,
        [data-baseweb="textarea"]:focus-within {
          border-color: rgba(203,223,144,.72) !important;
          box-shadow: 0 0 0 1px rgba(203,223,144,.34), 0 0 28px rgba(77,124,138,.26) !important;
          outline: none !important;
        }
        input::placeholder, textarea::placeholder { color: rgba(230,238,244,.48) !important; }
        [data-baseweb="select"] span,
        [data-baseweb="select"] div,
        [data-baseweb="select"] svg,
        [data-baseweb="input"] *,
        [data-baseweb="textarea"] * {
          color: #f8fbff !important;
          fill: #f8fbff !important;
        }
        [data-baseweb="popover"], [data-baseweb="menu"] {
          background: #101B24 !important;
          color: #f8fbff !important;
          border: 1px solid rgba(172,200,201,.28) !important;
          box-shadow: 0 22px 70px rgba(0,0,0,.44) !important;
        }
        [role="option"] { color: #f8fbff !important; background: #101B24 !important; }
        [role="option"]:hover, [aria-selected="true"][role="option"] { background: rgba(77,124,138,.42) !important; }
        div[data-testid="stRadio"] label,
        div[data-testid="stCheckbox"] label,
        div[data-testid="stRadio"] label *,
        div[data-testid="stCheckbox"] label * {
          color: var(--text-main) !important;
          opacity: 1 !important;
        }
        input[type="radio"], input[type="checkbox"] { accent-color: var(--om-mindaro) !important; }
        .stButton > button, .stDownloadButton > button,
        button[kind="primary"], button[kind="secondary"],
        [data-testid="stFileUploader"] button {
          border-radius: 16px !important;
          border: 1px solid rgba(203,223,144,.36) !important;
          color: #f8fbff !important;
          background: linear-gradient(135deg, rgba(77,124,138,.82), rgba(27,64,121,.75)) !important;
          box-shadow: 0 0 30px rgba(77,124,138,.22) !important;
          font-weight: 800 !important;
        }
        .stButton > button *, .stDownloadButton > button *,
        button[kind="primary"] *, button[kind="secondary"] *,
        [data-testid="stFileUploader"] button * { color: #f8fbff !important; }
        .stButton > button:hover, .stDownloadButton > button:hover,
        button[kind="primary"]:hover, button[kind="secondary"]:hover,
        [data-testid="stFileUploader"] button:hover {
          border-color: rgba(203,223,144,.62) !important;
          box-shadow: 0 0 40px rgba(203,223,144,.16) !important;
        }
        div[data-testid="stAlert"] {
          color: var(--text-main) !important;
          background: rgba(27,64,121,.40) !important;
          border: 1px solid rgba(172,200,201,.22) !important;
          border-radius: 16px !important;
        }
        div[data-testid="stAlert"] * { color: var(--text-main) !important; }
        div[data-testid="stDataFrame"], div[data-testid="stTable"], div[data-testid="stDataFrameResizable"] {
          border-radius: 18px !important;
          overflow: hidden !important;
          border: 1px solid rgba(172,200,201,.24) !important;
          box-shadow: 0 18px 50px rgba(0,0,0,.28) !important;
          background: rgba(5, 10, 18, .55) !important;
        }

        .landing-stage {
          min-height: calc(100vh - 8px);
          width: 100vw;
          display: grid;
          place-items: center;
          position: relative;
          overflow: hidden;
          margin: -1.75rem calc(50% - 50vw) 0;
          padding: 18px 24px;
          box-sizing: border-box;
        }
        .landing-click {
          display: block;
          position: relative;
          width: min(1500px, calc(100vw - 48px));
          height: min(900px, calc(100vh - 54px));
          min-height: 760px;
          text-decoration: none !important;
          color: inherit !important;
          border-radius: 42px;
          overflow: hidden;
          border: 1px solid rgba(172,200,201,.18);
          background: radial-gradient(circle at 50% 48%, rgba(77,124,138,.28), transparent 34%), radial-gradient(circle at 18% 54%, rgba(27,64,121,.38), transparent 35%), linear-gradient(135deg, rgba(28,40,46,.86), rgba(6,12,22,.96));
          box-shadow: 0 34px 120px rgba(0,0,0,.50), inset 0 1px 0 rgba(255,255,255,.10);
        }
        .landing-click::before {
          content: "";
          position: absolute;
          inset: -18%;
          background: linear-gradient(115deg, transparent 22%, rgba(77,124,138,.32) 42%, rgba(203,223,144,.14) 50%, transparent 66%), radial-gradient(ellipse at center, rgba(27,64,121,.34), transparent 58%);
          filter: blur(18px);
          animation: omRibbonSweep 18s ease-in-out infinite alternate;
        }
        .landing-click::after {
          content: "";
          position: absolute;
          inset: 18px;
          border: 1px solid rgba(255,255,255,.09);
          border-radius: 30px;
          pointer-events: none;
        }
        .landing-logo-wrap {
          position: absolute;
          inset: 0;
          display: grid;
          place-items: center;
          z-index: 5;
          pointer-events: none;
        }
        .landing-logo-halo {
          position: absolute;
          width: min(550px, 64vw);
          height: min(330px, 40vw);
          border-radius: 50%;
          background: radial-gradient(ellipse at center, rgba(172,200,201,.28), rgba(77,124,138,.14) 38%, transparent 68%);
          filter: blur(16px);
          animation: haloPulse 7s ease-in-out infinite;
        }
        .brand-logo {
          position: relative;
          z-index: 2;
          display: grid;
          place-items: center;
          filter: drop-shadow(0 0 24px rgba(172,200,201,.45)) drop-shadow(0 0 50px rgba(27,64,121,.50));
        }
        .brand-image {
          width: min(620px, 58vw);
          max-height: min(340px, 42vh);
          object-fit: contain;
          display: block;
        }
        .brand-logo-fallback {
          color: #ffffff;
          font-family: Georgia, 'Times New Roman', serif;
          font-weight: 800;
          font-size: clamp(2.3rem, 5.2vw, 4.6rem);
          letter-spacing: .13em;
        }

        .price-sheet {
          position: absolute;
          z-index: 2;
          width: 235px;
          min-height: 285px;
          padding: 24px 22px;
          border: 1px solid rgba(172,200,201,.26);
          border-radius: 8px;
          background: linear-gradient(160deg, rgba(27,64,121,.34), rgba(28,40,46,.72));
          box-shadow: 0 20px 50px rgba(0,0,0,.42), inset 0 1px 0 rgba(255,255,255,.10), 0 0 28px rgba(77,124,138,.12);
          backdrop-filter: blur(8px);
          animation: sheetFloat 9s ease-in-out infinite;
          --dx: 12px;
          --dy: -16px;
          --r: -7deg;
        }
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

        @media (max-width: 820px) {
          .landing-click { width: calc(100vw - 24px); height: calc(100vh - 48px); min-height: 680px; }
          .price-sheet { width: 190px; min-height: 235px; padding: 18px; opacity: .68; }
          .s2, .s5, .s7 { display: none; }
          .block-container { padding-left: 1rem; padding-right: 1rem; }
          .brand-image { width: min(520px, 72vw); }
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
    st.markdown(
        """
        <style>
        html, body, .stApp, [data-testid="stAppViewContainer"], section.main {
          height: 100vh !important;
          max-height: 100vh !important;
          overflow: hidden !important;
        }
        .block-container {
          max-width: none !important;
          padding: 0 !important;
        }
        .landing-stage {
          height: 100vh !important;
          min-height: 100vh !important;
          margin: 0 calc(50% - 50vw) !important;
          padding: 12px 18px !important;
        }
        .landing-click {
          width: calc(100vw - 36px) !important;
          height: calc(100vh - 24px) !important;
          min-height: 0 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
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
    html = f"""
    <div class="landing-stage">
      <a class="landing-click" href="?view=app" aria-label="Open pricing agreement generator">
        {sheets}
        <div class="landing-logo-wrap">
          <div class="landing-logo-halo"></div>
          {logo_markup()}
        </div>
      </a>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
    st.stop()
