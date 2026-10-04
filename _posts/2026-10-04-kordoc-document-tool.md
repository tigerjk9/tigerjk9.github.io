---
title: "kordoc, HWP·HWPX·PDF 문서를 마크다운으로 바꾸는 오픈소스 도구"
date: 2026-10-04 23:14:53 +0900
categories: [기술, 소프트웨어개발]
tags: [kordoc, HWP, HWPX, PDF, Markdown, 문서변환, CLI, MCP서버, 오픈소스, AI에이전트]
header:
  teaser: /assets/kordoc-document-tool-og.jpg
permalink: /post/kordoc-document-tool/
---
kordoc은 한국 공공기관에서 쓰는 HWP 문서와 PDF를 마크다운으로 바꿔 주는 오픈소스 도구다. HWP 3.x·5.x, HWPX, HWPML, PDF, XLS·XLSX, DOCX, PPTX, 그리고 PNG·JPG·WebP 이미지까지 받아 Markdown과 구조화 데이터로 변환한다. 라이브러리로 불러 쓸 수도, CLI로 돌릴 수도, AI 에이전트가 쓰는 MCP 서버로 붙일 수도 있다. 라이선스는 MIT다.

<figure>
<img src="/assets/kordoc-document-tool-og.jpg" alt="chrisryugj/kordoc 저장소의 GitHub 소개 카드. HWP·HWPX·PDF·Office 문서를 Markdown으로 바꾸는 CLI·MCP 서버라는 설명이 적혀 있다">
<figcaption>kordoc 저장소의 GitHub 소개 카드.</figcaption>
</figure>

## 공무원이 만든 문서 변환기

README의 첫 문구는 "모두 파싱해버리겠다"이다. 만든 사람은 광진구청에서 7년 동안 HWP 파일과 씨름한 지방공무원이다. 5개 공공 프로젝트에서 실제 관공서 문서 수천 건을 파싱하며 검증했다고 소개한다.

## 검증 결과

4.18.8 버전(2026년 10월 2일 배포)을 고정 코퍼스와 참조 기준으로 측정한 결과는 다음과 같다.

| 대상 | 규모 | 결과 |
|---|---|---|
| HWPX | 2,286문서 · 9,865개 표 | 보이는 표 9,865개 전부(100%) 구조 일치 |
| HWP 5.x ↔ HWPX | 1,120쌍 · 4,258개 표 | 짝 문서 간 표 구조 100% 일치 |
| PDF 글자 | 744쌍 | 글자 재현율 99.83% · 읽기 순서 99.15% |
| PDF 표 | 708쌍 · 2,331개 표 | 표 탐지 99.83% · 구조 일치 97.94% |

README는 표 구조 점수와 셀 내용·화면 재현을 별개 지표로 구분한다. 표 구조 일치율 100%가 셀 안 내용까지 100% 맞았다는 뜻은 아니다.

외부 PDF 벤치마크인 `opendataloader-bench`(200문서)에서는 4.18.6 버전 별도 측정에서 기본 설정 종합 0.960, OCR을 끈 설정 0.937을 받았다. 2026년 9월 29일 기록 기준으로 공개 파서 12개 가운데 1위다.

## 주요 기능과 AI 에이전트 연결

kordoc은 변환 말고도 문서 작업 전반을 다룬다.

| 작업 | 주요 기능 |
|---|---|
| 읽기 | 문서 → Markdown, IR, 쪽별 본문, RAG 청크 변환, 로컬 OCR |
| 비교·편집 | 블록·셀 단위 비교, HWPX·HWP 서식 보존 패치 |
| 작성 | Markdown → HWPX 변환, 공문서 프리셋, 표·수식·차트 생성 |
| 양식 | 필드·누름틀 채우기, 표준 기안문 2종, 도장 날인 |
| 검토 | HWPX·HWP 미리보기·영역 추출, 구조·표기법 검사, 개인정보 마스킹 |

서식 보존 패치에 쓸 Markdown은 `--keep-layout-tables`로 추출하고, 적용하지 못한 편집은 건너뛴 이유와 함께 보고한다.

`npx -y kordoc setup`을 실행하면 Claude Desktop, Claude Code, Cursor, Codex 등 설치된 AI 클라이언트에 MCP(Model Context Protocol) 서버로 등록된다. 클라이언트를 다시 시작하면 파싱, 비교, 생성, 렌더 등 17개 도구를 에이전트가 쓸 수 있다. Claude Code에서는 플러그인으로도 설치된다.

```text
/plugin marketplace add chrisryugj/kordoc
/plugin install kordoc@kordoc
```

## 설치와 사용

Node.js 20 이상이 필요하고 macOS, Linux, Windows에서 돌아간다.

```bash
npm install kordoc
```

CLI는 설치하지 않고 `npx kordoc`으로 바로 실행할 수 있다. PDF·OCR 관련 의존성은 기본으로 함께 설치되며, `--omit=optional`로 빼면 그 기능이 제한된다.

```bash
npx kordoc 문서.hwpx -o 문서.md                # HWPX를 마크다운으로 변환한다
npx kordoc *.pdf --jobs 4 -d ./결과            # 여러 PDF를 파일 단위로 병렬 변환해 결과 폴더에 저장한다
npx kordoc 문서.pdf --format json --pages 1-3  # 1~3쪽을 JSON으로 출력한다
npx kordoc 스캔본.pdf --ocr -o 스캔본.md        # 스캔한 PDF를 OCR로 처리해 마크다운으로 변환한다
npx kordoc generate 보고서.md --preset 보고서 -o 보고서.hwpx  # 마크다운으로 HWPX 보고서를 만든다
npx kordoc fill --template gian -j 값.json -o 기안문.hwpx    # 기안문 양식에 값을 채운다
```

`--jobs`는 파일 단위 병렬 변환이라 그만큼 메모리를 더 쓴다. JavaScript/TypeScript에서는 `parse`, `markdownToHwpx` 같은 API로 같은 작업을 코드에서 처리한다. 폐쇄망 설치 방법도 문서로 정리돼 있으며, `KORDOC_OFFLINE=1` 환경 변수와 MCP 접근 범위를 정하는 `KORDOC_ROOT`를 쓴다.

## 최근 업데이트

최신 배포는 2026년 10월 4일에 나온 4.18.12다. 최근 변경은 PDF 쪽 넘김 처리와 HWPX 셀 줄바꿈에 몰려 있다.

-   4.18.12: PDF 쪽 넘김 문단 잇기 판정을 HWPX 원문과 대조해 다시 맞췄다. 오판이 50건에서 11건으로 줄었다.
-   4.18.11: 글꼴 사전 수천 개가 글꼴 파일을 나눠 쓰는 PDF에서 메모리가 폭주해(힙 7GB 이상) 종료되던 문제를 고쳤다.
-   4.18.8: HWPX 셀 문단의 CRLF·CR·LF 줄바꿈을 보존하고, 줄 수가 같은 텍스트 편집을 지원한다. 빈 줄이 있거나 줄을 더하고 빼는 편집은 여전히 건너뛴다.

## 출처
- https://github.com/chrisryugj/kordoc
- https://www.npmjs.com/package/kordoc
