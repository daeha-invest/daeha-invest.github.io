// 운용 일정 계산 (외부 데이터 없음). 규칙이 바뀌면 RULES만 고치면 됩니다.
// month: 1~12

export const QUARTERLY = [ // 한국 소형주 · 미국 PSR 스크리너 (공시 마감 직후)
  {month: 4, day: 1}, {month: 6, day: 17}, {month: 8, day: 17}, {month: 11, day: 17}
];

export const RULES = [
  {id: "haa", short: "HAA", name: "HAA ETF 동적배분", kind: "monthly-last-friday",
   href: "strategies/haa-etf.html", note: "매월 마지막 금요일 국내장 아침"},
  {id: "kr", short: "한국 소형주", name: "한국 소형주 가치+모멘텀", kind: "quarterly",
   href: "strategies/kr-smallcap-value-momentum.html", note: "정기보고서 제출 마감 직후"},
  {id: "us", short: "미국 PSR", name: "미국 PSR", kind: "quarterly",
   href: "strategies/us-psr.html", note: "스크리너와 같은 날 점검"},
];

function lastFriday(year, month) {          // month 1~12
  const d = new Date(year, month, 0);       // 그 달 마지막 날
  while (d.getDay() !== 5) d.setDate(d.getDate() - 1);
  return d;
}

function startOfDay(d) { const x = new Date(d); x.setHours(0, 0, 0, 0); return x; }

export function upcoming(from = new Date(), monthsAhead = 12) {
  const today = startOfDay(from);
  const out = [];
  for (let k = 0; k <= monthsAhead; k++) {
    const y = today.getFullYear() + Math.floor((today.getMonth() + k) / 12);
    const m = ((today.getMonth() + k) % 12) + 1;
    for (const r of RULES) {
      if (r.kind === "monthly-last-friday") out.push({...r, date: lastFriday(y, m)});
      if (r.kind === "quarterly")
        for (const q of QUARTERLY) if (q.month === m) out.push({...r, date: new Date(y, m - 1, q.day)});
    }
  }
  return out
    .filter(e => e.date >= today)
    .sort((a, b) => a.date - b.date || a.name.localeCompare(b.name))
    .map(e => ({...e, days: Math.round((e.date - today) / 86400000),
                weekend: e.date.getDay() === 0 || e.date.getDay() === 6}));
}

export function fmt(d) {
  const w = "일월화수목금토"[d.getDay()];
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")} (${w})`;
}
