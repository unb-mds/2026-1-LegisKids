const BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000'

export async function fetchTemas() {
  const res = await fetch(`${BASE}/api/temas`)
  if (!res.ok) throw new Error(`Erro ${res.status}: ${res.statusText}`)
  return res.json()
}
