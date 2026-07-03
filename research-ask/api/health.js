// GET /api/health — 클라이언트가 AI 기능 노출 여부를 판단하는 프로브
// authorized: X-Ask-Key 헤더가 유효한지 (주인장 전용 모드에서 UI 노출 게이트)
import { applyCors, loadData, keyValid, authRequired } from '../lib/store.js';

export default async function handler(req, res) {
  if (applyCors(req, res)) return;
  try {
    const data = await loadData();
    res.status(200).json({
      ok: true,
      posts: data.posts.size,
      chunks: data.chunks.length,
      hasKey: Boolean(process.env.GEMINI_API_KEY),
      authRequired: authRequired(),
      authorized: keyValid(req),
    });
  } catch (e) {
    res.status(503).json({ ok: false, error: String(e.message || e) });
  }
}
