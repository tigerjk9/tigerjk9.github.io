// lib/store.js — 공용: 데이터 콜드스타트 로드, 코사인 검색, Gemini REST, CORS, 레이트리밋
// 의존성 제로. 블로그(GitHub Pages)가 데이터 원본이라 콘텐츠가 갱신돼도 이 서비스는 재배포 불필요.

const BLOG_ORIGIN = process.env.BLOG_ORIGIN || 'https://tigerjk9.github.io';
const GEMINI_KEY = process.env.GEMINI_API_KEY;
const GEN_MODEL = process.env.GEN_MODEL || 'gemini-2.5-flash';
const EMBED_MODEL = 'gemini-embedding-001';
const DATA_TTL_MS = 6 * 60 * 60 * 1000; // 6시간마다 인덱스 갱신

const DEFAULT_ORIGINS = [
  'https://tigerjk9.github.io',
  'http://localhost:4000',
  'http://127.0.0.1:4000',
];
const ALLOWED_ORIGINS = (process.env.ALLOWED_ORIGINS || '')
  .split(',').map((s) => s.trim()).filter(Boolean)
  .concat(DEFAULT_ORIGINS);

// ── CORS ──────────────────────────────────────────────────────
export function applyCors(req, res) {
  const origin = req.headers.origin || '';
  if (ALLOWED_ORIGINS.includes(origin)) {
    res.setHeader('Access-Control-Allow-Origin', origin);
    res.setHeader('Vary', 'Origin');
  }
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, X-Ask-Key, X-Gemini-Key');
  res.setHeader('Access-Control-Max-Age', '86400');
  if (req.method === 'OPTIONS') {
    res.status(204).end();
    return true; // preflight 종료
  }
  return false;
}

// ── 접근 키 (주인장 전용 운영) ────────────────────────────────
// ASK_ACCESS_KEY 미설정이면 공개 모드(하위 호환). 설정 시 embed/ask는 키 필수.
const ACCESS_KEY = process.env.ASK_ACCESS_KEY || '';

// ── BYOK (방문자 본인 Gemini API 키) ──────────────────────────
// X-Gemini-Key 헤더로 자기 키를 가져오면 접근 키 없이 이용 가능. 생성 비용은 방문자 키 부담.
// Google API 키 형식(AIza + 35자 내외)만 통과 — 형식이 다르면 없는 것으로 취급.
const GEMINI_KEY_RE = /^AIza[0-9A-Za-z_-]{30,80}$/;

export function userGeminiKey(req) {
  const k = String(req.headers['x-gemini-key'] || '').trim();
  return GEMINI_KEY_RE.test(k) ? k : '';
}

export function keyValid(req) {
  if (!ACCESS_KEY) return true; // 키 미설정 = 공개 모드
  if (userGeminiKey(req)) return true; // 본인 Gemini 키 지참 = 접근 키 불필요
  const given = String(req.headers['x-ask-key'] || '');
  if (given.length !== ACCESS_KEY.length) return false;
  let diff = 0;
  for (let i = 0; i < ACCESS_KEY.length; i++) diff |= given.charCodeAt(i) ^ ACCESS_KEY.charCodeAt(i);
  return diff === 0;
}

export function authRequired() {
  return Boolean(ACCESS_KEY);
}

export function requireKey(req, res) {
  if (keyValid(req)) return false;
  res.status(401).json({ error: 'unauthorized', message: '접근 키 또는 본인의 Gemini API 키가 필요하다. /ask/ 페이지에서 키를 입력해 달라.' });
  return true;
}

// ── Rate limit (인스턴스 로컬 — 완화용. 강한 보호가 필요하면 Upstash로 교체) ──
const hits = new Map(); // ip -> timestamps[]
let dayCount = 0;
let dayStamp = new Date().toDateString();

