#!/usr/bin/env python3
"""Look for anything that looks like a money amount in data/ and journal/.

    python3 scripts/check_amounts.py --all            # every file in data/ and journal/
    python3 scripts/check_amounts.py --staged FILES   # staged versions (used by the pre-commit hook)
    python3 scripts/check_amounts.py FILES            # given files as they are on disk

Exit code 1 when something is found, so the commit (or the deploy in GitHub
Actions) stops. If a hit is not an amount (e.g. a market index level you
want to quote), add the marker  amount-ok  on that line (in a .qmd use
<!-- amount-ok -->, in a CSV put it in the 사유 text) and commit again.

Checks
- number + 원/만원/억/조 (원자재·원칙·원인 같은 단어는 제외)
- $, ₩ next to a number; number + 달러/USD/KRW
- large numbers with thousands separators (1,234 / 12,345,678)
- CSV headers that suggest amounts (수량, 가격, 금액, 평가, 계좌, ...)
- CSV value checks: 비중(%) columns must be numbers between -100 and 100
"""
import csv
import io
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCOPES = ("data/", "journal/")
MARKER = "amount-ok"

PATTERNS = [
    ("숫자+원 단위", re.compile(
        r"\d[\d,.]*\s*(?:천|백|만|억|조)?\s*원(?!자재|칙|인|리|유|래|본|전|화|소|형|숭이|문|점|활)")),
    ("숫자+만/억/조", re.compile(
        r"\d[\d,.]*\s*(?:천만|백만|만|억|조)(?!\s*(?:명|개|건|회|번|배|%|년|주년))")),
    ("통화 기호", re.compile(r"[$₩￦]\s*\d|\d\s*[$₩￦]")),
    ("숫자+통화", re.compile(r"\d[\d,.]*\s*(?:달러|불|USD|KRW|usd|krw)(?![A-Za-z])")),
    ("쉼표가 들어간 큰 숫자", re.compile(r"(?<![\d.])\d{1,3}(?:,\d{3})+(?![\d])")),
]

FORBIDDEN_HEADER = re.compile(
    r"수량|주수|가격|단가|금액|평가|계좌|잔고|원금|예수금|매입|매도금|체결|손익|"
    r"qty|quantity|shares|price|amount|value|account|balance|cost|pnl",
    re.I,
)
PERCENT_COLS = {
    "trades.csv": ["비중변화_pp"],
    "allocation.csv": None,          # every column except 날짜
    "returns.csv": ["수익률_pct", "비교지수_pct"],
}


def in_scope(p: str) -> bool:
    p = p.replace("\\", "/")
    return p.startswith(SCOPES)


def read(path: str, staged: bool) -> str:
    if staged:
        r = subprocess.run(["git", "show", f":{path}"], cwd=ROOT, capture_output=True)
        return r.stdout.decode("utf-8", "replace")
    return (ROOT / path).read_text(encoding="utf-8", errors="replace")


def scan_text(path, text, hits):
    for n, line in enumerate(text.splitlines(), 1):
        if MARKER in line:
            continue
        for name, rx in PATTERNS:
            for m in rx.finditer(line):
                hits.append((path, n, name, m.group(0).strip(), line.strip()))


def scan_csv(path, text, hits):
    rows = list(csv.reader(io.StringIO(text)))
    if not rows:
        return
    header = rows[0]
    for col in header:
        if FORBIDDEN_HEADER.search(col):
            hits.append((path, 1, "금지된 열 이름", col, ",".join(header)))
    name = Path(path).name
    pct = PERCENT_COLS.get(name, [])
    if pct is None:
        pct = [c for c in header if c != "날짜"]
    idx = [header.index(c) for c in pct if c in header]
    for n, row in enumerate(rows[1:], 2):
        joined = ",".join(row)
        if MARKER in joined or not any(c.strip() for c in row):
            continue
        # an unquoted "1,200,000" splits into extra columns
        if len(row) != len(header):
            hits.append((path, n, f"열 개수가 머리글과 다름 ({len(row)} ≠ {len(header)}): "
                         "쉼표가 들어간 숫자가 따옴표 없이 들어갔을 수 있음", "", joined))
        for name_, rx in PATTERNS[:4]:          # unit / currency patterns on the whole line
            for m in rx.finditer(joined):
                hits.append((path, n, name_, m.group(0).strip(), joined))
        for j, cell in enumerate(row):
            if j in idx:
                v = cell.strip().replace("%", "")
                if v == "":
                    continue
                try:
                    f = float(v)
                    if not -100 <= f <= 100:
                        hits.append((path, n, "비중/수익률 범위(-100~100) 밖", cell, joined))
                except ValueError:
                    hits.append((path, n, "비중/수익률 칸에 숫자가 아님", cell, joined))
                continue
            for pname, rx in PATTERNS[4:]:      # thousands separators inside a quoted cell
                for m in rx.finditer(cell):
                    hits.append((path, n, pname, m.group(0).strip(), joined))
        if name == "allocation.csv" and idx:
            try:
                s = sum(float(row[j].replace("%", "") or 0) for j in idx if j < len(row))
                if abs(s - 100) > 0.5:
                    hits.append((path, n, f"비중 합계가 100%가 아님 ({s:g}%)", "", joined))
            except ValueError:
                pass


def main(argv):
    staged = "--staged" in argv
    files = [a for a in argv if not a.startswith("--")]
    if "--all" in argv:
        files = [str(p.relative_to(ROOT)) for d in SCOPES for p in (ROOT / d).rglob("*") if p.is_file()]
    files = [f for f in files if in_scope(f) and Path(f).suffix in (".csv", ".qmd", ".md", ".txt", ".json")]
    hits = []
    for f in sorted(files):
        text = read(f, staged)
        (scan_csv if f.endswith(".csv") else scan_text)(f, text, hits)
    if not hits:
        print(f"금액 패턴 검사 통과 ({len(files)}개 파일)")
        return 0
    print("\n⚠️  금액처럼 보이는 내용이 있습니다. 공개 저장소에 올라가기 전에 확인하세요.\n")
    for path, n, name, m, line in hits:
        print(f"  {path}:{n}  [{name}]  {m!r}")
        print(f"      {line[:120]}")
    print("\n금액이 아니라면 그 줄에 'amount-ok' 표시를 넣고 다시 커밋하세요.")
    print("(.qmd: <!-- amount-ok -->,  CSV: 사유 칸에 amount-ok)")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
