from __future__ import annotations

import hashlib
import io
import os
import re
import uuid
import zipfile
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import pandas as pd
import streamlit as st
from docx import Document
from docx.enum.text import WD_COLOR_INDEX

try:
    import psycopg
    from psycopg.rows import dict_row
except Exception:
    psycopg = None
    dict_row = None

APP_TITLE = "Pricing Agreement Generator"
TEMPLATE_DIR = Path(__file__).parent / "templates"
DOCX_MIME = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
AUTO_DETECT_LABEL = "Auto-detect from provider address"


@dataclass
class TemplateMeta:
    id: str
    name: str
    category: str
    requires_code: bool
    description: str
    source: str
    filename: str
    is_default: bool = False
    path: Optional[Path] = None
    bytes_data: Optional[bytes] = None
    file_sha256: str = ""


DEFAULT_TEMPLATES: List[TemplateMeta] = [
    TemplateMeta(
        id="default-overseas-medical-pricing-agreement",
        name="Overseas Medical Pricing Agreement",
        category="Overseas",
        requires_code=True,
        description="International medical pricing agreement. Gray highlights are filled with the currency code.",
        source="default",
        filename="Overseas Medical Pricing Agreement.docx",
        is_default=True,
        path=TEMPLATE_DIR / "Overseas Medical Pricing Agreement.docx",
    ),
    TemplateMeta(
        id="default-medical-pricing-agreement-2026",
        name="1 - Medical Pricing Agreement - 2026",
        category="United States - Medical",
        requires_code=False,
        description="US medical pricing agreement.",
        source="default",
        filename="1 - Medical Pricing Agreement - 2026.docx",
        is_default=True,
        path=TEMPLATE_DIR / "1 - Medical Pricing Agreement - 2026.docx",
    ),
    TemplateMeta(
        id="default-dental-pricing-agreement-2025",
        name="2 - Dental Pricing Agreement -2025",
        category="United States - Dental",
        requires_code=False,
        description="US dental pricing agreement.",
        source="default",
        filename="2 - Dental Pricing Agreement -2025.docx",
        is_default=True,
        path=TEMPLATE_DIR / "2 - Dental Pricing Agreement -2025.docx",
    ),
    TemplateMeta(
        id="default-cardiovascular-components-2026",
        name="13 - Cardiovascular Components - 2026",
        category="United States - Cardiology",
        requires_code=False,
        description="US cardiology/cardiovascular pricing agreement.",
        source="default",
        filename="13 - Cardiovascular Components - 2026.docx",
        is_default=True,
        path=TEMPLATE_DIR / "13 - Cardiovascular Components - 2026.docx",
    ),
]

HIGHLIGHT_TO_FIELD = {
    WD_COLOR_INDEX.YELLOW: "name",
    WD_COLOR_INDEX.BRIGHT_GREEN: "address",
    WD_COLOR_INDEX.GREEN: "address",
    WD_COLOR_INDEX.TURQUOISE: "date",
    WD_COLOR_INDEX.BLUE: "date",
    WD_COLOR_INDEX.TEAL: "date",
    WD_COLOR_INDEX.GRAY_25: "code",
    WD_COLOR_INDEX.GRAY_50: "code",
}

COUNTRY_CURRENCY: Dict[str, str] = {
    "Australia": "AUD",
    "Austria": "EUR",
    "Belgium": "EUR",
    "Brazil": "BRL",
    "Canada": "CAD",
    "China": "CNY",
    "Denmark": "DKK",
    "France": "EUR",
    "Germany": "EUR",
    "India": "INR",
    "Ireland": "EUR",
    "Israel": "ILS",
    "Italy": "EUR",
    "Japan": "JPY",
    "Mexico": "MXN",
    "Netherlands": "EUR",
    "New Zealand": "NZD",
    "Norway": "NOK",
    "Philippines": "PHP",
    "Saudi Arabia": "SAR",
    "South Africa": "ZAR",
    "South Korea": "KRW",
    "Spain": "EUR",
    "Sweden": "SEK",
    "Switzerland": "CHF",
    "Thailand": "THB",
    "Turkey": "TRY",
    "United Arab Emirates": "AED",
    "United Kingdom": "GBP",
    "United States": "USD",
}

