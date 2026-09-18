from __future__ import annotations

import json
import os
import secrets
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

try:
    from .ai_service import AIServiceError, analyze, lesson_content, lesson_sources, question_text
    from .db import connection, initialize
    from .schemas import AnalyzeRequest, AttemptRequest, EventRequest, QuestionFlagUpdate, StudentLoginRequest, TeacherLoginRequest
    from .learning_history import load_learning_context, record_learning_state
except ImportError:
    # Hỗ trợ chạy `uvicorn app:app` khi terminal đang ở thư mục codebase.
    from ai_service import AIServiceError, analyze, lesson_content, lesson_sources, question_text
    from db import connection, initialize
    from schemas import AnalyzeRequest, AttemptRequest, EventRequest, QuestionFlagUpdate, StudentLoginRequest, TeacherLoginRequest
    from learning_history import load_learning_context, record_learning_state


ROOT = Path(__file__).resolve().parent
TEMPLATE_ROOT = ROOT / "templates"
PAGE_PARTS = (
    "layout/start.html",
    "screens/01-dashboard.html",
    "screens/02-quiz.html",
    "screens/03-feedback.html",
    "screens/04-retry.html",
    "screens/05-summary.html",
    "views/flowchart.html",
    "layout/end.html",
)
PAGE_PARTS_STUDENT = PAGE_PARTS
PAGE_PARTS_TEACHER = PAGE_PARTS
app = FastAPI(title="Mistake Loop", version="0.1.0")
app.mount("/static", StaticFiles(directory=ROOT / "static"), name="static")


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


@app.on_event("startup")
def startup() -> None:
    initialize()


@app.get("/")
@app.get("/student")
def index() -> HTMLResponse:
    html = "\n".join((TEMPLATE_ROOT / part).read_text(encoding="utf-8") for part in PAGE_PARTS_STUDENT)
    return HTMLResponse(html)


@app.get("/instructor")
@app.get("/teacher")
def instructor_dashboard() -> HTMLResponse:
    html = "\n".join((TEMPLATE_ROOT / part).read_text(encoding="utf-8") for part in PAGE_PARTS_TEACHER)
    return HTMLResponse(html)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/sources")
def sources() -> dict[str, Any]:
    return {"sources": lesson_sources()}


@app.get("/api/lesson")
def lesson() -> dict[str, Any]:
    return lesson_content()


@app.get("/api/lesson/overview")
def lesson_overview() -> dict[str, Any]:
    """Return lesson metadata + top BM25 transcript passages for preview."""
    try:
        from .knowledge_base import retrieve as kb_retrieve
    except ImportError:
        from knowledge_base import retrieve as kb_retrieve

    content = lesson_content()
    query = f"{content['title']} {content['scope']}"
    passages = kb_retrieve(query, limit=6)
    return {
        "title": content["title"],
        "scope": content["scope"],
        "key_passages": [
            {"id": p["id"], "text": p["text"][:300]} for p in passages
        ],
        "question_topics": [
            {"id": q["id"], "concept": q.get("concept", ""), "type": q.get("type", "")}
            for q in content["questions"]
        ],
    }


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


@app.post("/api/auth/student")
def login_student(request: StudentLoginRequest) -> dict[str, str]:
    student_code = request.student_code.strip().upper()
    timestamp = now()
    with connection() as conn:
        existing = conn.execute(
            """SELECT id FROM sessions
               WHERE role = 'student' AND actor_id = ? AND status = 'active'
               ORDER BY updated_at DESC LIMIT 1""",
            (student_code,),
        ).fetchone()
        if existing:
            return {"session_id": existing[0], "role": "student", "display_name": student_code}
        session_id = str(uuid.uuid4())
        conn.execute(
            """INSERT INTO sessions(id, lesson_id, created_at, updated_at, role, actor_id)
               VALUES (?, ?, ?, ?, 'student', ?)""",
            (session_id, "foundation-rag", timestamp, timestamp, student_code),
        )
    return {"session_id": session_id, "role": "student", "display_name": student_code}


@app.post("/api/auth/teacher")
def login_teacher(request: TeacherLoginRequest) -> dict[str, str]:
    expected_username = os.getenv("TEACHER_USERNAME", "")
    expected_password = os.getenv("TEACHER_PASSWORD", "")
    if not expected_username or not expected_password:
        raise HTTPException(status_code=503, detail="Tài khoản giảng viên chưa được cấu hình trong .env")
    if not (
        secrets.compare_digest(request.username, expected_username)
        and secrets.compare_digest(request.password, expected_password)
    ):
        raise HTTPException(status_code=401, detail="Tài khoản hoặc mật khẩu không đúng")
    session_id = str(uuid.uuid4())
    timestamp = now()
    with connection() as conn:
        conn.execute(
            """INSERT INTO sessions(id, lesson_id, created_at, updated_at, role, actor_id)
               VALUES (?, ?, ?, ?, 'teacher', ?)""",
            (session_id, "foundation-rag", timestamp, timestamp, request.username),
        )
    return {"session_id": session_id, "role": "teacher", "display_name": request.username}


def require_session(conn: Any, session_id: str) -> None:
    found = conn.execute("SELECT 1 FROM sessions WHERE id = ?", (session_id,)).fetchone()
    if not found:
        raise HTTPException(status_code=404, detail="Phiên học không tồn tại")


