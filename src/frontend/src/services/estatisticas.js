const BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000'

export async function fetchEstatisticas() {
  const res = await fetch(`${BASE}/api/estatisticas`)
  if (!res.ok) throw new Error(`Erro ${res.status}: ${res.statusText}`)
  return res.json()
}
