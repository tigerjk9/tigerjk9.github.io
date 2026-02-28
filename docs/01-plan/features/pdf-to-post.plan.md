# [Plan] pdf-to-post

## 개요

**기능명:** PDF 논문 → 블로그 포스트 자동 변환 워크플로
**목적:** `_papers/` 폴더에 연구 논문 PDF를 넣으면, Claude API로 한국어 학술 요약 포스트를 자동 생성하고 GitHub `_posts/`에 커밋·푸시한다.
**우선순위:** High

---

## 사용자 스토리

> 연구자로서, PDF를 지정 폴더에 넣고 명령 하나를 실행하면 내 블로그 스타일대로 요약된 포스트가 자동으로 GitHub에 올라가길 원한다.

---

## 워크플로 전체 흐름

```
1. 사용자가 PDF를 _papers/ 폴더에 위치
2. 스크립트 실행: python scripts/pdf_to_post.py _papers/paper.pdf
3. PDF 텍스트 추출 (pdfplumber)
4. Claude API 호출 → 한국어 학술 요약 생성
5. _posts/YYYY-MM-DD-slug.md 저장
6. git add → git commit → git push (main)
```

---

## 구현 범위 (Scope)

### In Scope
- `_papers/` 폴더 생성 (PDF 보관 전용, Jekyll 빌드 제외)
- `scripts/pdf_to_post.py` Python 스크립트
  - CLI 인자: PDF 파일 경로, 날짜(옵션), 슬러그(옵션)
  - PDF → 텍스트 추출
  - Claude API 호출 (Anthropic SDK)
  - 마크다운 front matter 자동 생성
  - `_posts/` 저장 후 git 커밋·푸시
- `scripts/requirements.txt` 의존성 파일
- `scripts/prompt_template.md` 프롬프트 템플릿

### Out of Scope
- GitHub Actions 자동화 (수동 스크립트 실행으로 충분)
- 이미지 자동 추출 (이미지는 별도 수동 추가)
- 여러 PDF 일괄 처리 (단일 PDF 처리가 우선)

---

## 포스트 출력 형식 (고정 템플릿)

```markdown
---
title: "{논문 제목의 한국어 의역}"
date: YYYY-MM-DD HH:MM:SS +0900
categories: [{카테고리1}, {카테고리2}]
tags: [{태그1}, {태그2}, {태그3}]
---

# {제목}

> "{핵심 인사이트 한 문장}"

{연구 핵심 요약 2~3줄}

---

## 1. 연구의 목적 및 방법
### 연구의 목적
### 연구 방법

---

## 2. 주요 발견
### (1) {소제목}
### (2) {소제목}

---

## 3. 결론 및 시사점
### (1) {소제목}
### (2) {소제목}

---

## 4. 리뷰어의 ADD(+) One: 교육 정책 및 연수 제언
### (1) {제언1}
### (2) {제언2}

---

## 5. 추가 탐구 질문
- {질문1}
- {질문2}
- {질문3}

---

_**출처:** {APA 형식 원문 인용}_
```

---

## 기술 스택

| 항목 | 선택 | 이유 |
|------|------|------|
| PDF 파싱 | `pdfplumber` | 텍스트 추출 정확도 우수 |
| Claude API | `anthropic` SDK (Python) | 한국어 학술 요약 품질 |
| Git 자동화 | subprocess + git CLI | 추가 라이브러리 불필요 |
| 언어 | Python 3.10+ | 스크립팅 표준 |

---

## 파일 구조

```
tigerjk9.github.io/
├── _papers/              # PDF 보관 (Jekyll 빌드 제외)
│   └── .gitkeep
├── scripts/
│   ├── pdf_to_post.py    # 메인 변환 스크립트
│   ├── requirements.txt  # pdfplumber, anthropic
│   └── prompt_template.md # Claude 프롬프트 템플릿
└── _posts/
    └── YYYY-MM-DD-slug.md  # 자동 생성 결과
```

---

## _config.yml 수정 사항

`_papers/` 를 Jekyll 빌드 제외 목록에 추가:

```yaml
exclude:
  - _papers
  # (기존 항목들...)
```

---

## Claude API 프롬프트 전략

- **역할 지정:** "당신은 AI 교육 연구 논문을 한국어로 리뷰하는 교육공학 전문가입니다."
- **구조 강제:** 위 마크다운 템플릿을 그대로 JSON/마크다운으로 요구
- **섹션별 지시:** 각 섹션(연구 목적, 방법, 발견, 결론, 제언, 탐구 질문)을 명시적으로 요청
- **리뷰어 ADD(+) One:** 논문에 없는 실용적 교육 정책 제언 추가 요청
- **front matter 생성:** 제목·카테고리·태그를 JSON으로 먼저 추출 후 삽입

---

## 성공 기준

- [ ] PDF 1개를 입력했을 때 `_posts/`에 올바른 마크다운 파일이 생성된다
- [ ] front matter(title, date, categories, tags)가 자동으로 채워진다
- [ ] 포스트 구조가 기존 블로그 스타일(5개 섹션)을 따른다
- [ ] git push까지 자동으로 완료된다
- [ ] `_papers/` 폴더가 Jekyll 빌드에 포함되지 않는다

---

## 리스크

| 리스크 | 대응 |
|--------|------|
| PDF 텍스트 추출 실패 (스캔본) | pdfplumber 실패 시 에러 메시지 출력 후 종료 |
| Claude API 키 미설정 | `ANTHROPIC_API_KEY` 환경변수 검사 후 안내 메시지 |
| 이미 존재하는 슬러그 충돌 | 날짜+타임스탬프로 고유 파일명 보장 |
| Git push 권한 없음 | SSH 키 설정 필요 시 안내 메시지 출력 |
