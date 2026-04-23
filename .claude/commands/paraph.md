# /paraph — 웹 아티클 → 블로그 포스트 자동 패러프레이즈 변환

이 스킬은 유저 레벨 스킬이므로 어디서든 호출 가능하다.
모든 작업의 대상은 아래 블로그 프로젝트이다:

```
BLOG_ROOT = "I:/내 드라이브/Github Desktop/tigerjk9.github.io"
```

## 사용법
/paraph <URL> [URL2 URL3 ...] [옵션]
/paraph <URL> [URL2 ...] --into <기존_포스트_경로>     # 머지 모드

## 설명
웹 페이지 URL을 받아 내용을 한국어로 패러프레이즈해 Jekyll 블로그 포스트(`_posts/`)로 자동 변환합니다.
원본의 내용 구조는 그대로 유지하되, 교육 전문가의 시선으로 더 쉽고 재미있게 재구성합니다.
번역이 아닌 재서술 — 원본 논지를 이해한 뒤 처음부터 새로 씁니다.

**URL을 여러 개 전달하면 하나의 통합 포스트로 종합합니다.**
각 출처의 핵심 논점을 목차식으로 나열하지 않고, 하나의 응집된 흐름으로 재구성합니다.

**`--into` 머지 모드**: 신규 포스트를 만드는 대신, 기존 포스트에 신규 자료를 녹여 같은 파일을 덮어씁니다.
기존 구조·문체·날짜·크로스오버 섹션을 보존하고, 신규 자료에서 수치·비유·인용·균형 관점·구조적 대안을 채굴해 자연스럽게 통합합니다.

## 실행

`$ARGUMENTS`가 비어 있으면 URL을 먼저 물어보세요.

아래 명령어를 실행하세요:

```bash
cd "I:/내 드라이브/Github Desktop/tigerjk9.github.io"
python scripts/web_to_post.py $ARGUMENTS
```

**복수 URL 예시**:
```bash
python scripts/web_to_post.py https://a.com/article1 https://b.com/article2
```
→ 두 출처를 하나의 포스트로 통합 생성

**머지 모드 예시**:
```bash
python scripts/web_to_post.py https://example.com/new-source --into _posts/2026-04-23-stolen-focus-systemic-crisis.md
```
→ 신규 자료를 기존 포스트에 통합·덮어쓰기. front matter의 `date`는 그대로 유지되어 SEO 슬러그·발행 시각이 보존됩니다.

## 동작 순서
1. `.env`에서 GEMINI_API_KEY 자동 로드
2. 각 URL에서 제목·본문 텍스트 추출 (requests + BeautifulSoup)
3. 본문 500자 미만이면 Jina Reader 폴백 (JS 렌더링 사이트 대응)
4. 기존 포스트에서 카테고리·태그 수집
5. Gemini로 한국어 패러프레이즈 블로그 포스트 생성
   - URL 1개: 단일 출처 패러프레이즈
   - URL 2개 이상: 복수 출처 통합·종합 포스트
6. `_posts/`에 저장 후 git push

## 포스트 스타일
- **패러프레이즈**: 원문 이해 후 재서술. 번역 금지.
- **교육 전문가 컨셉**: 전문 용어를 쉽게 풀고, 한국 교육 맥락 예시 추가
- **크로스오버**: 뜻밖의 분야와 연결하는 마지막 섹션 (20개 분야 풀에서 랜덤)
- **문체**: 단정체(`~이다`, `~한다`)

## 옵션
- `--dry-run` : 파일 저장 없이 출력만 (테스트용)
- `--no-push` : git push 없이 로컬 저장만
- `--slug SLUG` : 파일명 슬러그 직접 지정
- `--date YYYY-MM-DD` : 포스트 날짜 지정
- `--model MODEL` : Gemini 모델 ID (기본값: gemini-2.5-flash)
