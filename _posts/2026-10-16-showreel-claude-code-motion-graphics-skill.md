---
title: "showreel, 기획부터 내레이션·렌더·검수까지 한 번에 하는 Claude Code 모션그래픽 스킬"
date: 2026-10-16 01:22:46 +0900
categories: [AI, 콘텐츠 제작]
tags: [AI, 생성형AI, ClaudeCode, 모션그래픽, ElevenLabs, 오픈소스, 콘텐츠제작, 웹앱]
header:
  teaser: /assets/showreel-claude-code-motion-graphics-skill-demo-stills.jpg
permalink: /post/showreel-claude-code-motion-graphics-skill/
---
showreel은 GitHub 사용자 revfactory가 MIT 라이선스로 공개한 Claude Code 스킬이다. 짧은 요청 하나를 받아 콘셉트, 조사, 원고, 내레이션, 음악, 이미지, 렌더, 비평과 재작업, 믹스, 검수까지 맡아 한국어 모션그래픽 영상을 납품용으로 완성한다. 같은 개발자의 iso-reel은 아이소메트릭 도시의 건물 한 채가 영상 한 편인 쇼릴 사이트다. 두 저장소의 README를 바탕으로 무엇을 하고, 무엇이 필요하며, 어떻게 쓰는지 정리한다.

<figure>
<img src="/assets/showreel-claude-code-motion-graphics-skill-demo-stills.jpg" alt="showreel 데모 영상 스틸 네 장. 질문 다섯 개 브리프 카드, 소리 먼저 화면, 단어와 박자 타임라인, qa_check.py 검수 화면">
<figcaption>showreel README에 실린 2분 데모 영상 스틸 8장 중 4장. 주제·분위기·길이·이미지·나레이션을 묻는 브리프 카드, '소리 먼저' 단계, 화면을 단어와 박자에 맞추는 타임라인, qa_check.py --stt 검수 화면이다.</figcaption>
</figure>

## showreel이 하는 일

showreel에는 정해 둔 무드나 템플릿이 없다. Claude가 요청마다 콘셉트 후보를 여러 개 쓰고 같은 기준으로 점수를 매겨 하나를 고른다. 그다음 구간마다 매체, 색, 서체, 움직임의 성격 같은 아트 디렉션을 따로 정하고, 화면은 DOM, Canvas 2D, WebGL 셰이더, three.js로 코드를 짜서 만든다. 초안이 나올 때마다 가장 약한 구간을 다시 만들고, 글로 쓴 비평이 모든 구간을 유지 판정할 때까지 이 과정을 되풀이한다.

사용자에게는 사용자만 아는 사실, 곧 대상과 꼭 넣을 정보와 자료 위치만 묻는다. 무드, 길이, 화면 비율, 내레이션 여부, 이미지 사용 같은 창작 결정은 Claude가 내린다. README는 이 스킬이 요청 하나를 중심으로 설계됐다고 설명한다. 얼마나 놀라운 모션 그래픽 디자이너인지 보여 주는 역동적인 1분 한국어 영상을 이력서용 쇼릴처럼, 전력을 다해 만들어 보라는 요청이다. 영상 자체가 솜씨를 증명해야 한다는 뜻이다. 한국어 서체와 한국어 내레이션·발음 규칙에 맞춰 썼지만, 엔진과 렌더러와 오디오 도구는 언어를 가리지 않는다. 인물 프로필, 기업 홍보, 행사, 교육, 티저, 음악 기반 영상 등 실제 제작 13건에서 쓴 방법을 스크립트와 문서로 정리했다.

README가 밝힌 영역별 기능은 다음과 같다.