COUNTRY_ALIASES = {
    "usa": "United States",
    "us": "United States",
    "u.s.": "United States",
    "u.s.a.": "United States",
    "america": "United States",
    "uk": "United Kingdom",
    "u.k.": "United Kingdom",
    "england": "United Kingdom",
    "scotland": "United Kingdom",
    "wales": "United Kingdom",
    "uae": "United Arab Emirates",
    "u.a.e.": "United Arab Emirates",
    "emirates": "United Arab Emirates",
    "korea": "South Korea",
    "republic of korea": "South Korea",
    "nz": "New Zealand",
}

COUNTRY_PATTERNS: List[Tuple[str, str]] = sorted(
    [(country.lower(), country) for country in COUNTRY_CURRENCY] + list(COUNTRY_ALIASES.items()),
    key=lambda item: len(item[0]),
    reverse=True,
)


def page_style() -> None:
    st.set_page_config(page_title=APP_TITLE, page_icon="📄", layout="wide")
    st.markdown(
        """
        <style>
        .stApp {
            background:
              radial-gradient(circle at 12% 18%, rgba(99, 210, 255, .18), transparent 34%),
              radial-gradient(circle at 84% 10%, rgba(155, 92, 255, .24), transparent 36%),
              linear-gradient(135deg, #071421 0%, #11142a 50%, #050914 100%);
            color: #f5f7fb;
        }
        [data-testid="stHeader"] { background: transparent; }
        .hero {
            padding: 34px 38px;
            border: 1px solid rgba(255,255,255,.16);
            border-radius: 26px;
            background: linear-gradient(135deg, rgba(255,255,255,.18), rgba(255,255,255,.05));
            box-shadow: 0 28px 90px rgba(0,0,0,.34), inset 0 1px 0 rgba(255,255,255,.15);
            backdrop-filter: blur(20px) saturate(150%);
            margin-bottom: 22px;
        }
        .hero h1 { margin: 0 0 10px 0; font-size: 2.35rem; letter-spacing: -.04em; }
        .hero p { color: rgba(245,247,251,.82); font-size: 1.03rem; line-height: 1.65; max-width: 900px; }
        .status-box {
            padding: 12px 14px;
            border-radius: 14px;
            background: rgba(255,255,255,.08);
            border: 1px solid rgba(255,255,255,.12);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def today_label() -> str:
    today = date.today()
    return f"{today.strftime('%B')} {today.day}, {today.year}"


def safe_filename(value: str, max_length: int = 110) -> str:
    cleaned = re.sub(r"[\\/:*?\"<>|]+", "-", str(value or "Agreement"))
    cleaned = re.sub(r"\s+", " ", cleaned).strip(" .")
    return (cleaned[:max_length].rstrip() or "Agreement")


def slugify(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "-", str(value).lower()).strip("-")
    return cleaned or "template"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def normalize_country(value: str) -> Optional[str]:
    if not value or str(value).strip().lower() in {"nan", "none", "null"}:
        return None
    raw = re.sub(r"\s+", " ", str(value).strip())
    lowered = raw.lower().strip(".,;:()[]{}")
    if lowered in COUNTRY_ALIASES:
        return COUNTRY_ALIASES[lowered]
    for country in COUNTRY_CURRENCY:
        if lowered == country.lower():
            return country
    return None


def detect_country_from_text(text: str) -> Optional[str]:
    if not text:
        return None
    cleaned_text = re.sub(r"[^A-Za-zÀ-ÿ.'’ -]+", " ", text)
    haystack = f" {re.sub(r'\s+', ' ', cleaned_text).lower()} "
    for pattern, canonical in COUNTRY_PATTERNS:
        pattern_re = re.escape(pattern).replace(r"\ ", r"\s+")
        if re.search(rf"(?<![a-z]){pattern_re}(?![a-z])", haystack):
            return canonical
    return None


def resolve_currency_code(country: Optional[str], manual_code: str = "") -> str:
    manual_code = re.sub(r"[^A-Za-z]", "", manual_code or "").upper()[:3]
    if manual_code:
        return manual_code
    if not country:
        return ""
    canonical = normalize_country(country) or country
    return COUNTRY_CURRENCY.get(canonical, "")


def get_database_url() -> str:
    return os.getenv("DATABASE_URL", "").strip()


def database_configured() -> bool:
    return bool(get_database_url()) and psycopg is not None


def get_db_connection():
    if not database_configured():
        raise RuntimeError("DATABASE_URL is not configured or psycopg is not installed.")
    return psycopg.connect(get_database_url(), row_factory=dict_row, autocommit=True)


def ensure_template_table() -> None:
    with get_db_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS agreement_templates (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                requires_code BOOLEAN NOT NULL DEFAULT FALSE,
                description TEXT NOT NULL DEFAULT '',
                filename TEXT NOT NULL,
                content_type TEXT NOT NULL DEFAULT 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                file_bytes BYTEA NOT NULL,
                file_sha256 TEXT NOT NULL,
                is_default BOOLEAN NOT NULL DEFAULT FALSE,
                is_active BOOLEAN NOT NULL DEFAULT TRUE,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            );
            """
        )


