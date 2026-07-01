<template>
  <div class="dashboard">
    <div class="container">

      <header class="dashboard-header">
        <div>
          <h1 class="dashboard-title">Dashboard de Monitoramento</h1>
          <p class="dashboard-desc">Acompanhamento de proposições relacionadas à proteção infantil digital.</p>
        </div>
        <div class="header-flags">
          <span v-if="ultimaAtualizacao" class="last-update">
            Última atualização: {{ ultimaAtualizacao }}
          </span>
          <span v-if="periodoTexto" class="last-update">
            Proposições salvas de {{ periodoTexto }}
          </span>
        </div>
      </header>

      <div class="alert-banner" role="status">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/>
          <line x1="12" y1="9" x2="12" y2="13"/>
          <line x1="12" y1="17" x2="12.01" y2="17"/>
        </svg>
        <div class="alert-banner__text">
          <strong>Fique atento:</strong> acompanhe proposições com tramitação ativa relacionadas à proteção infantil digital.
        </div>
        <button type="button" class="alert-banner__btn" @click="$router.push('/busca')">Ver Detalhes</button>
      </div>

      <form class="quick-search" role="search" @submit.prevent="buscarRapido">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <circle cx="11" cy="11" r="8"/>
          <line x1="21" y1="21" x2="16.65" y2="16.65"/>
        </svg>
        <input
          v-model="termoBuscaRapida"
          type="search"
          class="quick-search__input"
          placeholder="Buscar projetos de lei, temas ou instituições..."
          aria-label="Buscar projetos de lei, temas ou instituições"
        />
        <button type="submit" class="quick-search__btn">Buscar</button>
      </form>

      <LoadingSpinner v-if="carregando" />

      <template v-else>
        <div class="stats-grid" aria-label="Estatísticas resumidas">
          <div class="stats-card">
            <div class="stats-card__icon" style="background:#DBEAFE" aria-hidden="true">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/>
                <polyline points="14,2 14,8 20,8"/>
              </svg>
            </div>
            <div class="stats-card__info">
              <span class="stats-value">{{ stats.total ?? '—' }}</span>
              <span class="stats-label">Proposições Monitoradas</span>
            </div>
          </div>

          <div class="stats-card">
            <div class="stats-card__icon" style="background:#D1FAE5" aria-hidden="true">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#059669" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M22 11.08V12a10 10 0 11-5.93-9.14"/>
                <polyline points="22,4 12,14.01 9,11.01"/>
              </svg>
            </div>
            <div class="stats-card__info">
              <span class="stats-value">{{ stats.ativas ?? '—' }}</span>
              <span class="stats-label">Em Tramitação</span>
            </div>
          </div>

          <div class="stats-card">
            <div class="stats-card__icon" style="background:#EDE9FE" aria-hidden="true">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#7C3AED" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="20" x2="18" y2="10"/>
                <line x1="12" y1="20" x2="12" y2="4"/>
                <line x1="6" y1="20" x2="6" y2="14"/>
              </svg>
            </div>
            <div class="stats-card__info">
              <span class="stats-value">{{ stats.subtemas ?? '—' }}</span>
              <span class="stats-label">Subtemas Cobertos</span>
            </div>
          </div>

          <div class="stats-card">
            <div class="stats-card__icon" style="background:#FEE2E2" aria-hidden="true">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#DC2626" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/>
                <line x1="12" y1="9" x2="12" y2="13"/>
                <line x1="12" y1="17" x2="12.01" y2="17"/>
              </svg>
            </div>
            <div class="stats-card__info">
              <span class="stats-value">{{ stats.alertas ?? '—' }}</span>
              <span class="stats-label">Alertas Ativos</span>
            </div>
          </div>
        </div>

        <section id="graficos-secao" class="graficos-section" aria-label="Visualizações de dados">
          <h2 class="section-title">Distribuição por Subtema</h2>
          <div class="graficos-grid">
            <div class="grafico-card">
              <h3 class="grafico-titulo">Proposições por Subtema</h3>
              <GraficoSubtemas
                :subtemas="graficoSubtemas.labels"
                :totais="graficoSubtemas.values"
                :cores="graficoSubtemas.cores"
              />
            </div>
            <div class="grafico-card">
              <h3 class="grafico-titulo">Distribuição por Status</h3>
              <GraficoStatus
                :labels="graficoStatus.labels"
                :values="graficoStatus.values"
              />
            </div>
            <div class="grafico-card grafico-card--wide">
              <h3 class="grafico-titulo">Evolução Temporal</h3>
              <GraficoTemporal
                :meses="graficoTemporal.labels"
                :contagens="graficoTemporal.values"
              />
            </div>
          </div>
        </section>

        <div v-if="erro" class="erro-banner" role="alert">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true">
            <circle cx="12" cy="12" r="10"/>
            <line x1="12" y1="8" x2="12" y2="12"/>
            <line x1="12" y1="16" x2="12.01" y2="16"/>
          </svg>
          {{ erro }}
        </div>

        <section class="quick-actions" aria-label="Ações rápidas">
          <h2 class="section-title">Ações Rápidas</h2>
          <div class="quick-actions-grid">
            <RouterLink to="/busca" class="quick-action-card">
              <div class="quick-action-card__icon" style="background:#DDF7E5" aria-hidden="true">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#059669" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="9" cy="7" r="4"/>
                  <path d="M2 21v-2a4 4 0 014-4h6a4 4 0 014 4v2"/>
                  <path d="M23 21v-2a4 4 0 00-3-3.87"/>
                  <path d="M16 3.13a4 4 0 010 7.75"/>
                </svg>
              </div>
              <div>
                <span class="quick-action-card__title">Participação Pública</span>
                <span class="quick-action-card__desc">Contribua com consultas públicas abertas</span>
              </div>
            </RouterLink>

            <RouterLink to="/analises" class="quick-action-card">
              <div class="quick-action-card__icon" style="background:#F1E4FF" aria-hidden="true">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#7C3AED" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <line x1="18" y1="20" x2="18" y2="10"/>
                  <line x1="12" y1="20" x2="12" y2="4"/>
                  <line x1="6" y1="20" x2="6" y2="14"/>
                </svg>
              </div>
              <div>
                <span class="quick-action-card__title">Análises e Relatórios</span>
                <span class="quick-action-card__desc">Acesse métricas e indicadores legislativos</span>
              </div>
            </RouterLink>

            <RouterLink to="/configuracoes" class="quick-action-card">
              <div class="quick-action-card__icon" style="background:#D9E4FF" aria-hidden="true">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="3"/>
                  <path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 11-2.83 2.83l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-4 0v-.09a1.65 1.65 0 00-1-1.51 1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 11-2.83-2.83l.06-.06a1.65 1.65 0 00.33-1.82 1.65 1.65 0 00-1.51-1H3a2 2 0 010-4h.09a1.65 1.65 0 001.51-1 1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 112.83-2.83l.06.06a1.65 1.65 0 001.82.33H9a1.65 1.65 0 001-1.51V3a2 2 0 014 0v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 112.83 2.83l-.06.06a1.65 1.65 0 00-.33 1.82V9a1.65 1.65 0 001.51 1H21a2 2 0 010 4h-.09a1.65 1.65 0 00-1.51 1z"/>
                </svg>
              </div>
              <div>
                <span class="quick-action-card__title">Configurar Alertas</span>
                <span class="quick-action-card__desc">Receba notificações sobre temas relevantes</span>
              </div>
            </RouterLink>
          </div>
        </section>
      </template>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import GraficoSubtemas from '@/components/charts/GraficoSubtemas.vue'
