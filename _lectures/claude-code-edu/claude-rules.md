---
layout: lecture
lecture_slug: claude-code-edu
feature_id: F-037
feature_name: ".claude/rules/ 와 paths 글롭"
title: ".claude/rules/ 와 paths 글롭"
track: basic
order: 12
permalink: /lectures/claude-code-edu/claude-rules/
---

## 정의

`.claude/rules/`는 CLAUDE.md를 토픽별·파일별로 쪼개고, 글롭 패턴에 매칭되는 파일을 다룰 때만 해당 룰을 컨텍스트에 로드하는 메커니즘이다. 토큰 절약과 정확도를 동시에 확보한다. "토큰 0 / 정확도 1" 슬로건의 도구다.

## 핵심 동작

- 위치는 `.claude/rules/<topic>.md`. 모든 .md 재귀 발견. 하위 폴더(`frontend/`·`backend/`) 가능
- 프론트매터 `paths` 없으면 무조건 로드. 있으면 매칭 시점에만 로드
- 패턴은 `**/*.ts`·`src/**/*`·`*.md`·`src/**/*.{ts,tsx}` 같은 brace expansion 지원
- 심링크 지원. 회사·학교 표준을 `~/shared` 한 곳에 두고 프로젝트마다 링크
- 사용자 룰 `~/.claude/rules/`는 모든 프로젝트에 적용되며 프로젝트 룰이 우선

## 사용법

`.claude/rules/data-files.md`.

```markdown
---
paths:
  - "data/raw_*.csv"
  - "students/**/*.json"
---

# 원본 데이터 보호 룰
- raw_*.csv 파일은 절대 수정 금지. 새 파일을 같은 이름 + `_clean` 접미사로 만든다
- 첫 5행을 다시 읽고 헤더 검증 후 작업 시작
- 인코딩은 UTF-8 BOM 없이 표준화
```

심링크로 공용 룰 끌어 쓰기.

```bash
ln -s ~/shared-claude-rules .claude/rules/shared
ln -s ~/school-standards/safety.md .claude/rules/safety.md
```

## 강사 멘트

> 12번째 기능 `.claude/rules`다. CLAUDE.md가 길어지면 토큰이 매번 다 들어가니, 토픽별로 쪼개서 필요할 때만 로드하는 구조다. "토큰 0 / 정확도 1" 슬로건 — 안 쓸 때는 0, 쓸 때는 정확. 글롭 한 줄이 핵심이다. 본인 폴더의 원본 데이터 파일에 매칭되는 작업이 들어오면 자동으로 이 룰이 로드되고, 그 외에는 0 토큰. 정확도가 핵심이다 — 학생이 원본 데이터를 만질 때만 룰이 떠서 보호해 준다. 데이터 무결성은 룰 한 줄로 잡힌다. 학년부에서 데이터 관리를 담당하는 사람에게는 보안·재현성의 직접 답이다.

## 실습

`.claude/rules/data.md`에 `paths: ["data/raw_*.csv"]` 글롭 한 줄을 추가하고, 매칭되는 파일을 만지는 프롬프트를 보내 룰이 자동 로드되는지 확인한다. 매칭되지 않는 파일을 만질 때는 룰이 로드되지 않아 토큰이 0인 것을 본다.

## 활용 시사점

교육 현장에서 `.claude/rules/`는 다음 세 가지로 활용된다.

- **학생 개인정보 자동 보호**. `paths: ["students/**/*.json"]`로 학생 개인정보 파일을 만질 때만 자동 로드되는 보호 룰을 두면, 평상시에는 토큰 0이면서 위험 작업에서는 정확한 보호가 활성화된다
- **교과별 룰 분리**. `.claude/rules/math.md`(수학)·`.claude/rules/korean.md`(국어)를 분리하면 각 교과 자료를 만질 때만 해당 표기 규칙·용어 가이드가 로드된다
- **학교 공용 룰 심링크**. 학교 표준을 한 곳에 두고 모든 프로젝트가 심링크로 끌어 쓰면, 표준이 갱신될 때 한 번 수정으로 전체에 반영된다

---

[← 이전 기능](/lectures/claude-code-edu/agent-teams/) | [허브로 돌아가기](/lectures/claude-code-edu/) | [다음 기능 →](/lectures/claude-code-edu/headless/)
