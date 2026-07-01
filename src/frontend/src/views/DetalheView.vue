<template>
  <div class="detalhe-page">
    <div class="container">

      <LoadingSpinner v-if="carregando" />

      <div v-else-if="erro" class="erro-banner" role="alert">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true">
          <circle cx="12" cy="12" r="10"/>
          <line x1="12" y1="8" x2="12" y2="12"/>
          <line x1="12" y1="16" x2="12.01" y2="16"/>
        </svg>
        {{ erro }}
      </div>

      <template v-else-if="proposicao">

        <!-- Top bar -->
        <div class="top-bar">
          <RouterLink to="/busca" class="top-bar__back">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <polyline points="15,18 9,12 15,6"/>
            </svg>
            Voltar à busca
          </RouterLink>
          <div class="top-bar__actions">
            <a
              v-if="fichaOficialUrl"
              :href="fichaOficialUrl"
              target="_blank"
              rel="noopener noreferrer"
              class="btn-outline btn-outline--primary"
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                <path d="M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6"/>
                <polyline points="15,3 21,3 21,9"/>
                <line x1="10" y1="14" x2="21" y2="3"/>
              </svg>
              Ver PL na Câmara
            </a>
            <button type="button" class="btn-outline" @click="compartilhar">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                <circle cx="18" cy="5" r="3"/>
                <circle cx="6" cy="12" r="3"/>
                <circle cx="18" cy="19" r="3"/>
                <line x1="8.6" y1="10.6" x2="15.4" y2="6.4"/>
                <line x1="8.6" y1="13.4" x2="15.4" y2="17.6"/>
              </svg>
              Compartilhar
              <span v-if="mensagemCompartilhar" class="top-bar__toast">{{ mensagemCompartilhar }}</span>
            </button>
            <button type="button" class="btn-outline" @click="salvar">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                <path d="M19 21l-7-5-7 5V5a2 2 0 012-2h10a2 2 0 012 2z"/>
              </svg>
              Salvar
              <span v-if="mensagemSalvar" class="top-bar__toast">{{ mensagemSalvar }}</span>
            </button>
          </div>
        </div>

        <!-- Cabeçalho -->
        <header class="project-header">
          <div class="project-header__badges">
            <span class="badge badge--id">{{ codigo }}</span>
            <StatusBadge :status="situacaoLabel" />
            <span
              v-for="s in subtemasNormalizados"
              :key="s.nome"
              class="badge"
              :style="{ background: corBadge(s.cor).background, color: corBadge(s.cor).color }"
            >{{ s.nome }}</span>
          </div>
          <h1 class="project-header__title">{{ proposicao.titulo || proposicao.ementa }}</h1>
          <div class="project-header__meta">
            <div class="meta-item">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                <rect x="3" y="4" width="18" height="18" rx="2"/>
                <line x1="16" y1="2" x2="16" y2="6"/>
                <line x1="8" y1="2" x2="8" y2="6"/>
                <line x1="3" y1="10" x2="21" y2="10"/>
              </svg>
              <div>
                <span class="meta-item__label">Data de apresentação</span>
                <span class="meta-item__value">{{ dataFormatada }}</span>
              </div>
            </div>
            <div class="meta-item">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                <path d="M12 3v18M4 7l8-4 8 4M4 7v6a4 4 0 008 0V7M12 13v6a4 4 0 008 0V7"/>
              </svg>
              <div>
                <span class="meta-item__label">Situação atual</span>
                <span class="meta-item__value">{{ situacaoLabel }}</span>
              </div>
            </div>
          </div>
        </header>

        <!-- Abas -->
        <nav class="tabs" role="tablist" aria-label="Seções do projeto">
          <button
            v-for="tab in tabs"
            :key="tab.id"
            type="button"
            class="tab"
            :class="{ 'tab--active': abaAtiva === tab.id }"
            role="tab"
            :aria-selected="abaAtiva === tab.id"
            @click="abaAtiva = tab.id"
          >
            {{ tab.label }}
          </button>
        </nav>

        <div class="content-grid">
          <div class="main-column">

            <template v-if="abaAtiva === 'visao-geral'">
              <div class="card">
                <h2 class="card__title">Sobre o projeto</h2>
                <div class="card__body" :class="{ collapsed: !sobreExpandido }">
                  <p>{{ proposicao.ementa || proposicao.titulo || 'Ementa não disponível.' }}</p>
                </div>
                <button type="button" class="btn-expand" @click="sobreExpandido = !sobreExpandido">
                  {{ sobreExpandido ? 'Ver menos' : 'Ver mais' }}
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" :style="{ transform: sobreExpandido ? 'rotate(180deg)' : 'none' }" aria-hidden="true">
                    <polyline points="6,9 12,15 18,9"/>
                  </svg>
                </button>
              </div>

              <div class="card">
                <h2 class="card__title">Informações do projeto</h2>
                <div class="info-grid">
                  <div class="info-cell">
                    <span class="info-cell__label">Partido</span>
                    <span class="info-cell__value">{{ partidoLabel || 'Não informado' }}</span>
                  </div>
                  <div class="info-cell">
                    <span class="info-cell__label">Data de apresentação</span>
                    <span class="info-cell__value">{{ dataFormatada }}</span>
                  </div>
                  <div class="info-cell">
                    <span class="info-cell__label">Situação atual</span>
                    <span class="info-cell__value">{{ situacaoLabel }}</span>
                  </div>
                </div>
              </div>

              <div class="card">
                <h2 class="card__title">Objetivos do projeto</h2>
                <div class="empty-state">
                  <p>Objetivos ainda não disponíveis para esta proposição.</p>
                </div>
              </div>

              <div class="card">
                <h2 class="card__title">Projetos relacionados</h2>
                <div v-if="relacionados.length" class="related-grid">
                <RouterLink
                  v-for="r in relacionados"
                  :key="r.id"
                  :to="{ name: 'detalhe', params: { id: r.id } }"
                  class="related-card"
                >
                  <span class="badge badge--id">{{ codigoRelacionado(r) }}</span>

                  <p class="related-card__title">
                    {{ r.titulo || r.ementa }}
                  </p>

                  <StatusBadge
                    :status="r.status || r.descricao_situacao || 'Em tramitação'"
                  />
                </RouterLink>
              </div>
                <div v-else class="empty-state">
                  <p>Nenhum projeto relacionado disponível no momento.</p>
                </div>
              </div>
            </template>

            <template v-else-if="abaAtiva === 'tramitacao'">
              <div class="card">
                <h2 class="card__title">Histórico de tramitação</h2>
                <ol v-if="tramitacoes.length" class="timeline-full" aria-label="Histórico de tramitação">
                  <li v-for="(t, i) in tramitacoes" :key="i" class="timeline-full-item">
                    <div class="timeline-full-dot" aria-hidden="true"></div>
                    <div class="timeline-full-content">
                      <span class="timeline-full-data">{{ formatarData(t.data || t.dataHora) }}</span>
                      <p class="timeline-full-desc">{{ t.descricao || t.descricaoSituacao || t.despacho }}</p>
                      <span v-if="t.orgao || t.siglaOrgao" class="timeline-full-orgao">{{ t.orgao || t.siglaOrgao }}</span>
                    </div>
                  </li>
                </ol>
                <div v-else class="empty-state">
                  <p>Nenhuma tramitação registrada para esta proposição.</p>
                </div>
              </div>
            </template>

            <template v-else-if="abaAtiva === 'analise'">
              <div class="card">
                <h2 class="card__title">Análise e indicadores</h2>
                <div class="empty-state">
                  <p>Indicadores de relevância, impacto social e apoio popular ainda não estão disponíveis.</p>
                </div>
              </div>
            </template>

            <template v-else-if="abaAtiva === 'documentos'">
              <div class="card">
                <h2 class="card__title">Documentos e anexos</h2>
                <div v-if="fichaOficialUrl" class="doc-list">
                  <div class="doc-item">
                    <div class="doc-item__icon" aria-hidden="true">
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6"/>
                        <polyline points="15,3 21,3 21,9"/>
                        <line x1="10" y1="14" x2="21" y2="3"/>
                      </svg>
                    </div>
                    <div class="doc-item__info">
                      <span class="doc-item__name">Ficha oficial da proposição</span>
                      <span class="doc-item__meta">camara.leg.br</span>
                    </div>
                    <a :href="fichaOficialUrl" target="_blank" rel="noopener noreferrer" class="btn-download">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                        <path d="M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6"/>
                        <polyline points="15,3 21,3 21,9"/>
                        <line x1="10" y1="14" x2="21" y2="3"/>
                      </svg>
                      Abrir
                    </a>
                  </div>
                </div>
                <div v-else class="empty-state">
                  <p>Nenhum documento disponível para esta proposição.</p>
                </div>
              </div>
            </template>

            <template v-else-if="abaAtiva === 'comentarios'">
              <div class="card">
                <h2 class="card__title">Comentários</h2>
                <div class="empty-state">
                  <p>A funcionalidade de comentários ainda não está disponível.</p>
                </div>
              </div>
            </template>

          </div>

          <aside class="sidebar-column">
            <div class="card sidebar-card">
              <div class="sidebar-card__header">
                <h3>Status da tramitação</h3>
                <StatusBadge :status="situacaoLabel" />
              </div>
              <p class="sidebar-card__subtitle">Acompanhe o andamento do projeto</p>

              <ol v-if="tramitacoesResumo.length" class="timeline">
                <li v-for="(t, i) in tramitacoesResumo" :key="i" class="timeline-item">
                  <div class="timeline-node" aria-hidden="true">
                    <svg v-if="i === 0" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
                      <polyline points="20,6 9,17 4,12"/>
                    </svg>
                  </div>
                  <div class="timeline-content">
                    <span class="timeline-content__title">{{ t.descricao || t.descricaoSituacao || t.despacho }}</span>
                    <span class="timeline-content__date">{{ formatarData(t.data || t.dataHora) }}</span>
                  </div>
                </li>
              </ol>
              <div v-else class="empty-state empty-state--compact">
                <p>Sem tramitações registradas.</p>
              </div>

              <button type="button" class="sidebar-card__link" @click="abaAtiva = 'tramitacao'">
                Ver tramitação completa
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                  <polyline points="9,18 15,12 9,6"/>
                </svg>
              </button>
            </div>

            <div class="card sidebar-card">
              <h3>Análise e indicadores</h3>
              <div class="empty-state empty-state--compact">
                <p>Indicadores ainda não disponíveis.</p>
              </div>
              <button type="button" class="sidebar-card__link" @click="abaAtiva = 'analise'">
                Ver análise detalhada
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                  <polyline points="9,18 15,12 9,6"/>
                </svg>
              </button>
            </div>

            <div class="card sidebar-card">
              <h3>Compartilhe este projeto</h3>
              <p class="sidebar-card__subtitle">Ajude a divulgar informações importantes sobre esse projeto de lei</p>
              <div class="share-buttons">
                <button type="button" class="share-btn" aria-label="Copiar link" @click="copiarLink">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                    <path d="M10 13a5 5 0 007.07 0l2.83-2.83a5 5 0 00-7.07-7.07l-1.5 1.5"/>
                    <path d="M14 11a5 5 0 00-7.07 0L4.1 13.83a5 5 0 007.07 7.07l1.5-1.5"/>
                  </svg>
                </button>
                <button type="button" class="share-btn" aria-label="Compartilhar no WhatsApp" @click="abrirWhatsapp">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                    <path d="M21 11.5a8.38 8.38 0 01-.9 3.8 8.5 8.5 0 01-7.6 4.7 8.38 8.38 0 01-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 01-.9-3.8 8.5 8.5 0 014.7-7.6 8.38 8.38 0 013.8-.9h.5a8.48 8.48 0 018 8v.5z"/>
                  </svg>
                </button>
                <button type="button" class="share-btn" aria-label="Compartilhar no Twitter/X" @click="abrirTwitter">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                    <line x1="18" y1="6" x2="6" y2="18"/>
                    <line x1="6" y1="6" x2="18" y2="18"/>
                  </svg>
                </button>
                <button type="button" class="share-btn" aria-label="Compartilhar no Facebook" @click="abrirFacebook">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                    <path d="M18 2h-3a5 5 0 00-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 011-1h3z"/>
                  </svg>
                </button>
              </div>
            </div>
          </aside>
        </div>

      </template>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import StatusBadge from '@/components/StatusBadge.vue'
