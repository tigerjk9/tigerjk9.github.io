# /plain-paraph — 웹 아티클 → 블로그 포스트 (담백한 전달 버전, 교육 앵커링 없음)

## 사용법
/plain-paraph <URL> [URL2 URL3 ...] [옵션]

## 설명
웹 페이지 URL을 받아 내용을 한국어로 재서술해 Jekyll 블로그 포스트(`_posts/`)로 변환합니다.
기존 `/paraph`·`/edit-paraph`와 달리 **교육 앵커링 없는 담백한 전달** 프롬프트(`plain_web_*`)를 사용합니다.
GEMINI_API_KEY는 프로젝트 루트의 `.env` 파일에서 자동으로 읽습니다.

**스타일 특징 (담백한 설명자)**:
- 특정 분야(교육)에 얽매이지 않음 — 기술·경제·문화·과학·역사 등 주제는 원문이 정함
- "교육 전문가가 한국 교육 현장에 적용하면" 같은 렌즈를 끼우지 않음
- 원문 정보를 정확하게·빠짐없이 전달하는 데 집중. 개인 의견은 절제
- 원문에 없는 사실·수치·인용을 지어내지 않음
- 크로스오버(분야 연결) 섹션은 자연스러울 때만, 억지면 생략
- 단정체(`~이다`·`~한다`), 표 활용, AI 슬롭 금지 규칙은 동일하게 유지

**URL을 여러 개 전달하면 하나의 통합 포스트로 종합합니다.**

## 실행

`$ARGUMENTS`가 비어 있으면 URL을 먼저 물어보세요.

아래 명령어를 실행하세요:

```bash
python scripts/web_to_post.py $ARGUMENTS --plain
```

**복수 URL 예시**:
```bash
python scripts/web_to_post.py https://a.com/article1 https://b.com/article2 --plain
```
→ 두 출처를 하나의 담백한 통합 포스트로 생성

## 동작 순서
1. `.env`에서 GEMINI_API_KEY 자동 로드
2. 각 URL에서 제목·본문 텍스트 추출 (requests + BeautifulSoup, 폴백 Jina Reader)
3. 기존 포스트에서 카테고리·태그 수집
4. Gemini로 담백한 전달 포스트 생성 (단일: `plain_web_prompt_template.txt`, 복수: `plain_web_multi_prompt_template.txt`)
5. 이미지 자동 삽입 (teaser + 본문 첫 `##` 앞 figure) — `/paraph` 기본 경로와 동일
6. 영문 permalink 삽입 후 `_posts/`에 저장 → git push

## 옵션
- `--dry-run` : 파일 저장 없이 출력만 (테스트용)
- `--no-push` : git push 없이 로컬 저장만
- `--slug SLUG` : 파일명 슬러그 직접 지정
- `--date YYYY-MM-DD` : 포스트 날짜 지정
- `--notes '<메모>'` : 추가 맥락을 Gemini 프롬프트에 전달 (단일 URL)
- `--model MODEL` : Gemini 모델 ID (기본값: gemini-2.5-flash)

## 후처리 (필수)
생성 직후 스크립트가 그대로 commit·push하므로, CLAUDE.md의 **자동화 포스트 후처리 QA 체크리스트** 7단계를 점검·교정한 뒤 별도 커밋합니다 (잔류 코드펜스·콜론 헤딩·출처 정확성·figure 빈 줄 등).
교육 앵커링 제거가 목적이므로, 생성물에 "교육 현장", "교사" 같은 억지 교육 연결이 섞여 있으면 원문 주제에 맞게 교정합니다.
