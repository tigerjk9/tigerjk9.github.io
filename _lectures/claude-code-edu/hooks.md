---
layout: lecture
lecture_slug: claude-code-edu
feature_id: F-017
feature_name: "Hooks"
title: "Hooks"
track: advanced
order: 14
permalink: /lectures/claude-code-edu/hooks/
---

## 정의

Hooks는 Claude Code 라이프사이클의 특정 이벤트(도구 실행·세션·프롬프트 제출·권한·압축 등) 30종에 자동 핸들러를 붙이는 시스템이다. 도구 호출 직전·직후, 응답 완료, 컨텍스트 압축 직전 등 30개가 넘는 시점에 본인 명령을 끼울 수 있다.

## 핵심 동작

- 이벤트 30+종. `PreToolUse`·`PostToolUse`·`PostToolUseFailure`·`PostToolBatch`·`PermissionRequest`·`PermissionDenied`·`SessionStart`·`SessionEnd`·`UserPromptSubmit`·`PreCompact`/`PostCompact`·`Stop`·`Notification`·`SubagentStart`/`SubagentStop`·`FileChanged`·`WorktreeCreate`/`WorktreeRemove` 등
- 핸들러 type 5종. `command`(셸)·`http`(웹훅)·`mcp_tool`·`prompt`(다른 프롬프트)·`agent`(다른 에이전트)
- `matcher`(도구 이름·정규식·`mcp__server__.*`)로 1차 필터, `if`(`Bash(rm *)`·`Edit(*.ts)`)로 2차 필터
- exit 0 통과·exit 2 차단·기타 비차단 경고. `hookSpecificOutput.permissionDecision`로 `allow`/`deny`/`ask`/`defer` 결정
- `PostToolUse`는 v2.1.121부터 `updatedToolOutput`으로 모든 도구의 출력을 교체 가능

## 사용법

`.claude/settings.json`.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "if": "Bash(rm *)",
            "command": "powershell.exe -File \"$CLAUDE_PROJECT_DIR\\.claude\\hooks\\block-rm.ps1\"",
            "timeout": 30
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "if": "Edit(*.py)",
            "command": "ruff format ${tool_input.file_path}"
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "matcher": "startup",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'export PROJ_KEY=2026-Q2' >> $CLAUDE_ENV_FILE"
          }
        ]
      }
    ]
  }
}
```

## 강사 멘트

> Hooks는 Claude Code의 자동화 핵심이다. 도구 호출 직전·직후, 응답 완료, 컨텍스트 압축 직전 등 30개가 넘는 시점에 본인 명령을 끼울 수 있다. 5종 핸들러 — command(셸)·http(웹훅)·mcp_tool·prompt(다른 프롬프트)·agent(다른 에이전트). exit 2가 핵심이다. exit 0은 통과, exit 2는 차단, 1은 경고만. matcher는 도구·인자 패턴 매칭. Bash·Edit·Read 등 도구별로 분리할 수 있다. 본인 일상에서 "매번 같은 후처리"를 하고 있다면 hook이 답이다. 모든 Edit를 로그로 쌓아두면 누가 언제 무엇을 바꿨는지 추적 가능 — 디버깅·재현성에 도움이 된다. hook이 강력한 만큼 위험하다. 무한 루프 방지용 트리거 보호와 외부 호출 차단 정책, 이 두 가지가 안전벨트다.

## 활용 시사점

교육 현장에서 Hooks는 다음 세 가지로 활용된다.

- **학생 데이터 폴더 보호**. `PreToolUse` + `if "Bash(Remove-Item students/*)"`로 학생 데이터 삭제 시도를 자동 차단한다. 정책을 코드로 박는다
- **활동지 자동 포맷**. `PostToolUse`에서 `.md` 변경 시 자동으로 prettier·markdownlint를 호출해 일관된 양식 유지
- **세션 종료 시 자동 백업**. `SessionEnd` 훅으로 작업 내용·생성 파일 목록을 자동 백업. 실수로 닫혀도 추적 가능

---

[← 이전 기능](/lectures/claude-code-edu/headless/) | [허브로 돌아가기](/lectures/claude-code-edu/) | [다음 기능 →](/lectures/claude-code-edu/mcp/)
