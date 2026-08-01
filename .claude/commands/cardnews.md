# /cardnews — 유튜브·기사·논문 → 닷커넥터 카드뉴스

## 사용법
/cardnews <YouTube URL | 웹 URL | PDF 경로·URL | 로컬 md> [옵션]

## 실행

`$ARGUMENTS`가 비어 있으면 입력(URL/PDF/주제)을 먼저 물어보세요.

### 1단계 — 스타일 선택 (실행 전 필수)
사용자가 이미 `--style`을 명시했으면 이 단계를 건너뛴다. 아니면 아래를 **반드시 먼저** 한다:

1. 입력의 주제·구조를 파악한다(제목·핵심 내용 훑기. URL/PDF는 대략의 주제만 봐도 된다).
2. 어느 스타일이 맞는지 판정하고, **추천 근거를 곁들여** `AskUserQuestion`으로 사용자가 고르게 한다.
   추천하는 쪽을 첫 옵션에 두고 라벨에 `(추천)`을 붙인다.
   - **diagram (밝은 개념 다이어그램 · journey)** — 내용이 "과정·여정·단계·성장" 또는
     "기대 vs 현실"처럼 **시간 흐름을 따라 나아가는 궤적** 하나로 요약될 때.
     신호: 학습·성장 과정, 목표 달성, 프로젝트·창업 진행, 습관 형성, before→after,
     "실제로는 이렇게 흘러간다"류. v1 아키타입이 journey 하나뿐이라 **이 틀에 맞을 때만** 추천한다.
   - **cinematic (다크 사진 카드, 기본값)** — 그 외 대부분. 사실 설명, 여러 갈래 논점,
     연구 결과, 뉴스, 서로 다른 아이디어 나열, 개념 해설.
3. 추천은 한 줄 근거와 함께 말한다.
   예: "이 글은 'AI 도입의 시행착오 과정'이 핵심이라 diagram(journey)을 추천합니다."
   예: "이 논문은 발견이 여러 갈래라 cinematic이 낫습니다."
4. 사용자가 고른 스타일로 2단계를 실행한다.

### 2단계 — 생성
```bash
py -X utf8 scripts/cardnews.py <입력> --cards 10                          # cinematic
py -X utf8 scripts/cardnews.py --style diagram <입력 | --topic "주제">    # diagram
```

## 설명
입력을 분석해 1080x1350(4:5) 카드뉴스 PNG 세트를 생성합니다.
출력: 바탕화면 `cardnews/<날짜>-<슬러그>/card-01.png ...` + `cards.json`(재편집용).

**디자인 (2026-07-27 리뉴얼 — 다크 시네마틱)**: 짙은 차콜 그라디언트 배경 · 좌상단 흰
스크립트 로고 + 우상단 노란 닷네트워크 마크 · 헤드라인 2단(흰 주제 라벨 + **노란 핵심 주장**,
Black Han Sans, 폭·높이 자동 맞춤 60~122px) · 노란 세로 바가 붙은 본문 2~3줄(**단정체**) ·
라운드 16:9 이미지 · 하단 큰 페이지 번호 + `출처: OOO`. **마지막 장은 고정 브랜드 아웃트로**
(닷커넥터 · @Dot_Connector · linktr.ee 버튼 · 페이스북/인스타/스레드 아이콘).

**카피 톤**: 퇴근길에 스마트폰으로 넘겨보는 독자 기준. 쉽게 쓰되 얕지 않게 —
전문 용어는 그 자리에서 괄호로 풀고, 카드마다 수치·고유명·메커니즘 중 하나는 남긴다.
**친절함은 존댓말이 아니라 쉬운 설명에서 나온다**(종결은 단정체 `~다`). 훈계조(`~해야 한다`)와
AI 티 나는 상투어는 금지. 이 규칙들은 프롬프트만으로는 지켜지지 않아서 **생성 후 코드가 검사하고
위반 카드만 Gemini에 되돌려 최대 2회 재작성**시킨다(`validate_cards`/`repair_cards`).
본문 줄바꿈도 어절 단위 DP로 재배치해 한 어절짜리 고아 줄을 없앤다(`wrap_body`).

