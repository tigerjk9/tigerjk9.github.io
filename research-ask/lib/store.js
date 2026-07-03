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
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  res.setHeader('Access-Control-Max-Age', '86400');
  if (req.method === 'OPTIONS') {
    res.status(204).end();
    return true; // preflight 종료
  }
  return false;
}

// ── Rate limit (인스턴스 로컬 — 완화용. 강한 보호가 필요하면 Upstash로 교체) ──
const hits = new Map(); // ip -> timestamps[]
let dayCount = 0;
let dayStamp = new Date().toDateString();

export function rateLimit(req, res, perMin = 8, perDayInstance = 800) {
  const today = new Date().toDateString();
  if (today !== dayStamp) { dayStamp = today; dayCount = 0; }
  if (dayCount >= perDayInstance) {
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
  dayCount++;
  return false;
}

// ── 데이터 로드 (모듈 스코프 캐시) ─────────────────────────────
let cache = null; // { loadedAt, posts: Map<id, post>, chunks: [{id, sec, vec}] }

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

export async function embedQuery(text) {
  if (!GEMINI_KEY) throw new Error('GEMINI_API_KEY 미설정');
  const r = await fetch(`${API_BASE}/${EMBED_MODEL}:embedContent?key=${GEMINI_KEY}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      content: { parts: [{ text: text.slice(0, 2000) }] },
      taskType: 'RETRIEVAL_QUERY',
      outputDimensionality: 768,
    }),
  });
  if (!r.ok) throw new Error(`embed API ${r.status}: ${(await r.text()).slice(0, 200)}`);
  const data = await r.json();
  // 768 truncate 벡터는 비정규 → 반드시 정규화
  return normalize(data.embedding.values);
}

export async function generate(prompt, maxTokens = 2000) {
  if (!GEMINI_KEY) throw new Error('GEMINI_API_KEY 미설정');
  const r = await fetch(`${API_BASE}/${GEN_MODEL}:generateContent?key=${GEMINI_KEY}`, {
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
  if (!r.ok) throw new Error(`generate API ${r.status}: ${(await r.text()).slice(0, 200)}`);
  const data = await r.json();
  const parts = data.candidates?.[0]?.content?.parts || [];
  return parts.map((p) => p.text || '').join('');
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
