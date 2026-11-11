# Quant & Current (daeha-invest.github.io)

Quarto 웹사이트입니다. 책 공부 노트, 투자 전략, 투자일지, 대시보드로 구성됩니다.
**투자 금액은 어디에도 기록하지 않습니다.** 비중(%)과 수익률(%)만 씁니다.

## 처음 한 번

```bash
export PATH="$HOME/Applications/quarto/bin:$PATH"   # ~/.zshrc 에 넣어 두면 편합니다
git config core.hooksPath .githooks                 # 금액 검사 pre-commit 훅 켜기
```

## 로컬 미리보기

```bash
quarto preview
```

브라우저가 열리고, 파일을 저장하면 바로 갱신됩니다. `draft: true`인 일지도 미리보기에서는 보입니다.

## 자주 하는 일

| 하고 싶은 일 | 방법 |
|---|---|
| 새 일지 | `./scripts/new_journal.sh` (오늘) / `./scripts/new_journal.sh 2026-11-10 "제목"` |
| 일지 공개 | 일지 머리말의 `draft: true` 줄 지우기 |
| 새 투자 가설 | `./scripts/new_hypothesis.sh "가설 한 줄"` (기한 기본 3개월, 두 번째 인자로 지정) |
| 가설 결과 기록 | 가설 머리말의 `status`를 `맞음`·`틀림`·`보류`로 바꾸고 결과·배운 점 작성 |
| 용어 추가 | `books/glossary.qmd`에 `### 용어` 한 단락 추가 |
| 리밸런싱 일정 변경 | `js/schedule.js`의 `RULES`, `QUARTERLY` 수정 (홈 D-day와 운용 캘린더에 반영) |
| 매매 기록 | `data/trades.csv`에 한 줄 추가 |
| 자산배분 기록 | `data/allocation.csv`에 날짜별 비중(%) 한 줄 추가 (합계 100) |
| 전략 수익률 | `data/returns.csv`에 한 줄 추가 |
| 책 '내 생각' 작성 | 장 파일 끝의 '내 생각'을 채우고 머리말 `my-thoughts: true` |
| 금액 검사만 돌리기 | `python3 scripts/check_amounts.py --all` |

### CSV 형식

`data/trades.csv`: 수량·가격·평가금액·계좌 열은 만들지 않습니다 (훅이 막습니다).

```
날짜,전략,종목,매수매도,비중변화_pp,사유
2026-11-28,HAA,GLD,매수,+33.3,모멘텀 상위 3위 진입
```

`data/allocation.csv`: 열(자산군)은 자유롭게 추가할 수 있습니다. 첫 열은 `날짜`.

```
날짜,주식,채권,금·원자재,현금
2026-11-28,50,25,15,10
```

`data/returns.csv`: 전략별 구간 수익률(%).

```
기준일,전략,구간,수익률_pct,비교지수,비교지수_pct
2026-12-31,HAA,2026년,8.4,SPY,12.1
```

전략 이름은 `한국 소형주`, `미국 PSR`, `HAA`처럼 일정하게 써 주세요 (대시보드 필터에 그대로 쓰입니다).

## 금액 안전장치

- `private/`: 계좌번호, 증권사 정보, 원본 데이터, 원본 노트북. `.gitignore`로 제외됩니다.
- **pre-commit 훅**: 커밋할 때 `data/`, `journal/`, `hypotheses/`에서 금액처럼 보이는 패턴을 찾으면 커밋을 멈춥니다.
  숫자+원·만원·억, `$`·₩, 달러·USD·KRW, `1,234` 같은 쉼표 숫자, 금지된 CSV 열 이름, 100을 넘는 비중 값.
  금액이 아니면 그 줄에 `amount-ok`를 넣으세요 (.qmd는 `<!-- amount-ok -->`).
- **GitHub Actions**: 같은 검사를 배포 전에 한 번 더 합니다. 걸리면 배포되지 않습니다.
- 대시보드는 CSV에서 정해진 열만 읽습니다. 다른 열이 있어도 화면에 나오지 않습니다.

## 책 노트 추가 (docx → qmd)

```bash
python3 scripts/docx_to_qmd.py sources/damodaran/ch09.docx books/damodaran-iv/ch09.qmd
```

- 기존 .qmd는 `--force` 없이는 덮어쓰지 않습니다 ('내 생각'을 지키기 위해).
- 원본 docx는 `sources/`에 두고, 공개 저장소에는 올라가지 않습니다.
- 텍스트로 쓴 수식 중 핵심 공식은 `scripts/formulas.py`에 LaTeX로 등록해 두었습니다.
  새 장의 공식도 같은 방식으로 추가할 수 있습니다.
- 다른 책은 `books/<책-이름>/index.qmd`를 만들고 같은 방식으로 장을 넣으면 됩니다.

## 노트북 공개본

```bash
python3 scripts/sanitize_notebook.py "<원본.ipynb>" strategies/notebooks/portfolio-kr-us-stocks.ipynb
```

투자금 설정값(`KR_POSITION_SIZE`, `TOTAL_KR`, `TOTAL_US`)과 그 값이 드러나는 출력을 지운 사본을 만듭니다.
남은 금액이 보이면 저장하지 않고 멈춥니다. 노트북은 사이트에서 실행되지 않고 저장된 출력만 보입니다.

## 폴더

```
books/        책 노트 (책마다 폴더)
strategies/   전략 페이지, notebooks/ 공개용 노트북
journal/      일지 YYYY-MM-DD.qmd
hypotheses/   투자 가설 YYYY-MM-DD-N.qmd
tools/        계산기 4종, 운용 캘린더 (브라우저 안에서만 계산)
js/           운용 일정 규칙 (schedule.js)
data/         trades.csv, allocation.csv, returns.csv (비중·수익률 %만)
scripts/      일지 생성, docx 변환, 금액 검사, 노트북 정리
private/      비공개 (Git 제외)
sources/      원본 docx (Git 제외)
```
