# Pricing Agreement Generator

A Streamlit app that generates clean provider pricing agreements from saved `.docx` templates using highlight colors as replacement markers.

## What it does

- Selects a bundled or saved Word template.
- Accepts providers by Excel/CSV upload or manual paste.
- Replaces highlighted template markers:
  - Yellow = provider/clinic name
  - Green = address
  - Blue/cyan = today's date
  - Gray = currency code for overseas templates
- Removes highlight formatting from generated output documents.
- Creates one `.docx` per provider.
- Packages generated files into a downloadable ZIP with a `manifest.csv`.
- Saves custom templates permanently in Neon when `DATABASE_URL` is configured.
- Falls back safely to bundled/session templates when Neon is not configured.

## Default bundled templates

The default templates live in `templates/`:

- `Overseas Medical Pricing Agreement.docx`
- `1 - Medical Pricing Agreement - 2026.docx`
- `2 - Dental Pricing Agreement -2025.docx`
- `13 - Cardiovascular Components - 2026.docx`

## Provider input

Spreadsheet uploads should include these columns, or close equivalents:

```text
clinic_name
address
```

Accepted aliases include `name`, `provider_name`, `clinic name`, `provider name`, `clinic address`, `full address`, and `country`.

The paste box accepts one provider per blank-line-separated block:

```text
Clinic Name
123 Main St
City, Country

Next Clinic
456 Second St
City, Country
```

## Overseas currency codes

For overseas templates, the app can:

1. Use one selected country for the full batch.
2. Auto-detect common countries from the address.
3. Accept a manual 3-letter currency code override.

## Render deployment

Runtime is pinned to Python `3.12.8`.

Build command:

```bash
pip install --upgrade pip && pip install -r requirements.txt
```

Start command:

```bash
streamlit run app.py --server.address=0.0.0.0 --server.port=$PORT --server.headless=true
```

Required environment variable for permanent template storage:

```text
DATABASE_URL
```

The app still works without `DATABASE_URL`; bundled templates remain available and uploaded custom templates are session-only.

## Local run

```bash
pip install -r requirements.txt
streamlit run app.py
```

Do not hardcode secrets in the repo. Use Render environment variables for production.
