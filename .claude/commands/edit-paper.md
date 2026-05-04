# /edit-paper — PDF 논문 → 블로그 포스트 (블로그 주인장 목소리 강화 버전)

## 사용법
/edit-paper <PDF_경로> [옵션]

## 설명
PDF 논문 파일을 받아 내용을 분석하고 Jekyll 블로그 포스트(`_posts/`)로 자동 변환합니다.
기존 `/paper`와 달리 **블로그 주인장 목소리 강화** 프롬프트를 사용합니다.
GEMINI_API_KEY는 프로젝트 루트의 `.env` 파일에서 자동으로 읽습니다.

**스타일 특징**:
- 6섹션 고정 구조 대신 3~5개 자유 구조 (논문 흐름에 맞게 필자가 결정)
- 필자의 직접 판단과 절제된 비관론이 최소 2곳 드러남
- 도입부가 질문에 국한되지 않음 — 선언·탄식·일화·역설 등 다양한 첫 문장
- 크로스오버 섹션이 억지 연결이면 본문에 통합하거나 생략
- 본문 내 [IMAGE: query] 마커로 다중 이미지 자동 삽입 (Pexels/DDG 검색)
- 동사형 단정체(`~이다`, `~한다`), 강조 시 `~됨·~임` 허용

## 실행

`$ARGUMENTS`가 비어 있으면 PDF 경로를 먼저 물어보세요.

아래 명령어를 실행하세요:

```bash
python scripts/pdf_to_post.py $ARGUMENTS --edit
```

## 동작 순서
1. `.env`에서 GEMINI_API_KEY 자동 로드
2. PDF에서 텍스트 추출 (pdfplumber)
3. PyMuPDF로 300×200px 이상 이미지 최대 6개 추출 → `assets/` 저장
4. Gemini로 블로그 주인장 목소리 포스트 생성 (`edit_paper_prompt_template.txt` 사용)
5. [IMAGE: query] 마커를 Pexels/DDG 이미지로 교체 (다중 이미지)
6. `_posts/`에 저장 후 git push

## 포스트 구조 (자유 구조)

3~5개 섹션을 논문 흐름에 따라 자유 구성. 필수 포함 요소:
- 이 연구가 왜 나왔는가 (배경·문제의식)
- 무엇을 어떻게 했는가 (방법·발견)
- 현장에서 어떤 의미인가 (시사점)
- 이 연구의 한계나 필자의 비판적 관점 (1곳 이상)

## 옵션
- `--dry-run` : 파일 저장 없이 출력만 (테스트용)
- `--no-push` : git push 없이 로컬 저장만
- `--keep-pdf`: 처리 후 원본 PDF 보존 (기본은 자동 삭제)

## .env 설정
프로젝트 루트에 `.env` 파일 생성:
```
GEMINI_API_KEY=AIza...
```
`.env`는 `.gitignore`에 등록되어 있어 git에 올라가지 않습니다.

## PDF 파일 위치 및 생명주기
논문 PDF는 `_papers/` 디렉토리에 넣습니다:
```bash
python scripts/pdf_to_post.py _papers/paper.pdf --edit
```

- `_papers/*.pdf`는 `.gitignore`에 등록되어 저장소에 커밋되지 않습니다.
- 처리가 완료되면 **원본 PDF는 자동 삭제**되어 로컬 용량이 쌓이지 않습니다.
- 원본을 보존하려면 `--keep-pdf` 플래그를 사용하세요.
