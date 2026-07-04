from __future__ import annotations

from pathlib import Path

APP_PATH = Path(__file__).with_name("app.py")
source = APP_PATH.read_text(encoding="utf-8")

patched_lines: list[str] = []
for line in source.splitlines():
    if line.strip().startswith('haystack = f" {re.sub('):
        patched_lines.append('    cleaned_text = re.sub(r"[^A-Za-zÀ-ÿ.\'’ -]+", " ", text)')
        patched_lines.append('    haystack = f" {cleaned_text.lower()} "')
    else:
        patched_lines.append(line)

patched_source = "\n".join(patched_lines) + "\n"
compiled = compile(patched_source, str(APP_PATH), "exec")
exec_globals = {
    "__file__": str(APP_PATH),
    "__name__": "__main__",
    "__package__": None,
}
exec(compiled, exec_globals)