def require_teacher(conn: Any, session_id: str) -> None:
    found = conn.execute(
        "SELECT 1 FROM sessions WHERE id = ? AND role = 'teacher' AND status = 'active'",
        (session_id,),
    ).fetchone()
    if not found:
        raise HTTPException(status_code=403, detail="Cần đăng nhập bằng tài khoản giảng viên")


@app.post("/api/analyze")
def analyze_reasoning(request: AnalyzeRequest) -> dict[str, Any]:
    with connection() as conn:
        require_session(conn, request.session_id)
        duplicate = conn.execute(
            "SELECT ai_payload FROM attempts WHERE request_id = ?", (request.request_id,)
        ).fetchone()
        if duplicate and duplicate[0]:
            return json.loads(duplicate[0])
        question = question_text(request.question_id)
        previous_attempts, learning_history = load_learning_context(
            conn, request.session_id, request.question_id
        )
    attempt_number = previous_attempts + 1
    try:
        result = analyze(
            request.question_id,
            request.selected_answer,
            request.reasoning,
            attempt_number=attempt_number,
            learning_history=learning_history,
        )
    except AIServiceError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    timestamp = now()
    with connection() as conn:
        conn.execute(
            """INSERT INTO attempts(
                session_id, request_id, stage, question_id, question, selected_answer,
                reasoning, decision, misconception_id, confidence, ai_payload,
                assessment_type, engagement_status, support_counted, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                request.session_id, request.request_id, request.stage, request.question_id, question,
                request.selected_answer, request.reasoning,
                result.get("decision"), result.get("misconception_id"), result.get("confidence"),
                json.dumps(result, ensure_ascii=False), result.get("assessment_type"),
                result.get("engagement_status"), int(result.get("submission_counted_for_support") is True), timestamp
            )
        )
        record_learning_state(conn, request.session_id, request.question_id, result, timestamp)
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
            """SELECT id, request_id, stage, question_id, question, selected_answer,
                      reasoning, decision, assessment_type, engagement_status,
                      misconception_id, confidence, support_counted, created_at
               FROM attempts WHERE session_id = ? ORDER BY id""",
            (session_id,)
        ).fetchall()]
        misconceptions = [dict(row) for row in conn.execute(
            "SELECT * FROM misconception_history WHERE session_id = ? ORDER BY last_seen_at DESC",
            (session_id,),
        ).fetchall()]
        question_flags = [dict(row) for row in conn.execute(
            "SELECT * FROM question_flags WHERE session_id = ? ORDER BY created_at DESC",
            (session_id,),
        ).fetchall()]
    return {
        "session": session,
        "attempts": attempts,
        "misconceptions": misconceptions,
        "question_flags": question_flags,
    }


@app.get("/api/instructor/report")
def instructor_report(session_id: str) -> dict[str, Any]:
    with connection() as conn:
        require_teacher(conn, session_id)
        student_sessions = [dict(row) for row in conn.execute(
            """SELECT s.id AS session_id,
                      s.actor_id AS student_code,
                      s.status,
                      s.created_at,
                      s.updated_at,
                      COUNT(a.id) AS total_attempts,
                      MAX(a.created_at) AS last_attempt_at,
                      (SELECT decision FROM attempts WHERE session_id = s.id ORDER BY id DESC LIMIT 1) AS latest_decision,
                      (SELECT assessment_type FROM attempts WHERE session_id = s.id ORDER BY id DESC LIMIT 1) AS latest_assessment_type
               FROM sessions s
               LEFT JOIN attempts a ON s.id = a.session_id
               WHERE s.role = 'student'
               GROUP BY s.id, s.actor_id, s.status, s.created_at, s.updated_at
               ORDER BY s.updated_at DESC
               LIMIT 30"""
        ).fetchall()]
        misconceptions = [dict(row) for row in conn.execute(
            """SELECT concept, misconception_id, misconception,
                      SUM(occurrence_count) AS occurrences,
                      SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END) AS active_learners
               FROM misconception_history
               GROUP BY concept, misconception_id, misconception
               ORDER BY occurrences DESC"""
        ).fetchall()]
        question_flags = [dict(row) for row in conn.execute(
            "SELECT * FROM question_flags ORDER BY created_at DESC"
        ).fetchall()]
        assessment_counts = [dict(row) for row in conn.execute(
            """SELECT assessment_type, COUNT(*) AS total
               FROM attempts WHERE assessment_type IS NOT NULL
               GROUP BY assessment_type ORDER BY total DESC"""
        ).fetchall()]
    return {
        "student_sessions": student_sessions,
        "misconceptions": misconceptions,
        "question_flags": question_flags,
        "assessment_counts": assessment_counts,
    }



@app.patch("/api/instructor/question-flags/{flag_id}")
def update_question_flag(flag_id: int, request: QuestionFlagUpdate) -> dict[str, Any]:
    with connection() as conn:
        require_teacher(conn, request.session_id)
        found = conn.execute("SELECT id FROM question_flags WHERE id = ?", (flag_id,)).fetchone()
        if not found:
            raise HTTPException(status_code=404, detail="Không tìm thấy cảnh báo câu hỏi")
        conn.execute("UPDATE question_flags SET status = ? WHERE id = ?", (request.status, flag_id))
    return {"updated": True, "flag_id": flag_id, "status": request.status}