import GraficoStatus from '@/components/charts/GraficoStatus.vue'
import GraficoTemporal from '@/components/charts/GraficoTemporal.vue'
import { fetchEstatisticas } from '@/services/estatisticas'
import { fetchTemas } from '@/services/temas'

const router = useRouter()
const carregando = ref(true)
const erro = ref(null)
const termoBuscaRapida = ref('')

function buscarRapido() {
  router.push({ path: '/busca', query: termoBuscaRapida.value ? { q: termoBuscaRapida.value } : {} })
}

function formatarDataSimples(isoDate) {
  const [ano, mes, dia] = isoDate.split('-')
  return `${dia}/${mes}/${ano}`
}

const stats = ref({})
const ultimaAtualizacao = ref('')
const periodoTexto = ref('')

const graficoSubtemas = ref({ labels: [], values: [], cores: [] })
const graficoStatus = ref({ labels: [], values: [] })
const graficoTemporal = ref({ labels: [], values: [] })

onMounted(async () => {
  try {
    const [data, temas] = await Promise.all([
      fetchEstatisticas(),
      fetchTemas().catch(() => [])
    ])

    stats.value = data.resumo ?? {}
    ultimaAtualizacao.value = data.ultima_atualizacao
      ? new Date(data.ultima_atualizacao).toLocaleString('pt-BR')
      : ''

    periodoTexto.value = data.periodo
      ? `${formatarDataSimples(data.periodo.data_inicio)} até ${formatarDataSimples(data.periodo.data_fim)}`
      : ''

    const porSubtema = data.por_subtema ?? { labels: [], values: [] }
    const corPorNome = new Map((Array.isArray(temas) ? temas : []).map(t => [t.nome, t.cor]))
    graficoSubtemas.value = {
      ...porSubtema,
      cores: porSubtema.labels.map(nome => corPorNome.get(nome) || null)
    }

    graficoStatus.value = data.por_status ?? { labels: [], values: [] }
    graficoTemporal.value = data.temporal ?? { labels: [], values: [] }
  } catch {
    erro.value = 'Não foi possível carregar as estatísticas. Verifique a conexão com o servidor.'
  } finally {
    carregando.value = false
  }
})
</script>