import { fetchProposicao, fetchProposicoes } from '@/services/proposicoes'
import { corBadge, linkFichaCamara } from '@/utils/proposicao'

const route = useRoute()
const carregando = ref(true)
const erro = ref(null)
const proposicao = ref(null)
const tramitacoes = ref([])
const relacionados = ref([])

const abaAtiva = ref('visao-geral')
const sobreExpandido = ref(false)
const mensagemCompartilhar = ref('')
const mensagemSalvar = ref('')

const tabs = [
  { id: 'visao-geral', label: 'Visão geral' },
  { id: 'tramitacao', label: 'Tramitação' },
  { id: 'analise', label: 'Análise' },
  { id: 'documentos', label: 'Documentos' },
  { id: 'comentarios', label: 'Comentários' }
]

const dataFormatada = computed(() => {
  const d = proposicao.value?.data || proposicao.value?.data_apresentacao
  if (!d) return 'Não informada'
  try { return new Date(d).toLocaleDateString('pt-BR') } catch { return d }
})

const partidoLabel = computed(() => {
  const p = proposicao.value
  if (!p) return ''
  if (p.partido && typeof p.partido === 'object') {
    return p.partido.sigla || p.partido.nome || ''
  }
  return p.partido || p.sigla_partido || ''
})

const situacaoLabel = computed(() => proposicao.value?.status || proposicao.value?.descricao_situacao || 'Em tramitação')

