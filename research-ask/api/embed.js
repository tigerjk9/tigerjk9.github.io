// POST /api/embed {q} → {vec: float[768]} — 허브 시맨틱 검색용 쿼리 임베딩
// 문서 벡터는 블로그 정적 파일(research-emb-posts.json)에 있으므로 코사인은 클라이언트가 계산한다.
import { applyCors, rateLimit, requireKey, embedQuery } from '../lib/store.js';

export default async function handler(req, res) {
  if (applyCors(req, res)) return;
  if (req.method !== 'POST') return res.status(405).json({ error: 'method_not_allowed' });
  if (requireKey(req, res)) return;
  if (rateLimit(req, res, 10, 1200)) return;

  const q = (req.body?.q || '').trim();
  if (!q) return res.status(400).json({ error: 'empty_query' });
  if (q.length > 500) return res.status(400).json({ error: 'query_too_long' });

  try {
    const vec = await embedQuery(q);
    // 소수 5자리 반올림 — 응답 크기 절감 (검색 순위 영향 없음)
    res.status(200).json({ vec: vec.map((x) => Math.round(x * 1e5) / 1e5) });
  } catch (e) {
    console.error('embed error:', e);
    res.status(502).json({ error: 'embed_failed', message: '임베딩 생성에 실패했다. 잠시 후 다시 시도해 달라.' });
  }
}
