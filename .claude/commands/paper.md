# /paper — PDF 논문 → 블로그 포스트 자동 변환

## 사용법
/paper <PDF_경로> [옵션]

## 설명
PDF 논문 파일을 받아 내용을 분석하고 Jekyll 블로그 포스트(`_posts/`)로 자동 변환합니다.
GEMINI_API_KEY는 프로젝트 루트의 `.env` 파일에서 자동으로 읽습니다.

## 실행

`$ARGUMENTS`가 비어 있으면 PDF 경로를 먼저 물어보세요.

아래 명령어를 실행하세요:

```bash
python scripts/pdf_to_post.py $ARGUMENTS
```

## 동작 순서
1. `.env`에서 GEMINI_API_KEY 자동 로드
2. PDF에서 텍스트 추출 (pdfplumber)
3. PyMuPDF로 300×200px 이상 이미지 최대 6개 추출 → `assets/` 저장
4. Gemini로 한국어 블로그 포스트 생성 (6개 고정 섹션)
5. `_posts/`에 저장 후 git push

## 포스트 구조 (고정 6섹션)
1. 연구목적
2. 방법
3. 발견
4. 결론
5. ADD One
6. 탐구질문
+ APA 출처

## 옵션
- `--dry-run` : 파일 저장 없이 출력만 (테스트용)
- `--no-push` : git push 없이 로컬 저장만

## .env 설정
프로젝트 루트에 `.env` 파일 생성:
```
GEMINI_API_KEY=AIza...
```
`.env`는 `.gitignore`에 등록되어 있어 git에 올라가지 않습니다.

## PDF 파일 위치
논문 PDF는 `_papers/` 디렉토리에 넣는 것을 권장합니다:
```bash
python scripts/pdf_to_post.py _papers/paper.pdf
```
