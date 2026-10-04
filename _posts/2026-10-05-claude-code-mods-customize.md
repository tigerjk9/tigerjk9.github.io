---
title: "클로드 코드 모드 시작하기: 개발 워크플로 맞춤화"
date: 2026-10-05 01:14:55 +0900
categories: [AI, 소프트웨어개발]
tags: [클로드, AI, 프롬프트엔지니어링, 소프트웨어개발, 생산성, 자동화, 개발자도구, LLM]
header:
  teaser: /assets/claude-code-mods-customize-thumb.png
permalink: /post/claude-code-mods-customize/
---
**클로드 코드(Claude Code)**의 **모드(Mods)**는 사용자가 개발 환경을 자신만의 방식으로 깊이 맞춤화하도록 돕는 강력한 도구이다. 이는 단순한 설정 변경을 넘어, 클로드 코드의 동작 방식을 재정의하고 고유한 사용자 인터페이스를 추가하는 수준에 이른다. 이 글은 클로드 코드 모드의 기본 개념부터 실제 모드를 구축하는 방법, 그리고 더 나아가 복잡한 작업 흐름을 자동화하는 활용 사례까지 상세히 설명한다.

<figure>
<img src="/assets/claude-code-mods-customize-thumb.png" alt="클로드 코드 모드 시작하기: 개발 워크플로 맞춤화">
</figure>

## 클로드 코드 모드 개념

**모드**는 클로드 코드 세션 내에서 실행되는 작은 **자바스크립트(JavaScript)** 또는 **타입스크립트(TypeScript)** 파일이다. 이 파일은 클로드 코드의 활동을 관찰하고, 동작을 변경하며, 터미널이나 데스크톱 앱에 자체 UI를 그린다. 모드를 사용하기 위해 별도의 API를 학습할 필요는 없다. `claude`를 실행한 다음 원하는 모드를 설명하면 클로드 코드가 모드를 생성한다. 뜨거운 리로드(hot reload)를 허용하면 턴이 끝날 때 모드가 나타난다.

클로드 코드는 이미 설정, 권한 규칙, 슬래시 명령, 스킬, 상태 표시줄 등을 통해 동작 방식을 변경할 수 있는 기능을 제공한다. 모드는 여기서 한 발 더 나아간다. 클로드 코드의 동작을 재작성하거나 대체하고, 맞춤형 UI를 그릴 수 있다. 내부적으로 모드는 플러그인에 포함된 **훅(hook)**이며, 각 훅은 세션에서 발생하는 모든 이벤트를 실시간으로 확인한다. 이로써 모드는 클로드 코드를 사용자의 작업 방식에 완벽하게 맞춰준다. 자주 확인하는 정보를 표시하거나, 위험한 명령 앞에 보호막을 두거나, 변경 사항을 검토하는 자신만의 방식을 구축하는 일이 가능하다.

모드는 클로드 코드 2.1.287 버전 이상에서 기본적으로 활성화되어 있다. API는 릴리스마다 변경될 수 있으나, 클로드 코드가 모드를 로드할 때마다 해당 빌드에 맞는 타입 선언을 모드의 `.claude-plugin/types/` 폴더에 작성하므로, 이 선언 파일이 현재 버전의 기준이 된다.

## 모드의 작동 원리

모드는 동작 로직이 자바스크립트 또는 타입스크립트 모듈에 담긴 클로드 코드 플러그인이다.

*   모드 폴더는 일반 플러그인처럼 `.claude-plugin/plugin.json` 매니페스트 파일을 갖는다.
*   `hooks/hooks.json` 파일은 `modules` 아래에 하나의 모듈 이름을 지정한다.
*   모듈은 `register(on, options)` 함수를 내보내며, 이 함수 내에서 `on(event, matcher?, hook)`을 통해 훅을 추가한다.

모든 훅은 동일한 구조를 지닌다. `on("tool.call", { tool: "Bash" }, async ($, e, next) => { ... })`와 같은 형태이다. 여기서 `$`는 UI, 세션, 상태, 파일 시스템 등의 클로드 코드 API를 제공하고, `e`는 현재 이벤트의 입력 데이터를 담는다. `next`는 `e`를 다른 플러그인으로, 그리고 최종적으로 클로드 코드의 기본 동작으로 전달한다.

