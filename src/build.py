#!/usr/bin/env python3
"""Inline fonts and images into ../index.html so the site is a single self-contained file.

Edit src/index.template.html, drop images in src/assets/ and fonts in src/fonts/,
then run:  python3 src/build.py
"""
import base64
import pathlib
import re

SRC = pathlib.Path(__file__).resolve().parent
OUT = SRC.parent / "index.html"
MIME = {".webp": "image/webp", ".png": "image/png", ".jpg": "image/jpeg", ".svg": "image/svg+xml", ".woff2": "font/woff2"}


def data_uri(path: pathlib.Path) -> str:
    return f"data:{MIME[path.suffix]};base64,{base64.b64encode(path.read_bytes()).decode()}"


def main() -> None:
    html = (SRC / "index.template.html").read_text()
    html = re.sub(r"\{\{asset:([^}]+)\}\}", lambda m: data_uri(SRC / "assets" / m.group(1)), html)
    html = re.sub(r"\{\{font:([^}]+)\}\}", lambda m: data_uri(SRC / "fonts" / m.group(1)), html)
    missing = re.findall(r"\{\{[^}]+\}\}", html)
    if missing:
        raise SystemExit(f"Unresolved placeholders: {missing}")
    OUT.write_text(html)
    print(f"Wrote {OUT} ({OUT.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
