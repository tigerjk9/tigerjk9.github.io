# /paper

연구 논문 PDF를 한국어 블로그 포스트로 자동 변환하고 GitHub에 푸시합니다.
인자 없이 실행하면 `_papers/` 폴더에서 **아직 포스팅되지 않은 PDF만** 자동 선별해 일괄 처리합니다.

**사용법:**
```
/paper                          # _papers/ 미처리 PDF 전체 일괄 변환·푸시
/paper <PDF경로>                # 특정 PDF 1개만 변환·푸시
/paper <PDF경로> --date YYYY-MM-DD --slug 슬러그명
/paper <PDF경로> --no-push      # 로컬 저장만 (push 안 함)
/paper <PDF경로> --dry-run      # 출력만 (저장 안 함)
/paper --list                   # 미처리 PDF 목록만 확인 (처리 안 함)
```

---

## 워크플로

**$ARGUMENTS** = 비어있거나 / PDF 경로 및 옵션

### [1] 모드 결정

`$ARGUMENTS`를 파싱해 실행 모드를 결정한다:

- **배치 모드**: `$ARGUMENTS`가 비어있거나 `--list`만 있는 경우
- **단일 모드**: `$ARGUMENTS`의 첫 번째 인자가 `.pdf`로 끝나는 경우

---

### [배치 모드] 미처리 PDF 자동 선별

#### [B-1] 미처리 PDF 탐지

Bash tool로 다음 Python 스크립트를 실행해 미처리 PDF 목록을 얻는다:

```bash
cd "C:/Users/windo/Desktop/Github Desktop/tigerjk9.github.io"
python -c "
import re
from pathlib import Path

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\-]', '-', text)
    text = re.sub(r'-{2,}', '-', text)
    return text.strip('-')

papers = sorted(Path('_papers').glob('*.pdf'))
posts  = list(Path('_posts').glob('*.md'))

# _posts 파일명에서 날짜 제거 후 슬러그 추출
posted_slugs = set()
for p in posts:
    slug = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', p.stem)
    posted_slugs.add(slug)

for pdf in papers:
    slug = slugify(pdf.stem)
    status = 'DONE' if slug in posted_slugs else 'TODO'
    print(f'{status}|{pdf}|{slug}')
"
```

출력 형식: `TODO|_papers/논문.pdf|slug명` 또는 `DONE|_papers/논문.pdf|slug명`

#### [B-2] 결과 표시

탐지 결과를 아래 형식으로 사용자에게 보여준다:

```
📋 _papers/ 폴더 현황

✅ 이미 포스팅됨 (건너뜀):
  - 논문A.pdf  →  slug-a
  - 논문B.pdf  →  slug-b

🔄 미처리 (변환 예정):
  - 논문C.pdf  →  slug-c
  - 논문D.pdf  →  slug-d

총 N개 중 M개 처리 예정
```

`--list` 플래그가 있으면 여기서 중단한다.

미처리 PDF가 0개면: "모든 PDF가 이미 포스팅되어 있습니다." 출력 후 종료.

#### [B-3] GEMINI_API_KEY 확인

```bash
cd "C:/Users/windo/Desktop/Github Desktop/tigerjk9.github.io"
python -c "import os; print('OK' if os.environ.get('GEMINI_API_KEY') else 'MISSING')"
```

`MISSING`이면 아래를 안내하고 중단:
```
GEMINI_API_KEY가 설정되지 않았습니다.
PowerShell에서 먼저 실행하세요:
  $env:GEMINI_API_KEY = "AIza..."
```

#### [B-4] 미처리 PDF 순차 처리

`TODO` 상태인 PDF를 **하나씩 순서대로** 처리한다.
각 PDF마다:

```bash
cd "C:/Users/windo/Desktop/Github Desktop/tigerjk9.github.io"
python scripts/pdf_to_post.py {pdf_path}
```

각 실행 결과를 즉시 사용자에게 보여준다:
- 성공: `✅ {파일명} → 포스팅 완료`
- 실패: `❌ {파일명} → 오류: {메시지}` (실패해도 다음 PDF로 계속 진행)

#### [B-5] 배치 완료 보고

모든 처리가 끝나면 요약을 출력한다:

```
🎉 배치 처리 완료
  성공: N개
  실패: M개
  건너뜀(기존): K개
```

