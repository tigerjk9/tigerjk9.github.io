---
layout: lecture
lecture_slug: claude-code-edu
feature_id: F-006
feature_name: "헤드리스 모드 (-p + JSON)"
title: "헤드리스 모드 (-p + JSON)"
track: advanced
order: 13
permalink: /lectures/claude-code-edu/headless/
---

## 정의

헤드리스 모드(`claude -p` / `--print`)는 인터랙티브 세션 없이 한 번 실행하고 결과를 stdout으로 내보내는 모드다. JSON·스트림 JSON 출력으로 스크립트·파이프라인에 합성 가능하다. 셸 한 줄로 AI를 야간 잡·CI 후처리·데이터 정제 파이프라인에 끼워 넣는 표준 도구다.

## 핵심 동작

- 표준 입력(`stdin`) 파이프 입력을 그대로 컨텍스트로 받는다(`cat logs.txt | claude -p "explain"`)
- `--json-schema '{...}'`로 응답이 특정 JSON Schema에 맞도록 강제한다 — 응답의 `structured_output` 필드에 검증된 객체가 들어온다
- `--max-turns N`·`--max-budget-usd 5.00`로 자동 폭주 방지
- `--no-session-persistence`로 세션 저장조차 하지 않는다

## 사용법

```powershell
# 단순 호출
claude -p "What does the auth module do?"

# 구조화 출력 + jq로 파싱 (PowerShell 7+ 가정)
claude -p "Extract the main function names from auth.py" `
  --output-format json `
  --json-schema '{"type":"object","properties":{"functions":{"type":"array","items":{"type":"string"}}},"required":["functions"]}' `
  | jq '.structured_output'

# 빌드 에러 파이프
Get-Content build-error.txt | claude -p "explain root cause" > output.txt

# 스트리밍 + 부분 메시지
claude -p "Explain recursion" --output-format stream-json --verbose --include-partial-messages

# 예산 캡 필수
claude -p "review repo" --max-turns 5 --max-budget-usd 2.00
```

학생 활동지 일괄 변환 예시.

```powershell
Get-Content activities\messy.md | claude -p `
  "이 활동지를 학교 표준 양식(학습목표·활동단계·평가기준 3섹션)으로 다시 정리해 줘" `
  --max-budget-usd 1.00 > activities\clean.md
```

## 강사 멘트

> 첫 Advanced 기능 헤드리스다. CLI 도구로서 Claude Code의 진짜 힘이 여기서 나온다. 자동화·데이터 자리의 본편이다. 매일 도는 야간 잡, CI 후처리, 데이터 정제 파이프라인에 한 줄로 끼워 넣는다. 모범 프롬프트 #4를 그대로 쓴다. 본인이 PowerShell 한 줄을 외울 필요 없다. AI한테 "이런 한 줄 만들어 줘"라고 시키는 게 가장 빠른 길이다. `--max-budget-usd` 캡을 한 번 더 강조한다. 자동화 잡은 비용이 폭주할 수 있어서, 캡이 안전벨트 역할을 한다. PowerShell 5.x는 인코딩 이슈가 있을 수 있다. 7+ 기준으로 진행한다.

## 실습

`Get-Content data.csv | claude -p "표를 학교 보고서 문체로 두 단락 작성" --max-budget-usd 1.00`을 1회 실행한다. JSON 출력은 다음 단계의 `ConvertFrom-Json`이 그대로 받아 처리할 수 있다.

```powershell
Get-Content activities\messy.csv | claude -p `
  "각 활동을 학습목표·소요시간·필요물 3컬럼 CSV로 정리" `
  --output-format json `
  --max-budget-usd 0.50 `
  | ConvertFrom-Json `
  | Export-Csv activities\clean.csv -NoTypeInformation
```

## 활용 시사점

교육 현장에서 헤드리스 모드는 다음 세 가지로 활용된다.

- **활동지 일괄 변환**. 활동지 30편을 매 학기 새 양식으로 옮길 때 `Get-ChildItem *.md | ForEach { Get-Content $_ | claude -p "표준 양식으로" > converted/$_.Name }`로 한 줄에 처리
- **야간 보고서 후처리**. 매주 금요일 자동 보고서를 야간에 돌려 아침에 정리된 CSV로 받는다. 학년부 회의 시간에 즉시 활용 가능
- **빌드 파이프라인 통합**. npm/pnpm scripts·CI 워크플로우에 `"lint:claude"` 같은 항목으로 등록해 빌드 단계에 AI를 박는다. `--max-budget-usd` 캡으로 비용 안전벨트 필수

---

[← 이전 기능](/lectures/claude-code-edu/claude-rules/) | [허브로 돌아가기](/lectures/claude-code-edu/) | [다음 기능 →](/lectures/claude-code-edu/hooks/)