훅은 **미들웨어(middleware)**처럼 체인을 형성한다. 사용자의 훅이 실행되고, `next(e)`는 이벤트를 다음 플러그인으로 넘긴다. 체인 마지막에 도달하면 클로드 코드가 원래 수행하려던 동작을 실행한다.

훅은 크게 세 가지 방식으로 동작할 수 있다.

| 유형      | 방법                                    | 예시                                 |
| :-------- | :-------------------------------------- | :----------------------------------- |
| **관찰**  | `const r = await next(e); /* look */ return r` | 모든 파일 편집 기록. 턴 종료 후 측정. |
| **재작성** | `return next({ ...e, command: safer })` | 체인 후반부가 보는 이벤트 변경.      |
| **응답**  | `return { deny: "…" }` (next 미호출)     | 도구 호출 거부. 명령이나 도구 직접 처리. |

이벤트는 도구 호출, 제출된 프롬프트, 턴 시작 및 종료, 세션 시작 및 종료, 슬래시 명령, `ui.render` 등 인터페이스가 그려지는 모든 부분을 다룬다. 모듈은 자체 샌드박스에서 실행되며 DOM이나 Node.js 환경이 없어, 외부와의 모든 상호작용은 `$` 객체를 통해 이루어진다.

이러한 모드는 **설정 훅(settings hooks)**과 다르다. 설정 훅은 각 이벤트마다 셸 명령을 실행하고 JSON 데이터를 `stdin`/`stdout`으로 주고받는다. 반면 모드는 한 번 로드되면 세션 내에 상주하며, 상태를 유지하고, 이벤트 발생에 따라 UI를 업데이트하며, 클로드 코드에 다시 호출(open pane, run process, register slash command, register tool)하는 것이 가능하다. 클로드 코드 자체의 일부 기능(AGENTS.md 지원, `/diff` 창 등)도 모드로 구축된다. 이들의 소스 코드는 공개 **anthropics/claude-code** 저장소의 `mods/`에서 확인할 수 있다.

## 첫 모드 구축: 토큰 웨더

**토큰 웨더(Token Weather)**는 각 턴이 끝난 후 컨텍스트 창의 사용량을 읽어 프롬프트 위에 한 줄로 표시한다. 이 한 줄은 날씨 아이콘, 사용률 백분율, 전체 컨텍스트 창에서 사용된 토큰 수, 최근 턴 사용량 차트, 그리고 마지막 턴에서 추가된 토큰 양을 보여준다.

토큰 웨더의 컨텍스트 창 사용량에 따른 예측 표는 다음과 같다.

| 사용량     | 예측               |
| :--------- | :----------------- |
| 25% 미만   | ☀ Clear (맑음)    |
| 25–49%     | ☁ Cloudy (흐림)   |
| 50–74%     | ☂ Showers (소나기) |
| 75–89%     | ☇ Storm (폭풍)    |
| 90% 이상   | ↯ Compact soon (압축 임박) |

### 클로드를 활용한 모드 자동 생성

여섯 단계를 건너뛰고 클로드를 활용해 모드를 직접 생성할 수 있다. 클로드 코드는 모드를 작성하는 방법을 알고 있으므로, 원하는 모드를 설명하면 클로드가 직접 코드를 만든다. `claude`로 세션을 시작하고 다음 프롬프트를 붙여 넣는다.

```text
Make me a Claude Code mod called token-weather: a live forecast of my context window, shown in the band above the prompt. What it should show, on one line: - A weather icon and word for how full the context window is: under 25% ☀ Clear (yellow), 25–49% ☁ Cloudy (cyan), 50–74% ☂ Showers (blue), 75–89% ☇ Storm (magenta), 90% and up ↯ Compact soon (red). - The percentage used, then the tokens used out of the window, like "134.4k / 200k". - A small chart of the last 12 turns, drawn with ▁▂▃▄▅▆▇█. - How much the last turn added, like "▲ +98.3k last turn". It should update after every turn.
```

