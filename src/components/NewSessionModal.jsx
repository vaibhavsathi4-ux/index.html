import { useState } from 'react'

export default function NewSessionModal({ onCreate, onClose, submitting }) {
  const [name, setName] = useState('')
  const [subject, setSubject] = useState('')

  function handleSubmit(e) {
    e.preventDefault()
    onCreate({ student_name: name.trim() || undefined, subject: subject.trim() || undefined })
  }

  return (
    <div className="modal-overlay" onMouseDown={(e) => e.target === e.currentTarget && onClose()}>
      <div className="modal-card">
        <h2 className="modal-title">Start a session</h2>
        <p className="modal-sub">Give your tutor a little context to work with.</p>

        <form onSubmit={handleSubmit}>
          <div className="field">
            <label htmlFor="student_name">Your name (optional)</label>
            <input
              id="student_name"
              autoFocus
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="e.g. Alex"
            />
          </div>

          <div className="field">
            <label htmlFor="subject">What are you studying?</label>
            <input
              id="subject"
              value={subject}
              onChange={(e) => setSubject(e.target.value)}
              placeholder="e.g. Python loops, algebra, cell biology"
            />
          </div>

          <div className="modal-actions">
            <button type="button" className="btn btn-ghost" onClick={onClose}>
              Cancel
            </button>
            <button type="submit" className="btn btn-primary" disabled={submitting}>
              {submitting ? 'Starting…' : 'Start session'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