// skipDaily: BYOK 요청은 생성 비용이 방문자 키 부담이라 일일 총량(주인장 키 보호)에서 제외.
// 단 서버 자체 보호용 분당 IP 제한은 항상 적용.
export function rateLimit(req, res, perMin = 8, perDayInstance = 800, skipDaily = false) {
  const today = new Date().toDateString();
  if (today !== dayStamp) { dayStamp = today; dayCount = 0; }
  if (!skipDaily && dayCount >= perDayInstance) {
    res.status(429).json({ error: 'daily_quota', message: '오늘의 사용량이 모두 소진됐다. 내일 다시 시도해 달라.' });
    return true;
  }
  const ip = (req.headers['x-forwarded-for'] || '').split(',')[0].trim() || 'unknown';
  const now = Date.now();
  const arr = (hits.get(ip) || []).filter((t) => now - t < 60_000);
  if (arr.length >= perMin) {
    res.status(429).json({ error: 'rate_limited', message: '요청이 너무 잦다. 잠시 후 다시 시도해 달라.' });
    return true;
  }
  arr.push(now);
  hits.set(ip, arr);
  if (hits.size > 5000) hits.clear(); // 메모리 상한
  if (!skipDaily) dayCount++;
  return false;
}

// ── 데이터 로드 (모듈 스코프 캐시) ─────────────────────────────
let cache = null; // { loadedAt, posts: Map<id, post>, chunks: [{id, sec, vec}] }
let warming = null; // 진행 중인 loadData() — 콜드스타트 때 동시 요청이 중복 로드하지 않게 dedupe

function dequantize(b64, scale) {
  const bin = Buffer.from(b64, 'base64');
  const v = new Float32Array(bin.length);
  for (let i = 0; i < bin.length; i++) {
    const x = bin[i] > 127 ? bin[i] - 256 : bin[i];
    v[i] = x * scale;
  }
  return v;
}

export async function loadData() {
  if (cache && Date.now() - cache.loadedAt < DATA_TTL_MS) return cache;
  if (warming) return warming;
  warming = (async () => {
    const [dbRes, idxRes] = await Promise.all([
      fetch(`${BLOG_ORIGIN}/assets/research-db.json`),
      fetch(`${BLOG_ORIGIN}/assets/research-rag-index.json`),
    ]);
    if (!dbRes.ok || !idxRes.ok) {
      throw new Error(`데이터 로드 실패: db=${dbRes.status} idx=${idxRes.status}`);
    }
    const db = await dbRes.json();
    const idx = await idxRes.json();
    const posts = new Map();
    for (const p of db.posts) posts.set(p.id, p);
    const chunks = idx.chunks.map((c) => ({
      id: c.id, sec: c.sec, vec: dequantize(c.v, c.s),
    }));
    cache = { loadedAt: Date.now(), posts, chunks, dim: idx.dim };
    return cache;
  })();
  try {
    return await warming;
  } finally {
    warming = null;
  }
}

// health 프로브 전용 — RAG 청크(벡터 디코딩 포함)까지 기다리지 않고 포스트 수만 가볍게 반환한다.
// 캐시가 이미 따뜻하면 즉시 반환. 차가우면 research-db.json 하나만 받아 카운트를 내고,
// 무거운 전체 로드(loadData)는 백그라운드로 미룬다 — 프로브가 4초+ 걸려 프론트 타임아웃과
// 경합하는 바람에 AI 버튼이 안 뜨는 것처럼 보이던 문제의 원인이었다.
export async function getPostsCount() {
  if (cache && Date.now() - cache.loadedAt < DATA_TTL_MS) return cache.posts.size;
  loadData().catch(() => {}); // 백그라운드 워밍 — 이 응답은 기다리지 않는다
  try {
    const r = await fetch(`${BLOG_ORIGIN}/assets/research-db.json`);
    if (!r.ok) return null;
    const db = await r.json();
    return db.posts.length;
  } catch (e) {
    return null;
  }
}

// ── 벡터 연산 ─────────────────────────────────────────────────
export function cosine(a, b) {
  let dot = 0;
  for (let i = 0; i < a.length; i++) dot += a[i] * b[i];
  return dot; // 양쪽 모두 unit vector 전제
}

export function normalize(v) {
  let n = 0;
  for (const x of v) n += x * x;
  n = Math.sqrt(n) || 1;
  return v.map((x) => x / n);
}

