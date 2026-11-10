#!/usr/bin/env python3
"""Convert a book-note .docx (Google Docs export) into a chapter .qmd page.

Usage:
    python3 scripts/docx_to_qmd.py sources/damodaran/ch01.docx books/damodaran-iv/ch01.qmd
    python3 scripts/docx_to_qmd.py ... --force      # overwrite an existing .qmd

An existing .qmd is never overwritten without --force, so text you wrote in
"내 생각" is not lost by re-running the conversion.

What it does
- pandoc docx -> Markdown (pipe tables, grid tables only when a cell needs it)
- the first H1 becomes the front-matter title / subtitle
- the "Oct 21, 2026 · @name" line becomes the front-matter date
- literal **bold** that Google Docs exported as escaped text is restored
- lines listed in FORMULAS (exact text) are replaced by LaTeX display math
"""
import argparse
import datetime as dt
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from formulas import FORMULAS  # noqa: E402


def find_pandoc():
    for cand in (shutil.which("pandoc"),
                 shutil.which("quarto") and "quarto-pandoc",
                 os.path.expanduser("~/Applications/quarto/bin/tools/aarch64/pandoc"),
                 os.path.expanduser("~/Applications/quarto/bin/tools/x86_64/pandoc")):
        if cand == "quarto-pandoc":
            return ["quarto", "pandoc"]
        if cand and os.path.exists(cand):
            return [cand]
    sys.exit("pandoc not found: install Quarto (it bundles pandoc)")


def convert(src: Path) -> str:
    cmd = find_pandoc() + [
        str(src), "-f", "docx",
        "-t", "markdown-simple_tables-multiline_tables-raw_attribute-bracketed_spans-native_spans",
        "--wrap=none", "--markdown-headings=atx",
    ]
    return subprocess.run(cmd, check=True, capture_output=True, text=True).stdout


def build(md: str, chapter: int, book: str):
    lines = md.splitlines()
    title, subtitle, date = f"{chapter}장", None, None

    # title: first H1
    for i, l in enumerate(lines):
        if l.startswith("# "):
            t = re.sub(r"^#\s+", "", l)
            t = re.sub(r"^\\?\[.*?\\?\]\s*", "", t)          # drop "[... 읽기]"
            parts = re.split(r"\s+(?:—|---)\s+", t, maxsplit=1)
            title = parts[0].strip()
            subtitle = parts[1].strip() if len(parts) > 1 else None
            lines[i] = None
            break

    # date / byline line
    for i, l in enumerate(lines):
        if l is None:
            continue
        m = re.match(r"^([A-Z][a-z]{2} \d{1,2}, \d{4})\s*·", l.strip())
        if m:
            date = dt.datetime.strptime(m.group(1), "%b %d, %Y").date().isoformat()
            lines[i] = None
            break

    body = "\n".join(l for l in lines if l is not None).strip() + "\n"

    # restore literal **bold** exported as escaped asterisks
    body = re.sub(r"\\\*\\\*(.+?)\\\*\\\*", r"**\1**", body)

    # formulas: replace whole lines (exact match) with the LaTeX version
    missing = []
    out = body.split("\n")
    for plain, repl in FORMULAS.get(chapter, []):
        if plain in out:
            out[out.index(plain)] = repl
        else:
            missing.append(plain)
    body = "\n".join(out)

    fm = ["---", f'title: "{title}"']
    if subtitle:
        fm.append(f'subtitle: "{subtitle}"')
    if date:
        fm.append(f"date: {date}")
    fm += [f"chapter: {chapter}", f'book: "{book}"', 'status: "요약 완료"',
           "my-thoughts: false   # '내 생각'을 채우면 true로 바꾸세요", "---", ""]
    return "\n".join(fm) + body, missing


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src", type=Path)
    ap.add_argument("dst", type=Path)
    ap.add_argument("--book", default="Investment Valuation")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    if a.dst.exists() and not a.force:
        sys.exit(f"{a.dst} exists; use --force to overwrite (your '내 생각' text would be lost)")
    chapter = int(re.search(r"(\d+)", a.src.stem).group(1))
    text, missing = build(convert(a.src), chapter, a.book)
    a.dst.parent.mkdir(parents=True, exist_ok=True)
    a.dst.write_text(text, encoding="utf-8")
    print(f"wrote {a.dst}")
    for m in missing:
        print(f"  ! formula not found: {m[:60]}")


if __name__ == "__main__":
    main()