| 영역 | 하는 일 |
|---|---|
| 요청과 콘셉트 | 사용자만 아는 것(대상, 꼭 넣을 사실, 자료 위치)만 묻는다. 콘셉트 후보 3개 이상을 같은 기준으로 채점하고, 고른 안을 구간별 아트 디렉션과 함께 `concept.md`에 적는다. |
| 조사 | 조사 에이전트를 백그라운드로 돌린다. 영상에 들어가는 모든 사실에 출처 URL과 신뢰도를 붙이고, 날짜는 달력과 대조한다. |
| 원고 | 화면 문구와 발음용 문구를 나누고, 길이에 맞춰 분량을 정한다(60초는 한국어 약 240~255자). 장면 전환에 쓸 큐 단어를 지정한다. |
| 내레이션 | 요청하거나 내용상 필요할 때만 쓴다. ElevenLabs TTS로 콘셉트에 맞는 목소리를 고르고(깊은 바리톤 Marcus는 검증된 읽기 설정이 있다), 대사별로 테이크를 받아 바뀐 대사만 다시 생성하며, 모든 대사를 STT로 확인한다. |
| 음악과 효과음 | ElevenLabs Music을 4마디 단위로 계획하고, 박자·타격점 분석과 이어 붙이기로 드롭 위치를 옮긴다. 대체 수단으로 NumPy 신시사이저가 있고, 효과음 프리셋 24종을 갖췄다. |
| 이미지 | 이미지가 필요한 장면만 [codex-image](https://github.com/revfactory/skills)로 생성한다. 레터박스 제거, 업스케일, macOS Vision 컷아웃을 지원한다. 실존 인물은 생성하지 않는다. |
| 모션 엔진 | 결정적 HTML/JS 타임라인(`REEL`)을 쓴다. 모든 프레임이 시간의 순수 함수라서 병렬 워커가 어떤 순서로든 렌더할 수 있다. |
| 기법 | 한글 자모 조립, 가변 굵기 물결, 유리 활자, 입자 활자, 매치 컷 등 검증된 코드 기법 22가지와 WebGL2 셰이더, three.js 3D, 사전 계산 시뮬레이션을 쓴다. 기법 목록은 고르는 메뉴가 아니라 코드 라이브러리이고, 구간은 콘셉트에서 출발한다. |
| 렌더 | Playwright와 시스템 Chrome으로 렌더한다. 서브프레임 모션 블러(180° 셔터), 중단 후 이어 하는 청크 렌더, BT.709 `yuv420p` TV 범위 출력을 지원한다. |
| 믹스와 마스터링 | 음성 대역 더킹, 대사별 '내레이션 대 배경음' 보고서, 트루 피크 여유를 둔 −14 LUFS 2패스 loudnorm을 적용한다. |
| 비평 루프 | 초안마다 각 구간을 유지·수정·재제작으로 판정한다. 기준은 여덟 질문(템플릿처럼 보이는가, 표현의 폭, '어떻게 만들었지' 싶은 순간, 재료로서의 한글, 프레임 스트립에서의 무게, 리듬, 예측 가능성, 가장 약한 구간)이고, 결과는 `qa/critique_NN.md`에 남긴다. |
| 자동 검수 | 규격, 음량, 어두운 구간, 광과민성 섬광, 멈춘 화면, 움직임이 적은 구간 경고, 최종 믹스의 STT를 점검해 `qa/qa_report.md`에 쓴다. |

화면 전환은 내레이션 단어와 음악 박자에 프레임 단위로 맞춘다. 완성본은 받아쓰기(STT)로 발음을 다시 확인하고 음량, 섬광, 멈춘 화면을 검사한 뒤 납품한다. README의 데모 영상(1080p, 2분, 31MB)도 이 스킬이 프롬프트 하나로 만든 것으로, ElevenLabs 목소리 4개, 생성 음악, 효과음, AI 이미지, 모션 기법 22가지, 자동 검수가 들어갔다. 영상 파일은 [v1.0.0 릴리스](https://github.com/revfactory/showreel/releases/download/v1.0.0/showreel-promo-120s.mp4)에서 받을 수 있다.

## 작업 순서

README의 흐름도는 0번부터 11번까지 열두 단계다.

| 단계 | 내용 |
|---|---|
| 0 | 사전 점검(Preflight) |
| 1 | 요청 읽기, 사실만 묻기 |
| 2 | 콘셉트, 후보 3개 이상 채점 |
| 3 | 조사와 자료 수집 |
| 4 | 스토리보드와 원고 |
| 5 | 소리 먼저, 음악·효과음·내레이션을 만든 뒤 타임라인 구성 |
| 6 | 이미지 |
| 7 | 구간별 스타일 프레임 |
| 8 | 장면 제작 |
| 9 | 초안과 비평 루프, 가장 약한 구간 재제작 |
| 10 | 최종 렌더, 믹스, 마감 |
| 11 | 자동 검수와 납품 보고 |

이 순서에서는 소리를 화면보다 먼저 만든다. `timeline.py`가 내레이션의 단어 타이밍과 음악의 타격점을 이름 붙은 큐로 바꾸고, 장면은 초 단위 숫자를 박아 넣는 대신 `REEL.cue('name')`으로 큐를 읽는다. 그래서 내레이션 한 줄을 다시 생성해도 화면은 고칠 필요 없이 따라간다. 조사, TTS, 음악, 이미지 생성, 최종 렌더처럼 오래 걸리는 단계는 백그라운드에서 돌고, 그동안 Claude는 다음 단계를 진행한다.

## 설치와 필요한 것

| 도구 | 필요 여부 | 쓰임 |
|---|---|---|
| Claude Code | 필수 | 스킬 실행 |
| macOS | 권장 | 테스트한 플랫폼. Linux에서도 `REEL_CHROME_PATH`를 지정하면 렌더와 오디오는 되지만, 컷아웃은 macOS가 필요하다 |
| Python 3.10+ (`numpy`, `Pillow`) | 필수 | 타임라인, 믹스, 검수, 이미지 준비, 신시사이저 |
| Node.js 20+ | 필수 | 렌더러(`playwright-core`) |
| Google Chrome 또는 Chromium | 필수 | 헤드리스 렌더링. 브라우저를 따로 내려받을 필요는 없다 |
| ffmpeg (`loudnorm`, `ebur128`, `freezedetect`, `signalstats`, `tmix` 포함) | 필수 | 인코딩, 음량 측정, 검수 |
| ElevenLabs API 키 | 내레이션에 필요 | TTS, STT 검증, 효과음. 음악은 유료 요금제가 있어야 하고, Marcus 같은 라이브러리 목소리는 무료 요금제에서 쓸 수 없다 |
| Codex CLI와 codex-image 스킬 | 선택 | AI 이미지 생성. 없으면 타이포그래피, 그래픽, 사용자 사진으로 영상을 만든다 |
| photoreal 스킬 | 선택 | 인물이 나오는 사진풍 이미지의 프롬프트 설계 |
| Xcode 명령줄 도구(`swiftc`) | 선택 | macOS Vision으로 인물 컷아웃 |

README에서 비용 이야기가 나오는 곳은 ElevenLabs다. 사용에는 크레딧이 들고, 상업적 이용은 각자의 요금제 약관을 따른다. Music API가 `402`를 돌려주면 유료 요금제가 필요하다는 뜻이고, 이때는 `synth_music.py`로 음악을 합성한다. 한국어 서체(Pretendard와 Google Fonts 계열, 모두 SIL OFL)는 저장소에 들어 있지 않고, `new_project.py`가 시스템에서 복사하거나 프로젝트마다 내려받는다.

설치는 README의 네 단계를 따른다. 저장소를 Claude Code 스킬 폴더에 클론하고, 의존성을 설치하고, ElevenLabs API 키를 넣고, 환경을 점검한다.

```bash
# 개인 스킬(모든 프로젝트에서 사용)
git clone https://github.com/revfactory/showreel.git ~/.claude/skills/showreel

# 또는 프로젝트 스킬(저장소로 팀과 공유)
git clone https://github.com/revfactory/showreel.git .claude/skills/showreel

# 의존성
brew install ffmpeg node
python3 -m pip install numpy pillow
cd ~/.claude/skills/showreel/scripts && npm install

# ElevenLabs API 키(내레이션에 필요)
echo 'export ELEVENLABS_API_KEY="sk_..."' >> ~/.zshrc && source ~/.zshrc

# 환경 점검
python3 ~/.claude/skills/showreel/scripts/preflight.py
```

API 키는 프로젝트 폴더의 `.env` 파일에 `ELEVENLABS_API_KEY=sk_...`로 넣어도 된다. `preflight.py`는 도구마다 ✓ 또는 ✗를 표시하고, 빠진 도구의 설치 명령과 쓸 수 있는 제작 경로(내레이션, 음악 API, 이미지 생성)를 알려 준다. 기본 경로에 Chrome이 없으면 `REEL_CHROME_PATH`로 실행 파일 경로를 지정하고, Playwright 브라우저 채널은 `REEL_CHROME_CHANNEL`(기본 `chrome`)로 바꾼다.

## 쓰는 법과 산출물

빈 폴더에서 Claude Code를 열고 원하는 영상을 설명하면 된다. "showreel", "motion graphics", "promo video", "teaser", "60-second video" 같은 요청이나 `/showreel` 입력으로 스킬이 작동한다. README의 빠른 시작 예시 가운데 하나는 이렇다.

```text
/showreel 우리 팀이 만든 사내 검색 서비스 소개 60초 영상. 웅장한 분위기, 나레이션 넣어 줘.
```

Claude는 스스로 찾을 수 없는 사실(예를 들어 행사의 정확한 날짜)만 묻는다. 콘셉트를 직접 골라 한두 줄로 알린 뒤, 확인을 기다리지 않고 납품까지 진행한다. Claude 자신이 주제인 쇼릴 요청이라면 아무것도 묻지 않는다.

완성된 프로젝트 폴더는 다음과 같다.

```text
my-promo/
├── concept.md, storyboard.md, script.json, timeline.json
├── research/        research.md (facts with sources), photos.md
├── audio/           vo/ (narration takes), music/, sfx/, mix.wav
├── assets/          gen/ (generated images), img/ (processed)
├── reel/            index.html, engine.js, fx.js, timeline.js, scenes.js, fonts/
├── qa/              stills, contact sheets, critique_NN.md, qa_report.md
├── out/             <title>.mp4, <title>_공유용.mp4, poster, .srt
└── 제작노트.md       production note
```

납품물은 마스터 MP4, 공유용으로 가볍게 만든 MP4, 포스터 JPG, SRT 자막(내레이션이 있을 때), 제작 노트다. 제작 노트에는 출처, 설정, 남은 확인 사항, 모든 에셋을 다시 만드는 명령이 들어간다. 따로 지정하지 않은 항목은 다음 기본값을 쓴다.

| 항목 | 기본값 |
|---|---|
| 길이와 형식 | 60초, 16:9, 1920×1080, 30fps. 15초·30초·60초·100초·5분과 9:16 세로도 지원 |
| 무드와 아트 디렉션 | 기본값 없음. 프로젝트와 구간마다 `concept.md`에서 정한다 |
| 내레이션 | 요청하거나 필요할 때만. 목소리는 콘셉트마다 고른다. ElevenLabs Marcus(`ibCGc01503OQd2R6i1n1`)의 검증된 설정은 `eleven_multilingual_v2`, stability 0.45, similarity 0.8, style 0.4이고, 목소리에 잔향을 넣지 않는다 |
| 음악 | ElevenLabs Music. API를 쓸 수 없으면 `synth_music.py` |
| 이미지 | 필요한 곳에만 생성. 실존 인물은 실제 사진으로만 |
| 음량 | 통합 −14 LUFS. `mix.py`는 −2.0 dBTP 트루 피크로 마스터링하고, 검수는 −1.0 dBTP 이하를 통과로 본다 |
| 납품물 | 마스터 MP4, 공유용 MP4, 포스터 JPG, SRT(내레이션이 있을 때), 제작 노트 |

## 프롬프트 예시 하나

책 한 권을 소개하는 30초 영상을 요청하는 예시다. 중괄호 부분은 자기 자료의 링크로 바꿔 넣는 자리다.

```text
/showreel 역사 데자뷰를 중심으로 책의 내용을 소개하는 30초 영상을 만들어줘. 책에 나오는 역사적 사건들을 연속적으로 이어지는 영상으로 만들어주면 좋겠어. 영상 톤은 옛날 역사영화를 보는 느낌으로. 도서 본문은 여기: {pdf 파일 링크}, 본문에 나오는 역사기록은 여기 모아뒀어: {연대분포 엑셀파일 링크}
엑셀파일 내용을 참값으로 간주하고 만들어. 내 캐릭터는 이 이미지의 왼쪽 위에 있는 인물이야: {가족 캐릭터 그림 링크}
이 이미지로 기존에 만든 장면들은 여기 있는 그림들을 참고해: {도서 삽입그림 링크}
```

README의 기능에 비춰 보면 이 요청은 다음 부분을 건드린다.

- `/showreel`로 시작해 스킬을 바로 부른다. 30초는 지원하는 길이 가운데 하나다. 화면 비율이나 내레이션 여부처럼 요청에 없는 창작 결정은 Claude가 정한다.
- 스킬은 사용자에게 대상, 꼭 넣을 사실, 자료 위치만 묻는다. 이 예시는 도서 본문 PDF, 연대 정리 엑셀, 캐릭터 그림, 기존 삽입 그림의 위치를 처음부터 모두 알려 준다.
- README는 영상에 들어가는 모든 사실에 출처와 신뢰도를 붙인다고 적었다. 예시는 엑셀 파일을 참값으로 삼으라고 해서 사실의 기준을 사용자가 미리 정해 둔다.
- '옛날 역사영화' 같은 톤은 무드와 아트 디렉션에 해당한다. README에서 이 항목은 기본값 없이 프로젝트와 구간마다 `concept.md`에서 정한다.
- 캐릭터 그림과 기존 삽입 그림을 참고하라는 대목은 이미지 단계와 이어진다. README의 이미지 생성은 선택 항목인 Codex CLI와 codex-image 스킬을 쓰고, 스크립트 목록에는 참조 사진을 넣어 이미지를 생성하는 `codex_ref_image.sh`가 있다. 이 도구가 없으면 타이포그래피, 그래픽, 사용자가 준 사진으로만 영상을 만든다.

## iso-reel, 건물 하나가 영상 하나인 쇼릴 도시

iso-reel은 "움직임으로 말하는 모션 디자이너의 쇼릴 도시"다. 아이소메트릭 도시의 건물 한 채가 영상 한 편이고, 도시는 창 불빛, 차량, 크레인, 지면 박동, 건물 재배치로 계속 움직인다. 건물을 고르면 타워의 화면이 떨어져 나와 플레이어 크기로 커지며 영상이 재생된다. Vite, three.js, GSAP로 만든 정적 사이트이고 GitHub Pages로 배포한다. showreel README는 데모 영상에 만든 이의 이전 쇼릴 장면이 들어 있다고 밝혔는데, 데모 스틸 가운데 하나에 ISO/REEL 표기와 '서울 24시' 장면이 보인다.

<figure>
<img src="/assets/showreel-claude-code-motion-graphics-skill-iso-reel-city.jpg" alt="iso-reel 쇼케이스 첫 화면. 밤의 아이소메트릭 도시에 영상 제목이 적힌 타워들이 서 있고 아래에 01부터 09까지 영상 카드가 놓여 있다">
<figcaption>iso-reel 쇼케이스 첫 화면. 샘플 영상마다 제목을 단 타워가 서 있고, 아래 인덱스 띠에 '01 쇼릴 2026'부터 '09 유리 활자'까지 카드가 놓인다.</figcaption>
</figure>

도시는 다음처럼 조작한다.

| 입력 | 동작 |
|---|---|
| 드래그(마우스·한 손가락) | 지도처럼 이동, 관성 있음 |
| 휠·핀치 | 커서 위치를 기준으로 확대·축소 |
| `Q` / `E`, 회전 버튼 | 도시를 90° 회전 |
| 방향키 / `WASD` | 이동 |
| `Tab` / `Shift+Tab`, `[` / `]` | 다음·이전 건물로 이동 |
| `Enter` / `Space` | 고른 건물의 영상 재생 |
| `1`~`9` | 그 번호의 건물로 이동 |
| `L` | 목록 보기 전환 |
| `Esc` | 플레이어·패널 닫기 |
| `?` | 조작 도움말 |

플레이어 안에서는 `Space`로 재생과 일시정지, `←` / `→`로 5초 이동, `M`으로 음소거, `F`로 전체 화면, `[` / `]`로 이전·다음 영상을 고른다. 영상이 끝나면 2초 뒤 다음 영상으로 넘어가며, 이 동작은 끌 수 있다. 터치 화면에서는 건물을 한 번 누르면 고르고 한 번 더 누르면 재생하며, 아래 인덱스 띠의 카드를 누르면 바로 재생한다. 주소로 바로 열 수도 있다. `#/reel/<slug>`는 그 영상의 플레이어를, `#/list`는 목록 보기를 열고, `?q=high|medium|low`는 화질 단계를 고정한다(기본은 자동).

샘플 쇼릴은 9편이다. 모두 15초, 1920×1080, 30fps이고, 화면과 소리가 같은 비트 격자(`cues.json`)를 따른다.

| 번호 | 제목 | 기법 | 제작 도구 | BPM |
|---|---|---|---|---|
| 01 | 쇼릴 2026 | 비트 컷 몽타주와 키네틱 타이틀 카드 | HTML 컴포지션, Canvas 2D, FFmpeg | 128 |
| 02 | 한글, 움직이다 | 자모 조립 키네틱 타이포와 가변 굵기 비트 싱크 | Canvas 2D, fontTools, 가변 폰트 | 128 |
| 03 | 서울 24시 | 미니어처 도시 라이팅 타임랩스와 HUD 합성 | Blender(EEVEE), HTML 컴포지션 | 96 |
| 04 | 숫자의 맥박 | 자기 참조 인포그래픽(실제 프로젝트 데이터) | Canvas 2D, JavaScript | 144 |
| 05 | 빛의 입자 | GPU 인스턴싱 파티클 글자 형성·폭발·재형성 | Unity, Python, HTML 컴포지션 | 112 |
| 06 | 한 잔의 아침 | 실사 2.5D 패럴랙스와 원형 매치 컷 커머셜 | codex-image, WebGL(three.js), rembg | 80 |
| 07 | 리듬의 격자 | 음악 싱크 제너러티브 타일 격자 | Canvas 2D, JavaScript | 160 |
| 08 | 손끝의 흐름 | 3D 폰 목업 위 UI 전환과 마이크로 인터랙션 | HTML, CSS 3D, SVG | 112 |
| 09 | 유리 활자 | 유리·크롬 입체 한글의 굴절 라이팅 | Blender(Cycles), HTML 컴포지션 | 64 |

HTML 컴포지션은 시각 t의 순수 함수로 만들어 Playwright로 프레임마다 렌더했다. Blender 장면은 스크립트가 원본이고, Unity는 배치 모드에서 시간을 직접 진행시켜 프레임을 결정적으로 캡처했다. 3D 렌더와 실사 플레이트는 HTML 컴포지션 위에서 타이틀·HUD와 합성했고, 마스터는 H.264 1080p30, 정확히 15초, −14 LUFS로 인코딩했다.

사이트의 배경 건물과 소품 키트, '서울 24시'의 아파트·상가·버스, '유리 활자'의 바닥과 배경막은 투영 베이크 텍스처로 표면을 만들었다. 상자 조합 모델을 직교 카메라로 여러 방향에서 렌더해 가이드를 만들고, 가이드를 참조해 codex-image로 방향별 이미지를 생성한다. 실루엣을 맞춘 뒤 방향별 이미지를 직교 투영으로 입히고, 보이는 정도에 따라 가중 합성해 UV 아틀라스로 굽는다. 배경 건물에는 밤 아틀라스와 창 발광 맵이 들어 있어서, 사이트가 발광 맵에 시간 노이즈를 곱해 창 불빛을 바꾼다.

음악과 효과음은 외부 샘플 없이 numpy·scipy 신시사이저로 합성했다. 각 편의 `cues.json`에서 악보(`score.json`)를 쓰고, 큐 시각에 효과음을 붙여 48kHz 24bit 믹스로 렌더한 뒤 라우드니스(−14 LUFS)와 트루 피크를 측정 스크립트로 확인했다. 출고 전에는 모든 마스터를 WCAG 2.3.1을 보수적으로 단순화한 섬광 검사 스크립트로 확인했다. 화면 면적 10% 이상에서 밝기가 크게 오르내리는 반전이 1초에 3회를 넘지 않아야 통과다. 박자 연출은 큰 면의 흑백 반전 대신 밝기가 비슷한 색 쌍, 작은 면적, 위치·회전·크기 움직임으로 만들었다.

저장소의 `.claude/`에는 이 프로젝트를 만든 에이전트 팀 정의(`agents/`)와 연출, HTML 모션, Blender, Unity, 투영 베이크, 사운드, 마감, 콘텐츠 파이프라인, 사이트, QA 작업 규칙(`skills/`)이 들어 있다. 사이트를 빌드하거나 실행하는 데는 필요하지 않다.

직접 돌려 보려면 Node.js 22와 ffmpeg가 필요하다. `npm ci` 후 `npm run dev`로 개발 서버를, `npm run build`로 정적 사이트를 만든다. 새 영상은 `content/reels/<slug>/` 폴더에 `reel.json`과 `video.mp4`(또는 유튜브 주소)를 넣어 PR로 올리면 건물 한 채로 지어진다. 배포는 저장소 Settings의 Pages 소스를 GitHub Actions로 바꾸고 `main`에 푸시하면 된다. `vite.config.js`의 `base: './'`와 해시 라우팅 덕분에 `/iso-reel/` 같은 하위 경로에서도 설정을 바꾸지 않고 동작한다. 샘플 9편을 넣은 빌드의 `dist/`는 약 100MB(영상 92MB, 3D 모델 3.1MB, 코드·글꼴 5.5MB)이고, 첫 화면을 띄우는 JS는 gzip으로 약 243KB다.

WebGL2를 지원하는 최신 Chrome, Edge, Safari, Firefox에서 동작한다. WebGL을 쓸 수 없으면 목록 보기로 시작하고 모든 영상을 그대로 재생할 수 있다. `prefers-reduced-motion: reduce` 설정이면 인트로를 건너뛰고 카메라 비행과 배경 재배치를 페이드로 바꾼다. 평균 FPS가 3초 동안 45 미만이면 화질을 높음, 보통, 낮음 순으로 한 단계씩 낮추고, 휴대폰은 보통에서 시작한다. README에는 서체(모두 SIL OFL 1.1)와 three.js(MIT), GSAP(Standard 'No Charge' License)의 라이선스가 정리돼 있지만, 저장소에는 프로젝트 자체의 라이선스 파일이 없다.

## 쓰기 전에 알아 둘 한계

showreel README가 직접 밝힌 한계는 다섯 가지다.

- Claude는 소리를 들을 수 없다. 음량, 내레이션과 배경음의 비율, 잔향 꼬리, STT는 수치로만 점검하므로 공개 전에 직접 들어 봐야 한다.
- 한국어 내레이션과 타이포그래피에 맞춰 썼다. 다른 언어는 원고 규칙과 발음 규칙을 새로 만들어야 한다.
- ElevenLabs 사용에는 크레딧이 들고, 상업적 이용은 요금제 약관을 따른다.
- 실존 인물의 얼굴과 몸은 생성하지 않는다. 허락받은 실제 사진을 써야 한다.
- macOS에서 개발하고 테스트했으며, 컷아웃은 macOS Vision에 의존한다.

README는 API 키, `.env` 파일, 공개할 권리가 없는 생성 내레이션을 커밋하지 말라고도 당부한다. showreel은 Anthropic, ElevenLabs, OpenAI와 제휴하거나 보증받은 프로젝트가 아닌 독립 프로젝트다. Claude로 모션그래픽을 만드는 다른 사례는 이 블로그의 [motion-studio 스킬 글](/post/claude-motion-studio-animation-and-motion-graphics/), [Claude Opus 5.5의 모션 디자인 15편](/post/mg-styles-15-motion-design-by-opus/), [motion-video-production 스킬 글](/post/motion-video-production-skill-harness/)에서도 다뤘다.

## 출처

- revfactory, showreel, GitHub 저장소. https://github.com/revfactory/showreel
- revfactory, iso-reel, GitHub 저장소. https://github.com/revfactory/iso-reel
- iso-reel 쇼케이스. https://revfactory.github.io/iso-reel/
