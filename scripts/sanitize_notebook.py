#!/usr/bin/env python3
"""Make a public copy of a strategy notebook with money amounts removed.

    python3 scripts/sanitize_notebook.py "<original.ipynb>" strategies/notebooks/<name>.ipynb

The original is never changed. The copy keeps code and saved outputs (it is
not executed) and:
- replaces the value of amount settings (REDACT_VARS) with None
- removes comments that reveal an amount derived from them
- rewrites output lines that mention the per-stock amount
- drops Colab metadata
Then it scans the copy and stops with an error if anything amount-like
remains in code or outputs, so check the message before publishing.
Edit REDACT_VARS / OUTPUT_RULES when a new notebook version adds settings.
"""
import json
import re
import sys
from pathlib import Path

REDACT_VARS = ["KR_POSITION_SIZE", "TOTAL_KR", "TOTAL_US"]
COMMENT_RULES = [
    (re.compile(r"\s*#\s*→\s*기본\s*[\d천백만억,.]+\s*원.*$"), ""),       # "# → 기본 5천만원"
]
OUTPUT_RULES = [
    (re.compile(r"20일 평균 거래대금 [\d.]+억 이상 \(종목당 [\d,]+만원 기준\)"),
     "20일 평균 거래대금 하한 이상 (종목당 투자금 기준, 금액 비공개)"),
]
# anything still matching these after sanitizing stops the script
LEAK = re.compile(r"종목당\s*[\d,]+\s*만원|(?:POSITION_SIZE|TOTAL_KR|TOTAL_US)\s*=\s*[\d_]+")


def lines(src):
    return "".join(src) if isinstance(src, list) else src


def to_list(text):
    parts = text.split("\n")
    return [p + "\n" for p in parts[:-1]] + ([parts[-1]] if parts[-1] else [])


def sanitize_code(code: str) -> str:
    out = []
    for line in code.split("\n"):
        for var in REDACT_VARS:
            m = re.match(rf"^(\s*{var}\s*=\s*)[^#\n]*(#.*)?$", line)
            if m:
                line = f"{m.group(1)}None  # 비공개: 실제 값은 원본 노트북(private)에만 둠"
        for rx, rep in COMMENT_RULES:
            line = rx.sub(rep, line)
        out.append(line)
    return "\n".join(out)


def sanitize_text(text: str) -> str:
    for rx, rep in OUTPUT_RULES:
        text = rx.sub(rep, text)
    return text


def main(src, dst):
    nb = json.loads(Path(src).read_text(encoding="utf-8"))
    nb["metadata"].pop("colab", None)
    nb["metadata"].pop("widgets", None)
    for cell in nb["cells"]:
        cell.get("metadata", {}).pop("colab", None)
        cell.get("metadata", {}).pop("executionInfo", None)
        cell.get("metadata", {}).pop("outputId", None)
        if cell["cell_type"] != "code":
            continue
        cell["source"] = to_list(sanitize_code(lines(cell["source"])))
        for o in cell.get("outputs", []):
            if "text" in o:
                o["text"] = to_list(sanitize_text(lines(o["text"])))
            for k in ("text/plain", "text/html", "text/markdown"):
                if k in o.get("data", {}):
                    o["data"][k] = to_list(sanitize_text(lines(o["data"][k])))

    # public-copy note + Quarto options as the first cells
    note = {"cell_type": "markdown", "metadata": {}, "source": to_list(
        "::: {.callout-note}\n"
        "공개용 정리본입니다. 실행하지 않고 저장된 출력만 보여 줍니다. "
        "투자금 관련 설정값과 그 값이 드러나는 출력은 지웠습니다.\n"
        ":::\n")}
    nb["cells"].insert(1, note)

    leaks = []
    for i, cell in enumerate(nb["cells"]):
        blobs = [lines(cell["source"])]
        for o in cell.get("outputs", []):
            blobs.append(lines(o.get("text", "")))
            blobs += [lines(v) for k, v in o.get("data", {}).items() if k.startswith("text/")]
        for b in blobs:
            leaks += [(i, m.group(0)) for m in LEAK.finditer(b)]
    if leaks:
        for i, m in leaks:
            print(f"  cell {i}: {m!r}")
        sys.exit("금액이 남아 있어 저장하지 않았습니다. REDACT_VARS / OUTPUT_RULES를 고치세요.")

    Path(dst).parent.mkdir(parents=True, exist_ok=True)
    Path(dst).write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"wrote {dst}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
