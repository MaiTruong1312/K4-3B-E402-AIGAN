from __future__ import annotations

import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB = ROOT / "codebase" / "mistake_loop.db"


def database_path() -> Path:
    configured = os.getenv("DATABASE_PATH")
    path = Path(configured) if configured else DEFAULT_DB
    if not path.is_absolute():
        path = ROOT / path
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


@contextmanager
def connection() -> Iterator[sqlite3.Connection]:
    conn = sqlite3.connect(database_path())
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def initialize() -> None:
    statements = [
        """
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY,
            lesson_id TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'active'
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            stage TEXT NOT NULL,
            question TEXT NOT NULL,
            selected_answer TEXT,
            reasoning TEXT NOT NULL,
            decision TEXT,
            misconception_id TEXT,
            confidence REAL,
            ai_payload TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY(session_id) REFERENCES sessions(id) ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            event_type TEXT NOT NULL,
            payload TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY(session_id) REFERENCES sessions(id) ON DELETE CASCADE
        )
        """,
        "CREATE INDEX IF NOT EXISTS idx_attempts_session_stage ON attempts(session_id, stage)",
        "CREATE INDEX IF NOT EXISTS idx_events_session_created ON events(session_id, created_at)"
    ]
    with connection() as conn:
        for statement in statements:
            conn.execute(statement)
        existing_columns = {row[1] for row in conn.execute("PRAGMA table_info(attempts)")}
        migrations = {
            "request_id": "TEXT",
            "question_id": "TEXT",
            "question_version": "TEXT NOT NULL DEFAULT '1'",
            "assessment_type": "TEXT",
            "engagement_status": "TEXT",
            "support_counted": "INTEGER NOT NULL DEFAULT 0",
        }
        for column, definition in migrations.items():
            if column not in existing_columns:
                conn.execute(f"ALTER TABLE attempts ADD COLUMN {column} {definition}")
        session_columns = {row[1] for row in conn.execute("PRAGMA table_info(sessions)")}
        session_migrations = {
            "role": "TEXT NOT NULL DEFAULT 'student'",
            "actor_id": "TEXT",
        }
        for column, definition in session_migrations.items():
            if column not in session_columns:
                conn.execute(f"ALTER TABLE sessions ADD COLUMN {column} {definition}")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_sessions_actor ON sessions(role, actor_id, status)")
        conn.execute(
            """CREATE TABLE IF NOT EXISTS misconception_history (
                session_id TEXT NOT NULL,
                concept TEXT NOT NULL,
                misconception_id TEXT NOT NULL,
                misconception TEXT,
                occurrence_count INTEGER NOT NULL DEFAULT 1,
                status TEXT NOT NULL DEFAULT 'active',
                first_seen_at TEXT NOT NULL,
                last_seen_at TEXT NOT NULL,
                resolved_at TEXT,
                PRIMARY KEY(session_id, concept, misconception_id),
                FOREIGN KEY(session_id) REFERENCES sessions(id) ON DELETE CASCADE
            )"""
        )
        conn.execute(
            """CREATE TABLE IF NOT EXISTS question_flags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                question_id TEXT NOT NULL,
                issue TEXT NOT NULL,
                source_ids TEXT NOT NULL DEFAULT '[]',
                status TEXT NOT NULL DEFAULT 'pending_review',
                created_at TEXT NOT NULL,
                FOREIGN KEY(session_id) REFERENCES sessions(id) ON DELETE CASCADE
            )"""
        )
        conn.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_attempts_request_id ON attempts(request_id) WHERE request_id IS NOT NULL")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_attempts_session_question ON attempts(session_id, question_id, created_at)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_question_flags_status ON question_flags(status, created_at)")
        conn.execute("PRAGMA optimize")