const subtemasNormalizados = computed(() => proposicao.value?.categorias ?? [])

const fichaOficialUrl = computed(() => linkFichaCamara(proposicao.value?.id))

const codigo = computed(() => {
  const p = proposicao.value
  if (!p) return ''
  if (p.sigla_tipo && p.numero && p.ano) {
    return `${p.sigla_tipo} ${p.numero}/${p.ano}`
  }
  return p.id
})

const tramitacoesResumo = computed(() => tramitacoes.value.slice(0, 4))

function formatarData(d) {
  if (!d) return '—'
  try { return new Date(d).toLocaleDateString('pt-BR') } catch { return d }
}

function codigoRelacionado(r) {
  if (r.sigla_tipo && r.numero && r.ano) {
    return `${r.sigla_tipo} ${r.numero}/${r.ano}`
  }
  return r.id
}

function mostrarToast(alvo, texto) {
  alvo.value = texto
  setTimeout(() => { alvo.value = '' }, 2000)
}

async function compartilhar() {
  const url = window.location.href
  if (navigator.share) {
    try {
      await navigator.share({ title: proposicao.value?.titulo || codigo.value, url })
      return
    } catch {
      // usuário cancelou o compartilhamento nativo — não é erro
      return
    }
  }
  await copiarLink()
}

