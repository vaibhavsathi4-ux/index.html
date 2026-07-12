import { useEffect, useState, useCallback } from 'react'
import { AlertTriangle } from 'lucide-react'
import { api } from './api.js'
import Sidebar from './components/Sidebar.jsx'
import NewSessionModal from './components/NewSessionModal.jsx'
import ChatThread from './components/ChatThread.jsx'
import Composer from './components/Composer.jsx'

const LAST_SESSION_KEY = 'chattutor:lastSessionId'

export default function App() {
  const [sessions, setSessions] = useState([])
  const [activeId, setActiveId] = useState(null)
  const [messages, setMessages] = useState([])
  const [showModal, setShowModal] = useState(false)
  const [creating, setCreating] = useState(false)
  const [pending, setPending] = useState(false)
  const [error, setError] = useState(null)
  const [booting, setBooting] = useState(true)

  const activeSession = sessions.find((s) => s.id === activeId) || null

  // Initial load: fetch sessions, restore last-used session if it still exists.
  useEffect(() => {
    ;(async () => {
      try {
        const list = await api.listSessions()
        setSessions(list)
        const lastId = localStorage.getItem(LAST_SESSION_KEY)
        const restored = list.find((s) => s.id === lastId)
        if (restored) {
          setActiveId(restored.id)
        } else if (list.length > 0) {
          setActiveId(list[0].id)
        }
      } catch (err) {
        setError(err.message)
      } finally {
        setBooting(false)
      }
    })()
  }, [])

  // Load history whenever the active session changes.
  useEffect(() => {
    if (!activeId) {
      setMessages([])
      return
    }
    localStorage.setItem(LAST_SESSION_KEY, activeId)
    ;(async () => {
      try {
        const history = await api.getHistory(activeId)
        setMessages(history)
      } catch (err) {
        setError(err.message)
      }
    })()
  }, [activeId])

  const handleCreateSession = useCallback(async (payload) => {
    setCreating(true)
    setError(null)
    try {
      const session = await api.createSession(payload)
      setSessions((prev) => [session, ...prev])
      setActiveId(session.id)
      setMessages([])
      setShowModal(false)
    } catch (err) {
      setError(err.message)
    } finally {
      setCreating(false)
    }
  }, [])

  const handleSend = useCallback(
    async (question) => {
      if (!activeId) return
      setError(null)
      const optimisticUser = { role: 'user', content: question, created_at: new Date().toISOString() }
      setMessages((prev) => [...prev, optimisticUser])
      setPending(true)
      try {
        const res = await api.ask({ session_id: activeId, question })
        setMessages(res.history)
      } catch (err) {
        setError(err.message)
        // Roll back the optimistic message so it doesn't look like it sent.
        setMessages((prev) => prev.filter((m) => m !== optimisticUser))
      } finally {
        setPending(false)
      }
    },
    [activeId],
  )

  return (
    <div className="app">
      <header className="topbar">
        <div className="brand">
          <div className="brand-mark">
            <svg width="16" height="16" viewBox="0 0 32 32" aria-hidden="true">
              <path
                d="M9 20 L16 10 L23 20"
                stroke="#ffffff"
                strokeWidth="2.5"
                fill="none"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
          </div>
          <div>
            <div className="brand-name">ChatTutor</div>
            <div className="brand-tagline">office hours, on demand</div>
          </div>
        </div>

        {activeSession && (
          <div className="topbar-session">
            <div className="topbar-session-name">{activeSession.student_name || 'Untitled session'}</div>
            <div className="topbar-session-subject">{activeSession.subject || 'general study'}</div>
          </div>
        )}
      </header>

      <div className="layout">
        <Sidebar
          sessions={sessions}
          activeId={activeId}
          onSelect={setActiveId}
          onNew={() => setShowModal(true)}
        />

        <main className="main">
          {error && (
            <div className="error-banner">
              <AlertTriangle size={15} />
              {error}
            </div>
          )}

          {booting ? (
            <div className="thread-empty" style={{ margin: 'auto' }}>
              Loading your sessions…
            </div>
          ) : activeId ? (
            <ChatThread messages={messages} pending={pending} subject={activeSession?.subject} />
          ) : (
            <div className="thread">
              <div className="thread-empty">
                <div className="thread-empty-title">No session selected.</div>
                Start a new session to begin — your tutor will pick up right where you
                left off every time you come back.
              </div>
            </div>
          )}

          <Composer onSend={handleSend} disabled={!activeId || pending} />
        </main>
      </div>

      {showModal && (
        <NewSessionModal
          onCreate={handleCreateSession}
          onClose={() => setShowModal(false)}
          submitting={creating}
        />
      )}
    </div>
  )
}