def bundled_templates() -> List[TemplateMeta]:
    return [template for template in DEFAULT_TEMPLATES if template.path and template.path.exists()]


def seed_default_templates_to_neon() -> None:
    ensure_template_table()
    with get_db_connection() as conn:
        for template in bundled_templates():
            data = template.path.read_bytes()
            conn.execute(
                """
                INSERT INTO agreement_templates
                    (id, name, category, requires_code, description, filename, content_type, file_bytes, file_sha256, is_default, is_active)
                VALUES
                    (%(id)s, %(name)s, %(category)s, %(requires_code)s, %(description)s, %(filename)s, %(content_type)s, %(file_bytes)s, %(file_sha256)s, TRUE, TRUE)
                ON CONFLICT (id) DO UPDATE SET
                    name = EXCLUDED.name,
                    category = EXCLUDED.category,
                    requires_code = EXCLUDED.requires_code,
                    description = EXCLUDED.description,
                    filename = EXCLUDED.filename,
                    content_type = EXCLUDED.content_type,
                    file_bytes = EXCLUDED.file_bytes,
                    file_sha256 = EXCLUDED.file_sha256,
                    is_default = TRUE,
                    is_active = TRUE,
                    updated_at = NOW();
                """,
                {
                    "id": template.id,
                    "name": template.name,
                    "category": template.category,
                    "requires_code": template.requires_code,
                    "description": template.description,
                    "filename": template.filename,
                    "content_type": DOCX_MIME,
                    "file_bytes": data,
                    "file_sha256": sha256_bytes(data),
                },
            )


def load_templates_from_neon() -> List[TemplateMeta]:
    seed_default_templates_to_neon()
    with get_db_connection() as conn:
        rows = conn.execute(
            """
            SELECT id, name, category, requires_code, description, filename, file_bytes, file_sha256, is_default
            FROM agreement_templates
            WHERE is_active = TRUE
            ORDER BY is_default DESC, category ASC, name ASC;
            """
        ).fetchall()

    templates: List[TemplateMeta] = []
    for row in rows:
        templates.append(
            TemplateMeta(
                id=row["id"],
                name=row["name"],
                category=row["category"],
                requires_code=bool(row["requires_code"]),
                description=row["description"] or "",
                source="database",
                filename=row["filename"],
                is_default=bool(row["is_default"]),
                bytes_data=bytes(row["file_bytes"]),
                file_sha256=row["file_sha256"] or "",
            )
        )
    return templates