async function copiarLink() {
  try {
    await navigator.clipboard.writeText(window.location.href)
    mostrarToast(mensagemCompartilhar, 'Link copiado!')
  } catch {
    mostrarToast(mensagemCompartilhar, 'Copie o link da barra de endereço')
  }
}

function abrirWhatsapp() {
  window.open(`https://wa.me/?text=${encodeURIComponent(window.location.href)}`, '_blank', 'noopener')
}

function abrirTwitter() {
  const texto = proposicao.value?.titulo || codigo.value
  window.open(`https://twitter.com/intent/tweet?url=${encodeURIComponent(window.location.href)}&text=${encodeURIComponent(texto)}`, '_blank', 'noopener')
}

function abrirFacebook() {
  window.open(`https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(window.location.href)}`, '_blank', 'noopener')
}

function salvar() {
  mostrarToast(mensagemSalvar, 'Disponível em breve')
}

function excluirAtual(lista) {
  return lista.filter(p => String(p.id) !== String(proposicao.value?.id))
}

async function carregarRelacionados() {
  const p = proposicao.value
  if (!p) return

  const primeiroSubtema = subtemasNormalizados.value[0]?.nome

  try {
    if (primeiroSubtema) {
      const data = await fetchProposicoes({ subtema: primeiroSubtema }, 1, 4)
      const encontrados = excluirAtual(data.items ?? [])
      if (encontrados.length > 0) {
        relacionados.value = encontrados.slice(0, 3)
        return
      }
    }

    if (p.sigla_partido) {
      const data = await fetchProposicoes({ partido: p.sigla_partido }, 1, 4)
      relacionados.value = excluirAtual(data.items ?? []).slice(0, 3)
    }
  } catch {
    // relacionados são complementares — falha silenciosa mantém estado vazio
  }
}

