from __future__ import annotations

import unittest

from codebase.ai_service import (
    _apply_support_policy,
    _enforce_choice_consistency,
    _enforce_original_reasoning,
    _validate,
)


SOURCES = [{"id": "T03-036", "text": "Đoạn bài giảng thật", "file": "transcript-03-clean.md"}]
MCQ = {
    "type": "multiple_choice",
    "correct_option": "B",
    "options": [{"id": "A", "text": "Sai"}, {"id": "B", "text": "Đúng"}],
}


class AssessmentPolicyTests(unittest.TestCase):
    def test_correct_choice_without_reasoning_cannot_pass(self) -> None:
        payload = self._payload(
            decision="VERIFY", assessment_type="INSUFFICIENT",
            engagement_status="INSUFFICIENT", reasoning_is_substantive=False,
            rubric_coverage=[], verification_evidence=None,
        )
        result = _validate(payload, SOURCES)
        self.assertEqual(result["decision"], "CLARIFY")

    def test_wrong_choice_with_valid_reasoning_is_selection_mismatch(self) -> None:
        payload = _validate(self._payload(), SOURCES)
        result = _enforce_choice_consistency(payload, MCQ, "A")
        self.assertEqual(result["decision"], "CLARIFY")
        self.assertEqual(result["assessment_type"], "SELECTION_MISMATCH")
        self.assertIsNone(result["misconception"])

    def test_low_effort_never_reveals_answer(self) -> None:
        payload = self._payload(
            decision="CLARIFY", assessment_type="OFF_TASK",
            engagement_status="OFF_TASK", reasoning_is_substantive=False,
        )
        result = _apply_support_policy(_validate(payload, SOURCES), MCQ, 8)
        self.assertFalse(result["submission_counted_for_support"])
        self.assertFalse(result["reveal_answer"])

    def test_third_productive_error_reveals_mcq_answer(self) -> None:
        payload = self._payload(
            decision="DIAGNOSE", assessment_type="MISCONCEPTION",
            misconception="Nhầm cơ chế", misconception_id="rag-mechanism",
        )
        result = _apply_support_policy(_validate(payload, SOURCES), MCQ, 3)
        self.assertTrue(result["reveal_answer"])
        self.assertEqual(result["revealed_correct_option"]["id"], "B")

    def test_verbatim_copy_cannot_pass(self) -> None:
        payload = _validate(self._payload(), SOURCES)
        result = _enforce_original_reasoning(payload, "Đúng", {"id": "B", "text": "Đúng"})
        self.assertEqual(result["decision"], "CLARIFY")
        self.assertEqual(result["assessment_type"], "COPYING")

    @staticmethod
    def _payload(**overrides):
        payload = {
            "decision": "VERIFY",
            "assessment_type": "UNDERSTOOD",
            "engagement_status": "SUBSTANTIVE",
            "reasoning_is_substantive": True,
            "rubric_coverage": ["Có lý do"],
            "verification_evidence": "vì có lý do",
            "source_ids": ["T03-036"],
            "confidence": 0.9,
            "misconception": None,
            "misconception_id": None,
        }
        payload.update(overrides)
        return payload


if __name__ == "__main__":
    unittest.main()
