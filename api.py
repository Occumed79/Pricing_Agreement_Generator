from __future__ import annotations

import base64
import hashlib
import re
from typing import Dict, List

import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app import (
    TemplateMeta,
    bundled_templates,
    database_configured,
    generate_document,
    load_templates_from_neon,
    normalize_country,
    resolve_currency_code,
    safe_filename,
)


app = FastAPI(
    title="Occu-Med Pricing Agreement Generator API",
    version="1.0.0",
)


TEMPLATE_KEY_ALIASES: Dict[str, List[str]] = {
    "overseas-medical": [
        "default-overseas-medical-pricing-agreement",
        "Overseas Medical Pricing Agreement",
    ],
    "medical": [
        "default-medical-pricing-agreement-2026",
        "1 - Medical Pricing Agreement - 2026",
    ],
    "dental": [
        "default-dental-pricing-agreement-2025",
        "2 - Dental Pricing Agreement -2025",
    ],
    "cardiovascular": [
        "default-cardiovascular-components-2026",
        "13 - Cardiovascular Components - 2026",
    ],
}


class GenerateRequest(BaseModel):
    campaignTargetId: str | None = None
    facilityId: str | None = None
    providerName: str = Field(min_length=1, max_length=300)
    providerType: str | None = Field(default=None, max_length=100)
    address: str = Field(default="", max_length=2000)
    country: str | None = Field(default=None, max_length=120)
    currencyCode: str | None = Field(default=None, min_length=3, max_length=3)
    templateKey: str = Field(min_length=1, max_length=200)


def _available_templates() -> List[TemplateMeta]:
    if database_configured():
        try:
            return load_templates_from_neon()
        except Exception:
            pass
    return bundled_templates()


def resolve_template(template_key: str, templates: List[TemplateMeta]) -> TemplateMeta:
    key = re.sub(r"\s+", " ", template_key or "").strip()
    if not key:
        raise ValueError("templateKey is required.")

    aliases = TEMPLATE_KEY_ALIASES.get(key, [key])
    lowered = {alias.lower() for alias in aliases}

    for template in templates:
        if template.id.lower() in lowered or template.name.lower() in lowered:
            return template

    raise ValueError(
        f"No active agreement template matches '{template_key}'."
    )


@app.get("/api/health")
def health() -> dict:
    templates = _available_templates()
    return {
        "ok": True,
        "service": "pricing-agreement-generator-api",
        "templateCount": len(templates),
        "databaseConfigured": database_configured(),
        "templateKeys": sorted(TEMPLATE_KEY_ALIASES),
    }


@app.post("/api/outreach/generate")
def generate_outreach_agreement(request: GenerateRequest) -> dict:
    try:
        templates = _available_templates()
        template = resolve_template(request.templateKey, templates)

        canonical_country = normalize_country(request.country or "")
        currency = (request.currencyCode or "").upper().strip()
        if not currency and template.requires_code:
            currency = resolve_currency_code(canonical_country, "")

        if template.requires_code and not currency:
            raise ValueError(
                "A 3-letter currency code is required for this overseas agreement."
            )

        row = pd.Series(
            {
                "clinic_name": request.providerName.strip(),
                "address": request.address.strip(),
                "country": canonical_country or request.country or "",
                "currency_code": currency,
            }
        )

        document_bytes, replacement_counts = generate_document(template, row)
        digest = hashlib.sha256(document_bytes).hexdigest()
        filename = (
            f"{safe_filename(request.providerName)} - "
            f"{safe_filename(template.name)}.docx"
        )

        return {
            "status": "GENERATED",
            "id": digest[:24],
            "fileName": filename,
            "contentType": (
                "application/vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            ),
            "sha256": digest,
            "fileBase64": base64.b64encode(document_bytes).decode("ascii"),
            "template": {
                "id": template.id,
                "name": template.name,
                "requiresCode": template.requires_code,
            },
            "replacementCounts": replacement_counts,
            "currencyCode": currency or None,
            "campaignTargetId": request.campaignTargetId,
            "facilityId": request.facilityId,
        }
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Agreement generation failed: {exc}",
        ) from exc
