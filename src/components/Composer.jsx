import { useState, useRef } from 'react'
import { ArrowUp } from 'lucide-react'

export default function Composer({ onSend, disabled }) {
  const [value, setValue] = useState('')
  const taRef = useRef(null)

  function submit() {
    const trimmed = value.trim()
    if (!trimmed || disabled) return
    onSend(trimmed)
    setValue('')
    if (taRef.current) taRef.current.style.height = 'auto'
  }

  function handleKeyDown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      submit()
    }
  }

  function handleInput(e) {
    setValue(e.target.value)
    e.target.style.height = 'auto'
    e.target.style.height = `${Math.min(e.target.scrollHeight, 140)}px`
  }

  return (
    <div className="composer">
      <div className="composer-inner">
        <textarea
          ref={taRef}
          rows={1}
          placeholder="Ask your tutor anything…"
          value={value}
          onChange={handleInput}
          onKeyDown={handleKeyDown}
          disabled={disabled}
        />
        <button className="send-btn" onClick={submit} disabled={disabled || !value.trim()}>
          <ArrowUp size={17} />
        </button>
      </div>
      <div className="composer-hint">Enter to send · Shift + Enter for a new line</div>
    </div>
  )
}
