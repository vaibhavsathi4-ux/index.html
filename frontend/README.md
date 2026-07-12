# ChatTutor — Frontend (React + Vite)

The chat UI for ChatTutor. "Aurora" look: a deep indigo-violet background,
glass topbar/sidebar, and a violet→blue gradient accent used on the brand
name, buttons, and your own messages. Tutor replies render full Markdown
(bold, tables, code, lists).

## Setup

1. **Install dependencies** (Node 18+ recommended):
   ```bash
   npm install
   ```

2. **Point it at your backend** (only needed if it's not on the default URL):
   ```bash
   cp .env.example .env
   # edit .env if your backend isn't at http://localhost:8000
   ```

3. **Run the dev server**:
   ```bash
   npm run dev
   ```
   Open the URL Vite prints (usually `http://localhost:5173`).

Make sure the FastAPI backend (`../backend`) is running first — see its README.

## What's in here

- `src/App.jsx` — top-level state: sessions, active session, message history,
  error handling
- `src/api.js` — thin fetch wrapper around the backend's REST endpoints
- `src/components/Sidebar.jsx` — session list, styled as colored pill tabs
- `src/components/NewSessionModal.jsx` — create-session form
- `src/components/ChatThread.jsx` / `MessageBubble.jsx` — the conversation
  view; tutor replies render through `react-markdown` + `remark-gfm`
- `src/components/Composer.jsx` — the message input bar
- `src/styles.css` — the whole design system (colors, type, layout) as CSS
  variables

## Design notes

- Sessions are fetched from the backend on load; the last-opened session ID is
  remembered in `localStorage` so refreshing the page doesn't lose your place.
- Ambiguous questions get a small "Quick check" tag above the tutor's reply,
  mirroring the backend's ambiguity flag.
- If the backend is unreachable or returns an error, it shows an inline banner
  instead of failing silently — check that `npm run dev` (frontend) and
  `uvicorn main:app` (backend) are both running if you see this.

## Known limitations (24-hour scope)

- No auth — anyone with a session ID can view/continue it, same as the backend.
- No message editing/deletion.
- Styling is hand-rolled CSS, not a component library — trade-off for a
  distinctive look within a hackathon timeframe.