<style scoped>
.dashboard {
  padding: 28px 20px;
}

.dashboard-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
  margin-bottom: var(--gap);
}

.dashboard-title {
  font-size: 24px;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.02em;
  margin-bottom: 4px;
}

.dashboard-desc {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.6;
}

.header-flags {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 8px;
}

.last-update {
  font-size: 12px;
  color: var(--text-caption);
  background: var(--card);
  border: 1px solid var(--border);
  padding: 7px 14px;
  border-radius: 999px;
  box-shadow: var(--shadow);
  white-space: nowrap;
  align-self: flex-end;
}

.alert-banner {
  display: flex;
  align-items: center;
  gap: 12px;
  background: var(--warning-bg);
  border-left: 4px solid var(--warning-border);
  border-radius: var(--radius);
  padding: 14px 18px;
  margin-bottom: 16px;
  color: var(--warning-text);
}

.alert-banner svg {
  flex-shrink: 0;
}

.alert-banner__text {
  flex: 1;
  font-size: 14px;
  line-height: 1.5;
}

.alert-banner__btn {
  flex-shrink: 0;
  background: #fff;
  border: 1px solid var(--warning-border);
  color: var(--warning-text);
  border-radius: var(--radius);
  padding: 7px 14px;
  font-size: 13px;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  transition: background var(--transition);
}

.alert-banner__btn:hover {
  background: var(--warning-bg);
}

.quick-search {
  display: flex;
  align-items: center;
  gap: 10px;
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 999px;
  padding: 10px 20px;
  margin-bottom: var(--gap);
  color: var(--text-caption);
  box-shadow: var(--shadow);
}

.quick-search__input {
  flex: 1;
  border: none;
  outline: none;
  background: none;
  font-size: 14px;
  font-family: inherit;
  color: var(--text-primary);
}

.quick-search__btn {
  flex-shrink: 0;
  background: var(--primary);
  color: #fff;
  border: none;
  border-radius: 999px;
  padding: 8px 20px;
  font-size: 13px;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  transition: background var(--transition);
}

.quick-search__btn:hover {
  background: var(--primary-light);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: var(--gap);
}

.stats-card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  transition: transform var(--transition), box-shadow var(--transition), border-color var(--transition);
}

.stats-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-hover);
  border-color: var(--primary);
}

.stats-card__icon {
  width: 48px;
  height: 48px;
  border-radius: var(--radius);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stats-card__info {
  display: flex;
  flex-direction: column;
}

.stats-value {
  font-size: 28px;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1;
  letter-spacing: -0.02em;
}

.stats-label {
  font-size: 13px;
  color: var(--text-secondary);
  margin-top: 4px;
}

.graficos-section {
  margin-top: var(--gap);
}

.graficos-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.grafico-card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  padding: 20px;
}

.grafico-card--wide {
  grid-column: 1 / -1;
}

.grafico-titulo {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-secondary);
  margin-bottom: 16px;
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
  margin-top: var(--gap);
}

.quick-actions {
  margin-top: var(--gap);
}

.quick-actions-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.quick-action-card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  text-decoration: none;
  transition: transform var(--transition), box-shadow var(--transition), border-color var(--transition);
}

.quick-action-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-hover);
  border-color: var(--primary);
}

.quick-action-card__icon {
  width: 48px;
  height: 48px;
  border-radius: var(--radius);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.quick-action-card__title {
  display: block;
  font-size: 14px;
  font-weight: 700;
  color: var(--text-primary);
}

.quick-action-card__desc {
  display: block;
  font-size: 12px;
  color: var(--text-secondary);
  margin-top: 4px;
  line-height: 1.4;
}

@media (max-width: 900px) {
  .quick-actions-grid {
    grid-template-columns: 1fr;
  }

  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .graficos-grid {
    grid-template-columns: 1fr;
  }

  .grafico-card--wide {
    grid-column: 1;
  }
}

@media (max-width: 640px) {
  .dashboard-header {
    flex-direction: column;
    gap: 8px;
  }

  .stats-grid {
    gap: 12px;
  }
}
</style>
