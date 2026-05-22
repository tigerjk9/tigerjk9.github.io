---
layout: lecture
lecture_slug: claude-code-edu
feature_id: F-020
feature_name: "MCP (Model Context Protocol)"
title: "MCP (Model Context Protocol)"
track: advanced
order: 15
permalink: /lectures/claude-code-edu/mcp/
---

## 정의

MCP(Model Context Protocol)는 Claude Code를 GitHub·Slack·Linear·Google Drive·기관 위키 같은 외부 시스템에 연결하는 오픈 표준 프로토콜이다. ChatGPT 커넥터가 닫힌 생태계라면 MCP는 오픈 표준이라 사내 자체 시스템도 직접 어댑터를 짜 연결할 수 있다.

## 핵심 동작

- 등록. `claude mcp add <name> --transport stdio|sse|http --scope user|project|local --env KEY=VALUE -- <command>`
- 프로젝트 레벨 `.mcp.json`은 팀과 공유. 사용자 레벨은 `~/.claude/.mcp.json`
- `alwaysLoad: true`(v2.1.121) — 그 서버의 모든 도구를 tool-search 지연 없이 즉시 로드
- 도구 네이밍. `mcp__<server>__<tool>`. 권한 룰에서 매처로 사용(`mcp__memory__.*`)
- 자동 재시도(v2.1.121). startup transient 에러 시 최대 3회. 동시 연결로 기동 시간 단축
- 관리자 정책. `allowedMcpServers`·`deniedMcpServers`·`allowManagedMcpServersOnly`로 사내 화이트리스트 강제

## 사용법

```powershell
# GitHub MCP 서버 추가 (project scope)
claude mcp add github --transport http --scope project `
  --env GITHUB_TOKEN=ghp_xxxxx -- `
  https://api.github.com/mcp

# 상태 확인
/mcp

# MCP 리소스 참조 (스킬·프롬프트에서)
Show me the data from @github:repos/owner/repo/issues
```

`.mcp.json`.

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-filesystem", "D:\\학교공용자료"],
      "alwaysLoad": true
    }
  }
}
```

## 강사 멘트

> MCP(Model Context Protocol)는 오픈 표준이다. GitHub·Slack·Drive 말고도 학교 위키·학사 시스템·DB에 어댑터를 한 번 짜 두면 어디서든 호출된다. 행정 업무가 많은 사람에게 결정타다. 학교 위키 회의록 다섯 개를 한 채팅에서 끌고 와 요약한 다음 메신저에 올리는 일이 한 흐름에서 끝난다. 학교 위키·메신저 같은 외부 시스템 리소스를 채팅 안에서 바로 참조한다. `.mcp.json` 파일에 등록만 하면 바로 호출된다. transport는 http·stdio·websocket 세 가지. 학교 시스템은 보통 http 아니면 stdio다. 본인 일상에서 자주 오가는 외부 시스템 한 개를 MCP로 잡으면 매주 한 시간이 회수된다. MCP는 강력한 만큼 보안 검토가 필수다. 본인 노트북에 학교 MCP를 붙이기 전에 IT 정책 담당자와 사전 협의 권장. 주의 패턴 — OAuth 토큰을 settings.json에 평문으로 적으면 git에 그대로 커밋될 위험이 있다. 토큰은 환경 변수로만 사용한다.

## 활용 시사점

교육 현장에서 MCP는 다음 세 가지로 활용된다.

- **학교 위키·메신저 통합**. 위키 회의록 5개 → 요약 → 메신저 게시를 한 흐름에서 처리. ChatGPT 커넥터는 닫힌 생태계지만 MCP는 오픈 표준이라 사내 자체 시스템도 어댑터를 짜 연결 가능
- **학사 시스템 조회**. 학사 시스템 MCP를 한 번 연결해 두면 "지난 학기 성적 분포를 학년별 표로" 같은 요청이 한 문장으로 끝난다
- **보안 검토 필수**. 학교 MCP를 붙이기 전 IT 정책 담당자와 사전 협의. `allowedMcpServers`·`allowManagedMcpServersOnly`로 학교 화이트리스트 강제. OAuth 토큰은 환경 변수로만 사용

---

[← 이전 기능](/lectures/claude-code-edu/hooks/) | [허브로 돌아가기](/lectures/claude-code-edu/) | [다음 기능 →](/lectures/claude-code-edu/plugins/)
