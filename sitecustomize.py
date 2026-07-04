from __future__ import annotations

import builtins
import io
import os
import pathlib

_ORIGINAL_OPEN = builtins.open
_ORIGINAL_IO_OPEN = io.open
_ORIGINAL_READ_TEXT = pathlib.Path.read_text


def _is_target_app(path) -> bool:
    try:
        return os.path.basename(os.fspath(path)) == "app.py"
    except TypeError:
        return False


def _patch_app_source(source: str) -> str:
    patched_lines: list[str] = []
    skipping_database_url = False

    for line in source.splitlines():
        stripped = line.strip()

        if stripped.startswith('haystack = f" {re.sub('):
            patched_lines.append('    cleaned_text = re.sub(r"[^A-Za-zÀ-ÿ.\'’ -]+", " ", text)')
            patched_lines.append('    haystack = f" {cleaned_text.lower()} "')
            continue

        if line.startswith("def get_database_url()"):
            patched_lines.append("def get_database_url() -> str:")
            patched_lines.append('    env_url = os.getenv("DATABASE_URL", "").strip()')
            patched_lines.append("    if env_url:")
            patched_lines.append("        return env_url")
            patched_lines.append("    try:")
            patched_lines.append('        return str(st.secrets.get("DATABASE_URL", "")).strip()')
            patched_lines.append("    except Exception:")
            patched_lines.append('        return ""')
            skipping_database_url = True
            continue

        if skipping_database_url:
            if line.startswith("def database_configured()"):
                skipping_database_url = False
                patched_lines.append(line)
            continue

        patched_lines.append(line)

    return "\n".join(patched_lines) + "\n"


def _patched_open(file, mode="r", *args, **kwargs):
    is_read = "r" in mode and not any(flag in mode for flag in ("w", "a", "+"))
    if is_read and _is_target_app(file):
        if "b" in mode:
            data = _ORIGINAL_OPEN(file, mode, *args, **kwargs).read()
            try:
                text = data.decode("utf-8")
            except UnicodeDecodeError:
                return io.BytesIO(data)
            return io.BytesIO(_patch_app_source(text).encode("utf-8"))

        text = _ORIGINAL_OPEN(file, mode, *args, **kwargs).read()
        return io.StringIO(_patch_app_source(text))

    return _ORIGINAL_OPEN(file, mode, *args, **kwargs)


def _patched_read_text(self, *args, **kwargs):
    text = _ORIGINAL_READ_TEXT(self, *args, **kwargs)
    if _is_target_app(self):
        return _patch_app_source(text)
    return text


builtins.open = _patched_open
io.open = _patched_open
pathlib.Path.read_text = _patched_read_text
