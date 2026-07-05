// GET /api/health — 클라이언트가 AI 기능 노출 여부를 판단하는 프로브
// authorized: X-Ask-Key 헤더가 유효한지 (주인장 전용 모드에서 UI 노출 게이트)
// posts 카운트는 getPostsCount()로 가볍게 얻는다 — RAG 청크(loadData 전체)까지 기다리면
// 콜드스타트 때 4초+ 걸려 프론트 타임아웃과 경합해 AI 버튼이 안 뜨는 문제가 있었다.
import { applyCors, getPostsCount, keyValid, authRequired } from '../lib/store.js';

export default async function handler(req, res) {
  if (applyCors(req, res)) return;
  try {
    const posts = await getPostsCount();
    res.status(200).json({
      ok: true,
      posts,
      hasKey: Boolean(process.env.GEMINI_API_KEY),
      authRequired: authRequired(),
      authorized: keyValid(req),
      byok: true, // 방문자 본인 Gemini 키(X-Gemini-Key) 지원 — 구버전 배포와 구분하는 기능 플래그

    });
  } catch (e) {
    res.status(503).json({ ok: false, error: String(e.message || e) });
  }
}
