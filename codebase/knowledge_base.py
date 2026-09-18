from __future__ import annotations

import re
import math
import unicodedata
from collections import Counter
from functools import lru_cache
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_ROOTS = (ROOT / "data" / "vlearn", ROOT / "data" / "vlearn-pack")
PASSAGE_RE = re.compile(r"\*\*\[(T\d{2}-\d{3})\]\*\*\s*(.*?)(?=\n\*\*\[T\d{2}-\d{3}\]\*\*|\Z)", re.S)
TOKEN_RE = re.compile(r"[a-z0-9]{2,}")
STOP_WORDS = {
    "cua", "cho", "mot", "nhung", "cac", "voi", "trong", "khi", "thi", "la", "va",
    "duoc", "nay", "do", "nhu", "the", "co", "khong", "hoc", "vien", "cau", "tra", "loi",
}


def _normalise(text: str) -> str:
    text = unicodedata.normalize("NFD", text.lower())
    return "".join(char for char in text if unicodedata.category(char) != "Mn")


def _tokens(text: str) -> set[str]:
    return {token for token in TOKEN_RE.findall(_normalise(text)) if token not in STOP_WORDS}


def _token_list(text: str) -> list[str]:
    return [token for token in TOKEN_RE.findall(_normalise(text)) if token not in STOP_WORDS]


def _data_root() -> Path:
    for root in DATA_ROOTS:
        if (root / "transcript").is_dir():
            return root
    raise RuntimeError("Không tìm thấy data/vlearn hoặc data/vlearn-pack/transcript")


@lru_cache(maxsize=1)
def passages() -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    for path in sorted((_data_root() / "transcript").glob("transcript-*-clean.md")):
        content = path.read_text(encoding="utf-8")
        for passage_id, raw_text in PASSAGE_RE.findall(content):
            text = " ".join(raw_text.strip().split())
            if text:
                records.append({"id": passage_id, "text": text, "file": path.name})
    if not records:
        raise RuntimeError("Không đọc được đoạn bài giảng có mã trích dẫn")
    return records


@lru_cache(maxsize=1)
def _bm25_index() -> tuple[list[Counter[str]], Counter[str], float]:
    documents = [Counter(_token_list(item["text"])) for item in passages()]
    document_frequency: Counter[str] = Counter()
    for document in documents:
        document_frequency.update(document.keys())
    average_length = sum(sum(document.values()) for document in documents) / max(len(documents), 1)
    return documents, document_frequency, average_length


def retrieve(query: str, limit: int = 6) -> list[dict[str, str]]:
    """BM25 retrieval over exact VLearn transcript passages."""
    query_terms = _token_list(query)
    query_frequency = Counter(query_terms)
    documents, document_frequency, average_length = _bm25_index()
    total_documents = len(documents)
    ranked: list[tuple[float, dict[str, str]]] = []
    k1, b = 1.5, 0.75
    for passage, document in zip(passages(), documents):
        document_length = sum(document.values())
        score = 0.0
        for term, query_count in query_frequency.items():
            term_frequency = document.get(term, 0)
            if not term_frequency:
                continue
            frequency = document_frequency[term]
            inverse_document_frequency = math.log(1 + (total_documents - frequency + 0.5) / (frequency + 0.5))
            denominator = term_frequency + k1 * (1 - b + b * document_length / max(average_length, 1))
            score += inverse_document_frequency * (term_frequency * (k1 + 1) / denominator) * min(query_count, 2)
        if score <= 0:
            continue
        ranked.append((score, passage))
    ranked.sort(key=lambda item: item[0], reverse=True)
    return [passage for _, passage in ranked[:limit]]


def by_ids(ids: list[str]) -> list[dict[str, str]]:
    wanted = set(ids)
    return [passage for passage in passages() if passage["id"] in wanted]
