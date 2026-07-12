import { Plus } from 'lucide-react'

export const TAB_COLORS = ['#8B7CF6', '#60A5FA', '#FB7185', '#34D399', '#FBBF24']

export default function Sidebar({ sessions, activeId, onSelect, onNew }) {
  return (
    <aside className="sidebar">
      <div className="sidebar-heading">Your sessions</div>

      {sessions.length === 0 ? (
        <p className="sidebar-empty">
          No sessions yet. Start one to begin studying with your tutor.
        </p>
      ) : (
        <div className="session-tabs">
          {sessions.map((s, i) => (
            <button
              key={s.id}
              className={`session-tab ${s.id === activeId ? 'active' : ''}`}
              onClick={() => onSelect(s.id)}
            >
              <span
                className="session-tab-chip"
                style={{ background: TAB_COLORS[i % TAB_COLORS.length] }}
              />
              <span className="session-tab-text">
                <span className="session-tab-name">{s.student_name || 'Untitled'}</span>
                <span className="session-tab-subject">{s.subject || 'general'}</span>
              </span>
            </button>
          ))}
        </div>
      )}

      <button className="new-session-btn" onClick={onNew}>
        <Plus size={15} /> New session
      </button>
    </aside>
  )
}