def save_template_to_neon(name: str, category: str, requires_code: bool, description: str, filename: str, template_bytes: bytes) -> str:
    ensure_template_table()
    template_id = f"custom-{slugify(name)}-{uuid.uuid4().hex[:8]}"
    with get_db_connection() as conn:
        conn.execute(
            """
            INSERT INTO agreement_templates
                (id, name, category, requires_code, description, filename, content_type, file_bytes, file_sha256, is_default, is_active)
            VALUES
                (%(id)s, %(name)s, %(category)s, %(requires_code)s, %(description)s, %(filename)s, %(content_type)s, %(file_bytes)s, %(file_sha256)s, FALSE, TRUE);
            """,
            {
                "id": template_id,
                "name": name,
                "category": category,
                "requires_code": requires_code,
                "description": description,
                "filename": filename,
                "content_type": DOCX_MIME,
                "file_bytes": template_bytes,
                "file_sha256": sha256_bytes(template_bytes),
            },
        )
    return template_id


def get_all_templates() -> Tuple[List[TemplateMeta], str]:
    session_templates = st.session_state.get("custom_templates", [])
    if database_configured():
        try:
            return load_templates_from_neon(), "Neon template library connected. Templates are saved permanently."
        except Exception as exc:
            st.session_state["db_error"] = str(exc)
            return bundled_templates() + session_templates, "Neon is configured but unavailable. Using bundled/session templates."
    return bundled_templates() + session_templates, "Neon is not configured. Bundled templates work; uploaded custom templates are session-only."


def get_template_bytes(template: TemplateMeta) -> bytes:
    if template.bytes_data is not None:
        return template.bytes_data
    if template.path and template.path.exists():
        return template.path.read_bytes()
    raise ValueError(f"Template bytes unavailable for {template.name}.")


def read_provider_file(uploaded_file) -> pd.DataFrame:
    name = uploaded_file.name.lower()
    if name.endswith(".csv"):
        return pd.read_csv(uploaded_file)
    return pd.read_excel(uploaded_file)


def parse_pasted_providers(text: str) -> pd.DataFrame:
    blocks = [block.strip() for block in re.split(r"\n\s*\n", text or "") if block.strip()]
    rows = []
    for block in blocks:
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if not lines:
            continue
        rows.append({"clinic_name": lines[0], "address": "\n".join(lines[1:])})
    return pd.DataFrame(rows)


def normalize_provider_rows(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["clinic_name", "address"])
    renamed = {str(col).strip().lower(): col for col in df.columns}
    name_col = next((renamed[key] for key in ["clinic_name", "clinic name", "provider_name", "provider name", "name"] if key in renamed), None)
    address_col = next((renamed[key] for key in ["address", "clinic_address", "clinic address", "full_address", "full address"] if key in renamed), None)
    country_col = next((renamed[key] for key in ["country", "country_name", "country name"] if key in renamed), None)
    if name_col is None or address_col is None:
        raise ValueError("Provider data must include clinic_name/name and address columns.")
    out = pd.DataFrame({"clinic_name": df[name_col].fillna("").astype(str), "address": df[address_col].fillna("").astype(str)})
    if country_col is not None:
        out["country"] = df[country_col].fillna("").astype(str)
    out = out[(out["clinic_name"].str.strip() != "") | (out["address"].str.strip() != "")]
    return out.reset_index(drop=True)


def prepare_records_for_template(records: pd.DataFrame, template: TemplateMeta, selected_country: str, manual_code: str) -> pd.DataFrame:
    out = records.copy()
    out["date"] = today_label()
    if not template.requires_code:
        out["resolved_country"] = ""
        out["currency_code"] = ""
        return out

    resolved_countries = []
    currency_codes = []
    manual_country = selected_country if selected_country != AUTO_DETECT_LABEL else ""
    for _, row in out.iterrows():
        country = normalize_country(manual_country)
        if not country and "country" in out.columns:
            country = normalize_country(str(row.get("country", "")))
        if not country:
            country = detect_country_from_text(str(row.get("address", "")))
        code = resolve_currency_code(country, manual_code)
        resolved_countries.append(country or "")
        currency_codes.append(code or "")
    out["resolved_country"] = resolved_countries
    out["currency_code"] = currency_codes
    return out


