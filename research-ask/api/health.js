// GET /api/health — 클라이언트가 AI 기능 노출 여부를 판단하는 프로브
import { applyCors, loadData } from '../lib/store.js';

export default async function handler(req, res) {
  if (applyCors(req, res)) return;
  try {
    const data = await loadData();
    res.status(200).json({
      ok: true,
      posts: data.posts.size,
      chunks: data.chunks.length,
      hasKey: Boolean(process.env.GEMINI_API_KEY),
    });
  } catch (e) {
    res.status(503).json({ ok: false, error: String(e.message || e) });
  }
}
