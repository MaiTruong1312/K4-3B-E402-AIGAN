from __future__ import annotations

import json
from typing import Any


def load_learning_context(conn: Any, session_id: str, question_id: str) -> tuple[int, list[dict[str, Any]]]:
    rows = conn.execute(
        """SELECT reasoning, decision, misconception_id, ai_payload, created_at
           FROM attempts WHERE session_id = ? AND question_id = ?
           ORDER BY id DESC LIMIT 8""",
        (session_id, question_id),
    ).fetchall()
    productive_attempts = 0
    history: list[dict[str, Any]] = []
    for row in reversed(rows):
        try:
            payload = json.loads(row[3] or "{}")
        except (TypeError, json.JSONDecodeError):
            payload = {}
        if payload.get("submission_counted_for_support") is True:
            productive_attempts += 1
        history.append({
            "reasoning": row[0], "decision": row[1],
            "assessment_type": payload.get("assessment_type"),
            "misconception_id": row[2], "misconception": payload.get("misconception"),
            "correct_claims": payload.get("correct_claims", []),
            "incorrect_claims": payload.get("incorrect_claims", []),
            "missing_concepts": payload.get("missing_concepts", []),
            "created_at": row[4],
        })
    memory = [dict(row) for row in conn.execute(
        """SELECT concept, misconception_id, misconception, occurrence_count,
                  status, first_seen_at, last_seen_at, resolved_at
           FROM misconception_history WHERE session_id = ?
           ORDER BY last_seen_at DESC LIMIT 12""",
        (session_id,),
    ).fetchall()]
    if memory:
        history.append({"concept_memory": memory})
    return productive_attempts, history


def record_learning_state(
    conn: Any, session_id: str, question_id: str, result: dict[str, Any], timestamp: str
) -> None:
    misconception_id = result.get("misconception_id")
    concept = result.get("concept") or question_id
    if result.get("decision") == "DIAGNOSE" and misconception_id:
        conn.execute(
            """INSERT INTO misconception_history(
                session_id, concept, misconception_id, misconception, first_seen_at, last_seen_at
            ) VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(session_id, concept, misconception_id) DO UPDATE SET
                misconception = excluded.misconception,
                occurrence_count = occurrence_count + 1,
                status = 'active', last_seen_at = excluded.last_seen_at, resolved_at = NULL""",
            (session_id, concept, misconception_id, result.get("misconception"), timestamp, timestamp),
        )
    elif result.get("decision") == "VERIFY":
        conn.execute(
            """UPDATE misconception_history SET status = 'resolved', resolved_at = ?
               WHERE session_id = ? AND concept = ? AND status = 'active'""",
            (timestamp, session_id, concept),
        )
    if result.get("assessment_type") == "QUESTION_DEFECT":
        conn.execute(
            """INSERT INTO question_flags(session_id, question_id, issue, source_ids, created_at)
               VALUES (?, ?, ?, ?, ?)""",
            (
                session_id, question_id, result.get("question_issue") or "Đề cần giảng viên kiểm tra",
                json.dumps(result.get("source_ids", []), ensure_ascii=False), timestamp,
            ),
        )
