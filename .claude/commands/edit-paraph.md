# /edit-paraph — 웹 아티클 → 블로그 포스트 (블로그 주인장 목소리 강화 버전)

이 스킬은 유저 레벨 스킬이므로 어디서든 호출 가능하다.
모든 작업의 대상은 아래 블로그 프로젝트이다:

```
BLOG_ROOT = "C:/Users/windo/Desktop/03_코딩·개발/Github Desktop/tigerjk9.github.io"
```

## 사용법
/edit-paraph <URL> [URL2 URL3 ...] [옵션]

## 설명
웹 페이지 URL을 받아 내용을 한국어로 패러프레이즈해 Jekyll 블로그 포스트(`_posts/`)로 자동 변환합니다.
기존 `/paraph`와 달리 **블로그 주인장 목소리 강화** 프롬프트를 사용합니다.

**스타일 특징**:
- 필자의 직접 판단과 절제된 비관론이 최소 2곳 드러남
- 도입부가 질문에 국한되지 않음 — 선언·탄식·일화·역설 등 다양한 첫 문장
- 크로스오버 섹션이 억지 연결이면 본문에 통합하거나 생략
- 본문 내 [IMAGE: query] 마커로 다중 이미지 자동 삽입 (Pexels/DDG 검색)
- 핵심 판단 강조 시 `~됨·~임` 명사형 단문 허용

## 실행

`$ARGUMENTS`가 비어 있으면 URL을 먼저 물어보세요.

아래 명령어를 실행하세요:

```bash
cd "C:/Users/windo/Desktop/03_코딩·개발/Github Desktop/tigerjk9.github.io"
python scripts/web_to_post.py $ARGUMENTS --edit
```

**복수 URL 예시**:
```bash
python scripts/web_to_post.py https://a.com/article1 https://b.com/article2 --edit
```

## 동작 순서
1. `.env`에서 GEMINI_API_KEY 자동 로드
2. 각 URL에서 제목·본문 텍스트 추출 (requests + BeautifulSoup)
3. 본문 500자 미만이면 Jina Reader 폴백
4. 기존 포스트에서 카테고리·태그 수집
5. Gemini로 블로그 주인장 목소리 한국어 포스트 생성 (`edit_web_prompt_template.txt` 사용)
6. [IMAGE: query] 마커를 Pexels/DDG 이미지로 교체 (다중 이미지)
7. `_posts/`에 저장 후 git push

## 포스트 스타일
- **필자 관점**: 직접 판단·절제된 비관·수사학적 의심 최소 2곳
- **자유로운 도입부**: 선언·탄식·단문·일화·역설 중 선택
- **크로스오버 옵션화**: 자연스러우면 본문 통합, 억지 연결이면 생략
- **다중 이미지**: 본문 마커 기반 2~4개 이미지 자동 삽입
- **문체**: 단정체(`~이다`, `~한다`), 강조 시 `~됨·~임` 허용

## 옵션
- `--dry-run` : 파일 저장 없이 출력만 (테스트용)
- `--no-push` : git push 없이 로컬 저장만
- `--slug SLUG` : 파일명 슬러그 직접 지정
- `--date YYYY-MM-DD` : 포스트 날짜 지정
- `--model MODEL` : Gemini 모델 ID (기본값: gemini-2.5-flash)