def iter_block_paragraphs(document: Document):
    for paragraph in document.paragraphs:
        yield paragraph
    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    yield paragraph


def values_for_record(row: pd.Series) -> Dict[str, str]:
    return {
        "name": str(row.get("clinic_name", "")).strip(),
        "address": str(row.get("address", "")).strip(),
        "date": today_label(),
        "code": str(row.get("currency_code", "")).strip(),
    }


def replace_highlighted_runs(paragraph, values: Dict[str, str]) -> Dict[str, int]:
    counts = {"name": 0, "address": 0, "date": 0, "code": 0}
    active_field = None
    for run in paragraph.runs:
        field = HIGHLIGHT_TO_FIELD.get(run.font.highlight_color)
        if field is None:
            active_field = None
            continue
        if field != active_field:
            run.text = values.get(field, "")
            counts[field] += 1
            active_field = field
        else:
            run.text = ""
        run.font.highlight_color = None
    return counts


def generate_document(template: TemplateMeta, row: pd.Series) -> Tuple[bytes, Dict[str, int]]:
    document = Document(io.BytesIO(get_template_bytes(template)))
    values = values_for_record(row)
    total_counts = {"name": 0, "address": 0, "date": 0, "code": 0}
    for paragraph in iter_block_paragraphs(document):
        counts = replace_highlighted_runs(paragraph, values)
        for key, value in counts.items():
            total_counts[key] += value
    output = io.BytesIO()
    document.save(output)
    return output.getvalue(), total_counts


def make_zip(template: TemplateMeta, records: pd.DataFrame) -> Tuple[bytes, List[Dict[str, object]]]:
    zip_buffer = io.BytesIO()
    manifest: List[Dict[str, object]] = []
    with zipfile.ZipFile(zip_buffer, "w", compression=zipfile.ZIP_DEFLATED) as zip_file:
        for idx, row in records.iterrows():
            doc_bytes, counts = generate_document(template, row)
            provider_name = str(row.get("clinic_name", f"Provider {idx + 1}")).strip() or f"Provider {idx + 1}"
            filename = f"{idx + 1:03d} - {safe_filename(provider_name)} - {safe_filename(template.name)}.docx"
            zip_file.writestr(filename, doc_bytes)
            manifest.append({"file": filename, "clinic_name": provider_name, **counts})
        manifest_df = pd.DataFrame(manifest)
        zip_file.writestr("manifest.csv", manifest_df.to_csv(index=False).encode("utf-8"))
    zip_buffer.seek(0)
    return zip_buffer.getvalue(), manifest


