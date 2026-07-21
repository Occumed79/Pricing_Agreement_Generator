"""Render entrypoint with duplicate placeholder protection.

The bundled agreement templates can contain more than one yellow provider-name
placeholder or green provider-address placeholder. The core generator replaces
all highlighted placeholders, which causes those values to appear twice.

This entrypoint keeps the existing app and template design intact while limiting
provider name and address to their first highlighted placeholder in each output
document. Date and currency-code placeholders retain the existing behavior.
"""

from __future__ import annotations

from typing import Dict, MutableSet

import app as generator_app

_SINGLE_INSTANCE_FIELDS = frozenset({"name", "address"})


def _replace_highlighted_runs_once(
    paragraph,
    values: Dict[str, str],
    populated_fields: MutableSet[str],
) -> Dict[str, int]:
    """Replace highlighted runs while suppressing duplicate name/address fields."""
    counts = {"name": 0, "address": 0, "date": 0, "code": 0}
    active_field = None

    for run in paragraph.runs:
        field = generator_app.HIGHLIGHT_TO_FIELD.get(run.font.highlight_color)
        if field is None:
            active_field = None
            continue

        if field != active_field:
            is_duplicate_singleton = (
                field in _SINGLE_INSTANCE_FIELDS and field in populated_fields
            )
            if is_duplicate_singleton:
                run.text = ""
            else:
                run.text = values.get(field, "")
                counts[field] += 1
                if field in _SINGLE_INSTANCE_FIELDS:
                    populated_fields.add(field)
            active_field = field
        else:
            # A single Word placeholder may be split across several adjacent runs.
            run.text = ""

        run.font.highlight_color = None

    return counts


def _generate_document_without_duplicate_provider_fields(template, row):
    document = generator_app.Document(
        generator_app.io.BytesIO(generator_app.get_template_bytes(template))
    )
    values = generator_app.values_for_record(row)
    total_counts = {"name": 0, "address": 0, "date": 0, "code": 0}
    populated_fields: MutableSet[str] = set()

    for paragraph in generator_app.iter_block_paragraphs(document):
        counts = _replace_highlighted_runs_once(
            paragraph,
            values,
            populated_fields,
        )
        for key, value in counts.items():
            total_counts[key] += value

    output = generator_app.io.BytesIO()
    document.save(output)
    return output.getvalue(), total_counts


# Keep the existing Streamlit UI and generation pipeline, replacing only the
# document-generation function responsible for the duplicate output.
generator_app.generate_document = _generate_document_without_duplicate_provider_fields


if __name__ == "__main__":
    generator_app.main()