클로드는 세션에 뜨거운 리로드(hot reloading)를 켤지 한 번 묻는다. 이를 허용하면 클로드의 턴이 끝날 때 프롬프트 위에 **토큰 웨더**가 나타난다. 이후 모든 변경 사항은 즉시 리로드되므로, "폭풍 예측을 70%부터 시작하게 해줘", "끝에 달러 비용을 추가해줘"와 같은 요청을 통해 모드를 수정하고 실시간으로 변화를 확인할 수 있다. 이 모드는 현재 세션에서만 로드되며, 폴더는 나중에 정리된다. 모드를 유지하려면 폴더를 복사하고 플러그인처럼 설치한다.

이 과정에서 프롬프트는 오직 "무엇을 보고 싶은지"만 설명한다. API를 알 필요 없이 모드를 작성한다. 클로드 코드의 내장 모드 작성 가이드는 상태 관리, `claude plugin validate`를 통한 플러그인 검증, 훅 이벤트 설정 등 **어떻게** 작성하는지를 다룬다.

### 단계별 모드 구축

**1단계: 폴더 생성**
클로드 코드 버전이 2.1.287 이상인지 확인한다: `claude --version`.
다음과 같은 폴더 구조를 생성한다.

```
token-weather/
├── .claude-plugin/
│   ├── plugin.json
│   └── types/ (클로드 코드가 모드를 로드할 때 작성됨)
├── hooks/
│   ├── hooks.json
│   └── token-weather.mjs
├── types/
│   └── index.d.ts (3단계에서 추가)
└── tests/
    └── token-weather.test.ts (5단계에서 추가)
```

`.claude-plugin/plugin.json`은 표준 플러그인 매니페스트이다.

```json
{
  "name": "token-weather",
  "version": "0.1.0",
  "description": "A live forecast of the context window, drawn above the prompt.",
  "author": {
    "name": "You"
  }
}
```

`hooks/hooks.json`은 모듈을 가리킨다. 모드는 하나의 모듈을 지닌다.

```json
{
  "modules": ["./token-weather.mjs"]
}
```

**2단계: UI 그리기**
프롬프트 바로 위 영역은 `AbovePrompt`라는 컴포넌트이다. 클로드 코드는 이 영역에 아무것도 그리지 않으므로, 첫 타겟으로 적합하다. `ui.render` 이벤트를 훅하고 요소 트리를 반환한다.

```javascript
// hooks/token-weather.mjs
export function register(on) {
  on("ui.render", { component: "AbovePrompt" }, ($, e, next) => {
    const { Box, Text } = $.ui.resolve(e);
    return Box({
      paddingX: 1,
      children: [
        Text({ color: "yellow", bold: true, children: "☀ Clear skies" })
      ],
    });
  });
}
```

요소들은 전역 변수가 아니다. `$.ui.resolve(e)`는 그려지는 표면(surface)에 따라 약간씩 다른 생성자를 반환한다. JSX도 `h`를 팩토리 함수로 사용하여 작동한다.
`claude --plugin-dir ./token-weather` 명령으로 플러그인을 로드하여 세션을 시작한다. "☀ Clear skies"가 프롬프트 위에 나타난다. 폴더가 감시되므로, 파일을 저장할 때마다 모듈이 재시작 없이 즉시 리로드된다. 이 빠른 피드백 루프는 모드 개발을 즐겁게 만드는 요소이다.

**3단계: 실제 데이터 읽기 및 `$.state`에 저장**
`$.session.usage()`는 상태 표시줄과 동일한 수치를 반환한다. `context.tokens`는 마지막 응답에 사용된 입력 토큰, `context.window`는 모델의 컨텍스트 창 크기, `context.percent`는 전자에 대한 후자의 비율이다. `breakdown`을 요청하지 않으면 이 호출은 무료이다.

세션 시작 시와 각 턴 종료 후 데이터를 읽는다.

```javascript
on("session.start", async ($, e, next) => {
  const result = await next(e);
  await takeReading($);
  return result;
});

on("turn.complete", async ($, e, next) => {
  const result = await next(e);
  if (!e.agentId) { // 서브 에이전트 턴 제외, 메인 루프 턴만 해당
    await takeReading($);
  }
  return result;
});
```

