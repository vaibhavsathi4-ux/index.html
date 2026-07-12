import os
from typing import List, Tuple
from dotenv import load_dotenv
from openai import OpenAI

from models import Message

load_dotenv()

OPENAI_MODEL = os.getenv("OPENAI_MODEL","openrouter/free")
CONTEXT_WINDOW_MESSAGES = int(os.getenv("CONTEXT_WINDOW_MESSAGES", "12"))

_client = OpenAI(base_url="https://openrouter.ai/api/v1")  # reads OPENAI_API_KEY from env


def is_ambiguous(question: str) -> bool:
    """
    Very lightweight heuristic for the 'ambiguous queries' edge case.
    Flags very short / vague questions so the tutor can ask a
    clarifying question instead of guessing at intent.
    """
    text = question.strip().lower()
    if len(text.split()) <= 2:
        return True
    vague_markers = ("this", "that", "it", "help", "?", "idk", "confused")
    return text in vague_markers or (len(text) < 12 and any(m in text for m in vague_markers))


def build_system_prompt(subject: str | None, difficulty_level: float, ambiguous: bool) -> str:
    level = "beginner" if difficulty_level < 1.5 else "intermediate" if difficulty_level < 2.5 else "advanced"
    subject_line = f"The student is working on: {subject}." if subject else ""

    base = (
        "You are ChatTutor, a patient, encouraging AI tutor. "
        f"{subject_line} Calibrate explanations for a {level} student. "
        "Explain concepts step by step, check understanding, and use small "
        "examples rather than just giving final answers when a concept is being learned. "
        "Keep responses focused and not overly long."
    )
    if ambiguous:
        base += (
            " The student's latest message is short or ambiguous. Before answering, "
            "ask one brief clarifying question to understand what they need, "
            "while offering your best guess at what they might mean."
        )
    return base


def adjust_difficulty(current: float, question: str) -> float:
    """
    Toy adaptive-learning signal: nudges difficulty up if the student's
    question suggests they're breezing through ('makes sense', 'easy'),
    and down if they're struggling ('confused', 'don't get it').
    Clamped to [1.0, 3.0]. Replace with real performance tracking later.
    """
    text = question.lower()
    if any(p in text for p in ["makes sense", "got it", "easy", "understand now"]):
        return min(3.0, current + 0.15)
    if any(p in text for p in ["confused", "don't get", "dont get", "lost", "still don't"]):
        return max(1.0, current - 0.15)
    return current


def _to_openai_messages(history: List[Message], new_question: str, system_prompt: str) -> List[dict]:
    trimmed = history[-CONTEXT_WINDOW_MESSAGES:]
    msgs = [{"role": "system", "content": system_prompt}]
    msgs += [{"role": m.role, "content": m.content} for m in trimmed]
    msgs.append({"role": "user", "content": new_question})
    return msgs


def ask_tutor(
    history: List[Message],
    question: str,
    subject: str | None,
    difficulty_level: float,
) -> Tuple[str, bool]:
    """
    Core Q&A call. Returns (answer_text, was_ambiguous).
    Raises openai.OpenAIError subclasses on failure; caller handles HTTP mapping.
    """
    ambiguous = is_ambiguous(question)
    system_prompt = build_system_prompt(subject, difficulty_level, ambiguous)
    messages = _to_openai_messages(history, question, system_prompt)

    response = _client.chat.completions.create(
        model=OPENAI_MODEL,
        max_tokens=1000,
        messages=messages,
    )

    answer = (response.choices[0].message.content or "").strip()
    return answer, ambiguous
