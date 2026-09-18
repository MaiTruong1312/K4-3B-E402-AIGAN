from __future__ import annotations

import json
import random
import uuid
from datetime import datetime, timedelta, timezone

from codebase.db import connection, initialize


STUDENT_LIST = [
    ("SV2026001", "Nguyễn Văn An"),
    ("SV2026002", "Trần Thị Bình"),
    ("SV2026003", "Lê Hoàng Cường"),
    ("SV2026004", "Phạm Minh Đức"),
    ("SV2026005", "Vũ Phương Thảo"),
    ("SV2026006", "Hoàng Quốc Anh"),
    ("SV2026007", "Đặng Ngọc Dung"),
    ("SV2026008", "Bùi Thanh Hà"),
    ("SV2026009", "Đỗ Hải Yến"),
    ("SV2026010", "Hồ Văn Nam"),
    ("SV2026011", "Ngô Tấn Phát"),
    ("SV2026012", "Dương Thu Trang"),
    ("SV2026013", "Lý Quang Khải"),
    ("SV2026014", "Nguyễn Khánh Linh"),
    ("SV2026015", "Phan Gia Huy"),
    ("SV2026016", "Võ Thị Như Quỳnh"),
    ("SV2026017", "Đinh Hữu Tài"),
    ("SV2026018", "Trịnh Bảo Ngọc"),
    ("SV2026019", "Đoàn Tấn Dũng"),
    ("SV2026020", "Lương Thị Kiều Oanh"),
]

MISCONCEPTIONS_SEED = [
    ("rag-foundation-01", "rag-vs-finetuning", "Nhầm lẫn giữa cơ chế RAG (truy xuất tri thức động) và Fine-tuning (điều chỉnh trọng số mô hình)"),
    ("rag-foundation-01", "missing-source-citation", "Chưa trích dẫn căn cứ từ đoạn bài giảng VLearn khi giải thích"),
    ("rag-foundation-02", "vector-search-hallucination", "Cho rằng Vector Search đảm bảo 100% không sinh ra suy diễn sai (hallucination)"),
    ("rag-foundation-02", "verbatim-copying", "Chép lại nguyên văn câu đáp án mà không diễn giải theo cách hiểu của bản thân"),
]

DECISIONS = ["DIAGNOSE", "VERIFY", "CLARIFY", "DIAGNOSE"]
ASSESSMENT_TYPES = ["CONCEPT_MISCONCEPTION", "UNDERSTOOD", "REASONING_INSUFFICIENT", "SELECTION_MISMATCH"]


def seed() -> None:
    initialize()
    now_dt = datetime.now(timezone.utc)
    print(f"Creating mock data for {len(STUDENT_LIST)} students...")

    with connection() as conn:
        for idx, (code, name) in enumerate(STUDENT_LIST):
            session_id = str(uuid.uuid4())
            minutes_ago = (len(STUDENT_LIST) - idx) * 12
            created_time = (now_dt - timedelta(minutes=minutes_ago)).isoformat()
            updated_time = (now_dt - timedelta(minutes=minutes_ago - 5)).isoformat()
            status = "complete" if idx % 3 == 0 else "active"

            # Create session
            conn.execute(
                """INSERT OR REPLACE INTO sessions (id, lesson_id, created_at, updated_at, status, role, actor_id)
                   VALUES (?, ?, ?, ?, ?, 'student', ?)""",
                (session_id, "foundation-rag", created_time, updated_time, status, f"{code} ({name})")
            )

            # Create attempts (1 to 3 attempts per student)
            num_attempts = random.randint(1, 3)
            for att in range(num_attempts):
                req_id = str(uuid.uuid4())
                q_id = "rag-foundation-01" if att == 0 else "rag-foundation-02"
                stage = "initial" if att == 0 else ("retry" if att == 1 else "transfer")
                dec = random.choice(DECISIONS)
                ass_type = random.choice(ASSESSMENT_TYPES)
                misc_item = random.choice(MISCONCEPTIONS_SEED) if dec == "DIAGNOSE" else None
                misc_id = misc_item[1] if misc_item else None
                misc_text = misc_item[2] if misc_item else None

                payload = {
                    "decision": dec,
                    "assessment_type": ass_type,
                    "confidence": 0.88,
                    "explanation": f"Bài giải thích của sinh viên {name} đối với câu hỏi {q_id}.",
                    "source_ids": ["T03-036", "T03-038"]
                }

                conn.execute(
                    """INSERT INTO attempts (
                        session_id, request_id, stage, question_id, question, selected_answer,
                        reasoning, decision, misconception_id, confidence, ai_payload,
                        assessment_type, engagement_status, support_counted, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        session_id, req_id, stage, q_id, f"Câu hỏi {q_id}", "B",
                        f"Theo tôi hiểu thì RAG giúp mở rộng tri thức LLM bằng cách truy xuất văn bản ({name}).",
                        dec, misc_id, 0.88, json.dumps(payload, ensure_ascii=False),
                        ass_type, "SUBSTANTIVE", 1 if dec == "DIAGNOSE" else 0, updated_time
                    )
                )

                # Record misconception if DIAGNOSE
                if dec == "DIAGNOSE" and misc_item:
                    concept, m_id, m_desc = misc_item
                    m_status = "active" if status == "active" else "resolved"
                    conn.execute(
                        """INSERT INTO misconception_history (
                            session_id, concept, misconception_id, misconception, occurrence_count,
                            status, first_seen_at, last_seen_at
                        ) VALUES (?, ?, ?, ?, 1, ?, ?, ?)
                        ON CONFLICT(session_id, concept, misconception_id) DO UPDATE SET
                            occurrence_count = occurrence_count + 1,
                            last_seen_at = excluded.last_seen_at""",
                        (session_id, concept, m_id, m_desc, m_status, created_time, updated_time)
                    )

        # Insert sample question flags
        conn.execute(
            """INSERT INTO question_flags (session_id, question_id, issue, source_ids, status, created_at)
               VALUES (?, ?, ?, ?, 'pending_review', ?)""",
            (session_id, "rag-foundation-02", "Đáp án C và D có phần diễn đạt dễ gây hiểu nhầm về k-NN search", json.dumps(["T03-038"]), updated_time)
        )

    print("Seed completed successfully! 20 student sessions created.")


if __name__ == "__main__":
    seed()
