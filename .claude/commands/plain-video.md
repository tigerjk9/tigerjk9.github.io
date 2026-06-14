# /plain-video — YouTube 영상 → 블로그 포스트 (담백한 전달 버전, 교육 앵커링 없음)

## 사용법
/plain-video <YouTube_URL> [URL2 URL3 ...] [옵션]

## 설명
YouTube URL을 받아 영상 내용을 분석하고 Jekyll 블로그 포스트(`_posts/`)로 변환합니다.
기존 `/video`·`/edit-video`와 달리 **교육 앵커링 없는 담백한 전달** 프롬프트(`plain_yt_*`)를 사용합니다.
GEMINI_API_KEY는 프로젝트 루트의 `.env` 파일에서 자동으로 읽습니다.

**스타일 특징 (담백한 설명자)**:
- 특정 분야(교육)에 얽매이지 않음 — 기술·경제·문화·과학·역사 등 주제는 영상이 정함
- 영상이 말한 내용을 정확하게·빠짐없이 전달하는 데 집중. 개인 의견은 절제
- 영상에 없는 사실·수치·인용을 지어내지 않음
- 프레임 추출(`--edit` 기능) 없이 썸네일/대표 이미지 1개 자동 삽입 (`/video` 기본 경로와 동일)
- 크로스오버(분야 연결) 섹션은 자연스러울 때만, 억지면 생략
- 단정체(`~이다`·`~한다`), 표 활용, AI 슬롭 금지 규칙은 동일하게 유지

**URL을 여러 개 전달하면 하나의 통합 포스트로 종합합니다.**

## 실행

`$ARGUMENTS`가 비어 있으면 YouTube URL을 먼저 물어보세요.

아래 명령어를 실행하세요 (yt_to_post.py 기본 모델 gemini-2.0-flash는 폐기되어 404가 나므로 `--model gemini-2.5-flash` 명시):

```bash
python scripts/yt_to_post.py $ARGUMENTS --plain --model gemini-2.5-flash
```

**복수 URL 예시**:
```bash
python scripts/yt_to_post.py https://youtu.be/A https://youtu.be/B --plain --model gemini-2.5-flash
```

## 동작 순서
1. `.env`에서 GEMINI_API_KEY 자동 로드
2. 각 영상 메타데이터 수집 (제목·채널·날짜)
3. 자막 다운로드 시도 (한국어 → 영어 → yt-dlp 자동자막)
4. 자막 없으면 영상 설명(description)으로 대체
5. Gemini로 담백한 전달 포스트 생성 (단일: `plain_yt_prompt_template.txt`, 복수: `plain_yt_multi_prompt_template.txt`)
6. 대표 이미지 자동 삽입 (teaser + 본문 첫 `##` 앞 figure)
7. 영문 permalink 삽입 후 `_posts/`에 저장 → git push

## 옵션
- `--dry-run` : 파일 저장 없이 출력만 (테스트용)
- `--no-push` : git push 없이 로컬 저장만
- `--lang en` : 영어 자막 우선
- `--slug SLUG` : 파일명 슬러그 직접 지정
- `--date YYYY-MM-DD` : 포스트 날짜 지정
- `--model MODEL` : Gemini 모델 ID (기본값 gemini-2.0-flash는 폐기 — 반드시 gemini-2.5-flash 지정)

## 후처리 (필수)
생성 직후 스크립트가 그대로 commit·push하므로, CLAUDE.md의 **자동화 포스트 후처리 QA 체크리스트** 7단계를 점검·교정한 뒤 별도 커밋합니다 (잔류 코드펜스·콜론 헤딩·출처 정확성·figure 빈 줄 등).
교육 앵커링 제거가 목적이므로, 생성물에 억지 교육 연결이 섞여 있으면 영상 주제에 맞게 교정합니다.

## .env 설정
프로젝트 루트에 `.env` 파일 생성:
```
GEMINI_API_KEY=AIza...
```
`.env`는 `.gitignore`에 등록되어 있어 git에 올라가지 않습니다.