실패한 항목이 있으면 파일명과 오류 원인을 목록으로 보여준다.

---

### [단일 모드] 특정 PDF 1개 처리

#### [S-1] 인자 파싱

`$ARGUMENTS`에서 파싱:
- `pdf_path`: 첫 번째 인자
- `--date`: 날짜 (없으면 오늘)
- `--slug`: 슬러그 (없으면 자동 생성)
- `--no-push`: 있으면 push 생략
- `--dry-run`: 있으면 저장 없이 출력만

#### [S-2] 이미 포스팅된 PDF 확인

Bash tool로 동일 슬러그의 포스트가 있는지 확인한다:

```bash
cd "C:/Users/windo/Desktop/Github Desktop/tigerjk9.github.io"
python -c "
import re
from pathlib import Path

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\-]', '-', text)
    text = re.sub(r'-{2,}', '-', text)
    return text.strip('-')

pdf_stem = '{pdf_path의 파일명(확장자 제외)}'
slug = slugify(pdf_stem)
matches = list(Path('_posts').glob(f'*-{slug}.md'))
print('DONE:' + str(matches[0]) if matches else 'TODO')
"
```

결과가 `DONE:...`이면 사용자에게 알린다:
```
⚠️  이 PDF는 이미 포스팅되어 있습니다: {기존 포스트 파일명}
계속 진행하면 중복 포스트가 생성됩니다. 계속하시겠습니까?
```
→ AskUserQuestion으로 확인 후 계속 또는 중단.

`--dry-run`이면 이 확인을 건너뛴다.

#### [S-3] PDF 위치 처리

`_papers/` 폴더 밖 경로면 자동 복사:

```bash
cp "{pdf_path}" "_papers/"
```

복사 후 pdf_path를 `_papers/{파일명}.pdf`로 업데이트.

#### [S-4] GEMINI_API_KEY 확인

`--dry-run`이 아닌 경우:

```bash
python -c "import os; print('OK' if os.environ.get('GEMINI_API_KEY') else 'MISSING')"
```

`MISSING`이면 안내 후 중단.

#### [S-5] pdf_to_post.py 실행

```bash
cd "C:/Users/windo/Desktop/Github Desktop/tigerjk9.github.io"
python scripts/pdf_to_post.py {pdf_path} {옵션들}
```

#### [S-6] 결과 보고

성공 시:
- 생성된 파일명 안내
- `--dry-run`이 아닌 경우 포스트 URL 안내: `https://tigerjk9.github.io/{slug}/`

실패 시:
- `[ERROR]` 내용과 해결 방법 안내

---

### [선택] PaperBanana 학술 삽화 생성

배치 모드의 [B-5] 완료 후 또는 단일 모드의 [S-6] 완료 후,
PaperBanana 환경이 설치되어 있으면 학술 삽화 추가를 제안한다.

#### 환경 확인

```bash
ls "C:/Users/windo/Desktop/Github Desktop/Image-Generation-for-Writing/PaperBanana/.venv/Scripts/python.exe" 2>/dev/null && echo "OK" || echo "MISSING"
```

`MISSING`이면 이 단계를 건너뛴다 (안내 없이 조용히 스킵).

#### 사용자 확인

`OK`이면 AskUserQuestion으로 묻는다:
```
🍌 PaperBanana 학술 삽화를 추가로 생성하시겠습니까?
PDF의 Figure 캡션을 기반으로 학술 다이어그램을 자동 생성합니다.
```
- 옵션: "예" / "아니오"

#### 실행

"예"를 선택하면:

```bash
cd "C:/Users/windo/Desktop/Github Desktop/Image-Generation-for-Writing"
PaperBanana/.venv/Scripts/python scripts/banana_generate.py \
  --pdf "{원본_pdf_경로}" \
  --slug "{slug}" \
  --output-dir "C:/Users/windo/Desktop/Github Desktop/tigerjk9.github.io/assets" \
  --max-rounds 2 --candidates 1
```

타임아웃: 300초

#### 결과 처리

`SUCCESS:` 줄을 파싱해 생성된 이미지 경로를 수집하고,
해당 이미지를 포스트에 삽입할 마크다운 코드를 사용자에게 제안한다:

```
🍌 PaperBanana 삽화 생성 완료!
포스트에 다음 코드를 추가하시겠습니까?

![Figure 1: caption](/assets/slug-fig1.jpg)
```
