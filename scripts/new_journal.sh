#!/bin/sh
# 새 투자일지 파일 만들기
#   ./scripts/new_journal.sh                  → 오늘 날짜
#   ./scripts/new_journal.sh 2026-11-10       → 지정한 날짜
#   ./scripts/new_journal.sh 2026-11-10 "HAA 리밸런싱"   → 제목까지
set -e
cd "$(dirname "$0")/.."
d="${1:-$(date +%F)}"
case "$d" in
  [0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]) ;;
  *) echo "날짜 형식은 YYYY-MM-DD 입니다: $d" >&2; exit 1 ;;
esac
title="${2:-$d 투자일지}"
f="journal/$d.qmd"
if [ -e "$f" ]; then echo "이미 있습니다: $f" >&2; exit 1; fi
cat > "$f" <<TEMPLATE
---
title: "$title"
date: $d
categories: []      # 태그 예: [HAA, 리밸런싱, 반성]
description: ""
draft: true         # 다 쓰면 이 줄을 지우세요. 그 전에는 사이트에 공개되지 않습니다.
---

## 판단

## 시장 메모

## 반성

TEMPLATE
echo "만들었습니다: $f"