두 훅 모두 먼저 `next(e)`를 호출한 다음 데이터를 관찰한다. 어떠한 동작도 변경하지 않는다.

**데이터 보관 장소**: 모듈 수준 `let readings = []`가 분명한 선택처럼 보일 수 있으나, 뜨거운 리로드는 모듈을 새로 로드하는 것이므로 `register`가 다시 실행되고 `session.start`가 다시 트리거되며 모듈 변수가 초기화된다. 대신 히스토리 데이터를 `$.state`에 저장한다. `$.state`는 호스트에서 전체 세션 동안 명명된 값을 유지하며 리로드 후에도 데이터를 보존한다.

```javascript
// 호스트가 유지하므로, 파일 뜨거운 리로드 후에도 히스토리가 보존된다.
const readings = { plugin: "token-weather", key: "readings" };

async function takeReading($) {
  const { context } = await $.session.usage();
  if (!context?.window) return;

  const tokens = context.tokens ?? 0;
  const percent = context.percent ?? Math.round((tokens / context.window) * 100);

  const { value: history = [] } = await $.state.get(readings);
  await $.state.set(readings, [...history, { tokens, window: context.window, percent }].slice(-HISTORY));
}
```

상태 값은 플러그인의 **타입 계약(type contract)**에 선언한다. 이는 매니페스트가 가리키는 작은 `.d.ts` 파일이다. `types/index.d.ts` 파일을 추가한다.

```typescript
export type TokenWeatherReading = { tokens: number; window: number; percent: number };
declare module "claude-code" {
  interface PluginState {
    "token-weather": { readings: TokenWeatherReading[] };
  }
}
```

그 후 `plugin.json`에 `"types": "./types/index.d.ts"`를 추가한다. 이 단계를 건너뛰면 `claude plugin validate`가 `token-weather.readings is not declared: the manifest's types contract must name it in interface PluginState { … }`라는 오류와 함께 수정을 요청한다.
이러한 설정을 통해 UI는 자동으로 다시 그려진다. 렌더 훅이 실행되는 동안 `$.state.get`은 해당 드로잉을 구독하므로, 이후의 모든 `$.state.set`은 밴드를 다시 그린다. `$.ui.invalidate`를 명시적으로 호출할 필요가 없다.

**4단계: 예측 그리기**
전체 모듈 코드는 다음과 같다.

