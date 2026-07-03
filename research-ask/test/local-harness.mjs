// 로컬 E2E 하네스 — 블로그 URL fetch를 로컬 파일로 몽키패치하고 실제 Gemini로 핸들러 실행.
// 사용: node research-ask/test/local-harness.mjs "질문"        (ask 테스트)
//       node research-ask/test/local-harness.mjs --embed "쿼리"  (embed 테스트)
//       node research-ask/test/local-harness.mjs --health        (health 테스트)
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');

// .env에서 GEMINI_API_KEY 로드
try {
  const env = await readFile(path.join(ROOT, '.env'), 'utf-8');
  for (const line of env.split('\n')) {
    const m = line.match(/^\s*([A-Z_]+)\s*=\s*(.+?)\s*$/);
    if (m && !process.env[m[1]]) process.env[m[1]] = m[2].replace(/^["']|["']$/g, '');
  }
} catch { /* .env 없으면 환경변수 사용 */ }

// 블로그 정적 파일 fetch → 로컬 파일 서빙
const realFetch = globalThis.fetch;
globalThis.fetch = async (url, opts) => {
  const u = String(url);
  const m = u.match(/tigerjk9\.github\.io(\/assets\/[^?]+)/);
  if (m) {
    const body = await readFile(path.join(ROOT, m[1]), 'utf-8');
    return new Response(body, { status: 200, headers: { 'Content-Type': 'application/json' } });
  }
  return realFetch(url, opts);
};

// Vercel req/res 모의 — .env의 ASK_ACCESS_KEY를 자동 첨부 (--no-key로 미인증 시뮬레이션)
const useKey = !process.argv.includes('--no-key');
function mockReq(body, method = 'POST') {
  const headers = { origin: 'https://tigerjk9.github.io', 'x-forwarded-for': '127.0.0.1' };
  if (useKey && process.env.ASK_ACCESS_KEY) headers['x-ask-key'] = process.env.ASK_ACCESS_KEY;
  return { method, headers, body };
}
function mockRes() {
  const res = { _status: 0, _json: null, _headers: {} };
  res.setHeader = (k, v) => { res._headers[k] = v; };
  res.status = (c) => { res._status = c; return res; };
  res.json = (o) => { res._json = o; return res; };
  res.end = () => res;
  return res;
}

const args = process.argv.slice(2);
const mode = args[0] === '--embed' ? 'embed' : args[0] === '--health' ? 'health' : 'ask';
const q = (mode === 'ask' ? args[0] : args[1]) || 'AI 피드백이 학습에 효과가 있나?';

const t0 = Date.now();
if (mode === 'health') {
  const { default: handler } = await import('../api/health.js');
  const res = mockRes();
  await handler(mockReq(null, 'GET'), res);
  console.log('status:', res._status);
  console.log(JSON.stringify(res._json, null, 2));
} else if (mode === 'embed') {
  const { default: handler } = await import('../api/embed.js');
  const res = mockRes();
  await handler(mockReq({ q }), res);
  console.log('status:', res._status, '| dim:', res._json?.vec?.length,
    '| CORS:', res._headers['Access-Control-Allow-Origin']);
} else {
  const { default: handler } = await import('../api/ask.js');
  const res = mockRes();
  await handler(mockReq({ q }), res);
  console.log('status:', res._status, `(${((Date.now() - t0) / 1000).toFixed(1)}s)`);
  console.log('\n=== 답변 ===\n' + (res._json?.answer || JSON.stringify(res._json)));
  console.log('\n=== 근거 ===');
  for (const s of res._json?.sources || []) {
    console.log(`[${s.n}] sim=${s.sim} ${s.title} (${s.secs.join('·')})\n    ${s.url}`);
  }
}