async function carregarProposicao(id) {
  carregando.value = true
  erro.value = null

  try {
    const data = await fetchProposicao(id)

    proposicao.value = data.proposicao ?? data
    tramitacoes.value = data.tramitacoes ?? []

    await carregarRelacionados()
  } catch (e) {
    erro.value = e.message?.includes('404')
      ? 'Proposição não encontrada.'
      : 'Não foi possível carregar a proposição. Verifique a conexão com o servidor.'
  } finally {
    carregando.value = false
  }
}

onMounted(() => {
  carregarProposicao(route.params.id)
})
watch(
  () => route.params.id,
  (novoId) => {
    carregarProposicao(novoId)
  }
)

</script>

<style scoped>
.detalhe-page {
  --d-primary: #2B3FBF;
  --d-primary-hover: #1E2E99;
  --d-primary-light-bg: #E8ECFB;
  --d-card-bg: #FFFFFF;
  --d-text-primary: #0F172A;
  --d-text-secondary: #475569;
  --d-text-caption: #64748B;
  --d-border: #D1D9E6;
  --d-border-light: #E8ECF4;
  padding: 24px 20px 40px;
}

.erro-banner {
  display: flex;
  align-items: center;
  gap: 10px;
  background: var(--warning-bg);
  border-left: 4px solid var(--warning-border);
  border-radius: var(--radius);
  padding: 14px 18px;
  font-size: 14px;
  color: var(--warning-text);
}

/* Top bar */
.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 4px 0 16px;
  flex-wrap: wrap;
  gap: 12px;
}

.top-bar__back {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--d-primary);
  font-size: 14px;
  font-weight: 500;
}

.top-bar__back:hover {
  text-decoration: underline;
}

.top-bar__actions {
  display: flex;
  gap: 12px;
}

.btn-outline {
  position: relative;
  display: flex;
  align-items: center;
  gap: 8px;
  background: #FFFFFF;
  border: 1px solid var(--d-border);
  border-radius: 8px;
  padding: 8px 16px;
  font-size: 14px;
  font-weight: 500;
  color: #374151;
  cursor: pointer;
  font-family: inherit;
  transition: background 0.15s ease;
}

.btn-outline:hover {
  background: #F1F5F9;
}

.btn-outline--primary {
  background: var(--d-primary);
  border-color: var(--d-primary);
  color: #fff;
  text-decoration: none;
}

.btn-outline--primary:hover {
  background: var(--d-primary-hover);
}

.top-bar__toast {
  position: absolute;
  top: calc(100% + 6px);
  right: 0;
  background: var(--d-text-primary);
  color: #fff;
  font-size: 12px;
  font-weight: 500;
  padding: 4px 10px;
  border-radius: 6px;
  white-space: nowrap;
}

/* Cabeçalho */
.project-header {
  padding: 8px 0 24px;
}

