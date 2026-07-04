from __future__ import annotations

from typing import List, Tuple

import streamlit as st


def logo_markup() -> str:
    return """
    <div class="brand-logo" aria-label="Occu-Med logo">
      <svg class="brand-mark" viewBox="0 0 320 150" role="img" aria-hidden="true">
        <path d="M42 74C42 32 76 8 116 8H154V142H116C76 142 42 116 42 74Z" />
        <path d="M166 8H204C244 8 278 32 278 74V142H166V8Z" />
        <line x1="156" y1="8" x2="156" y2="142" />
      </svg>
      <div class="brand-word">OCCU-MED</div>
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
          --om-slate: #547C86;
          --om-mist: #ACC8C9;
          --om-sage: #A0B894;
          --om-olive: #94A85F;
          --om-ink: #050913;
          --glass-line: rgba(172, 200, 201, .30);
          --glass-inner: rgba(255, 255, 255, .10);
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
          0%, 100% { translate: 0 0; opacity: .56; }
          50% { translate: var(--dx) var(--dy); opacity: .88; }
        }

        @keyframes lineGlow {
          0%, 18% { opacity: .24; text-shadow: none; }
          38%, 70% { opacity: 1; text-shadow: 0 0 10px rgba(203,223,144,.62), 0 0 20px rgba(77,124,138,.42); }
          100% { opacity: .30; text-shadow: none; }
        }

        @keyframes haloPulse {
          0%, 100% { transform: scale(.94); opacity: .30; }
          50% { transform: scale(1.08); opacity: .68; }
        }

        [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stStatusWidget"] { background: transparent !important; }
        [data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stStatusWidget"] { visibility: hidden !important; height: 0 !important; }
        footer { visibility: hidden !important; }
        .block-container { position: relative; z-index: 1; max-width: 1180px; padding-top: 2.25rem; }

        h1, h2, h3, h4, h5, h6,
        p, label, span, div[data-testid="stMarkdownContainer"],
        [data-testid="stWidgetLabel"], [data-testid="stWidgetLabel"] p {
          color: var(--text-main) !important;
        }

        .stCaptionContainer, small, .stMarkdown p { color: var(--text-soft) !important; }

        .hero,
        .status-box,
        div[data-testid="stForm"],
        div[data-testid="stFileUploader"] section {
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
        div[data-testid="stFileUploader"] section::after {
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

        .stTabs [data-baseweb="tab-list"] { gap: 12px; border-bottom: 1px solid rgba(172,200,201,.12); }
        .stTabs [data-baseweb="tab"] {
          border-radius: 999px !important;
          border: 1px solid rgba(172,200,201,.22) !important;
          background: rgba(255,255,255,.055) !important;
          padding: 10px 18px !important;
          color: rgba(245,248,251,.78) !important;
        }
        .stTabs [aria-selected="true"] {
          color: #F7FFE4 !important;
          border-color: rgba(203,223,144,.48) !important;
          background: linear-gradient(135deg, rgba(77,124,138,.42), rgba(27,64,121,.38)) !important;
          box-shadow: 0 0 26px rgba(77,124,138,.18) !important;
        }

        input, textarea,
        [data-baseweb="select"] > div,
        [data-baseweb="input"] > div,
        [data-baseweb="textarea"] > div {
          color: #f8fbff !important;
          background: rgba(5, 10, 18, .76) !important;
          border-color: rgba(172,200,201,.26) !important;
          border-radius: 13px !important;
          box-shadow: inset 0 1px 0 rgba(255,255,255,.06), 0 0 0 1px rgba(0,0,0,.10) !important;
        }

        input::placeholder, textarea::placeholder { color: rgba(230,238,244,.46) !important; }
        [data-baseweb="select"] span, [data-baseweb="select"] div { color: #f8fbff !important; }
        [data-baseweb="popover"], [data-baseweb="menu"] { background: #101B24 !important; color: #f8fbff !important; }
        [role="option"] { color: #f8fbff !important; background: #101B24 !important; }
        [role="option"]:hover { background: rgba(77,124,138,.35) !important; }

        div[data-testid="stRadio"] label,
        div[data-testid="stCheckbox"] label {
          color: var(--text-main) !important;
        }

        .stButton > button, .stDownloadButton > button {
          border-radius: 16px !important;
          border: 1px solid rgba(203,223,144,.36) !important;
          color: #f8fbff !important;
          background: linear-gradient(135deg, rgba(77,124,138,.82), rgba(27,64,121,.75)) !important;
          box-shadow: 0 0 30px rgba(77,124,138,.22) !important;
          font-weight: 800 !important;
        }
        .stButton > button:hover, .stDownloadButton > button:hover {
          border-color: rgba(203,223,144,.62) !important;
          box-shadow: 0 0 40px rgba(203,223,144,.16) !important;
        }

        div[data-testid="stAlert"] {
          color: var(--text-main) !important;
          background: rgba(27,64,121,.40) !important;
          border: 1px solid rgba(172,200,201,.22) !important;
          border-radius: 16px !important;
        }

        div[data-testid="stDataFrame"] {
          border-radius: 18px !important;
          overflow: hidden !important;
          border: 1px solid rgba(172,200,201,.24) !important;
          box-shadow: 0 18px 50px rgba(0,0,0,.28) !important;
        }

        .landing-stage {
          min-height: calc(100vh - 28px);
          display: grid;
          place-items: center;
          position: relative;
          overflow: hidden;
          margin: -1.5rem -1rem 0;
        }

        .landing-click {
          display: block;
          position: relative;
          width: min(1160px, 96vw);
          min-height: min(720px, calc(100vh - 80px));
          text-decoration: none !important;
          color: inherit !important;
          border-radius: 38px;
          overflow: hidden;
          border: 1px solid rgba(172,200,201,.14);
          background: radial-gradient(circle at 50% 48%, rgba(77,124,138,.25), transparent 34%), radial-gradient(circle at 18% 54%, rgba(27,64,121,.34), transparent 35%), linear-gradient(135deg, rgba(28,40,46,.72), rgba(6,12,22,.94));
          box-shadow: 0 34px 120px rgba(0,0,0,.48), inset 0 1px 0 rgba(255,255,255,.08);
        }
        .landing-click::before { content: ""; position: absolute; inset: -18%; background: linear-gradient(115deg, transparent 22%, rgba(77,124,138,.30) 42%, rgba(203,223,144,.13) 50%, transparent 66%), radial-gradient(ellipse at center, rgba(27,64,121,.32), transparent 58%); filter: blur(18px); animation: omRibbonSweep 18s ease-in-out infinite alternate; }
        .landing-click::after { content: ""; position: absolute; inset: 18px; border: 1px solid rgba(255,255,255,.08); border-radius: 28px; pointer-events: none; }

        .landing-logo-wrap { position: absolute; inset: 0; display: grid; place-items: center; z-index: 8; pointer-events: none; }
        .landing-logo-halo { position: absolute; width: min(500px, 58vw); height: min(290px, 34vw); border-radius: 50%; background: radial-gradient(ellipse at center, rgba(172,200,201,.25), rgba(77,124,138,.14) 38%, transparent 70%); filter: blur(16px); animation: haloPulse 7s ease-in-out infinite; }
        .brand-logo { position: relative; z-index: 2; display: grid; place-items: center; gap: 22px; filter: drop-shadow(0 0 24px rgba(172,200,201,.45)) drop-shadow(0 0 56px rgba(27,64,121,.48)); }
        .brand-mark { width: min(260px, 35vw); height: auto; overflow: visible; }
        .brand-mark path { fill: #ffffff; }
        .brand-mark line { stroke: #06101A; stroke-width: 8; stroke-linecap: square; }
        .brand-word { font-size: clamp(2.1rem, 5vw, 4.1rem); line-height: 1; letter-spacing: .13em; font-weight: 800; color: #ffffff; font-family: Georgia, 'Times New Roman', serif; }

        .price-sheet { position: absolute; z-index: 2; width: 225px; min-height: 272px; padding: 22px 20px; border: 1px solid rgba(172,200,201,.22); border-radius: 8px; background: linear-gradient(160deg, rgba(27,64,121,.30), rgba(28,40,46,.64)); box-shadow: 0 20px 50px rgba(0,0,0,.36), inset 0 1px 0 rgba(255,255,255,.09), 0 0 28px rgba(77,124,138,.10); backdrop-filter: blur(8px); animation: sheetFloat 9s ease-in-out infinite; --dx: 12px; --dy: -16px; --r: -7deg; transform: rotate(var(--r)); }
        .price-sheet::after { content: ""; position: absolute; inset: 8px; border: 1px solid rgba(255,255,255,.06); border-radius: 5px; pointer-events: none; }
        .price-title { text-align: center; font-weight: 900; letter-spacing: .12em; font-size: .72rem; color: #f7fbff; margin-bottom: 14px; text-transform: uppercase; }
        .line { display: grid; grid-template-columns: 1fr auto; gap: 12px; align-items: center; padding: 7px 0; border-bottom: 1px solid rgba(172,200,201,.16); color: rgba(245,248,251,.80); font-size: .77rem; animation: lineGlow 6.4s ease-in-out infinite; animation-delay: var(--delay); }
        .line span:last-child { color: #f2ffe0; }
        .s1 { left: 4%; top: 15%; --r: -6deg; --dx: 16px; --dy: -18px; }
        .s2 { left: 32%; top: 5%; transform: rotate(-3deg) scale(.70); --r: -3deg; --dx: -10px; --dy: 18px; animation-duration: 11s; }
        .s3 { right: 4%; top: 12%; --r: 8deg; --dx: -18px; --dy: -12px; animation-duration: 10s; }
        .s4 { left: 22%; bottom: 8%; transform: rotate(-5deg) scale(.72); --r: -5deg; --dx: 18px; --dy: 15px; animation-duration: 12s; }
        .s5 { right: 26%; bottom: 7%; transform: rotate(7deg) scale(.72); --r: 7deg; --dx: -10px; --dy: 12px; animation-duration: 9.5s; }
        .s6 { right: 10%; bottom: 25%; transform: rotate(10deg) scale(.76); --r: 10deg; --dx: 12px; --dy: -12px; animation-duration: 13s; }
        .s7 { display: none; }
        .enter-copy { position: absolute; left: 50%; bottom: 32px; transform: translateX(-50%); z-index: 9; color: rgba(245,248,251,.72); font-size: .88rem; letter-spacing: .16em; text-transform: uppercase; }

        @media (max-width: 820px) {
          .landing-click { min-height: 650px; }
          .price-sheet { width: 185px; min-height: 225px; padding: 17px; opacity: .60; }
          .s2, .s5, .s6, .s7 { display: none; }
          .block-container { padding-left: 1rem; padding-right: 1rem; }
          .brand-mark { width: min(210px, 48vw); }
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
    st.markdown(html.replace("__SHEETS__", sheets).replace("__LOGO__", logo_markup()), unsafe_allow_html=True)
    st.stop()
