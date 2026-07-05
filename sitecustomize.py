"""Runtime UI polish for the Streamlit app shell.

Python automatically imports sitecustomize on startup when it is on sys.path.
This lets us apply a small CSS override without touching the working app logic or
landing-page renderer.
"""

from __future__ import annotations

APP_LAYOUT_CSS = """
<style>
/* App view polish only. These selectors intentionally use high specificity so
   they win over the base luminous CSS without touching the backend behavior. */
html body .stApp [data-testid="stAppViewContainer"] .block-container {
  max-width: 1060px !important;
  padding-top: 1.05rem !important;
  padding-left: 1.25rem !important;
  padding-right: 1.25rem !important;
  padding-bottom: 3rem !important;
}

html body .stApp .hero {
  padding: 24px 30px !important;
  margin: 0 0 12px 0 !important;
  border-radius: 24px !important;
  box-shadow: 0 18px 54px rgba(0,0,0,.34), inset 0 1px 0 rgba(255,255,255,.12) !important;
}
html body .stApp .hero h1 {
  font-size: clamp(2rem, 3.25vw, 2.75rem) !important;
  line-height: 1.05 !important;
  margin: 0 0 8px 0 !important;
}
html body .stApp .hero p {
  font-size: .98rem !important;
  line-height: 1.55 !important;
  max-width: 860px !important;
  margin: 0 !important;
}

html body .stApp div[data-testid="stVerticalBlock"] {
  gap: .68rem !important;
}
html body .stApp h2,
html body .stApp h3 {
  margin-top: 1.05rem !important;
  margin-bottom: .45rem !important;
}
html body .stApp .status-box {
  padding: 11px 16px !important;
  margin: 10px 0 16px 0 !important;
  border-radius: 20px !important;
}

html body .stApp div[data-testid="stTabs"] {
  margin-top: .35rem !important;
}
html body .stApp div[data-testid="stTabs"] [role="tablist"] {
  gap: 16px !important;
  border-bottom: 1px solid rgba(172,200,201,.13) !important;
}
html body .stApp div[data-testid="stTabs"] [role="tab"] {
  color: rgba(248,251,255,.84) !important;
  padding: 8px 0 10px 0 !important;
  font-size: .92rem !important;
}
html body .stApp div[data-testid="stTabs"] [aria-selected="true"] {
  color: #f8fbff !important;
  border-bottom-color: #CBDF90 !important;
}

html body .stApp .glass-table-wrap {
  margin: 10px 0 18px 0 !important;
  border-radius: 16px !important;
  overflow: hidden !important;
  border: 1px solid rgba(172,200,201,.18) !important;
  background: rgba(5,10,18,.24) !important;
}
html body .stApp .glass-table {
  width: 100% !important;
  border-collapse: collapse !important;
  font-size: .92rem !important;
}
html body .stApp .glass-table th,
html body .stApp .glass-table td {
  padding: 10px 12px !important;
  border-bottom: 1px solid rgba(172,200,201,.11) !important;
  text-align: left !important;
}
html body .stApp .glass-pill {
  display: inline-flex !important;
  padding: 4px 9px !important;
  border-radius: 999px !important;
  border: 1px solid rgba(172,200,201,.24) !important;
  background: rgba(77,124,138,.18) !important;
}

html body .stApp input[type="radio"],
html body .stApp input[type="checkbox"] {
  accent-color: #CBDF90 !important;
}
html body .stApp div[data-testid="stFileUploader"] section,
html body .stApp div[data-testid="stFileUploaderDropzone"],
html body .stApp div[data-testid="stForm"] {
  border-radius: 22px !important;
  box-shadow: 0 16px 44px rgba(0,0,0,.28), inset 0 1px 0 rgba(255,255,255,.10) !important;
}
html body .stApp div[data-testid="stAlert"] {
  border-radius: 14px !important;
}

@media (max-width: 900px) {
  html body .stApp [data-testid="stAppViewContainer"] .block-container {
    padding-left: 1rem !important;
    padding-right: 1rem !important;
  }
  html body .stApp .hero {
    padding: 22px !important;
  }
}
</style>
"""


def _install_patch() -> None:
    try:
        import streamlit as st
    except Exception:
        return

    if getattr(st, "_occu_med_layout_patch_installed", False):
        return

    original_set_page_config = st.set_page_config

    def patched_set_page_config(*args, **kwargs):
        result = original_set_page_config(*args, **kwargs)
        try:
            st.markdown(APP_LAYOUT_CSS, unsafe_allow_html=True)
        except Exception:
            pass
        return result

    st.set_page_config = patched_set_page_config
    st._occu_med_layout_patch_installed = True


_install_patch()
