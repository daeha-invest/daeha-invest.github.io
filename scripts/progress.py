#!/usr/bin/env python3
"""Collect study progress from books/*/ chapter front matter -> books/progress.json.

Runs automatically before every render (pre-render in _quarto.yml).
Per book (books/<book>/index.qmd):  title, total-chapters (optional)
Per chapter (books/<book>/chNN.qmd): chapter, status, my-thoughts (true/false)
Standard library only.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def front_matter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    out = {}
    if not m:
        return out
    for line in m.group(1).splitlines():
        kv = re.match(r"^([A-Za-z][\w-]*):\s*(.*?)\s*(#.*)?$", line)
        if kv:
            v = kv.group(2).strip().strip('"').strip("'")
            out[kv.group(1)] = {"true": True, "false": False}.get(v.lower(), v)
    return out


def main():
    books = []
    for idx in sorted((ROOT / "books").glob("*/index.qmd")):
        meta = front_matter(idx)
        chapters = []
        for ch in sorted(idx.parent.glob("ch*.qmd")):
            fm = front_matter(ch)
            if fm.get("draft") is True:
                continue
            chapters.append({
                "chapter": int(fm.get("chapter", 0) or 0),
                "title": fm.get("title", ch.stem),
                "status": fm.get("status", ""),
                "my_thoughts": fm.get("my-thoughts") is True,
                "href": f"books/{idx.parent.name}/{ch.stem}.html",
            })
        total = meta.get("total-chapters")
        books.append({
            "title": meta.get("title", idx.parent.name),
            "href": f"books/{idx.parent.name}/index.html",
            "total_chapters": int(total) if str(total).isdigit() else None,
            "summarized": len(chapters),
            "my_thoughts": sum(c["my_thoughts"] for c in chapters),
            "chapters": chapters,
        })
    out = ROOT / "books" / "progress.json"
    out.write_text(json.dumps({"books": books}, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
