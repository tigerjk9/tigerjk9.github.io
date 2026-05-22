---
layout: lecture
lecture_slug: claude-code-edu
feature_id: F-019
feature_name: "Plugins"
title: "Plugins"
track: advanced
order: 16
permalink: /lectures/claude-code-edu/plugins/
---

## 정의

Plugins는 스킬·서브에이전트·훅·MCP 서버·LSP 서버·모니터·바이너리·기본 설정을 하나의 단위로 묶어 배포·버전 관리하는 확장 패키지 형식이다. 본인이 만든 스킬 5개·에이전트 3개·훅 2개를 플러그인 한 개로 묶으면, 동료 교사 5명이 한 줄 명령으로 본인 환경을 그대로 받아 갈 수 있다.

## 핵심 동작

- 구조. 루트의 `.claude-plugin/plugin.json`(name·description·version·author) + `skills/`·`agents/`·`commands/`·`hooks/hooks.json`·`.mcp.json`·`.lsp.json`·`monitors/monitors.json`·`bin/`·`settings.json`
- 스킬은 `/<plugin>:<skill>` 네임스페이스(충돌 방지). `name` 필드로 네임스페이스 변경
- CLI 명령. `claude plugin install <name>@<marketplace>`·`list`·`update`·`uninstall [--prune]`·`prune`(고아 의존성 제거)·`validate`(`$schema`/`version`/`description` 검증)·`tag`(릴리스 git 태그 생성)
- 로컬 개발. `claude --plugin-dir ./local-plugin` + 핫 리로드 `/reload-plugins`
- 공식 마켓플레이스 `claude-plugins-official`. 사내 마켓플레이스는 private repo로

## 사용법

```powershell
# 공식 마켓플레이스에서 설치
claude plugin install code-review@claude-plugins-official

# 로컬 개발 모드
claude --plugin-dir .\my-first-plugin

# 검증·태그·정리
claude plugin validate
claude plugin tag
claude plugin prune
```

`plugin.json`.

```json
{
  "name": "edu-lab-tools",
  "description": "교사 표준 활동지·평가 루브릭 작업 키트",
  "version": "1.0.0",
  "author": { "name": "교사 이름" }
}
```

Anthropic 공식 마켓플레이스 추가 + document-skills 설치.

```text
/plugin marketplace add anthropics/skills
/plugin marketplace list
/plugin install document-skills@anthropic-skills
/plugin list
```

## 강사 멘트

> Plugins는 기능들의 묶음 패키지다. 본인이 만든 스킬 다섯 개·에이전트 세 개·훅 두 개를 플러그인 한 개로 묶으면, 동료 교사 다섯 명이 한 줄 명령으로 본인 환경을 그대로 받아 간다. 학년부장 자리의 결정타 — "내 환경을 학년 교사들에게." plugin.json은 메타파일이다. 본인이 가진 스킬·에이전트·훅·MCP를 한곳에 나열하면 그게 곧 패키지가 된다. private-marketplace는 학교 git repo로 운영한다. 외부 공개 마켓플레이스에는 올리지 않는다. 활용 패턴 — 본인 환경(스킬·서브에이전트·룰)을 plugin으로 묶어 두면 새 합류자에게 install 한 줄로 동일 환경을 전달할 수 있다.

## 실습

Anthropic 공식 마켓플레이스를 추가해 document-skills 묶음을 설치하는 5단계.

1. `claude` 실행
2. `/plugin marketplace add anthropics/skills` — 공식 마켓플레이스 추가
3. `/plugin marketplace list`로 항목 확인
4. `/plugin install document-skills@anthropic-skills`로 묶음 설치
5. `/plugin list`로 확인하고 바로 PDF·docx·xlsx·pptx 처리 호출

한 묶음에 10여 종 스킬이 따라온다 — pdf·docx·xlsx·pptx·canvas-design·webapp-testing 등.

## 활용 시사점

교육 현장에서 Plugins는 다음 세 가지로 활용된다.

- **학년부 표준 환경 배포**. 학년부장의 활동지 작업 환경(스킬·에이전트·룰)을 plugin으로 묶어 두면 새 합류 교사에게 install 한 줄로 동일 환경 전달
- **공식 document-skills 활용**. Anthropic 공식 묶음 한 번 설치로 PDF·docx·xlsx·pptx 즉시 처리. 학교 행정문서·평가 자료 작업에 결정적
- **버전 관리·갱신**. plugin은 버전이 매겨져 갱신이 추적된다. 매번 폴더 복사하는 방식 대비 깔끔. `claude plugin validate`·`tag`·`prune`으로 라이프사이클 관리

---

[← 이전 기능](/lectures/claude-code-edu/mcp/) | [허브로 돌아가기](/lectures/claude-code-edu/) | [다음 기능 →](/lectures/claude-code-edu/routines/)
