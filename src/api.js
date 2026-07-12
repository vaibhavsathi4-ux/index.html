const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

async function request(path, options = {}) {
  let res
  try {
    res = await fetch(`${BASE_URL}${path}`, {
      headers: { 'Content-Type': 'application/json' },
      ...options,
    })
  } catch (err) {
    throw new Error(
      `Can't reach the ChatTutor server at ${BASE_URL}. Is the backend running?`,
    )
  }

  if (!res.ok) {
    let detail = `Request failed (${res.status})`
    try {
      const body = await res.json()
      if (body?.detail) detail = body.detail
    } catch {
      // response wasn't JSON, keep the generic message
    }
    throw new Error(detail)
  }

  if (res.status === 204) return null
  return res.json()
}

export const api = {
  listSessions: () => request('/sessions'),
  createSession: (payload) =>
    request('/session', { method: 'POST', body: JSON.stringify(payload) }),
  getSession: (id) => request(`/session/${id}`),
  getHistory: (id) => request(`/session/${id}/history`),
  ask: (payload) =>
    request('/ask', { method: 'POST', body: JSON.stringify(payload) }),
  deleteSession: (id) => request(`/session/${id}`, { method: 'DELETE' }),
}
