const COR_FALLBACK = { background: '#EDE9FE', color: '#7C3AED' }

export function corBadge(hex) {
  if (!hex || !/^#[0-9a-fA-F]{6}$/.test(hex)) return COR_FALLBACK
  return { background: `${hex}1A`, color: hex }
}

export function linkFichaCamara(id) {
  if (!id) return null
  return `https://www.camara.leg.br/proposicoesWeb/fichadetramitacao?idProposicao=${id}`
}