```javascript
// Token Weather: 프롬프트 위 컨텍스트 창의 실시간 예측
const HISTORY = 12;
const BARS = "▁▂▃▄▅▆▇█";
const FORECAST = [
  { upTo: 25, icon: "☀", word: "Clear", color: "yellow" },
  { upTo: 50, icon: "☁", word: "Cloudy", color: "cyan" },
  { upTo: 75, icon: "☂", word: "Showers", color: "blue" },
  { upTo: 90, icon: "☇", word: "Storm", color: "magenta" },
  { upTo: Infinity, icon: "↯", word: "Compact soon", color: "red" },
];

// 호스트가 유지하므로, 파일 뜨거운 리로드 후에도 히스토리가 보존된다.
const readings = { plugin: "token-weather", key: "readings" };

export function register(on) {
  on("session.start", async ($, e, next) => {
    const result = await next(e);
    await takeReading($);
    return result;
  });

  on("turn.complete", async ($, e, next) => {
    const result = await next(e);
    if (!e.agentId) { // 서브 에이전트 턴 제외, 메인 루프 턴만 해당
      await takeReading($);
    }
    return result;
  });

  on("ui.render", { component: "AbovePrompt" }, async ($, e, next) => {
    const { value: history = [] } = await $.state.get(readings);
    if (e.props.hasSurvey || history.length === 0) {
      return next(e);
    }

    const { Box, Text } = $.ui.resolve(e);
    return band(Box, Text, history, e.props.bodyColumns);
  });
}

async function takeReading($) {
  const { context } = await $.session.usage();
  if (!context?.window) return;

  const tokens = context.tokens ?? 0;
  const percent = context.percent ?? Math.round((tokens / context.window) * 100);

  const { value: history = [] } = await $.state.get(readings);
  await $.state.set(readings, [...history, { tokens, window: context.window, percent }].slice(-HISTORY));
}

function band(Box, Text, history, columns) {
  const now = history[history.length - 1];
  const f = FORECAST.find((b) => now.percent < b.upTo);

  const parts = [
    Text({ color: f.color, bold: true, children: `${f.icon} ${f.word}` }),
    Text({ children: ` ${now.percent}% of context` }),
    Text({ dimColor: true, children: ` ${short(now.tokens)} / ${short(now.window)}` }),
  ];

  if (columns >= 60) {
    parts.push(Text({ dimColor: true, children: " last turns " }));
    parts.push(Text({ color: f.color, children: sparkline(history) }));
    if (history.length > 1) {
      parts.push(Text({ dimColor: true, children: trend(history) }));
    }
  }

  return Box({ flexDirection: "row", paddingX: 1, children: parts });
}

function sparkline(history) {
  const top = Math.max(...history.map((r) => r.tokens), 1);
  return history.map((r) => BARS[Math.floor((r.tokens / top) * (BARS.length - 1))]).join("");
}

function trend(history) {
  const delta = history[history.length - 1].tokens - history[history.length - 2].tokens;
  if (delta === 0) return " steady";
  return delta > 0 ? ` ▲ +${short(delta)} last turn` : ` ▼ ${short(-delta)} last turn`;
}

function short(n) {
  if (n >= 1_000_000) return `${+(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000) return `${+(n / 1_000).toFixed(1)}k`;
  return String(n);
}
```

이 모듈 코드에서 세부 사항 몇 가지를 자신의 모드에 활용할 수 있다.

*   **컴포넌트의 `props`는 `e.props`에 있다.** `hasSurvey`는 설문조사가 밴드를 원하는지 알려주므로, 이 경우 훅은 `next(e)`를 통해 설문조사에 양보한다. `bodyColumns`는 밴드의 실제 너비로, 트랜스크립트 옆에 창(pane)이 도킹되어 있을 때는 터미널보다 좁아진다. 트리의 크기를 이에 맞춰 조정한다. 오직 `e.component`, `e.surface`, `e.requestId`, `e.viewport`만 `e`의 최상위 레벨에 위치한다.
*   **그릴 내용이 없을 때는 이벤트를 통과시킨다.** `next(e)`를 반환하면 밴드를 클로드 코드와 다른 모드에 다시 넘겨준다.
*   **이모지가 아닌 단일 너비 심볼을 사용한다.** ☀ ☁ ☂ ☇ ↯와 같은 심볼은 모든 터미널 폰트에서 정렬된다.

파일을 저장하면 실행 중인 세션이 변경 사항을 적용한다. 여러 턴이 지나며 큰 파일을 읽어 밴드가 Clear에서 Showers, Storm으로 변화하는 것을 확인할 수 있다.

**5단계: 유효성 검사 및 테스트**
`claude plugin validate` 명령은 매니페스트와 모듈 소스를 클로드 코드와 동일한 방식으로 읽어, 모듈이 어떤 훅을 사용하고 어떤 API를 호출하는지 보고한다.

```text
$ claude plugin validate ./token-weather
> types ./types/index.d.ts declares state: token-weather.readings
> ./token-weather.mjs hooks: session.start, turn.complete, ui.render{component=AbovePrompt}
> ./token-weather.mjs calls: $.session.usage (via takeReading), $.state.get, $.state.set (via takeReading), $.ui.resolve
> ./token-weather.mjs state writes: token-weather.readings
> ./token-weather.mjs state reads: token-weather.readings
√ Validation passed
```

`claude plugin test` 명령은 플러그인의 `*.test.ts` 파일을 실제 클로드 코드 런타임에 대해 실행한다. 테스트가 `on`으로 등록하는 훅은 체인에서 모드 **이후**에 실행되며, 클로드 코드가 응답할 내용을 스텁(stub)한다. 이를 통해 `$.session.usage()`가 반환하는 내용을 정확히 제어할 수 있다.

```typescript
// tests/token-weather.test.ts
import { describe, expect, test } from "claude-code/testing";

