# /video — YouTube 영상 → 블로그 포스트 자동 변환

## 사용법
/video <YouTube_URL> [옵션]

## 설명
YouTube URL을 받아 영상 내용을 분석하고 Jekyll 블로그 포스트(`_posts/`)로 자동 변환합니다.
GEMINI_API_KEY는 프로젝트 루트의 `.env` 파일에서 자동으로 읽습니다.

## 실행

`$ARGUMENTS`가 비어 있으면 YouTube URL을 먼저 물어보세요.

아래 명령어를 실행하세요:

```bash
python scripts/yt_to_post.py $ARGUMENTS
```

## 동작 순서
1. `.env`에서 GEMINI_API_KEY 자동 로드
2. 영상 메타데이터 수집 (제목·채널·날짜)
3. 자막 다운로드 시도 (한국어 → 영어 → yt-dlp 자동자막)
4. 자막 없으면 영상 설명(description)으로 대체
5. Gemini로 한국어 블로그 포스트 생성
6. `_posts/`에 저장 후 git push

## 옵션
- `--dry-run` : 파일 저장 없이 출력만 (테스트용)
- `--no-push` : git push 없이 로컬 저장만
- `--lang en` : 영어 자막 우선
- `--slug SLUG` : 파일명 슬러그 직접 지정

## .env 설정
프로젝트 루트에 `.env` 파일 생성:
```
GEMINI_API_KEY=AIza...
```
`.env`는 `.gitignore`에 등록되어 있어 git에 올라가지 않습니다.
