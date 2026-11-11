#!/bin/sh
# 새 투자 가설 파일 만들기
#   ./scripts/new_hypothesis.sh "HAA가 다음 분기 방어로 전환한다"
#   ./scripts/new_hypothesis.sh "제목" 2027-03-31        → 검증 기한 지정 (기본: 3개월 뒤)
set -e
cd "$(dirname "$0")/.."
title="${1:?가설 제목을 따옴표로 넣어 주세요}"
d=$(date +%F)
deadline="${2:-$(date -v+3m +%F 2>/dev/null || date -d '+3 months' +%F)}"
n=1; f="hypotheses/$d-$n.qmd"
while [ -e "$f" ]; do n=$((n+1)); f="hypotheses/$d-$n.qmd"; done
cat > "$f" <<TEMPLATE
---
title: "$title"
date: $d
deadline: $deadline
status: "진행 중"     # 진행 중 / 맞음 / 틀림 / 보류
confidence: 60        # 세울 때의 확신 (%)
categories: []        # 예: [HAA, 금리]
draft: true           # 다 쓰면 이 줄을 지우세요. 그 전에는 사이트에 공개되지 않습니다.
---

## 가설

## 근거

## 판단 기준
- 맞음: 
- 틀림: 

## 결과

## 배운 점

TEMPLATE
echo "만들었습니다: $f"
