// POST /api/ask {q, history?} → {answer, sources[]}
// RAG: 쿼리 임베딩 → 청크 코사인 top-k → 논문리뷰 근거로 Gemini가 인용 답변 생성.
import { applyCors, rateLimit, loadData, embedQuery, retrieve, generate } from '../lib/store.js';

// sections는 [{key, label, body}] 배열 (structured 6키 + article 자유 헤딩 공용)
function secOf(post, key) {
  if (key === 'overview') return { label: '개요', body: post.summary || '' };
  const s = (post.sections || []).find((x) => x.key === key);
  return s ? { label: s.label, body: s.body } : { label: key, body: '' };
}
// gemini-embedding 유사도 분포: 무관 질의도 top1 0.5~0.6이 나온다 (실측: 김치찌개 0.52, 주식 0.60,
// 관련 질의 0.79). 절대 컷 + top1 게이트 이중 방어.
const MIN_SIM = 0.6;         // 개별 근거 최소 유사도
const TOP_GATE = 0.63;       // 최고 근거가 이 미만이면 전체를 무관 처리
const CTX_CHAR_PER_SEC = 2200;

function buildPrompt(q, history, sources) {
  const ctx = sources.map((s, i) => {
    const n = i + 1;
    const secs = s.secs.map((x) => {
      const sec = secOf(s.post, x.sec);
      const body = (sec.body || s.post.summary || '').slice(0, CTX_CHAR_PER_SEC);
      return `(${sec.label})\n${body}`;
    }).join('\n');
    return `[${n}] ${s.post.title} (${s.post.date})\n${secs}`;
  }).join('\n\n---\n\n');

  const hist = (history || []).slice(-4).map((h) =>
    `${h.role === 'user' ? '이전 질문' : '이전 답변'}: ${String(h.text || '').slice(0, 500)}`).join('\n');

  return `당신은 교육 전문 블로그 '기록하는 닷커넥터'의 리서치 어시스턴트다. AI와 교육을 다룬 논문리뷰들을 근거로 질문에 답한다.

## 근거 자료 (논문리뷰 발췌)
${ctx}

${hist ? `## 대화 맥락\n${hist}\n` : ''}
## 질문
${q}

## 답변 규칙
- 반드시 위 근거 자료의 내용만 사용해 답한다. 근거에 없는 내용은 지어내지 않는다.
- 근거 자료가 질문 주제와 관련이 있으면 적극적으로 종합해 답한다. 질문 문구와 완전히 일치하지 않아도 관련 발견을 연결해 실질적인 답을 준다. "직접 다룬 논문리뷰가 없다"는 답변은 근거가 정말 무관할 때만 한다.
- 출처 번호 [1], [2]는 단락(또는 불릿)당 한 번, 해당 단락의 끝에만 붙인다. 문장마다 붙이지 않는다 — 인용 표시가 많으면 본문 가독성이 무너진다.
- 간결한 존댓말(합니다체)로, 300~700자 내외. 필요하면 불릿(-)을 쓴다.
- 수치·연구 결과는 정확히 인용한다. 과장·일반화하지 않는다. 연구들이 상반된 결과를 보이면 그 조건 차이를 밝힌다.
- 마크다운은 **볼드**와 불릿(-)만 사용한다. 헤딩(#)은 쓰지 않는다.`;
}

export default async function handler(req, res) {
  if (applyCors(req, res)) return;
  if (req.method !== 'POST') return res.status(405).json({ error: 'method_not_allowed' });
  if (rateLimit(req, res, 6, 400)) return;

  const q = (req.body?.q || '').trim();
  const history = Array.isArray(req.body?.history) ? req.body.history : [];
  if (!q) return res.status(400).json({ error: 'empty_query' });
  if (q.length > 500) return res.status(400).json({ error: 'query_too_long', message: '질문은 500자 이내로 해달라.' });

  try {
    const [data, queryVec] = await Promise.all([loadData(), embedQuery(q)]);
    const hits = retrieve(queryVec, data, { maxSources: 5 });
    const sources = hits.filter((h) => h.sim >= MIN_SIM);

    if (!sources.length || sources[0].sim < TOP_GATE) {
      return res.status(200).json({
        answer: '이 질문과 관련된 논문리뷰를 찾지 못했다. AI·교육·학습과학 주제의 질문이라면 표현을 바꿔 다시 물어봐 달라.',
        sources: [],
      });
    }

    const answer = await generate(buildPrompt(q, history, sources));
    res.status(200).json({
      answer: answer.trim(),
      sources: sources.map((s, i) => ({
        n: i + 1,
        title: s.post.title,
        url: s.post.url,
        date: s.post.date,
        sim: Math.round(s.sim * 100) / 100,
        secs: s.secs.map((x) => secOf(s.post, x.sec).label),
      })),
    });
  } catch (e) {
    console.error('ask error:', e);
    res.status(502).json({ error: 'ask_failed', message: '답변 생성에 실패했다. 잠시 후 다시 시도해 달라.' });
  }
}