.project-header__badges {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.badge {
  font-size: 12px;
  font-weight: 600;
  padding: 5px 14px;
  border-radius: 999px;
}

.badge--id {
  background: var(--d-primary-light-bg);
  color: var(--d-primary);
  font-family: 'IBM Plex Mono', monospace;
}

.badge--topic {
  background: var(--purple-bg);
  color: var(--purple-text);
}

.project-header__title {
  font-size: 28px;
  font-weight: 700;
  color: var(--d-text-primary);
  line-height: 1.25;
  margin-bottom: 20px;
}

.project-header__meta {
  display: flex;
  gap: 40px;
  flex-wrap: wrap;
}

.meta-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  color: #94A3B8;
}

.meta-item__label {
  display: block;
  font-size: 12px;
  color: var(--d-text-caption);
}

.meta-item__value {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: var(--d-text-primary);
}

/* Tabs */
.tabs {
  display: flex;
  gap: 0;
  background: var(--d-card-bg);
  border-radius: 12px;
  padding: 0 8px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.06);
  overflow-x: auto;
  margin-bottom: 20px;
}

.tab {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 16px 20px;
  font-size: 15px;
  font-weight: 500;
  color: var(--d-text-caption);
  background: none;
  border: none;
  cursor: pointer;
  border-bottom: 3px solid transparent;
  white-space: nowrap;
  font-family: inherit;
  transition: color 0.2s, border-color 0.2s;
}

.tab:hover {
  color: var(--d-primary);
  background: #F8F9FF;
}

.tab--active {
  color: var(--d-primary);
  border-bottom: 3px solid var(--d-primary);
  font-weight: 600;
}

/* Content grid */
.content-grid {
  display: flex;
  gap: 24px;
  align-items: flex-start;
}

