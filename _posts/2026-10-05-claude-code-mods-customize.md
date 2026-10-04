---
title: "클로드 코드 mod 시작하기, 세션 안에서 도는 나만의 확장 만들기"
date: 2026-10-05 01:14:55 +0900
categories: [AI, 소프트웨어개발]
tags: [ClaudeCode, 클로드, 개발자도구, 자동화, 생산성, LLM]
header:
  teaser: /assets/claude-code-mods-customize-og.jpg
permalink: /post/claude-code-mods-customize/
---
클로드 코드(Claude Code)의 mod는 세션 안에서 실행되는 작은 자바스크립트(JavaScript)나 타입스크립트(TypeScript) 파일이다. 세션에서 일어나는 일을 지켜보고, 클로드 코드가 하는 일을 바꾸고, 터미널이나 데스크톱 앱에 자체 UI를 그린다. 여기서 mod는 게임의 mod처럼 사용자가 덧붙이는 개조물을 가리키며, 작동 모드(mode)와는 다른 말이다.

API를 따로 배우지 않아도 써 볼 수 있다. `claude`를 실행한 뒤 원하는 mod를 설명하고, 핫 리로드(hot reload)를 허용할지 물을 때 허용하면 그 턴이 끝날 때 mod가 나타난다. 이 글은 claude.dev 블로그의 입문 가이드를 따라 빈 폴더에서 Token Weather라는 mod(약 80줄)를 만들고, 더 큰 mod 두 개인 Blast Radius와 Replay Theater를 살펴본다.

<figure>
<img src="/assets/claude-code-mods-customize-og.jpg" alt="claude.dev 블로그 튜토리얼 표지, Getting started with Claude Code mods">
<figcaption>claude.dev 블로그 튜토리얼 「Getting started with Claude Code mods」의 표지 이미지.</figcaption>
</figure>

## mod란 무엇인가

클로드 코드는 이미 설정, 권한 규칙, 슬래시 명령, 스킬, 상태 표시줄로 동작을 꽤 많이 바꿀 수 있다. mod는 여기서 더 들어가 클로드 코드가 하는 일을 다시 쓰거나 대체하고, 맞춤 UI를 그린다. 내부적으로 mod는 플러그인에 담겨 배포되는 훅(hook)이며, 각 훅은 세션에서 일어나는 모든 이벤트를 발생하는 즉시 본다.

그래서 mod는 클로드 코드를 자기 작업 방식에 맞추는 수단이 된다. 늘 확인하는 수치를 띄워 두거나, 불안한 명령 앞에 확인 장치를 두거나, 변경 사항을 원하는 방식으로 읽는 검토 화면을 만들 수 있다.

mod는 클로드 코드 2.1.287 이상에서 기본으로 켜져 있어 따로 활성화할 것이 없다. API는 릴리스마다 바뀔 수 있다. 클로드 코드는 mod를 불러올 때마다 현재 빌드에 맞는 타입 선언을 mod의 `.claude-plugin/types/` 폴더에 써 두며, 자기 버전에서는 이 선언이 기준이다.

## mod의 작동 원리

mod는 동작 로직을 자바스크립트나 타입스크립트 모듈에 담은 클로드 코드 플러그인이다.

- 폴더는 일반 플러그인과 같아서 `.claude-plugin/plugin.json` 매니페스트를 둔다.
- `hooks/hooks.json`은 `modules` 아래에 모듈 하나를 지정한다.
- 모듈은 `register(on, options)`를 내보내고, 그 안에서 `on(event, matcher?, hook)`으로 훅을 추가한다.

모든 훅은 모양이 같다.

```javascript
on("tool.call", { tool: "Bash" }, async ($, e, next) => {
  // $    mod API: ui, session, state, store, fs, process, clock, http, tool, command, model, ...
  // e    이 이벤트의 입력(일반 데이터)
  // next e를 다른 플러그인으로, 마지막에는 클로드 코드 자체 동작으로 넘긴다
  return next(e);
});
```

훅은 미들웨어처럼 체인을 이룬다. 내 훅이 실행되고 `next(e)`가 이벤트를 다음 플러그인에 넘기며, 체인 맨 아래에서 클로드 코드가 원래 하려던 일을 한다. 훅이 할 수 있는 일은 세 가지다.