describe("token-weather", () => {
  test("the band follows the context window", async ($, on) => {
    // 여기에 등록된 훅은 모드 다음에 실행되며 Claude Code가 응답할 내용을 스텁한다.
    let tokens = 36_100;
    on("session.start", ($, e) => ({ cwd: e.cwd }));
    on("session.usage", () => ({
      value: {
        startedAt: 0,
        rateLimits: [],
        context: { tokens, window: 200_000, percent: Math.round(tokens / 2_000) }
      },
    }));
    on("turn.complete", () => ({ text: "" }));

    await $.session.start({ surface: "terminal", isInteractive: true, cwd: "/work" } as any);
    const ui = await $.ui.mount({
      plugin: "token-weather",
      surface: "terminal",
      component: "AbovePrompt",
      props: { hasSurvey: false, isWorking: false, maxRows: 10, bodyColumns: 120 },
    } as any);

    expect(await ui.find({ type: "Text", text: /Clear/ })).toBeDefined();

    tokens = 134_400;
    await $.turn.complete({ reason: "answer", answer: "ok", durationMs: 1 } as any);

    expect(await ui.find({ type: "Text", text: /Showers/ })).toBeDefined();
    expect(await ui.find({ type: "Text", text: /67% of context/ })).toBeDefined();
    expect(await ui.find({ type: "Text", text: /▲ \+98\.3k last turn/ })).toBeDefined();

    await ui.unmount();
  });
});
```

```text
$ claude plugin test ./token-weather
(pass) token-weather > the band follows the context window
1 pass 0 fail
```

이 테스트는 3단계의 다시 그리기 동작도 확인한다. 모드가 다시 그리기를 명시적으로 요청하지 않아도 `turn.complete` 이후 밴드가 업데이트된다.

## 모드 활용 예시: 블래스트 레이디어스 및 리플레이 시어터

**토큰 웨더**는 단순히 관찰하고 그리는 모드이다. 다음 두 가지 모드는 이벤트에 개입하고, 창을 열며, 입력을 받는다.

### 블래스트 레이디어스 (Blast Radius)

**블래스트 레이디어스**는 `rm -rf`, `git reset --hard`, `git clean`, 강제 푸시, 데이터베이스 마이그레이션과 같이 위험할 수 있는 Bash 명령을 클로드가 호출할 때 해당 호출을 보류한다. 이 모드는 명령이 영향을 미칠 내용을 파악하고 **진행(Proceed)** 및 **취소(Cancel)** 버튼이 있는 창을 연다. `2`를 누르면 거부 이유와 함께 클로드에게 거부 응답이 전달된다. `1`을 누르면 명령이 원래대로 실행된다.

이 모드는 Bash에 대한 `tool.call`, `Pane` 및 `AbovePrompt`에 대한 `ui.render` 세 가지 훅을 사용한다. 핵심은 위 표에서 설명한 "응답" 동작이다.

```javascript
on("tool.call", { tool: "Bash" }, async ($, e, next) => {
  const risk = classify(String(e.command ?? ""));
  if (risk === null) return next(e); // 다른 모든 것은 정상적으로 실행

  const report = await measure($, risk, await $.session.cwd()); // git status, git clean -n, du, ...
  held = { command: e.command, risk, report, decision: null };

  const opened = await $.ui.open({ id: "blast-radius", title: "Blast Radius", focus: true });
  if (!opened.isPlaced) held.where = "band"; // 창이 너무 좁으면 프롬프트 위에 그린다.

  while (held.decision === null && !next.signal.aborted) {
    await $.process.run(["sleep", "0.25"]); // $ 호출 내 시간은 훅의 시간 제한에 포함되지 않는다.
  }

  if (held.decision === "proceed") return next(e); // 명령 실행
  return { deny: `Blast Radius held this command: the user pressed Cancel. It would have: ${report.summary}.` };
});
```

블래스트 레이디어스는 다음을 보여준다.

*   **`$.process.run`으로 드라이 런(dry run)**: 보고서는 도구 자체의 명령(`git status --porcelain`, `git clean -n`, `git log HEAD..origin/main`, `showmigrations`)에서 나온다. 인수는 `argv` 배열로 전달되므로, 경로 내의 어떤 것도 셸 코드로 실행되지 않는다.
*   **호출 보류**: 훅은 디스패치당 자체적으로 10초의 시간을 갖지만, `$` 호출 내에서 대기하는 시간은 이 제한에 포함되지 않는다. 루프는 버튼의 `onPress`가 결정을 설정할 때까지 짧은 `sleep` 프로세스에서 기다리며, `next.signal`이 중단되면(Esc를 누르면) 포기한다.
*   **단축키가 있는 버튼**: `Button({ label: "Proceed", hotkey: "1", onPress })`는 클릭, Tab+Enter, 또는 숫자 키로 작동한다.
*   **밴드로 기능 축소(Degrade to the band)**: 터미널은 충분히 넓을 때 트랜스크립트 옆에 창을 도킹한다. `$.ui.open`이 `isPlaced: false`를 반환하면, 동일한 보고서가 프롬프트 위에 그려진다.

이 모드는 안전망이지만 권한 시스템은 아니다. 명령 텍스트를 읽으므로, `$(...)`나 `rm`을 호출하는 별칭 및 스크립트는 이 모드를 우회할 수 있다. 하드 블록(hard block)을 위해서는 권한 규칙을 사용한다.

### 리플레이 시어터 (Replay Theater)

**리플레이 시어터**는 턴이 실행되는 동안 모든 Edit 및 Write 호출을 기록한다. 파일, 그리고 변경 전후의 텍스트를 기록한다. 턴이 끝나면 프롬프트 위에 힌트가 나타난다. `r`을 누르거나 `/replay`를 입력하면, 창이 열려 편집 내용을 하나의 diff 단위로 단계별로 보여주며, 번호가 매겨진 단계 스트립과 **이전(Prev)**, **다음(Next)**, **닫기(Close)** 버튼을 제공한다.

이 모드는 편집을 차단하거나 변경하지 않는다. 단순히 관찰한다.

```javascript
on("tool.call", async ($, e, next) => {
  if (EDIT_TOOLS.has(e.tool)) state.pending.push(...(await stepsFor($, e))); // 이전/새 텍스트 → diff
  return next(e); // 편집은 변경 없이 실행
});

