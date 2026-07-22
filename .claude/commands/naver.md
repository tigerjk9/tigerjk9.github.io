# /naver — 깃허브 블로그 포스트를 네이버 블로그로 크로스포스팅

## 사용법
/naver [옵션]

## 설명
`_posts/`의 포스트를 네이버 블로그(blog.naver.com/dot_connector)에 자동 발행합니다.
Playwright가 로그인된 브라우저(스크립트 전용 프로필)로 스마트에디터 ONE을 조작합니다.
카테고리는 3곳(인공지능교육 인사이트 26 / 뇌기반 학습 과학 84 / 생각하는 교실, 깊이있는 학습 87)
중 Gemini 일괄 분류 결과(`scripts/naver_category_overrides.json`)를 따르고,
본문은 마루부리 15(소제목 19)로 발행됩니다. 글 끝에 원 작성일 + 원문 링크가 자동 삽입됩니다.

## 실행

기본(미게시 포스트 5편 발행, 글 간 45~90초 대기):

```bash
py -u scripts/naver_crosspost.py --limit 5
```

`$ARGUMENTS`가 있으면 그대로 전달하세요. 주요 옵션:
- `--dry-run` — 대상 목록·분류 미리보기 (브라우저 안 뜸)
- `--post _posts/파일.md` — 특정 포스트만 발행 (게시 이력 무시하고 재발행)
- `--category ai|brain|class` — 분류 수동 지정
- `--limit N` — 이번 실행 발행 수 (기본 5)
- `--no-images` — 이미지 제외
- `--no-publish` — 발행 직전까지만 진행 (검수용, 브라우저 창을 닫으면 종료)
- `--login` — 로그인 쿠키 갱신 (401/로그인 풀림 시)
- `--classify-gemini` — 신규 포스트 추가 후 분류 갱신 (기존 수동 교정은 보존)
- `--update <logNo> --post <파일>` — 이미 발행된 네이버 글의 본문만 교체
  (제목·카테고리·태그 유지. 변환 로직 개선 후 기존 글 재포맷에 사용)

## 실행 후 반드시

1. 출력의 `[OK] <URL>` 라인으로 발행 성공 여부 확인. `[FAIL]`이면 `scripts/.naver_shots/`의
   에러 스크린샷을 확인하고 원인(팝업 변화, 로그인 만료 등)을 파악할 것
2. 첫 글 URL을 열어 서체(마루부리 15)·표·이미지 렌더링 확인 (모바일 API로 확인 가능:
   `curl -sk https://m.blog.naver.com/dot_connector/<logNo>` 에서 `se-ff-nanummaruburi`·`se-fs-fs15` 클래스)
3. `scripts/naver_crosspost_state.json` 변경분 커밋 (게시 이력 = 중복 발행 방지 데이터)

## 운영 규칙
- **자동 실행 등록됨 (2026-07-23부터)**: Windows 작업 스케줄러 `NaverCrosspost` 태스크가
  매일 10:00·16:00에 5편씩 자동 발행 (하루 10편, 로그 `scripts/naver_task.log`).
  PC가 꺼져 있으면 다음 부팅 시 실행(StartWhenAvailable). 수동 `/naver` 실행과 겹치면
  프로필 잠금으로 한쪽이 실패하니 스케줄 시간대는 피할 것
  - 시간 변경: `Set-ScheduledTask -TaskName NaverCrosspost -Trigger (New-ScheduledTaskTrigger -Daily -At HH:MM), ...`
  - 중지: `Disable-ScheduledTask -TaskName NaverCrosspost` / 재개: `Enable-ScheduledTask`
- 첫 며칠은 새 글이 네이버 검색에 노출되는지 확인 (검색 누락이 보이면 하루 5편으로 감속)
- 로그인이 풀리면(발행 실패 + "로그인 쿠키가 없습니다") `--login`으로 재로그인.
  쿠키는 `scripts/.naver_profile/cookies.json`에 백업됨 (gitignore, 절대 커밋 금지)
- 네이버 게시일은 실행일이 됨 (원 작성일은 글 말미 표기)
- 새 포스트가 늘면: 자동으로 대상에 포함됨. 분류가 필요하면 `--classify-gemini` 재실행
  (규칙 폴백이 있어 안 돌려도 발행은 됨)
- 분류를 고치고 싶으면 `scripts/naver_category_overrides.json`에서 해당 파일명의 값을
  `ai`/`brain`/`class`로 수정 (Gemini 재실행에도 수동값 우선)

## 동작 특성 (2026-07-22 실측 검증)
- 대상 범위: `BASELINE_FILENAME`(2026-05-14 measuring-ai...) 이후 ~ 최신, 주간다이제스트 제외
- 카테고리는 글쓰기 URL `postwrite?categoryNo=N`으로 사전 선택됨 (발행 팝업에서 이중 확인)
- 본문 크기 15는 붙여넣기 HTML의 인라인 `font-size:15px` → 에디터 `se-fs15` 매핑으로 구현
- **가독성 여백**: 네이버 에디터는 문단 여백이 없어 블록 요소(문단·표·목록·소제목 앞) 사이에
  빈 문단 `<p><br></p>`을 자동 삽입 (소제목 뒤는 본문과 밀착). 2026-07-22 첫 글에서 벽글
  현상 확인 후 추가 — 제거하면 가독성 회귀함
- 서체는 붙여넣기 후 Ctrl+A → 고정 툴바 서체 버튼(`data-group='propertyToolbar'`) → 마루부리 클릭
  (크기는 요소별 보존됨)
- 표·볼드·소제목(fs19)·링크가 에디터 네이티브 컴포넌트로 변환됨
- 태그는 포스트 태그 앞 5개 자동 입력
