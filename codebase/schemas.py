from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, field_validator


class AnalyzeRequest(BaseModel):
    session_id: str
    request_id: str = Field(min_length=8, max_length=120)
    question_id: str = Field(min_length=1, max_length=120)
    selected_answer: str | None = Field(default=None, max_length=80)
    reasoning: str = Field(min_length=1, max_length=4000)
    stage: str = Field(default="initial", pattern="^(initial|retry|transfer)$")

    @field_validator("reasoning")
    @classmethod
    def reasoning_must_not_be_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Phần giải thích không được chỉ chứa khoảng trắng")
        return value


class AttemptRequest(BaseModel):
    session_id: str
    question: str = Field(min_length=4, max_length=1000)
    reasoning: str = Field(min_length=1, max_length=4000)
    stage: str = Field(pattern="^(retry|transfer)$")

    @field_validator("reasoning")
    @classmethod
    def attempt_reasoning_must_not_be_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Phần giải thích không được chỉ chứa khoảng trắng")
        return value


class EventRequest(BaseModel):
    session_id: str
    event_type: str = Field(min_length=1, max_length=80)
    payload: dict[str, Any] = Field(default_factory=dict)


class QuestionFlagUpdate(BaseModel):
    session_id: str
    status: str = Field(pattern="^(pending_review|confirmed|dismissed|fixed)$")


class StudentLoginRequest(BaseModel):
    student_code: str = Field(min_length=3, max_length=40, pattern=r"^[A-Za-z0-9._-]+$")


class TeacherLoginRequest(BaseModel):
    username: str = Field(min_length=1, max_length=80)
    password: str = Field(min_length=1, max_length=200)