on("turn.start", ($, e, next) => {
  if (!e.agentId) state.pending = [];
  return next(e);
});

on("turn.complete", async ($, e, next) => {
  const r = await next(e);
  if (!e.agentId && state.pending.length) state.replay = state.pending; // 턴당 하나의 리플레이
  return r;
});

on("session.start", async ($, e, next) => {
  const r = await next(e);
  await $.command.register({ name: "replay", description: "Step through the last turn's file edits" });
  return r;
});

on("command.run", { command: "replay" }, async ($, e) => ({ text: (await openReplay($)) ? "Replaying" : "No edits" }));
```

리플레이 시어터는 다음을 보여준다.

*   **이벤트 페어링**: `turn.start`와 `turn.complete`는 편집 내용을 턴당 하나의 리플레이로 묶는다. `e.agentId`는 서브 에이전트 턴이 이 그룹화에 포함되지 않도록 한다.
*   **슬래시 명령 등록**: `session.start`에서 `$.command.register`를 사용하고, `command.run`에서 이에 응답한다.
*   **파일 읽기**: Write 작업의 경우, `$.fs.read`는 쓰기가 완료되기 직전의 이전 내용을 가져오므로, 실제 diff를 생성할 수 있다.
*   **배치는 표면(surface)의 역할**: 전체 화면에서는 창이 오른쪽에 도킹된다. 80열에서는 프롬프트 위에 인라인으로 열린다. 모드는 어떤 방식이든 동일한 트리를 그린다.

## 모드 개발 시 핵심 습관

모드를 개발할 때 다음 네 가지 습관을 유지하는 것이 좋다.

*   **클로드 코드가 생성하는 타입을 활용한다.** 모드를 로드할 때마다 클로드 코드는 해당 빌드에 대한 선언 파일을 모드의 `.claude-plugin/types/` 폴더에 작성한다. 이를 통해 별도의 설정 없이 편집기와 `tsc -p`가 작동한다. 이 파일들은 모든 이벤트, `$`의 모든 메서드, 모든 요소의 props에 대한 참조 역할을 한다.
*   **`e.props`에서 props를 읽는다.** `hasSurvey`, `bodyColumns` 등은 `e` 자체가 아니라 `e.props`에 위치한다.
*   **뜨거운 리로드를 염두에 두고 계획한다.** 파일을 저장할 때마다 `register`와 `session.start`가 다시 실행되므로, 모듈 변수가 아닌 `$.state`에 데이터를 보관한다.
*   **그림이 표시되지 않을 때는 로그를 확인한다.** `claude --debug`를 실행하고 훅이 유효성 검사를 통과하지 못하는 트리를 반환했다는 줄을 찾아본다.

## 나만의 모드 공유 및 설치

모드는 클로드 코드 플러그인이므로 다른 플러그인과 동일한 방식으로 공유한다. 새로운 것을 배울 필요가 없다. **깃허브(GitHub)** 저장소에 마켓플레이스 파일을 포함하면 해당 저장소가 마켓플레이스가 된다. 누구나 여기서 설치할 수 있으며, 일반적인 푸시로 업데이트할 수 있다.

설치는 클로드 코드에서 세 가지 명령어로 가능하다.

```text
/plugin marketplace add your-org/my-mods
/plugin install token-weather@my-mods
/reload-plugins
```

리로드하면 모드가 시작된다. 나타나지 않으면 클로드 코드를 다시 시작한다.
모드는 게시자가 작성하며, **앤스로픽(Anthropic)**이 작성한 것이 아니다. 모드는 클로드 코드 내에서 사용자의 머신에서 실행되며, 클로드 코드와 동일한 접근 권한을 갖는다. 따라서 패키지를 설치하는 것과 동일한 방식으로 모드를 설치해야 한다. 즉, 저장소를 먼저 읽고 신뢰할 수 있는 사람의 모드만 설치한다. 명령을 실행하기 전까지는 아무것도 설치되지 않는다.
클로드 디렉토리는 모드를 포함하는 플러그인을 허용하므로, 자신의 모드를 `claude.ai/directory/manage`에 제출하여 사람들이 링크 없이도 찾을 수 있게 할 수 있다.

## 복잡계 이론 관점에서 본 모드

클로드 코드 모드는 **복잡계(Complex Systems)** 내에서 국소적인 **에이전트(Agent)**가 전체 시스템의 **행동 패턴(Behavioral Patterns)**에 어떻게 영향을 미치는지 보여주는 좋은 사례이다. 각 모드는 `observe`, `rewrite`, `answer`라는 세 가지 상호작용 방식을 통해 시스템의 이벤트 스트림에 개입한다. 이는 복잡계 이론에서 시스템의 구성 요소들이 주변 환경과 상호작용하며 **피드백 루프(Feedback Loops)**를 형성하고, 이 피드백이 시스템의 **창발적 특성(Emergent Properties)**을 변화시키는 과정과 유사하다. 작은 자바스크립트 파일 하나가 거대한 AI 개발 환경의 사용자 경험을 근본적으로 재구성하는 모습은, 하위 시스템의 미세한 변경이 전체 시스템의 동역학을 바꾸는 복잡계의 본질을 잘 드러낸다.

## 출처
- C:/Users/windo/AppData/Local/Temp/claude/C--Users-windo-Desktop-03-------Github-Desktop-tigerjk9-github-io/80b40e5e-a667-4048-9cdf-88b40e5e-a667-4048-9cdf-88b40e5e-a667-4048-9cdf-88b40e5e-a667-4048-9cdf-88b40e5e-a667-4048-9cdf-88b40e5e-a667-4048-9cdf-88b40e5e-a667-4048-9cdf-88b40e5fd/scratchpad/src2/claude-code-mods.md