| 동작 | 방법 | 예시 |
| :--- | :--- | :--- |
| 관찰(Observe) | `const r = await next(e); /* look */ return r` | 모든 파일 편집 기록. 턴이 끝날 때마다 측정. |
| 재작성(Rewrite) | `return next({ ...e, command: safer })` | 체인 뒤쪽이 보는 이벤트를 바꾼다. |
| 응답(Answer) | `next`를 부르지 않고 `return { deny: "…" }` | 도구 호출 거부. 명령이나 도구를 직접 처리. |

이벤트는 도구 호출, 제출된 프롬프트, 턴의 시작과 끝, 세션의 시작과 끝, 슬래시 명령, 그리고 인터페이스의 각 부분이 그려질 때마다 발생하는 `ui.render`를 다룬다. 모듈은 DOM도 Node도 없는 자체 샌드박스에서 돌기 때문에 바깥과 주고받는 일은 모두 `$`를 거친다.

설정 훅(settings hooks)과는 다르다. 설정 훅은 이벤트마다 셸 명령을 실행하고 표준 입출력(stdin/stdout)으로 JSON을 주고받는다. mod는 한 번 불러오면 세션에 머문다. 상태를 기억하고, 이벤트에 따라 갱신되는 UI를 그리고, 클로드 코드를 다시 호출해 창(pane)을 열거나 프로세스를 실행하거나 슬래시 명령이나 모델이 부를 수 있는 도구를 등록한다.

