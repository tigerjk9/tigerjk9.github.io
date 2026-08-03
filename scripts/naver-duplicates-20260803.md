# 네이버 중복 발행 목록 (2026-08-03 확인)

> **정정 (2026-08-03)**: 아래 20쌍 중 `2026-06-11-codex-ai-education-lever` 는 중복이 아니었다.
> 구본 기록의 `url: "unknown"` 은 "다른 주소로 발행됨"이 아니라 **발행 결과를 확인하지 못함**을
> 뜻했고, 실제로 08-01 발행은 성사되지 않았다(블로그 최신 30건 확인 — 같은 배치의 앞뒤 글
> 224364934386 / 224364937243 사이에 해당 글이 없다). 즉 08-03 본이 유일본이었는데 이를
> 삭제해 글이 사라졌고, 이후 재발행으로 복구했다.
> **교훈: 구본 URL 이 `unknown` 인 행은 중복 판정에서 제외해야 한다.**

같은 포스트가 서로 다른 logNo 로 두 번 발행됐다. 게시 이력(`scripts/naver_crosspost_state.json`)이
커밋되지 않은 채 스케줄 실행이 돌아, 이미 올린 글을 미게시로 판단한 것이 원인이다.

- **남길 것(최신)** — 병합된 게시 이력에 기록된 값. posted_at 이 늦은 쪽.
- **지울 것(구본)** — 먼저 올라간 쪽.

| # | 포스트 | 지울 logNo (구본) | 발행 시각 | 남길 logNo (최신) | 발행 시각 |
|---|--------|------------------|-----------|------------------|-----------|
| 1 | 2026-06-11-claude-ai-use-cases | 224364934386 | 2026-08-01 16:43:52 | 224366340495 | 2026-08-03 08:57:01 |
| 2 | 2026-06-11-codex-ai-education-lever | unknown | 2026-08-01 16:46:08 | 224366341597 | 2026-08-03 08:58:28 |
| 3 | 2026-06-11-designing-tech-for-relational-learning | 224364937243 | 2026-08-01 16:47:44 | 224366342582 | 2026-08-03 08:59:46 |
| 4 | 2026-06-11-edu-tech-decisions | 224364938911 | 2026-08-01 16:49:58 | 224366343789 | 2026-08-03 09:01:14 |
| 5 | 2026-06-11-human-nature-tech-education-value | 224364939981 | 2026-08-01 16:51:18 | 224366345076 | 2026-08-03 09:02:53 |
| 6 | 2026-06-11-love-education-truth-paradox | 224364941653 | 2026-08-01 16:53:35 | 224366346037 | 2026-08-03 09:04:06 |
| 7 | 2026-06-11-peterson-education-challenge | 224364943121 | 2026-08-01 16:55:35 | 224366347582 | 2026-08-03 09:06:02 |
| 8 | 2026-06-11-tech-education-humility | 224364944405 | 2026-08-01 16:57:23 | 224366348951 | 2026-08-03 09:07:47 |
| 9 | 2026-06-11-thesis-evaluation-ai-era | 224364945708 | 2026-08-01 16:59:08 | 224366350387 | 2026-08-03 09:09:30 |
| 10 | 2026-06-12-claude-fable5-mythos5-launch | 224364947148 | 2026-08-01 17:01:03 | 224366351810 | 2026-08-03 09:11:10 |
| 11 | 2026-06-15-agi-asi-pathways | 224366112974 | 2026-08-03 00:22:24 | 224366396521 | 2026-08-03 10:00:34 |
| 12 | 2026-06-15-ai-agents-architecture-patterns | 224366114103 | 2026-08-03 00:23:55 | 224366398125 | 2026-08-03 10:02:06 |
| 13 | 2026-06-15-ai-smart-user-traits | 224366115254 | 2026-08-03 00:25:39 | 224366399613 | 2026-08-03 10:03:40 |
| 14 | 2026-06-15-claude-code-loop-pipeline | 224366116375 | 2026-08-03 00:27:09 | 224366401508 | 2026-08-03 10:05:32 |
| 15 | 2026-06-15-claude-remotion-video-automation | 224366117333 | 2026-08-03 00:28:30 | 224366403060 | 2026-08-03 10:07:07 |
| 16 | 2026-06-15-domain-coding-ai-weapon | 224366118442 | 2026-08-03 00:30:04 | 224366404840 | 2026-08-03 10:08:59 |
| 17 | 2026-06-15-envy-psychology-coping | 224366119608 | 2026-08-03 00:31:45 | 224366406375 | 2026-08-03 10:10:28 |
| 18 | 2026-06-15-github-repo-orchestrator-automation | 224366120564 | 2026-08-03 00:33:10 | 224366407810 | 2026-08-03 10:11:56 |
| 19 | 2026-06-15-loop-engineering-reality-use | 224366121620 | 2026-08-03 00:34:44 | 224366409322 | 2026-08-03 10:13:26 |
| 20 | 2026-06-15-son-heung-min-invisible-impact | 224366122722 | 2026-08-03 00:36:29 | 224366411240 | 2026-08-03 10:15:16 |