// ── Gemini REST ───────────────────────────────────────────────
const API_BASE = 'https://generativelanguage.googleapis.com/v1beta/models';

// BYOK 오류 분류 — 방문자 키가 무효(400/401/403)거나 할당량 소진(429)이면
// 프론트가 키 재입력/안내를 하도록 마킹된 오류를 던진다. 오류 메시지에 키는 포함하지 않는다.
function geminiApiError(kind, status, bodyText, usingUserKey) {
  const err = new Error(`${kind} API ${status}: ${String(bodyText).slice(0, 200)}`);
  if (usingUserKey && (status === 400 || status === 401 || status === 403)) err.badUserKey = true;
  if (usingUserKey && status === 429) err.userQuota = true;
  return err;
}

export async function embedQuery(text, apiKey = '') {
  const key = apiKey || GEMINI_KEY;
  if (!key) throw new Error('GEMINI_API_KEY 미설정');
  const r = await fetch(`${API_BASE}/${EMBED_MODEL}:embedContent?key=${key}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      content: { parts: [{ text: text.slice(0, 2000) }] },
      taskType: 'RETRIEVAL_QUERY',
      outputDimensionality: 768,
    }),
  });
  if (!r.ok) throw geminiApiError('embed', r.status, await r.text(), Boolean(apiKey));
  const data = await r.json();
  // 768 truncate 벡터는 비정규 → 반드시 정규화
  return normalize(data.embedding.values);
}

export async function generate(prompt, maxTokens = 2000, apiKey = '') {
  const key = apiKey || GEMINI_KEY;
  if (!key) throw new Error('GEMINI_API_KEY 미설정');
  const r = await fetch(`${API_BASE}/${GEN_MODEL}:generateContent?key=${key}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      contents: [{ role: 'user', parts: [{ text: prompt }] }],
      generationConfig: {
        temperature: 0.3,
        maxOutputTokens: maxTokens,
        // 2.5-flash는 thinking 토큰이 maxOutputTokens를 소진해 답변이 잘림 → thinking 비활성
        thinkingConfig: { thinkingBudget: 0 },
      },
    }),
  });
  if (!r.ok) throw geminiApiError('generate', r.status, await r.text(), Boolean(apiKey));
  const data = await r.json();
  const parts = data.candidates?.[0]?.content?.parts || [];
  return parts.map((p) => p.text || '').join('');
}

// 핸들러 공용 — BYOK 오류를 HTTP 응답으로 변환. 처리했으면 true.
export function handleByokError(e, res) {
  if (e && e.badUserKey) {
    res.status(401).json({ error: 'bad_gemini_key', message: '입력한 Gemini API 키가 유효하지 않다. 키를 다시 확인해 달라.' });
    return true;
  }
  if (e && e.userQuota) {
    res.status(429).json({ error: 'gemini_quota', message: '입력한 키의 무료 할당량이 소진된 것으로 보인다. 잠시 후 다시 시도해 달라.' });
    return true;
  }
  return false;
}

// ── 검색: 쿼리 벡터 → top 청크 → 포스트 단위 근거 목록 ─────────
export function retrieve(queryVec, data, { topChunks = 24, maxPerPost = 2, maxSources = 5 } = {}) {
  const scored = data.chunks
    .map((c) => ({ c, sim: cosine(queryVec, c.vec) }))
    .sort((a, b) => b.sim - a.sim)
    .slice(0, topChunks);
  const perPost = new Map(); // id -> [{sec, sim}]
  for (const { c, sim } of scored) {
    const arr = perPost.get(c.id) || [];
    if (arr.length < maxPerPost) { arr.push({ sec: c.sec, sim }); perPost.set(c.id, arr); }
  }
  const ranked = [...perPost.entries()]
    .map(([id, secs]) => ({ id, secs, best: Math.max(...secs.map((s) => s.sim)) }))
    .sort((a, b) => b.best - a.best)
    .slice(0, maxSources);
  return ranked.map(({ id, secs, best }) => {
    const post = data.posts.get(id);
    return post ? { post, secs, sim: best } : null;
  }).filter(Boolean);
}