클로드 코드도 자기 기능 일부를 mod로 만든다. AGENTS.md 지원과 대화 옆에 뜨는 `/diff` 창이 그렇다. 테스트를 포함한 소스가 공개 저장소 [anthropics/claude-code](https://github.com/anthropics/claude-code)의 `mods/` 아래에 있어서 팀이 mod를 어떻게 만드는지 읽어 볼 수 있다.

## 첫 mod 만들기, Token Weather

Token Weather는 턴이 끝날 때마다 컨텍스트 창이 얼마나 찼는지 읽어 프롬프트 위에 한 줄로 그린다. 날씨 아이콘, 사용률, 창 전체 대비 사용한 토큰 수, 최근 턴의 작은 막대 차트, 마지막 턴에서 늘어난 양이 그 한 줄에 들어간다.

| 사용량 | 예보 |
| :--- | :--- |
| 25% 미만 | ☀ Clear (맑음) |
| 25–49% | ☁ Cloudy (흐림) |
| 50–74% | ☂ Showers (소나기) |
| 75–89% | ☇ Storm (폭풍) |
| 90% 이상 | ↯ Compact soon (곧 압축) |

가이드의 시연에서는 턴마다 파일을 더 읽으면서 200k 창의 18%(Clear), 67%(Showers), 81%(Storm)로 밴드가 바뀐다.

<figure>
<img src="/assets/claude-code-mods-customize-band.png" alt="Token Weather 밴드가 Storm, 컨텍스트 81%, 161.1k / 200k를 표시한 터미널 한 줄">
<figcaption>Token Weather 밴드. 200k 창에서 161.1k(81%)를 써서 Storm으로 표시되고, 최근 턴 차트와 마지막 턴 증가량(+26.7k)이 함께 나온다. 출처 claude.dev 블로그.</figcaption>
</figure>

### 지름길, 클로드에게 만들게 하기

뒤에 나올 여섯 단계는 건너뛸 수 있다. 클로드 코드는 mod 작성법을 알고 있어서 원하는 mod를 설명하면 알아서 만든다. `claude`로 세션을 열고 아래 프롬프트를 붙여 넣는다.

```text
Make me a Claude Code mod called token-weather: a live forecast of my context window, shown in the band above the prompt.

What it should show, on one line:
- A weather icon and word for how full the context window is: under 25% ☀ Clear (yellow), 25–49% ☁ Cloudy (cyan), 50–74% ☂ Showers (blue), 75–89% ☇ Storm (magenta), 90% and up ↯ Compact soon (red).
- The percentage used, then the tokens used out of the window, like "134.4k / 200k".
- A small chart of the last 12 turns, drawn with ▁▂▃▄▅▆▇█.
- How much the last turn added, like "▲ +98.3k last turn".

It should update after every turn.
```

클로드는 이 세션에서 핫 리로드를 켤지 한 번 묻는다. 허용하면 클로드의 턴이 끝날 때 프롬프트 위에 밴드가 나타난다. 그다음부터는 변경 사항이 그 자리에서 다시 불러와지므로 "Storm을 70%부터 시작해 줘", "끝에 달러 비용을 붙여 줘" 같은 수정을 계속 요청하며 밴드가 바뀌는 모습을 볼 수 있다. 이렇게 만든 mod는 이 세션에서만 불러오고 폴더는 나중에 정리된다. 계속 쓰려면 폴더를 복사해 두고 일반 플러그인처럼 설치한다(6단계).

프롬프트는 무엇을 보고 싶은지만 설명한다. API를 몰라도 mod를 쓸 수 있다는 뜻이다. 어떻게 만드는지는 클로드 코드에 내장된 mod 작성 가이드가 맡는다. 리로드 뒤에도 남도록 상태를 어디에 둘지, `claude plugin validate`로 플러그인을 어떻게 검사할지, 어떤 이벤트에 훅을 걸지가 거기 들어 있다. "What it should show" 아래 줄만 바꾸면 자기만의 mod가 된다.

### 단계별로 만들기

구조를 먼저 이해하고 싶거나 클로드가 쓴 코드를 확인하고 싶다면 아래 단계를 따라간다.

#### 1단계. 폴더 만들기

클로드 코드 버전부터 확인한다.

```shell
claude --version   # 2.1.287 이상
```

다음 구조를 만든다.

```
token-weather/
├── .claude-plugin/
│   ├── plugin.json
│   └── types/ (클로드 코드가 mod를 불러올 때 작성)
├── hooks/
│   ├── hooks.json
│   └── token-weather.mjs
├── types/
│   └── index.d.ts (3단계에서 추가)
└── tests/
    └── token-weather.test.ts (5단계에서 추가)
```

`.claude-plugin/plugin.json`은 표준 플러그인 매니페스트다.

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

`hooks/hooks.json`은 모듈을 가리킨다. mod 하나에는 모듈이 정확히 하나 있다.

```json
{
  "modules": ["./token-weather.mjs"]
}
```

#### 2단계. 무언가 그려 보기

프롬프트 바로 위 띠 영역은 `AbovePrompt`라는 컴포넌트다. 클로드 코드는 이 자리에 아무것도 그리지 않으므로 첫 대상으로 알맞다. 이 컴포넌트의 `ui.render` 이벤트에 훅을 걸고 요소 트리를 반환한다.

```javascript
// hooks/token-weather.mjs
export function register(on) {
  on("ui.render", { component: "AbovePrompt" }, ($, e, next) => {
    const { Box, Text } = $.ui.resolve(e);
    return Box({
      paddingX: 1,
      children: [
        Text({ color: "yellow", bold: true, children: "☀  Clear skies" })
      ],
    });
  });
}
```

요소는 전역 변수가 아니다. 클로드 코드가 그리는 표면(surface)마다 지원하는 요소가 조금씩 달라서, `$.ui.resolve(e)`가 지금 그리는 표면에 맞는 생성자를 돌려준다. `h`를 팩토리로 쓰면 JSX도 된다.

플러그인을 불러온 상태로 세션을 연다.

```shell
claude --plugin-dir ./token-weather
```

프롬프트 위에 "☀ Clear skies"가 나타난다. 세션은 열어 둔다. 폴더를 감시하므로 저장할 때마다 재시작 없이 모듈이 그 자리에서 다시 불러와진다. mod를 만드는 재미의 대부분이 이 빠른 피드백에서 나온다.

구조를 익힌 뒤에는 다음 mod를 지름길처럼 클로드에게 설명해도 된다. 클로드는 같은 세션에서 핫 리로드되는 폴더에 플러그인을 써 준다.

#### 3단계. 실제 수치를 읽어 `$.state`에 보관하기

`$.session.usage()`는 상태 표시줄과 같은 수치를 돌려준다. `context.tokens`는 마지막 응답이 처리한 입력 토큰, `context.window`는 모델의 컨텍스트 창 크기, `context.percent`는 `tokens`를 `window`로 나눈 비율이다. 이 호출에는 비용이 들지 않는다. `breakdown`을 요청할 때만 토큰 계산 요청을 보낸다.

세션이 시작할 때와 턴이 끝날 때마다 값을 읽는다.

```javascript
on("session.start", async ($, e, next) => {
  const result = await next(e);
  await takeReading($);
  return result;
});

on("turn.complete", async ($, e, next) => {
  const result = await next(e);
  if (!e.agentId) { // 서브에이전트 턴은 빼고 메인 루프 턴만
    await takeReading($);
  }
  return result;
});
```

두 훅 모두 `next(e)`를 먼저 부르고 나서 관찰한다. 어느 쪽도 동작을 바꾸지 않는다.

읽은 값을 어디에 둘지가 관건이다. 모듈 수준의 `let readings = []`가 당연해 보이지만, 핫 리로드는 모듈을 새로 불러오는 일이라 `register`가 다시 실행되고 `session.start`가 다시 발생하며 모듈 변수가 초기화된다. 그래서 기록은 `$.state`에 둔다. `$.state`는 세션 내내 호스트 쪽에 이름 붙은 값을 보관하고, 이 값은 리로드 뒤에도 남는다.

```javascript
// 호스트가 보관하므로 이 파일을 핫 리로드해도 기록이 남는다.
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

상태 값은 플러그인의 타입 계약(type contract)에 선언한다. 매니페스트가 가리키는 작은 `.d.ts` 파일이다. `types/index.d.ts`를 추가한다.

```typescript
export type TokenWeatherReading = { tokens: number; window: number; percent: number };
declare module "claude-code" {
  interface PluginState {
    "token-weather": { readings: TokenWeatherReading[] };
  }
}
```

그리고 `plugin.json`에 `"types": "./types/index.d.ts"`를 넣는다. 이 단계를 빠뜨리면 `claude plugin validate`가 고칠 방법까지 적힌 오류를 내고 멈춘다. 오류 문구는 `token-weather.readings is not declared: the manifest's types contract must name it in interface PluginState { … }`이다.

대신 다시 그리기는 공짜로 얻는다. 렌더 훅이 실행되는 동안 부른 `$.state.get`은 그 그림을 구독하므로, 이후 `$.state.set`이 일어날 때마다 밴드가 다시 그려진다. `$.ui.invalidate`를 직접 부를 일이 없다.

#### 4단계. 예보 그리기

모듈 전체는 다음과 같다.

```javascript
// Token Weather: 프롬프트 위에 그리는 컨텍스트 창 실시간 예보
const HISTORY = 12;
const BARS = "▁▂▃▄▅▆▇█";
const FORECAST = [
  { upTo: 25, icon: "☀", word: "Clear", color: "yellow" },
  { upTo: 50, icon: "☁", word: "Cloudy", color: "cyan" },
  { upTo: 75, icon: "☂", word: "Showers", color: "blue" },
  { upTo: 90, icon: "☇", word: "Storm", color: "magenta" },
  { upTo: Infinity, icon: "↯", word: "Compact soon", color: "red" },
];

// 호스트가 보관하므로 이 파일을 핫 리로드해도 기록이 남는다.
const readings = { plugin: "token-weather", key: "readings" };

export function register(on) {
  on("session.start", async ($, e, next) => {
    const result = await next(e);
    await takeReading($);
    return result;
  });

  on("turn.complete", async ($, e, next) => {
    const result = await next(e);
    if (!e.agentId) { // 서브에이전트 턴은 빼고 메인 루프 턴만
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

여기서 자기 mod에 옮겨 쓸 만한 세부 사항이 세 가지 있다.

- 컴포넌트의 props는 `e.props`에 있다. `hasSurvey`는 설문이 이 밴드 자리를 원한다는 뜻이라 훅은 `next(e)`로 자리를 양보한다. `bodyColumns`는 밴드의 실제 너비로, 대화 기록 옆에 창이 붙어 있으면 터미널 너비보다 좁다. 트리 크기를 여기에 맞춘다. `e`의 최상위에 있는 값은 `e.component`, `e.surface`, `e.requestId`, `e.viewport`뿐이다.
- 그릴 것이 없으면 통과시킨다. `next(e)`를 반환하면 밴드가 클로드 코드와 다른 mod에 돌아간다.
- 이모지 대신 한 칸 너비 기호를 쓴다. ☀ ☁ ☂ ☇ ↯는 어느 터미널 글꼴에서나 줄이 맞는다.

파일을 저장하면 실행 중인 세션이 바로 반영한다. 큰 파일을 읽는 턴이 몇 번 지나면 밴드가 Clear에서 Showers, Storm으로 바뀐다.

#### 5단계. 검사와 테스트

`claude plugin validate`는 매니페스트와 모듈 소스를 클로드 코드와 같은 방식으로 읽고, 모듈이 어떤 훅을 걸고 무엇을 호출하는지 보고한다.

```text
$ claude plugin validate ./token-weather
> types ./types/index.d.ts declares state: token-weather.readings
> ./token-weather.mjs hooks: session.start, turn.complete, ui.render{component=AbovePrompt}
> ./token-weather.mjs calls: $.session.usage (via takeReading), $.state.get, $.state.set (via takeReading), $.ui.resolve
> ./token-weather.mjs state writes: token-weather.readings
> ./token-weather.mjs state reads: token-weather.readings
√ Validation passed
```

`claude plugin test`는 플러그인의 `*.test.ts` 파일을 실제 클로드 코드 런타임에서 실행한다. 테스트가 `on`으로 등록한 훅은 체인에서 mod보다 뒤에 실행되며 클로드 코드가 내놓을 응답을 대신한다(stub). 그래서 `$.session.usage()`가 무엇을 반환할지 정확히 정할 수 있다.

```typescript
// tests/token-weather.test.ts
import { describe, expect, test } from "claude-code/testing";

describe("token-weather", () => {
  test("the band follows the context window", async ($, on) => {
    // 여기서 등록한 훅은 mod 다음에 실행되며 클로드 코드의 응답을 대신한다.
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
 1 pass
 0 fail
```

이 테스트는 3단계의 다시 그리기 동작도 확인한다. mod가 다시 그려 달라고 요청하지 않아도 `turn.complete` 뒤에 밴드가 갱신된다.

#### 6단계. 공유하기

mod도 플러그인이므로 배포 방식이 같다. 마켓플레이스에 넣으면 되는데, 가장 단순한 마켓플레이스는 `.claude-plugin/marketplace.json`이 든 폴더 하나다.

```json
{
  "name": "my-mods",
  "owner": { "name": "You" },
  "plugins": [{ "name": "token-weather", "source": "./token-weather" }]
}
```

```shell
claude plugin marketplace add ./my-mods
claude plugin install token-weather@my-mods --scope user
```

## mod 공유와 설치

mod는 클로드 코드 플러그인이라 다른 플러그인과 똑같이 공유하며, 새로 배울 것이 없다. mod를 마켓플레이스 파일과 함께 GitHub 저장소에 올리면 그 저장소가 마켓플레이스가 된다. 누구나 거기서 설치할 수 있고, 평소처럼 푸시하면 업데이트된다.

설치는 클로드 코드 안에서 명령 세 개로 끝난다.

```text
/plugin marketplace add your-org/my-mods
/plugin install token-weather@my-mods
/reload-plugins
```

리로드하면 mod가 시작된다. 나타나지 않으면 클로드 코드를 다시 시작한다.

mod는 클로드 코드와 같은 권한으로 내 컴퓨터에서 실행되는 코드이고, Anthropic이 아니라 게시자가 쓴 것이다. 그러니 패키지를 설치할 때처럼 저장소를 먼저 읽어 보고 믿을 수 있는 사람의 mod만 설치한다. 명령을 실행하기 전에는 아무것도 설치되지 않는다.

Claude 디렉터리는 mod가 든 플러그인도 받는다. [claude.ai/directory/manage](https://claude.ai/directory/manage)에 제출하면 링크를 따로 건네지 않아도 사람들이 찾아 쓸 수 있다.

## mod 두 개 더, Blast Radius와 Replay Theater

Token Weather는 지켜보고 그리기만 한다. 다음 두 mod는 이벤트에 끼어들고, 창을 열고, 입력을 받는다.

### Blast Radius, 위험한 명령이 바꿀 것을 실행 전에 보기

클로드가 `rm -rf`, `git reset --hard`, `git clean`, 강제 푸시, 데이터베이스 마이그레이션 같은 Bash 명령을 호출하면 Blast Radius가 그 호출을 붙잡는다. 명령이 무엇을 건드릴지 계산한 뒤 Proceed와 Cancel 버튼이 있는 창을 연다. `2`를 누르면 클로드는 이유가 담긴 거부 응답을 받고, `1`을 누르면 명령이 쓰인 그대로 실행된다. 가이드의 시연에서는 `rm -rf build`를 붙잡아 지워질 파일 9개(1.1MB)를 보여 주고, Cancel로 한 번 거부한 뒤 두 번째 시도에서 Proceed로 실행한다.

훅은 세 개를 쓴다. Bash에 거는 `tool.call`, 그리고 `Pane`과 `AbovePrompt`에 거는 `ui.render`다. 핵심은 앞의 표에서 본 응답(Answer) 동작이다.

```javascript
on("tool.call", { tool: "Bash" }, async ($, e, next) => {
  const risk = classify(String(e.command ?? ""));
  if (risk === null) return next(e); // 나머지는 평소대로 실행

  const report = await measure($, risk, await $.session.cwd()); // git status, git clean -n, du, ...
  held = { command: e.command, risk, report, decision: null };

  const opened = await $.ui.open({ id: "blast-radius", title: "Blast Radius", focus: true });
  if (!opened.isPlaced) held.where = "band"; // 창을 붙이기엔 좁으면 프롬프트 위에 그린다

  while (held.decision === null && !next.signal.aborted) {
    await $.process.run(["sleep", "0.25"]); // $ 호출 안에서 보낸 시간은 훅 시간 제한에 들어가지 않는다
  }

  if (held.decision === "proceed") return next(e); // 실행 허용
  return { deny: `Blast Radius held this command: the user pressed Cancel. It would have: ${report.summary}.` };
});
```

이 mod에서 배울 점은 다음과 같다.

- `$.process.run`으로 미리 돌려 보기(dry run). 보고서는 각 도구의 명령(`git status --porcelain`, `git clean -n`, `git log HEAD..origin/main`, `showmigrations`)에서 나온다. 인수를 argv 배열로 넘기므로 경로에 든 문자열이 셸 코드로 실행되지 않는다.
- 호출 붙잡아 두기. 훅에는 디스패치마다 10초가 주어지지만 `$` 호출 안에서 기다리는 시간은 여기에 포함되지 않는다. 루프는 버튼의 `onPress`가 결정을 정할 때까지 짧은 `sleep` 프로세스로 기다리고, `next.signal`이 중단되면(Esc를 누르면) 포기한다.
- 단축키가 붙은 버튼. `Button({ label: "Proceed", hotkey: "1", onPress })`는 클릭, Tab과 Enter, 숫자 키로 모두 작동한다.
- 공간이 좁으면 밴드로 물러나기. 터미널이 충분히 넓으면 대화 기록 옆에 창을 붙인다. `$.ui.open`이 `isPlaced: false`를 돌려주면 같은 보고서를 프롬프트 위 밴드에 그린다.

Blast Radius는 안전망이지 권한 시스템이 아니다. 명령 텍스트를 읽는 방식이라 `$(…)`, 별칭, `rm`을 부르는 스크립트는 빠져나간다. 확실히 막아야 한다면 권한 규칙을 쓴다.

### Replay Theater, 마지막 턴의 편집을 한 단계씩 다시 보기

턴이 도는 동안 Replay Theater는 모든 Edit와 Write 호출을 기록한다. 대상 파일과 바뀌기 전후의 텍스트가 남는다. 턴이 끝나면 프롬프트 위에 안내가 뜨고, `r`을 누르거나 `/replay`를 입력하면 창이 열려 편집을 diff 하나씩 넘겨 보여 준다. 번호가 매겨진 단계 띠와 Prev, Next, Close 버튼이 함께 나온다. 가이드의 시연은 파일 3개에 걸쳐 이름을 바꾼 편집 5건을 1단계부터 5단계까지 넘겨 본다.

이 mod는 편집을 막거나 바꾸지 않고 지켜보기만 한다.

```javascript
on("tool.call", async ($, e, next) => {
  if (EDIT_TOOLS.has(e.tool)) state.pending.push(...(await stepsFor($, e))); // 이전/새 텍스트 → diff
  return next(e); // 편집은 손대지 않고 실행
});

on("turn.start", ($, e, next) => {
  if (!e.agentId) state.pending = [];
  return next(e);
});

on("turn.complete", async ($, e, next) => {
  const r = await next(e);
  if (!e.agentId && state.pending.length) state.replay = state.pending; // 턴마다 리플레이 하나
  return r;
});

on("session.start", async ($, e, next) => {
  const r = await next(e);
  await $.command.register({ name: "replay", description: "Step through the last turn's file edits" });
  return r;
});

on("command.run", { command: "replay" }, async ($, e) => ({ text: (await openReplay($)) ? "Replaying" : "No edits" }));
```

배울 점은 다음과 같다.

- 이벤트 짝짓기. `turn.start`와 `turn.complete`가 편집을 감싸 턴마다 리플레이 하나로 묶고, `e.agentId`로 서브에이전트 턴을 이 묶음에서 뺀다.
- 슬래시 명령 등록. `session.start`에서 `$.command.register`로 등록하고 `command.run`에서 응답한다.
- 파일 읽기. Write의 경우 `$.fs.read`가 쓰기 직전의 이전 내용을 가져오므로 실제 diff가 나온다.
- 배치는 표면이 정한다. 전체 화면에서는 창이 오른쪽에 붙고, 80열에서는 프롬프트 위에 인라인으로 열린다. mod는 어느 쪽이든 같은 트리를 그린다.

## mod를 만들 때 지킬 습관 네 가지

- 클로드 코드가 써 주는 타입에 기댄다. mod를 불러올 때마다 클로드 코드는 현재 빌드의 선언 파일을 `.claude-plugin/types/` 폴더에 쓰므로 편집기와 `tsc -p`가 추가 설정 없이 작동한다. 모든 이벤트, `$`의 모든 메서드, 모든 요소의 props를 여기서 확인한다.
- props는 `e.props`에서 읽는다. `hasSurvey`, `bodyColumns` 등은 `e` 자체가 아니라 여기에 있다.
- 핫 리로드를 전제로 짠다. 저장할 때마다 `register`와 `session.start`가 다시 실행되니 데이터는 모듈 변수가 아니라 `$.state`에 둔다.
- 그림이 안 보이면 로그를 읽는다. `claude --debug`로 실행하고, 훅이 검증을 통과하지 못하는 트리를 반환했다는 줄을 찾는다.

## 어떤 mod를 만들까

이 글의 세 mod는 각각 질문 하나에서 나왔다. 컨텍스트가 얼마나 찼나, 이 명령이 무엇을 지우려 하나, 클로드가 방금 무엇을 바꿨나. 질문은 사람마다 다르고, 가이드는 출발점으로 다음 아이디어를 든다.

- `$.session.usage()`로 비용이나 사용량 한도(rate limit)를 읽어 `$.ui.status`로 상태 표시줄에 띄우는 미터
- 모든 프롬프트에 팀 규칙을 덧붙이는 `prompt.submit` 훅
- 이번 세션에서 클로드가 읽은 파일을 나열해 무엇을 봤는지 보여 주는 창
- 긴 턴이 끝나면 `$.ui.toast`로 알림을 띄우는 집중 타이머
- 운영 환경 kubectl 컨텍스트나 `terraform apply`처럼 자기 기술 스택에 맞춘 `tool.call` 가드

## 출처
- Getting started with Claude Code mods, claude.dev 블로그(2026-10-01). https://claude.dev/blog/getting-started-with-claude-code-mods/