def render_generate_tab() -> None:
    templates, status = get_all_templates()
    st.markdown(f"<div class='status-box'>{status}</div>", unsafe_allow_html=True)
    if "db_error" in st.session_state:
        st.warning(f"Neon fallback reason: {st.session_state['db_error']}")
    if not templates:
        st.error("No templates found. Upload .docx templates into the templates folder or use Configure Templates.")
        return

    selected_name = st.selectbox("Template", [template.name for template in templates])
    template = next(item for item in templates if item.name == selected_name)
    st.caption(template.description)

    countries = [AUTO_DETECT_LABEL] + sorted(COUNTRY_CURRENCY)
    selected_country = AUTO_DETECT_LABEL
    manual_code = ""
    if template.requires_code:
        selected_country = st.selectbox("Overseas country for this batch", countries)
        manual_code = st.text_input("Optional manual 3-letter currency code override", max_chars=3).upper()

    input_mode = st.radio("Provider input", ["Upload Excel/CSV", "Paste providers"], horizontal=True)
    records = pd.DataFrame()
    if input_mode == "Upload Excel/CSV":
        uploaded = st.file_uploader("Upload spreadsheet", type=["xlsx", "xlsm", "xls", "csv"])
        if uploaded:
            try:
                records = normalize_provider_rows(read_provider_file(uploaded))
            except Exception as exc:
                st.error(str(exc))
    else:
        sample = "Clinic Name\n123 Main St\nCity, Country\n\nNext Clinic\n456 Second St\nCity, Country"
        pasted = st.text_area("Paste one provider block at a time", value="", placeholder=sample, height=220)
        if pasted.strip():
            try:
                records = normalize_provider_rows(parse_pasted_providers(pasted))
            except Exception as exc:
                st.error(str(exc))

    if records.empty:
        st.info("Add providers to continue. Required fields are clinic_name/name and address.")
        return

    prepared = prepare_records_for_template(records, template, selected_country, manual_code)
    if template.requires_code and prepared["currency_code"].eq("").any():
        st.warning("Some overseas rows do not have a currency code. Select a country or enter a manual 3-letter code before generating.")
    st.subheader("Preview")
    st.dataframe(prepared, use_container_width=True, hide_index=True)

    if st.button("Generate agreements", type="primary"):
        try:
            zip_bytes, manifest = make_zip(template, prepared)
            st.success(f"Generated {len(manifest)} agreement(s).")
            st.download_button(
                "Download ZIP",
                data=zip_bytes,
                file_name=f"pricing-agreements-{date.today().isoformat()}.zip",
                mime="application/zip",
            )
            st.dataframe(pd.DataFrame(manifest), use_container_width=True, hide_index=True)
        except Exception as exc:
            st.error(f"Generation failed: {exc}")


def render_configure_tab() -> None:
    st.subheader("Saved templates")
    templates, status = get_all_templates()
    st.caption(status)
    if templates:
        st.dataframe(
            pd.DataFrame(
                [
                    {
                        "name": template.name,
                        "category": template.category,
                        "requires_code": template.requires_code,
                        "source": template.source,
                        "filename": template.filename,
                    }
                    for template in templates
                ]
            ),
            use_container_width=True,
            hide_index=True,
        )

    st.subheader("Upload custom template")
    with st.form("template_upload_form", clear_on_submit=True):
        name = st.text_input("Template name")
        category = st.text_input("Category", value="Custom")
        description = st.text_area("Description", value="Custom pricing agreement template.")
        requires_code = st.checkbox("Requires overseas currency code / gray highlighted placeholders")
        uploaded_template = st.file_uploader("Template .docx", type=["docx"])
        submitted = st.form_submit_button("Save template")

    if submitted:
        if not name.strip() or uploaded_template is None:
            st.error("Template name and .docx file are required.")
            return
        template_bytes = uploaded_template.read()
        if database_configured():
            try:
                save_template_to_neon(name.strip(), category.strip() or "Custom", requires_code, description.strip(), uploaded_template.name, template_bytes)
                st.success("Template saved permanently in Neon.")
                st.rerun()
            except Exception as exc:
                st.error(f"Could not save to Neon: {exc}")
                return
        session_template = TemplateMeta(
            id=f"session-{uuid.uuid4().hex[:8]}",
            name=name.strip(),
            category=category.strip() or "Custom",
            requires_code=requires_code,
            description=description.strip(),
            source="session",
            filename=uploaded_template.name,
            bytes_data=template_bytes,
            file_sha256=sha256_bytes(template_bytes),
        )
        st.session_state.setdefault("custom_templates", []).append(session_template)
        st.success("Template saved for this browser session.")


def main() -> None:
    page_style()
    st.markdown(
        """
        <div class="hero">
          <h1>Pricing Agreement Generator</h1>
          <p>Generate provider agreements from saved Word templates. Upload a spreadsheet or paste providers, then download every completed agreement as a ZIP.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    tab_generate, tab_configure = st.tabs(["Generate Agreements", "Configure Templates"])
    with tab_generate:
        render_generate_tab()
    with tab_configure:
        render_configure_tab()


if __name__ == "__main__":
    main()