.main-column {
  flex: 1 1 0;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.sidebar-column {
  width: 320px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.card {
  background: var(--d-card-bg);
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}

.related-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
}

.related-card {
  display: flex;
  flex-direction: column;
  text-decoration: none;
  color: inherit;
  align-items: flex-start;
  gap: 8px;
  background: #F8FAFC;
  border: 1px solid #E2E8F0;
  border-radius: 10px;
  padding: 12px 14px;
  text-align: left;
  cursor: pointer;
  font-family: inherit;
  transition: border-color 0.15s ease, box-shadow 0.15s ease;
}

.related-card:hover {
  border-color: var(--d-primary);
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

.related-card__title {
  font-size: 13px;
  font-weight: 600;
  color: var(--d-text-primary);
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card__title {
  font-size: 18px;
  font-weight: 700;
  color: var(--d-text-primary);
  margin-bottom: 16px;
}

.card__body {
  font-size: 14px;
  color: var(--d-text-secondary);
  line-height: 1.6;
}

.card__body.collapsed {
  max-height: 4.8em;
  overflow: hidden;
}

.btn-expand {
  display: flex;
  align-items: center;
  gap: 6px;
  background: none;
  border: none;
  color: var(--d-primary);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  margin-top: 12px;
  padding: 0;
  font-family: inherit;
}

.btn-expand:hover {
  text-decoration: underline;
}

.btn-expand svg {
  transition: transform 0.2s ease;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.info-cell {
  background: #F8FAFC;
  border: 1px solid #E2E8F0;
  border-radius: 8px;
  padding: 12px 16px;
}

.info-cell__label {
  display: block;
  font-size: 12px;
  color: var(--d-text-caption);
  margin-bottom: 4px;
}

.info-cell__value {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: var(--d-text-primary);
}

.empty-state {
  text-align: center;
  padding: 28px 16px;
  color: var(--d-text-secondary);
  font-size: 14px;
  background: #F8FAFC;
  border: 1px dashed var(--d-border);
  border-radius: 8px;
}

.empty-state--compact {
  padding: 16px;
  font-size: 13px;
}

/* Documentos */
.doc-list {
  display: flex;
  flex-direction: column;
}

.doc-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 0;
}

.doc-item__icon {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  background: #FEE2E2;
  color: #EF4444;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.doc-item__info {
  flex: 1;
  min-width: 0;
}

.doc-item__name {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: var(--d-text-primary);
}

.doc-item__meta {
  display: block;
  font-size: 12px;
  color: var(--d-text-caption);
  margin-top: 2px;
}

.btn-download {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #FFFFFF;
  border: 1px solid var(--d-border);
  border-radius: 8px;
  padding: 8px 16px;
  font-size: 14px;
  font-weight: 500;
  color: #374151;
  white-space: nowrap;
}

.btn-download:hover {
  background: #F1F5F9;
}

/* Timeline completa (aba Tramitação) */
.timeline-full {
  list-style: none;
  position: relative;
  padding-left: 28px;
}

.timeline-full::before {
  content: '';
  position: absolute;
  left: 7px;
  top: 8px;
  bottom: 8px;
  width: 2px;
  background: var(--d-border);
}

.timeline-full-item {
  position: relative;
  padding-bottom: 24px;
}

.timeline-full-item:last-child {
  padding-bottom: 0;
}

.timeline-full-dot {
  position: absolute;
  left: -24px;
  top: 4px;
  width: 14px;
  height: 14px;
  background: var(--d-primary);
  border: 2px solid #fff;
  border-radius: 50%;
  box-shadow: 0 0 0 2px var(--d-border);
}

.timeline-full-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.timeline-full-data {
  font-size: 12px;
  font-weight: 600;
  color: var(--d-text-caption);
}

.timeline-full-desc {
  font-size: 14px;
  color: var(--d-text-primary);
  line-height: 1.5;
}

.timeline-full-orgao {
  font-size: 12px;
  font-weight: 600;
  color: var(--d-primary);
  background: var(--d-primary-light-bg);
  padding: 2px 8px;
  border-radius: 4px;
  align-self: flex-start;
}

/* Sidebar */
.sidebar-card__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.sidebar-card h3 {
  font-size: 15px;
  font-weight: 700;
  color: var(--d-text-primary);
  margin-bottom: 4px;
}

.sidebar-card__subtitle {
  font-size: 12px;
  color: var(--d-text-caption);
  margin-bottom: 20px;
  line-height: 1.5;
}

.timeline {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 0;
  margin-bottom: 8px;
}

.timeline-item {
  display: flex;
  gap: 12px;
  position: relative;
}

.timeline-item:not(:last-child)::before {
  content: '';
  position: absolute;
  left: 11px;
  top: 24px;
  bottom: -8px;
  width: 2px;
  background: var(--d-border);
}

.timeline-node {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  border: 2px solid var(--d-primary);
  background: var(--d-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  z-index: 1;
}

.timeline-content {
  padding-bottom: 20px;
  flex: 1;
  min-width: 0;
}

.timeline-content__title {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: var(--d-text-primary);
}

.timeline-content__date {
  display: block;
  font-size: 12px;
  color: var(--d-text-caption);
  margin-top: 2px;
}

.sidebar-card__link {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  padding: 12px 0 0;
  border-top: 1px solid var(--d-border-light);
  margin-top: 4px;
  font-size: 14px;
  font-weight: 500;
  color: var(--d-primary);
  background: none;
  border-left: none;
  border-right: none;
  border-bottom: none;
  cursor: pointer;
  font-family: inherit;
}

.sidebar-card__link:hover {
  text-decoration: underline;
}

.share-buttons {
  display: flex;
  gap: 8px;
}

.share-btn {
  width: 44px;
  height: 44px;
  border-radius: 8px;
  background: #F1F5F9;
  border: 1px solid #E2E8F0;
  color: var(--d-text-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background 0.15s;
}

.share-btn:hover {
  background: #E2E8F0;
}

@media (max-width: 1024px) {
  .content-grid {
    flex-direction: column;
  }

  .sidebar-column {
    width: 100%;
  }

  .info-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 640px) {
  .project-header__title {
    font-size: 22px;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }

  .top-bar {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