**카드 이미지 (원자료 캡처 우선)**:
1. **원자료에서 캡처** — YouTube는 실제 영상 프레임(yt-dlp+OpenCV, 암전 프레임 회피,
   푸터에 실측 `화면 MM:SS` 표기) / 기사는 본문 이미지·og:image(썸네일 URL을 원본 크기로
   자동 승급) / 논문은 **"Figure N" 캡션 위 영역을 페이지째 렌더**(벡터 도해까지 잡힘, `p.N` 표기)
2. **Gemini 이미지 생성** (`gemini-2.5-flash-image`, 16:9, 다크 시네마틱 톤)
3. **DuckDuckGo 이미지 검색** (`image_query`) — 레이트리밋이 잦은 최후 수단
4. 전부 실패하면 노란 인용 패널

카드↔이미지 짝짓기는 **Gemini 멀티모달이 후보 이미지를 직접 보고 배정**한다(실패 시 순서대로).
흰 바탕 도표는 종이 패널(`contain`), 세로로 긴 사진은 어두운 박스(`fit`), 나머지는 꽉 채움(`cover`).

`GEMINI_API_KEY`는 `.env`에서 자동 로드. 헤드라인 폰트(Black Han Sans, OFL)는 `.fonts/`에
없으면 자동으로 내려받는다.

## 밝은 다이어그램 스타일 (`--style diagram`, 2026-08-02)
사진 카드 대신 **밝은 크래프트지 배경 + 손그림 개념 다이어그램** 한 장을 만든다. 다이어그램은 이미지
생성이 아니라 **SVG로 그려 한글이 깨지지 않는다**(기존 Edge 캡처 파이프라인 재사용, 과금은 스펙 1회뿐).

**아키타입 5종** (`--archetype`, 기본 `auto`면 LLM이 내용에 맞게 선택):

| 아키타입 | 언제 | 스펙 필드 |
|----------|------|-----------|
| `journey` | 기대 vs 현실, 과정·성장·시행착오 궤적 | ideal_title, reality_title, start, end, nodes[6~8] |
| `comparison` | 두 대상 A vs B, 장단점, 전후 | title, left{label,items[3~5]}, right{label,items} |
| `cycle` | 끝이 처음으로 도는 반복(PDCA, 피드백) | title, nodes[3~6] |
| `steps` | 순서 있는 선형 절차·N단계·로드맵 | title, steps[{label,desc?} 3~5] |
| `quadrant` | 두 축 2×2 매트릭스(우선순위, 분류) | title, x_axis{label,low,high}, y_axis{...}, quadrants[4] |

```bash
py -X utf8 scripts/cardnews.py --style diagram --topic "목표 달성의 실제 과정"          # auto 선택
py -X utf8 scripts/cardnews.py --style diagram <URL|PDF>                                 # 원문에서 추출
py -X utf8 scripts/cardnews.py --style diagram --archetype comparison --topic "A vs B"   # 강제 지정
py -X utf8 scripts/cardnews.py --style diagram --topic "..." --dry-run                   # 스펙 JSON만
```

- LLM은 고른 아키타입의 스펙 JSON만 만들고(단정체·환각금지 상속), 파이썬이 SVG로 렌더한다.
  라벨은 명사·짧게(길면 폰트 자동 축소). 라벨 충돌은 배치 로직이 회피.
- 출력·`--rerender`·`cards.json`은 동일(`cards[].`스펙 필드를 고쳐 무과금 재렌더). 아웃트로 없이 각 장
  하단 `@Dot_Connector` 푸터. 파일: `cardnews_diagram_template.html`·`cardnews_diagram_prompt_template.txt`
  + `cardnews.py`의 `render_diagram_svg`(디스패처)·`render_{journey,comparison,cycle,steps,quadrant}_svg`.
  **cinematic(기본값)은 무영향.**
- QA: 라벨이 원문/주제와 맞는지, 겹침·넘침이 없는지 PNG 육안 확인. 어긋나면 cards.json 스펙을 고쳐 `--rerender`.

