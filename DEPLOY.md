# 배포 안내 (GitHub 웹에서 직접 하는 단계)

사이트 주소: **https://daeha-invest.github.io**  (비용 0원, 도메인 구매 없음)

## 1. Organization 만들기

1. GitHub에 로그인 → 오른쪽 위 프로필 사진 → **Your organizations** → **New organization**
2. 요금제는 **Free** 선택
3. Organization name: `daeha-invest`
4. Contact email: 본인 이메일 (공개되지 않음)
5. "This organization belongs to: **My personal account**" 선택 → 다음 화면은 **Skip this step**

## 2. 저장소 만들기

1. https://github.com/organizations/daeha-invest/repositories/new
2. Owner: `daeha-invest`, Repository name: **`daeha-invest.github.io`** (정확히 이 이름이어야 기본 주소가 됨)
3. **Public** 선택
4. README, .gitignore, license는 모두 **추가하지 않음** (빈 저장소로 만들기)

## 3. Pages 설정

1. 저장소 → **Settings** → 왼쪽 **Pages**
2. Build and deployment → Source: **GitHub Actions** 선택 (저장은 자동)

## 4. Actions 권한 확인

1. Organization 페이지 → **Settings** → **Actions** → **General**
2. "Allow all actions and reusable workflows"가 선택되어 있는지 확인 (기본값)

## 5. 로컬에서 처음 올리기 (터미널)

```bash
cd ~/Documents/daehakim-waterlab/daeha-invest.github.io
git config core.hooksPath .githooks
python3 scripts/check_amounts.py --all
git add .
git status            # private/, sources/*.docx 가 목록에 없는지 확인
git commit -m "사이트 시작"
git branch -M main
git remote add origin https://github.com/daeha-invest/daeha-invest.github.io.git
git push -u origin main
```

푸시하면 저장소의 **Actions** 탭에서 "Publish site"가 돌아갑니다 (2~3분).
초록색 체크가 뜨면 https://daeha-invest.github.io 에서 확인하세요.

## 6. 이후

- 내용을 고치고 `git add` → `git commit` → `git push` 하면 자동으로 다시 배포됩니다.
- 금액 검사에 걸리면 커밋이 멈춥니다. 메시지를 보고 고치거나, 금액이 아니면 `amount-ok` 표시를 넣으세요.
- 배포가 실패하면 Actions 탭의 빨간 X를 눌러 로그를 확인하세요. 첫 단계(금액 검사)에서 멈췄다면 위와 같은 이유입니다.

## 확인해 둘 것

- 저장소가 Public이므로 커밋 기록 전체가 공개됩니다. 한 번 올린 금액은 나중에 지워도 기록에 남으니,
  커밋 전에 `git status`와 `git diff --cached`로 한 번 더 보는 습관을 들이세요.
- `private/`와 `sources/*.docx`는 `.gitignore`로 제외됩니다. `git add -f`로 강제로 넣지 마세요.