총 20쌍. 삭제 URL 확보 19건, logNo 미기록 1건.

## logNo 미기록 — 수동 확인 필요
- `2026-06-11-codex-ai-education-lever` — 구본의 logNo 가 `unknown` 으로 저장돼 URL 을 특정할 수 없다.
  발행 직후 URL 추출에 실패한 건이다. 네이버 글 목록에서 같은 제목 2건을 눈으로 확인해야 한다.

## 삭제 대상 URL

- https://blog.naver.com/dot_connector/224364934386  <!-- 2026-06-11-claude-ai-use-cases -->
- https://blog.naver.com/dot_connector/224364937243  <!-- 2026-06-11-designing-tech-for-relational-learning -->
- https://blog.naver.com/dot_connector/224364938911  <!-- 2026-06-11-edu-tech-decisions -->
- https://blog.naver.com/dot_connector/224364939981  <!-- 2026-06-11-human-nature-tech-education-value -->
- https://blog.naver.com/dot_connector/224364941653  <!-- 2026-06-11-love-education-truth-paradox -->
- https://blog.naver.com/dot_connector/224364943121  <!-- 2026-06-11-peterson-education-challenge -->
- https://blog.naver.com/dot_connector/224364944405  <!-- 2026-06-11-tech-education-humility -->
- https://blog.naver.com/dot_connector/224364945708  <!-- 2026-06-11-thesis-evaluation-ai-era -->
- https://blog.naver.com/dot_connector/224364947148  <!-- 2026-06-12-claude-fable5-mythos5-launch -->
- https://blog.naver.com/dot_connector/224366112974  <!-- 2026-06-15-agi-asi-pathways -->
- https://blog.naver.com/dot_connector/224366114103  <!-- 2026-06-15-ai-agents-architecture-patterns -->
- https://blog.naver.com/dot_connector/224366115254  <!-- 2026-06-15-ai-smart-user-traits -->
- https://blog.naver.com/dot_connector/224366116375  <!-- 2026-06-15-claude-code-loop-pipeline -->
- https://blog.naver.com/dot_connector/224366117333  <!-- 2026-06-15-claude-remotion-video-automation -->
- https://blog.naver.com/dot_connector/224366118442  <!-- 2026-06-15-domain-coding-ai-weapon -->
- https://blog.naver.com/dot_connector/224366119608  <!-- 2026-06-15-envy-psychology-coping -->
- https://blog.naver.com/dot_connector/224366120564  <!-- 2026-06-15-github-repo-orchestrator-automation -->
- https://blog.naver.com/dot_connector/224366121620  <!-- 2026-06-15-loop-engineering-reality-use -->
- https://blog.naver.com/dot_connector/224366122722  <!-- 2026-06-15-son-heung-min-invisible-impact -->

