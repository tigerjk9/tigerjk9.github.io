# /paraph — 웹 아티클 → 블로그 포스트 자동 패러프레이즈 변환

## 사용법
/paraph <URL> [옵션]

## 설명
웹 페이지 URL을 받아 내용을 한국어로 패러프레이즈해 Jekyll 블로그 포스트(`_posts/`)로 자동 변환합니다.
원본의 내용 구조는 그대로 유지하되, 교육 전문가의 시선으로 더 쉽고 재미있게 재구성합니다.
GEMINI_API_KEY는 프로젝트 루트의 `.env` 파일에서 자동으로 읽습니다.

## 실행

`$ARGUMENTS`가 비어 있으면 URL을 먼저 물어보세요.

아래 명령어를 실행하세요:

```bash
python scripts/web_to_post.py $ARGUMENTS
```

## 동작 순서
1. `.env`에서 GEMINI_API_KEY 자동 로드
2. URL에서 제목·본문 텍스트 추출 (requests + BeautifulSoup)
3. 기존 포스트에서 카테고리·태그 수집
4. Gemini로 한국어 패러프레이즈 블로그 포스트 생성
5. `_posts/`에 저장 후 git push

## 포스트 스타일
- **패러프레이즈**: 원본 내용 구조 유지, 서술 방식 재구성
- **교육 전문가 컨셉**: 전문 용어를 쉽게 풀고, 예시·비유 추가
- **크로스오버**: 뜻밖의 분야와 연결하는 마지막 섹션 (20개 분야 풀에서 랜덤)
- **문체**: 단정체(`~이다`, `~한다`)

## 옵션
- `--dry-run` : 파일 저장 없이 출력만 (테스트용)
- `--no-push` : git push 없이 로컬 저장만
- `--slug SLUG` : 파일명 슬러그 직접 지정
- `--date YYYY-MM-DD` : 포스트 날짜 지정
- `--model MODEL` : Gemini 모델 ID (기본값: gemini-2.5-flash)

## 의존성
`requests`와 `beautifulsoup4`가 필요합니다:
```bash
pip install requests beautifulsoup4
```

## .env 설정
프로젝트 루트에 `.env` 파일 생성:
```
GEMINI_API_KEY=AIza...
```
`.env`는 `.gitignore`에 등록되어 있어 git에 올라가지 않습니다.
