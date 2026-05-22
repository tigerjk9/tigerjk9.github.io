---
layout: lecture
lecture_slug: claude-code-edu
feature_id: F-029
feature_name: "Permission Modes 6종"
title: "Permission Modes 6종"
track: basic
order: 4
permalink: /lectures/claude-code-edu/permission-modes/
---

## 정의

Permission Modes는 Claude가 파일 수정·셸 실행·네트워크 요청 시 사용자에게 prompt를 얼마나 자주 띄울지 결정하는 6단계 자율성 다이얼이다. `default`·`acceptEdits`·`plan`·`auto`·`dontAsk`·`bypassPermissions` 중 하나로 시작하거나 세션 중 사이클로 전환한다.

## 핵심 동작

- `default` — 읽기만 자동 승인. 첫 진입에 적합
- `acceptEdits` — 읽기 + 파일 수정 + 일반 fs 명령(`mkdir`·`mv`·`cp` 등 안전 명령) 자동 승인
- `plan` — 읽기만, 절대 수정 없음
- `auto` — 분류기 모델이 위험 평가 후 자동 승인. `curl|bash`·force push·외부 인프라 변경 등은 차단
- `dontAsk` — `permissions.allow`에 없으면 모두 거부. CI 락다운용
- `bypassPermissions` — 모든 prompt 스킵(보호 경로 제외). 격리 컨테이너·VM 전용
- 보호 경로(`.git`·`.vscode`·`.claude`·`.bashrc` 등)는 어떤 모드에서도 자동 승인되지 않는다

## 사용법

```powershell
# 모드별 시작
claude --permission-mode plan
claude --permission-mode acceptEdits
claude --permission-mode auto
claude --permission-mode dontAsk -p "lint and report issues only"

# 세션 안에서 사이클
# Shift+Tab → default → acceptEdits → plan 순환
```

settings.json으로 영구 설정.

```json
{
  "permissions": {
    "defaultMode": "acceptEdits",
    "deny": ["Bash(Remove-Item *)", "Read(~/.ssh/**)"],
    "ask":  ["Bash(git push *)"],
    "allow": ["Bash(git status)", "Bash(Rscript *)", "Read(./data/**)"]
  }
}
```

## 강사 멘트

> 6단계라고 적었지만 일상은 두 개다. plan은 앞에서 봤고, default는 매번 묻기, acceptEdits는 편집은 자동으로 가고 터미널 명령은 묻기. auto·dontAsk·bypass는 야간 헤드리스 잡 같은 자동화에서만 의미가 있다. 본인 노트북에는 settings.json 한 개를 두고 매일 acceptEdits로 시작하는 것이 무난하다. 모범 프롬프트의 핵심은 본인이 매일 쓰는 명령을 가지고 AI에게 설정 파일을 직접 짜게 시키는 것이다. 일일이 외울 필요 없다. bypass는 강한 어조로 한 번 더 — 격리 환경(컨테이너·VM·일회용 폴더) 외에는 절대 금지. 기관 정책 위반이 될 수 있으니 주의한다.

## 실습

자기 폴더에 `.claude/settings.json`을 만들어 deny 한 줄을 넣는다. JSON은 PowerShell here-string의 single-quote 형식(`@'...'@`)으로 작성해 변수 확장과 충돌을 피한다.

```powershell
PS C:\work\edu-lab\demo01> New-Item -ItemType Directory -Path .claude -Force
PS C:\work\edu-lab\demo01> @'
{
  "permissions": {
    "deny": ["Bash(Remove-Item *)"],
    "ask":  ["Bash(git push *)"]
  }
}
'@ | Out-File -Encoding UTF8 .claude\settings.json
```

세션 안에서 "이 폴더의 .md 파일을 모두 지워줘"라고 요청해 차단 메시지가 뜨면 성공이다.

## 활용 시사점

교육 현장에서 Permission Modes는 다음 세 가지로 활용된다.

- **자리별 진입점 분리**. Claude Code를 처음 쓰는 동료 교사는 `plan`, 익숙한 교사는 `acceptEdits`, 야간 자동 보고서 생성 잡은 `dontAsk`로 시작한다. 같은 도구가 사람·상황별로 다른 자율성을 가진다
- **위험 명령 영구 deny**. 학생 데이터 폴더에서 `Remove-Item`·`Read(~/.ssh/**)` 같은 위험 명령을 deny 룰로 박아 두면, 학생이 실수로 실행해도 차단된다. settings.json 한 줄이 사고 예방의 핵심
- **AI에게 settings.json 작성 시키기**. 본인이 매일 쓰는 명령을 나열한 뒤 "이걸 기반으로 settings.json deny·ask·allow 룰을 짜 줘"라고 요청한다. 일일이 외울 필요 없는 메타 패턴이다

---

[← 이전 기능](/lectures/claude-code-edu/plan-mode/) | [허브로 돌아가기](/lectures/claude-code-edu/) | [다음 기능 →](/lectures/claude-code-edu/skills/)
