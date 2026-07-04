# Pricing Agreement Generator

A Streamlit app that generates clean provider pricing agreements from permanently saved `.docx` templates using highlight colors as replacement markers.

## What it does

- Selects a saved Word template.
- Accepts providers by Excel/CSV upload or manual paste.
- Replaces highlighted template markers:
  - Yellow = provider/clinic name
  - Green = address
  - Blue/cyan = today's date
  - Gray = automatic ISO 4217 currency code for overseas templates
- Removes highlight formatting from the generated output documents.
- Creates one `.docx` per provider.
- Packages generated files into a downloadable ZIP.
- Saves templates permanently in Neon when `DATABASE_URL` is configured.
- Does **not** save generated output files or provider lists permanently.

## Overseas currency code handling

Users do **not** type the three-letter code manually.

For templates marked as requiring an automatic overseas currency code, the app fills gray highlighted placeholders using an offline country-to-currency map.

Examples:

- New Zealand -> `NZD`
- Canada -> `CAD`
- United Kingdom -> `GBP`
- Australia -> `AUD`
- Mexico -> `MXN`
- United Arab Emirates -> `AED`
- Saudi Arabia -> `SAR`
- Germany / France / Spain -> `EUR`

The app supports two methods:

1. Select one country for the whole batch.
2. Use auto-detection from the provider address.

The preview table shows the resolved country and currency code before generating. If the country cannot be detected, the app asks the user to select a country.

## Default templates bundled in the repo

The four default templates live in `templates/` and are automatically seeded into Neon on app startup:

- `Overseas Medical Pricing Agreement.docx`
- `1 - Medical Pricing Agreement - 2026.docx`
- `2 - Dental Pricing Agreement -2025.docx`
- `13 - Cardiovascular Components - 2026.docx`

## Provider input options

### Excel/CSV upload

Required headers:

```text
clinic_name
address
```

Optional overseas helper header:

```text
country
```

### Paste box

Format:

```text
Clinic Name
Address line 1
Address line 2
Country

Next Clinic Name
Address line 1
Address line 2
Country
```

The first line of each block is the provider name. Remaining lines are joined as the address.

## Template configuration

Before uploading a template:

- File must be `.docx`.
- Highlight provider/clinic name placeholders in yellow.
- Highlight address placeholders in green.
- Highlight date placeholders in blue/light blue.
- Highlight currency/code placeholders in gray only when needed.
- Do not highlight labels. Only highlight the exact text to replace.

When Neon is connected, configured templates are saved permanently in the `agreement_templates` table.

## Neon setup

Set the Neon connection string as a Render environment variable named:

```text
DATABASE_URL
```

Do not hardcode the database URL inside `app.py`.

On startup, the app creates this table if it does not already exist:

```sql
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
```

## Render deployment

1. Push this folder to GitHub.
2. Create a new Render Web Service from the GitHub repo.
3. Use the included `render.yaml` settings or configure manually:
   - Build command: `pip install -r requirements.txt`
   - Start command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
4. Add the `DATABASE_URL` environment variable in Render.
5. Deploy.

## Local run

```bash
pip install -r requirements.txt
streamlit run app.py
```

For local Neon testing, export `DATABASE_URL` in your shell before starting Streamlit.
