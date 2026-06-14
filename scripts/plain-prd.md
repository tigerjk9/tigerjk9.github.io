# plain 모드 PRD — 담백한 전달 블로거 스킬 (`/plain-paraph`·`/plain-video`)

> 설계일: 2026-06-15. 기존 `/paraph`·`/video`·`/edit-*`가 모두 교육 앵커링에 묶여 블로그 콘텐츠가 단조로워지는 문제를 해소하기 위한 제3의 변형.

## 문제

`web_prompt_template.txt`·`yt_prompt_template.txt`와 `edit_*` 변형 전부가 페르소나를 "기술과 교육의 접점을 탐구하는 전략적 탐구자", 독자를 "한국의 교사·교육 관계자"로 고정한다. 어떤 URL·영상을 넣어도 결과물이 교육 렌즈로 수렴해 주제 다양성이 사라진다.

## 해결: plain 모드

교육 앵커링을 제거하고 "담백한 설명자" 페르소나로 원문을 충실하게 전달하는 모드. **신규 스크립트를 만들지 않고** 기존 `web_to_post.py`·`yt_to_post.py`에 `--plain` 플래그를 더해 템플릿만 교체한다.

### 페르소나 — 담백한 설명자

- 특정 분야(교육)에 얽매이지 않음. 주제는 원문이 정함 (기술·경제·문화·과학·역사·예술 등)
- 원문 정보를 정확하게·빠짐없이 전달하는 데 집중. 개인 의견은 절제 (글의 중심은 원문 내용이지 필자 입장이 아님)
- 원문에 없는 사실·수치·인용을 지어내지 않음
- 기존 `edit_*`의 "날카로움 + 따뜻함 원칙"을 "명료함 원칙"으로 대체 — 정확성·명료함·절제

### 유지 vs 제거

| 항목 | plain 처리 |
|------|-----------|
| 단정체 문체 절대 규칙 | 유지 |
| AI 슬롭 금지(Humanize KR v2.0.0) | 유지 |
| 콜론 헤딩 금지 | 유지 |
| 표 활용 규칙 | 유지 |
| 이미지 자동 삽입 (teaser + 본문 figure) | 유지 (default 경로 = `fetch_and_inject_image`) |
| 크로스오버(분야 연결) 섹션 | 유지하되 **선택적**(억지면 생략) |
| 교육 페르소나·"한국의 교사·교육 관계자" 독자 | 제거 |
| "한국 교육 현장 사례 추가" | 제거 |
| PLC·교사 협력·강한 "필자 관점 2곳 필수" | 제거 (의견 절제) |
| `[IMAGE:]` 마커·프레임 추출(`--edit` 기능) | 미사용 |

## 아키텍처

### 신규 파일 (6)

- `scripts/plain_web_prompt_template.txt` — 단일 웹 (`{OWNER_NOTES}` 지원)
- `scripts/plain_web_multi_prompt_template.txt` — 복수 웹
- `scripts/plain_yt_prompt_template.txt` — 단일 영상 (`{FRAME_INFO}` 없음)
- `scripts/plain_yt_multi_prompt_template.txt` — 복수 영상
- `.claude/commands/plain-paraph.md` — `/plain-paraph` 커맨드
- `.claude/commands/plain-video.md` — `/plain-video` 커맨드

### 스크립트 변경 (2)

`web_to_post.py`·`yt_to_post.py` 동일 패턴:
1. `PLAIN_PROMPT_TEMPLATE_PATH`·`PLAIN_MULTI_PROMPT_TEMPLATE_PATH` 상수 추가
2. `load_prompt_template`·`load_multi_prompt_template`에 `plain: bool = False` 파라미터 추가
3. 템플릿 선택을 3-way로 일반화: `if plain → PLAIN / elif edit → EDIT / else → default`
4. argparse `--plain` 플래그 추가
5. 단일·복수 호출부에 `plain=args.plain` 전달

### 분기 일관성

- 이미지/프레임 분기는 전부 `if args.edit:` 게이트 → plain(edit=False)은 자동으로 default(자동 주입) 경로로 흐름. 추가 분기 불필요.
- `yt_to_post.py`의 `frame_info`는 852행에서 `""`로 초기화 → plain에서 프레임 추출 스킵, plain 템플릿에 `{FRAME_INFO}` 플레이스홀더가 없어 치환은 no-op.

## 호출

```bash
python scripts/web_to_post.py <URL> [URL2 ...] --plain
python scripts/yt_to_post.py <URL> [URL2 ...] --plain --model gemini-2.5-flash
```

> `/plain-video`는 `yt_to_post.py` 기본 모델 `gemini-2.0-flash`가 폐기(404)되어 `--model gemini-2.5-flash`를 반드시 명시. `web_to_post.py` 기본값은 이미 `gemini-2.5-flash`.

`--dry-run`·`--no-push`·`--slug`·`--date`·`--notes`(웹 단일) 등 기존 옵션 모두 상속.

## 검증 (2026-06-15)

- `py_compile` 양 스크립트 통과
- plain 템플릿 4종 필수 플레이스홀더 전수 존재 확인
- 교육 앵커링 잔재(전략적 탐구자·교사·교육 현장·PLC 등) 0건
- 로더 단위 테스트: `plain=True` → plain 템플릿 선택 + 플레이스홀더 치환 + 교육 페르소나 미포함 확인 (web·yt 단일/복수 4종)
- 회귀: `plain=False`에서 default/edit 템플릿 정상 선택 확인

## 후처리

생성물은 기존 자동화와 동일하게 CLAUDE.md의 **자동화 포스트 후처리 QA 체크리스트** 7단계 점검 대상. plain 고유 추가 점검: 억지 교육 연결 혼입 여부(있으면 원문 주제로 교정).
