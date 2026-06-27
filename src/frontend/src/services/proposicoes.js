const BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000'

export async function fetchProposicoes(filtros = {}, pagina = 1, porPagina = 10) {
  const params = new URLSearchParams()
  params.set('pagina', pagina)
  params.set('por_pagina', porPagina)
  if (filtros.termo) params.set('q', filtros.termo)
  if (filtros.parlamentar) params.set('parlamentar', filtros.parlamentar)
  if (filtros.partido) params.set('partido', filtros.partido)
  if (filtros.dataInicio) params.set('data_inicio', filtros.dataInicio)
  if (filtros.dataFim) params.set('data_fim', filtros.dataFim)
  if (filtros.subtema) params.set('subtema', filtros.subtema)

  const res = await fetch(`${BASE}/api/proposicoes?${params}`)
  if (!res.ok) throw new Error(`Erro ${res.status}: ${res.statusText}`)
  return res.json()
}

export async function fetchProposicao(id) {
  const res = await fetch(`${BASE}/api/proposicoes/${id}`)
  if (!res.ok) throw new Error(`Erro ${res.status}: ${res.statusText}`)
  return res.json()
}
