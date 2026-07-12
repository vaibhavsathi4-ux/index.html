import { useEffect, useRef } from 'react'
import MessageBubble from './MessageBubble.jsx'

export default function ChatThread({ messages, pending, subject }) {
  const endRef = useRef(null)

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth', block: 'end' })
  }, [messages, pending])

  if (messages.length === 0 && !pending) {
    return (
      <div className="thread">
        <div className="thread-empty">
          <div className="thread-empty-title">This page is blank.</div>
          Ask a question about {subject || 'whatever you\u2019re studying'} to start
          filling it in — your tutor will remember what you cover as you go.
        </div>
      </div>
    )
  }

  return (
    <div className="thread">
      {messages.map((m, i) => (
        <MessageBubble
          key={i}
          role={m.role}
          content={m.content}
          createdAt={m.created_at}
          ambiguous={m.is_ambiguous}
        />
      ))}

      {pending && (
        <div className="msg-row tutor">
          <div className="avatar" style={{ background: 'var(--surface-deep)' }} />
          <div className="bubble tutor typing">
            <span />
            <span />
            <span />
          </div>
        </div>
      )}

      <div ref={endRef} />
    </div>
  )
}
