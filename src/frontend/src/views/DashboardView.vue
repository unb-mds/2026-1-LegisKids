<template>
  <div class="dashboard">
    <div class="container">

      <header class="dashboard-header">
        <div>
          <h1 class="dashboard-title">Dashboard de Monitoramento</h1>
          <p class="dashboard-desc">Acompanhamento de proposições relacionadas à proteção infantil digital.</p>
        </div>
        <span v-if="ultimaAtualizacao" class="last-update">
          Última atualização: {{ ultimaAtualizacao }}
        </span>
      </header>

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

        <section class="graficos-section" aria-label="Visualizações de dados">
          <h2 class="section-title">Distribuição por Subtema</h2>
          <div class="graficos-grid">
            <div class="grafico-card">
              <h3 class="grafico-titulo">Proposições por Subtema</h3>
              <GraficoSubtemas
                :subtemas="graficoSubtemas.labels"
                :totais="graficoSubtemas.values"
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
      </template>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import GraficoSubtemas from '@/components/charts/GraficoSubtemas.vue'
import GraficoStatus from '@/components/charts/GraficoStatus.vue'
import GraficoTemporal from '@/components/charts/GraficoTemporal.vue'
import { fetchEstatisticas } from '@/services/estatisticas'

const carregando = ref(true)
const erro = ref(null)

const stats = ref({})
const ultimaAtualizacao = ref('')

const graficoSubtemas = ref({ labels: [], values: [] })
const graficoStatus = ref({ labels: [], values: [] })
const graficoTemporal = ref({ labels: [], values: [] })

onMounted(async () => {
  try {
    const data = await fetchEstatisticas()
    stats.value = data.resumo ?? {}
    ultimaAtualizacao.value = data.ultima_atualizacao
      ? new Date(data.ultima_atualizacao).toLocaleString('pt-BR')
      : ''
    graficoSubtemas.value = data.por_subtema ?? { labels: [], values: [] }
    graficoStatus.value = data.por_status ?? { labels: [], values: [] }
    graficoTemporal.value = data.temporal ?? { labels: [], values: [] }
  } catch (e) {
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

.last-update {
  font-size: 12px;
  color: var(--text-caption);
  background: var(--card);
  border: 1px solid var(--border);
  padding: 7px 14px;
  border-radius: 999px;
  box-shadow: var(--shadow);
  white-space: nowrap;
  align-self: flex-start;
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

@media (max-width: 900px) {
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
