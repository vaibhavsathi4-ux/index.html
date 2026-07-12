import { GraduationCap, User } from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

function formatTime(iso) {
  try {
    return new Date(iso).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  } catch {
    return ''
  }
}

export default function MessageBubble({ role, content, createdAt, ambiguous }) {
  const isUser = role === 'user'

  return (
    <div className={`msg-row ${isUser ? 'user' : 'tutor'}`}>
      <div
        className="avatar"
        style={{ background: isUser ? 'var(--accent-gradient)' : 'var(--surface-deep)' }}
      >
        {isUser ? (
          <User size={15} color="#ffffff" />
        ) : (
          <GraduationCap size={15} color="var(--text)" />
        )}
      </div>
      <div style={{ display: 'flex', flexDirection: 'column' }}>
        {!isUser && ambiguous && <span className="ambiguous-chip">Quick check</span>}
        <div className={`bubble ${isUser ? 'user' : 'tutor'}`}>
          {isUser ? (
            content
          ) : (
            <div className="markdown">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>{content}</ReactMarkdown>
            </div>
          )}
        </div>
        {createdAt && <div className="bubble-meta">{formatTime(createdAt)}</div>}
      </div>
    </div>
  )
}
