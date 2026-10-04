---
title: "kordoc: HWP·PDF 문서, 마크다운으로 완벽 변환"
date: 2026-10-04 23:14:53 +0900
categories: [기술, 소프트웨어개발]
tags: [kordoc, HWP, HWPX, PDF, Markdown, 문서변환, CLI, MCP서버, 오픈소스, AI에이전트]
header:
  teaser: /assets/kordoc-document-tool-thumb.jpg
permalink: /post/kordoc-document-tool/
---
한국의 복잡한 문서 형식을 마크다운으로 변환하는 강력한 도구 **kordoc**이 주목받는다. 이 도구는 HWP, HWPX, PDF, MS Office 문서 등 다양한 포맷의 문서를 정확한 마크다운과 구조화된 데이터로 변환한다. 라이브러리, CLI, 그리고 AI 에이전트와 연결되는 MCP 서버로 활용할 수 있다.

<figure>
<img src="/assets/kordoc-document-tool-thumb.jpg" alt="kordoc: HWP·PDF 문서, 마크다운으로 완벽 변환">
</figure>

## 한국 문서 지옥을 해소하는 도구

kordoc은 대한민국에서 7년간 공문서 처리에 시달리던 한 지방공무원이 개발했다. 수많은 실제 관공서 문서를 처리하며 검증을 거친 만큼, 한국의 특수한 문서 환경에 최적화된 기능을 제공한다. HWP 3.x·5.x, HWPX, HWPML은 물론 PDF, XLS·XLSX, DOCX, PPTX, PNG·JPG·WebP 등 광범위한 문서와 이미지 포맷을 지원한다.

## 압도적인 변환 정확도

kordoc의 핵심 강점은 **변환 정확도**에 있다. 특히 한국 공문서의 복잡한 표 구조와 PDF 문서의 글자 및 표 인식에서 탁월한 성능을 보인다.

다음 표는 4.18.8 버전(2026년 10월 2일 배포) 기준 주요 검증 결과다.

| 대상          | 규모                    | 결과                                        | 비고                                     |
|---------------|-------------------------|---------------------------------------------|------------------------------------------|
| HWPX 표 구조  | 2,286문서 · 9,865개 표  | 9,865/9,865 (100%) 표 구조 일치           | 보이는 표 기준                           |
| HWP 5.x ↔ HWPX 표 | 1,120쌍 · 4,258개 표    | 100% 표 구조 일치                         | 짝 문서 기준                             |
| PDF 글자 재현 | 744쌍                   | 99.83% 글자 재현율 · 99.15% 읽기 순서     |                                          |
| PDF 표 감지   | 708쌍 · 2,331개 표      | 99.83% 표 탐지율 · 97.94% 구조 일치율     |                                          |

외부 PDF 벤치마크인 `opendataloader-bench` 200개 문서 테스트에서도 종합 점수 0.960으로 12개 공개 파서 중 1위를 기록한다.

## 다재다능한 기능과 AI 통합

kordoc은 단순히 문서를 변환하는 것을 넘어, 문서 작업을 위한 포괄적인 기능을 제공한다. 특히 AI 에이전트와의 통합은 이 도구의 활용성을 크게 확장한다.

| 작업       | 주요 기능                                                          |
|------------|--------------------------------------------------------------------|
| **읽기**   | 문서 → Markdown, IR, 쪽별 본문, RAG 청크 변환, 로컬 OCR             |
| **비교·편집** | 블록·셀 단위 비교, HWPX·HWP 서식 보존 패치                      |
| **작성**   | Markdown → HWPX 변환, 공문서 프리셋, 표·수식·차트 생성            |
| **양식**   | 필드·누름틀 채우기, 표준 기안문 2종 지원, 도장 날인                 |
| **검토**   | HWPX·HWP 미리보기·영역 추출, 구조·표기법 검사, 개인정보 마스킹     |

kordoc은 Claude Desktop, Claude Code, Cursor, Codex 등 설치된 AI 클라이언트에 MCP(Message Command Protocol) 서버로 등록된다. 클라이언트 재시작 후 파싱, 비교, 생성, 렌더 등 총 17개 도구를 AI 에이전트와 연동하여 사용할 수 있다.

## 간편한 설치와 활용

kordoc은 Node.js 20 이상 환경에서 macOS, Linux, Windows 모두 지원한다. `npm`을 사용한 설치가 간편하다.

```bash
npm install kordoc
```

CLI는 설치 없이 `npx kordoc`으로 바로 실행할 수 있다. PDF 및 OCR 관련 의존성은 기본 설치되나, `--omit=optional` 옵션으로 제외할 수 있다. AI 에이전트 연결은 `npx -y kordoc setup` 명령으로 쉽게 진행한다.

CLI를 통해 다양한 문서 변환 및 조작을 수행한다.

```bash
npx kordoc 문서.hwpx -o 문서.md         # HWPX를 마크다운으로 변환한다
npx kordoc *.pdf --jobs 4 -d ./결과   # 여러 PDF 파일을 병렬 변환하여 결과 폴더에 저장한다
npx kordoc 스캔본.pdf --ocr -o 스캔본.md # 스캔된 PDF를 OCR 처리하여 마크다운으로 변환한다
npx kordoc generate 보고서.md --preset 보고서 -o 보고서.hwpx # 마크다운으로 HWPX 보고서를 생성한다
```

JavaScript/TypeScript 환경에서는 `parse`와 `markdownToHwpx` 등의 API를 활용하여 프로그램으로 문서를 처리한다.

## 지속적인 개선과 검증

kordoc은 꾸준히 업데이트되며 성능을 개선한다. 최근 업데이트는 PDF 쪽 넘김 문단 잇기 판정 개선, 글꼴 사전으로 인한 메모리 문제 수정, HWPX 셀 줄바꿈 보존 등 다양한 부분에 집중한다. 모든 변경 사항은 고정 코퍼스와 참조 기준을 통해 엄격하게 검증된다.

## 출처
- C:/Users/windo/AppData/Local/Temp/claude/C--Users-windo-Desktop-03-------Github-Desktop-tigerjk9-github-io/80b40e5e-a667-4048-9cdf-88b68df405fd/scratchpad/src/kordoc.md
