# -*- coding: utf-8 -*-
"""
build_embeddings.py — 리서치 DB(research-db.json)를 Gemini 임베딩으로 벡터화한다.

출력 2종:
  assets/research-emb-posts.json  — 포스트당 overview 벡터 1개 (허브 클라이언트 시맨틱 검색용, ~100KB)
  assets/research-rag-index.json  — 포스트 x 섹션 청크 벡터 전체 (RAG 서비스 콜드스타트 로드용)

설계
- 모델: gemini-embedding-001, 768차원 (output_dimensionality 미지원 SDK면 truncate+renormalize — MRL 안전)
- 양자화: unit vector → per-vector scale int8 (base64). JS 복원: Int8Array * s
- 증분: (id, sec, text md5-8) 동일하면 기존 벡터 재사용 → 신규 포스트만 임베딩
- 무료 티어 대응: 배치 + 429 지수 백오프

실행:  py scripts/build_embeddings.py            # 증분 빌드
       py scripts/build_embeddings.py --limit 3  # 테스트 (앞 3편만)
       py scripts/build_embeddings.py --force    # 전체 재임베딩

research-db.json 재생성(build_research_db.py) 후에 실행한다.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import math
import os
import sys
import time
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

REPO_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = REPO_ROOT / "assets" / "research-db.json"
POSTS_OUT = REPO_ROOT / "assets" / "research-emb-posts.json"
RAG_OUT = REPO_ROOT / "assets" / "research-rag-index.json"

EMBED_MODEL = "models/gemini-embedding-001"
DIM = 768
CHUNK_CHAR_LIMIT = 3000   # 임베딩 입력 트림 (토큰 절약, 신호 충분)
BATCH = 10                # 배치 크기 (무료 티어 TPM 배려)


def _load_dotenv() -> None:
    env_path = REPO_ROOT / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


_load_dotenv()


def text_hash(s: str) -> str:
    return hashlib.md5(s.encode("utf-8")).hexdigest()[:8]


def build_chunks(db: dict) -> "list[dict]":
    """포스트 → 청크 목록. overview + 섹션 배열(구조화/아티클 공용).

    청크 텍스트는 "[제목] <섹션key>\\n<본문>" — key를 쓰는 이유는 기존 structured
    청크의 텍스트 해시를 보존해 증분 재사용을 극대화하기 위함.
    """
    chunks = []
    for p in db["posts"]:
        overview = "제목: %s\n태그: %s\n요약: %s" % (
            p["title"], ", ".join(p.get("tags", [])), p.get("summary", ""))
        chunks.append({"id": p["id"], "sec": "overview",
                       "text": overview[:CHUNK_CHAR_LIMIT]})
        for s in p.get("sections", []):
            if not s.get("body"):
                continue
            text = "[%s] %s\n%s" % (p["title"], s["key"], s["body"])
            chunks.append({"id": p["id"], "sec": s["key"],
                           "text": text[:CHUNK_CHAR_LIMIT]})
    return chunks


def quantize(vec: "list[float]") -> "tuple[str, float]":
    """unit vector → (base64 int8, scale)."""
    norm = math.sqrt(sum(x * x for x in vec)) or 1.0
    unit = [x / norm for x in vec]
    mx = max(abs(x) for x in unit) or 1.0
    scale = mx / 127.0
    q = bytes((round(x / scale)) & 0xFF for x in unit)
    return base64.b64encode(q).decode("ascii"), scale


def load_existing(path: Path) -> "dict[tuple, dict]":
    """기존 출력에서 (id, sec) → {h, s, v} 맵 로드 (증분용)."""
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        out = {}
        for c in data.get("chunks", data.get("items", [])):
            out[(c["id"], c.get("sec", "overview"))] = c
        return out
    except Exception:
        return {}


def embed_batch(texts: "list[str]", genai) -> "list[list[float]]":
    """배치 임베딩 + 429 백오프. output_dimensionality 미지원이면 truncate."""
    delay = 5
    for attempt in range(7):
        try:
            try:
                res = genai.embed_content(
                    model=EMBED_MODEL, content=texts,
                    task_type="retrieval_document",
                    output_dimensionality=DIM)
            except TypeError:
                res = genai.embed_content(
                    model=EMBED_MODEL, content=texts,
                    task_type="retrieval_document")
            embs = res["embedding"]
            if texts and not isinstance(embs[0], list):
                embs = [embs]
            # 차원 보정: MRL truncate + (양자화 단계에서 renormalize)
            return [e[:DIM] for e in embs]
        except Exception as e:
            msg = str(e)
            if "429" in msg or "quota" in msg.lower() or "rate" in msg.lower():
                print("  [429] %ds 대기 후 재시도 (%d/7)" % (delay, attempt + 1))
                time.sleep(delay)
                delay = min(delay * 2, 120)
                continue
            raise
    raise RuntimeError("임베딩 재시도 한도 초과")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0, help="앞 N편만 처리 (테스트)")
    ap.add_argument("--force", action="store_true", help="증분 무시, 전체 재임베딩")
    args = ap.parse_args()

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("[ERROR] GEMINI_API_KEY 미설정 (.env 확인)")
        sys.exit(1)

    import google.generativeai as genai
    genai.configure(api_key=api_key)

    db = json.loads(DB_PATH.read_text(encoding="utf-8"))
    if args.limit:
        db = {"meta": db["meta"], "posts": db["posts"][:args.limit]}
    chunks = build_chunks(db)
    print("청크 %d개 (포스트 %d편)" % (len(chunks), len(db["posts"])))

    existing = {} if args.force else load_existing(RAG_OUT)
    todo, reused = [], 0
    for c in chunks:
        h = text_hash(c["text"])
        c["h"] = h
        prev = existing.get((c["id"], c["sec"]))
        if prev and prev.get("h") == h:
            c["v"], c["s"] = prev["v"], prev["s"]
            reused += 1
        else:
            todo.append(c)
    print("재사용 %d / 신규 임베딩 %d" % (reused, len(todo)))

    done = 0
    t0 = time.time()
    for i in range(0, len(todo), BATCH):
        batch = todo[i:i + BATCH]
        embs = embed_batch([c["text"] for c in batch], genai)
        for c, e in zip(batch, embs):
            c["v"], c["s"] = quantize(e)
        done += len(batch)
        el = time.time() - t0
        print("  %d/%d (%.0fs)" % (done, len(todo), el), flush=True)
        time.sleep(1.2)  # RPM 배려

    # ── 출력 1: RAG 인덱스 (전 청크) ──
    rag = {
        "model": EMBED_MODEL.replace("models/", ""),
        "dim": DIM,
        "chunks": [{"id": c["id"], "sec": c["sec"], "h": c["h"],
                    "s": round(c["s"], 8), "v": c["v"]} for c in chunks],
    }
    RAG_OUT.write_text(json.dumps(rag, ensure_ascii=False, separators=(",", ":")),
                       encoding="utf-8")
    print("기록: %s (%.0f KB)" % (RAG_OUT.name, RAG_OUT.stat().st_size / 1024))

    # ── 출력 2: 포스트 overview 벡터 (허브 검색용) ──
    posts = {
        "model": EMBED_MODEL.replace("models/", ""),
        "dim": DIM,
        "items": [{"id": c["id"], "h": c["h"], "s": round(c["s"], 8), "v": c["v"]}
                  for c in chunks if c["sec"] == "overview"],
    }
    POSTS_OUT.write_text(json.dumps(posts, ensure_ascii=False, separators=(",", ":")),
                         encoding="utf-8")
    print("기록: %s (%.0f KB)" % (POSTS_OUT.name, POSTS_OUT.stat().st_size / 1024))
    print("완료.")


if __name__ == "__main__":
    main()
