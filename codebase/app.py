from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

try:
    from .ai_service import AIServiceError, analyze, lesson_content, lesson_sources
    from .db import connection, initialize
except ImportError:
    # Hỗ trợ chạy `uvicorn app:app` khi terminal đang ở thư mục codebase.
    from ai_service import AIServiceError, analyze, lesson_content, lesson_sources
    from db import connection, initialize


ROOT = Path(__file__).resolve().parent
INDEX_HTML = ROOT / "cp2-flow.html"
app = FastAPI(title="Mistake Loop", version="0.1.0")


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


class AnalyzeRequest(BaseModel):
    session_id: str
    question: str = Field(min_length=4, max_length=1000)
    selected_answer: str | None = Field(default=None, max_length=80)
    reasoning: str = Field(min_length=1, max_length=4000)


class AttemptRequest(BaseModel):
    session_id: str
    question: str = Field(min_length=4, max_length=1000)
    reasoning: str = Field(min_length=1, max_length=4000)
    stage: str = Field(pattern="^(retry|transfer)$")


class EventRequest(BaseModel):
    session_id: str
    event_type: str = Field(min_length=1, max_length=80)
    payload: dict[str, Any] = Field(default_factory=dict)


@app.on_event("startup")
def startup() -> None:
    initialize()


@app.get("/")
def index() -> FileResponse:
    return FileResponse(INDEX_HTML)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/sources")
def sources() -> dict[str, Any]:
    return {"sources": lesson_sources()}


@app.get("/api/lesson")
def lesson() -> dict[str, Any]:
    return lesson_content()


@app.post("/api/session")
def create_session() -> dict[str, str]:
    session_id = str(uuid.uuid4())
    timestamp = now()
    with connection() as conn:
        conn.execute(
            "INSERT INTO sessions(id, lesson_id, created_at, updated_at) VALUES (?, ?, ?, ?)",
            (session_id, "foundation-rag", timestamp, timestamp)
        )
    return {"session_id": session_id}


def require_session(conn: Any, session_id: str) -> None:
    found = conn.execute("SELECT 1 FROM sessions WHERE id = ?", (session_id,)).fetchone()
    if not found:
        raise HTTPException(status_code=404, detail="Phiên học không tồn tại")


@app.post("/api/analyze")
def analyze_reasoning(request: AnalyzeRequest) -> dict[str, Any]:
    with connection() as conn:
        require_session(conn, request.session_id)
    try:
        result = analyze(request.question, request.selected_answer, request.reasoning)
    except AIServiceError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    timestamp = now()
    with connection() as conn:
        conn.execute(
            """INSERT INTO attempts(
                session_id, stage, question, selected_answer, reasoning, decision,
                misconception_id, confidence, ai_payload, created_at
            ) VALUES (?, 'initial', ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                request.session_id, request.question, request.selected_answer, request.reasoning,
                result.get("decision"), result.get("misconception_id"), result.get("confidence"),
                json.dumps(result, ensure_ascii=False), timestamp
            )
        )
        conn.execute("UPDATE sessions SET updated_at = ? WHERE id = ?", (timestamp, request.session_id))
    return result


@app.post("/api/attempt")
def save_attempt(request: AttemptRequest) -> dict[str, bool]:
    timestamp = now()
    with connection() as conn:
        require_session(conn, request.session_id)
        conn.execute(
            "INSERT INTO attempts(session_id, stage, question, reasoning, created_at) VALUES (?, ?, ?, ?, ?)",
            (request.session_id, request.stage, request.question, request.reasoning, timestamp)
        )
        if request.stage == "transfer":
            conn.execute("UPDATE sessions SET status = 'complete', updated_at = ? WHERE id = ?", (timestamp, request.session_id))
        else:
            conn.execute("UPDATE sessions SET updated_at = ? WHERE id = ?", (timestamp, request.session_id))
    return {"saved": True}


@app.post("/api/event")
def save_event(request: EventRequest) -> dict[str, bool]:
    with connection() as conn:
        require_session(conn, request.session_id)
        conn.execute(
            "INSERT INTO events(session_id, event_type, payload, created_at) VALUES (?, ?, ?, ?)",
            (request.session_id, request.event_type, json.dumps(request.payload, ensure_ascii=False), now())
        )
    return {"saved": True}


@app.get("/api/session/{session_id}")
def read_session(session_id: str) -> dict[str, Any]:
    with connection() as conn:
        require_session(conn, session_id)
        session = dict(conn.execute("SELECT * FROM sessions WHERE id = ?", (session_id,)).fetchone())
        attempts = [dict(row) for row in conn.execute(
            "SELECT id, stage, question, selected_answer, reasoning, decision, misconception_id, confidence, created_at FROM attempts WHERE session_id = ? ORDER BY id",
            (session_id,)
        ).fetchall()]
    return {"session": session, "attempts": attempts}
