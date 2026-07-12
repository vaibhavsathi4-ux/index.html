# ChatTutor — Backend (FastAPI)

AI tutor backend for the ChatTutor hackathon project. MVP scope: **Q&A with per-session
context memory**, plus a simple **adaptive difficulty** signal as a bonus feature.

## Features implemented

- `POST /ask` — ask a question, get a tutor response grounded in the session's history
- Context memory — each session's last N messages are replayed to the LLM so the tutor
  remembers what was discussed
- Ambiguous query handling — very short/vague questions (e.g. "this?", "help") are
  flagged, and the tutor is instructed to ask a clarifying question instead of guessing
- Adaptive difficulty (bonus) — a lightweight heuristic nudges a per-session
  `difficulty_level` up or down based on phrases like "makes sense" or "I'm confused"
- Persistent history — SQLite via SQLAlchemy, so history/memory survives server restarts

## Project structure

```
chattutor-backend/
├── main.py          # FastAPI app + routes
├── llm_service.py    # LLM calls, prompt building, ambiguity check, adaptive logic
├── models.py         # SQLAlchemy models: TutorSession, Message
├── schemas.py         # Pydantic request/response schemas
├── database.py       # DB engine/session setup
├── requirements.txt
└── .env.example
```

## Setup

1. **Install dependencies** (Python 3.10+ recommended):
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure your API key**:
   ```bash
   cp .env.example .env
   # then edit .env and set OPENAI_API_KEY=sk-...
   ```

3. **Run the server**:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

4. Open the interactive API docs at `http://localhost:8000/docs`.

A `chattutor.db` SQLite file will be created automatically in the project folder on
first run — no manual migration step needed for the MVP.

## API reference

### `POST /session`
Create a new tutoring session.
```json
// request
{ "student_name": "Alex", "subject": "python loops" }

// response
{ "id": "uuid", "student_name": "Alex", "subject": "python loops",
  "difficulty_level": 1.0, "created_at": "..." }
```

### `POST /ask`
Ask a question inside a session. Automatically stores both the question and the
tutor's answer, and updates `difficulty_level`.
```json
// request
{ "session_id": "uuid", "question": "What is a for loop?" }

// response
{ "session_id": "uuid", "answer": "...", "is_ambiguous": false,
  "difficulty_level": 1.0, "history": [ { "role": "user", "content": "...", "created_at": "..." }, ... ] }
```

### `GET /sessions`
List all sessions (most recent first) — used by the frontend to populate the sidebar.

### `GET /session/{session_id}`
Fetch session metadata (subject, difficulty level, etc).

### `GET /session/{session_id}/history`
Fetch the full message history for a session.

### `DELETE /session/{session_id}`
Delete a session and its history.

### `GET /health`
Basic liveness check.

## Design notes / known limitations (for judges)

- **Context window**: only the last `CONTEXT_WINDOW_MESSAGES` (default 12) messages are
  sent back to the LLM per request, to control token usage. For very long tutoring
  sessions this means older context can drop off — a good "next step" would be
  summarizing older turns instead of truncating them.
- **Ambiguity detection** is a simple heuristic (message length/keyword based), not a
  classifier. It's meant to demonstrate handling of the "ambiguous queries" edge case
  within a 24-hour scope.
- **Adaptive difficulty** is a rule-based stub (keyword nudges), intentionally simple so
  it's easy to replace with a real signal (e.g. quiz correctness, response latency)
  after the hackathon.
- **Model**: defaults to `gpt-4o-mini` via `OPENAI_MODEL` in `.env` — swap in `gpt-4o`
  or another chat-completions-compatible model if your friend's key supports it.
- **CORS is wide open** (`allow_origins=["*"]`) for ease of frontend integration during
  the hackathon — restrict this before any real deployment.
- **Auth**: there's no user authentication layer; `session_id` alone gates access to a
  session's history. Fine for a demo, not for production.

## Example curl flow

```bash
# 1. Create a session
curl -X POST http://localhost:8000/session \
  -H "Content-Type: application/json" \
  -d '{"student_name": "Alex", "subject": "python loops"}'

# 2. Ask a question (use the session_id returned above)
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"session_id": "<SESSION_ID>", "question": "What is a for loop?"}'

# 3. Ask a follow-up — the tutor will remember the previous exchange
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"session_id": "<SESSION_ID>", "question": "Can you show an example in Python?"}'
```
