# /edit-video — YouTube 영상 → 블로그 포스트 (블로그 주인장 목소리 강화 버전)

## 사용법
/edit-video <YouTube_URL> [URL2 URL3 ...] [옵션]

## 설명
YouTube URL을 받아 영상 내용을 분석하고 Jekyll 블로그 포스트(`_posts/`)로 자동 변환합니다.
기존 `/video`와 달리 **블로그 주인장 목소리 강화** 프롬프트를 사용합니다.
GEMINI_API_KEY는 프로젝트 루트의 `.env` 파일에서 자동으로 읽습니다.

**스타일 특징**:
- 필자가 인상 깊었던 부분 중심으로 선택적 구성 (전체 내용 빠짐없이 다루지 않아도 됨)
- 필자의 직접 판단과 절제된 비관론이 최소 2곳 드러남
- 도입부가 질문에 국한되지 않음 — 선언·탄식·일화·역설 등 다양한 첫 문장
- 크로스오버 섹션이 억지 연결이면 본문에 통합하거나 생략
- 본문 내 [IMAGE: query] 마커로 다중 이미지 자동 삽입 (Pexels/DDG 검색)
- 핵심 판단 강조 시 `~됨·~임` 명사형 단문 허용

## 실행

`$ARGUMENTS`가 비어 있으면 YouTube URL을 먼저 물어보세요.

아래 명령어를 실행하세요:

```bash
python scripts/yt_to_post.py $ARGUMENTS --edit
```

**복수 URL 예시**:
```bash
python scripts/yt_to_post.py https://youtu.be/A https://youtu.be/B --edit
```

## 동작 순서
1. `.env`에서 GEMINI_API_KEY 자동 로드
2. 각 영상 메타데이터 수집 (제목·채널·날짜)
3. 자막 다운로드 시도 (한국어 → 영어 → yt-dlp 자동자막)
4. 자막 없으면 영상 설명(description)으로 대체
5. Gemini로 블로그 주인장 목소리 포스트 생성 (단일: `edit_yt_prompt_template.txt`, 복수: `edit_yt_multi_prompt_template.txt` 사용)
6. [IMAGE: query] 마커를 Pexels/DDG 이미지로 교체 (다중 이미지)
7. `_posts/`에 저장 후 git push

## 포스트 스타일
- **선택적 구성**: 인상 깊은 부분 중심, 덜 흥미로운 부분은 압축
- **필자 관점**: 직접 판단·절제된 비관·수사학적 의심 최소 2곳
- **자유로운 도입부**: 선언·탄식·단문·일화·역설 중 선택
- **크로스오버 옵션화**: 자연스러우면 본문 통합, 억지 연결이면 생략
- **다중 이미지**: 본문 마커 기반 2~4개 이미지 자동 삽입
- **문체**: 단정체(`~이다`, `~한다`), 강조 시 `~됨·~임` 허용

## 옵션
- `--dry-run` : 파일 저장 없이 출력만 (테스트용)
- `--no-push` : git push 없이 로컬 저장만
- `--lang en` : 영어 자막 우선
- `--slug SLUG` : 파일명 슬러그 직접 지정
- `--date YYYY-MM-DD` : 포스트 날짜 지정
- `--model MODEL` : Gemini 모델 ID (기본값: gemini-2.0-flash)

## .env 설정
프로젝트 루트에 `.env` 파일 생성:
```
GEMINI_API_KEY=AIza...
```
`.env`는 `.gitignore`에 등록되어 있어 git에 올라가지 않습니다.