## 옵션
- `--style {cinematic,diagram}` : 기본 cinematic(다크 사진 카드). `diagram`은 밝은 개념 다이어그램
- `--topic "주제"` : diagram 모드에서 URL/PDF 대신 개념·주제를 직접 입력
- `--archetype {auto,journey,comparison,cycle,steps,quadrant}` : diagram 아키타입 (기본 auto=LLM 선택)
- `--cards N` : **총** 카드 수 (기본 10 — 아웃트로 포함이라 본문은 9장). diagram 모드는 무시(1장)
- `--dry-run` : 카피 JSON만 출력 (렌더 없음 — 카피 검토용)
- `--no-imggen` : Gemini 이미지 생성 생략
- `--no-search` : DDG 검색 폴백 생략
- `--no-outro` : 브랜드 아웃트로 카드 생략
- `--out DIR` : 출력 폴더 지정
- `--model M` : 카피·배정 모델 (기본 gemini-2.5-flash)
- `--rerender DIR` : cards.json 수정 후 **Gemini 재호출 없이** 카드만 다시 렌더
- `--keep-images` : `--out` 폴더의 기존 이미지를 재사용하고 **카피만 다시 생성**
  (톤을 바꿔 다시 뽑을 때. 프레임 재추출·이미지 재생성 비용 0)

## 실행 후 QA (필수 — 생성 직후 항상 점검)
1. **카피 사실성**: cards.json의 수치·주장을 원문과 대조. 원문에 없는 내용이 있으면
   cards.json을 고치고 `--rerender`
2. **문체**: 실행 로그에 `[WARN] 교정 후에도 규칙 위반 N장 남음`이 뜨면 그 카드를 직접 손본다.
   자동 검사가 못 잡는 것 — 훅 카드가 사실 대신 수사 의문문으로 끝나는지, 헤드라인이 본문보다
   과장됐는지(예: 본문은 "참여도 2배"인데 헤드라인은 "참여도와 지식이 2배")
3. **헤드라인 2단**: 흰 줄은 주제 라벨, 노란 줄은 그 자체로 완결된 단언인지
4. **이미지-내용 관련성**: 각 PNG를 열어 육안 확인. 생성 이미지에 글자·왜곡 아티팩트가 있거나
   프레임이 내용과 어긋나면 해당 이미지를 교체하고 `--rerender`
5. **글자 넘침**: 자동 축소가 걸린 카드(헤드라인이 유난히 작은 장)는 카피를 줄이는 편이 낫다
6. **논문 figure**: 캡션 영역이 잘렸거나 엉뚱한 그림이면 `render/fig-NN.png`를 교체 후 재렌더
7. **논문 출처 정확성 (환각 절대 금지)**: 논문·자료 카드의 `출처`(source_label)를 **원문에서 그대로 확인**한다.
   저자·연도·제목·저널을 지어내거나 요약·의역하지 말 것 — 제목은 원문 verbatim(길면 실제 앞부분 + `…`),
   arXiv/DOI ID는 추출된 값만 사용(첫 8000자 검색, 추측 금지). `cards.json`의 `source_label`이 원문과
   다르면(예: 실제 제목을 그럴듯한 짧은 제목으로 바꿈) 원문 verbatim으로 고치고 `--rerender`.
   ※ hook-image 스킬과 동일 원칙 — 실제 논문에서 저자·연도·제목을 읽어 옮기고, 없는 값은 만들지 않는다.

## 재렌더 (카피·이미지 수정 후)
```bash
py -X utf8 scripts/cardnews.py --rerender "C:\Users\user\Desktop\cardnews\<폴더>"
```
`cards.json`의 `cards[]`(카피)와 `images[]`(`{path, fit, note}`)를 그대로 읽어 다시 그린다.
**같은 입력으로 재실행하면 카피가 새로 생성돼 수정분을 덮어쓰므로 금지.**

## 알려진 특성
- 유튜브 자막 없는 영상은 description으로 폴백 → 카피가 얕아질 수 있음 (본문 200자 미만이면
  환각 방지를 위해 생성 자체를 중단)
- 프레임은 균등 분포로 뽑은 뒤 **멀티모달 배정**으로 카드에 붙는다. 타임스탬프는 실측값
- JS 렌더링 기사(The Verge 등)는 정적 HTML에 이미지가 없어 캡처 0장 → 생성으로 대체됨
- 이미지 생성은 카드당 1회 API 호출. 배정 1회 + 카피 1회가 추가로 든다
