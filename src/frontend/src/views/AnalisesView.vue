<template>
  <div class="analises">
    <div class="container">

      <header class="analises-header">
        <h1 class="analises-title">Análises e Relatórios</h1>
        <p class="analises-desc">Indicadores consolidados sobre as proposições monitoradas pelo LegisKids.</p>
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
              <span class="stats-label">Total de Proposições</span>
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
            <div class="stats-card__icon" style="background:#FFEDD5" aria-hidden="true">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#EA580C" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="4" width="18" height="18" rx="2"/>
                <line x1="16" y1="2" x2="16" y2="6"/>
                <line x1="8" y1="2" x2="8" y2="6"/>
                <line x1="3" y1="10" x2="21" y2="10"/>
              </svg>
            </div>
            <div class="stats-card__info">
              <span class="stats-value stats-value--periodo">{{ periodoTexto || '—' }}</span>
              <span class="stats-label">Período Coberto</span>
            </div>
          </div>
        </div>

        <section class="graficos-section" aria-label="Visualizações de dados">
          <h2 class="section-title">Indicadores</h2>
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
            <div class="grafico-card grafico-card--wide">
              <h3 class="grafico-titulo">Temas ao Longo do Tempo</h3>
              <p class="grafico-subtitulo">Clique em um subtema na legenda para focar apenas nele.</p>
              <GraficoTemasTempo
                :labels="graficoTemasTempo.labels"
                :series="graficoTemasTempo.series"
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

        <div class="nota-futura" role="note">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <path d="M12 2l1.9 5.8L20 9.5l-6.1 1.7L12 17l-1.9-5.8L4 9.5l6.1-1.7L12 2z"/>
            <path d="M19 15l.7 2.1L22 18l-2.3.9L19 21l-.7-2.1L16 18l2.3-.9L19 15z"/>
          </svg>
          <span><strong>Em breve:</strong> novos gráficos e análises serão adicionados a esta página.</span>
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
import GraficoTemasTempo from '@/components/charts/GraficoTemasTempo.vue'
import { fetchEstatisticas } from '@/services/estatisticas'
import { fetchTemas } from '@/services/temas'

const carregando = ref(true)
const erro = ref(null)

function formatarDataSimples(isoDate) {
  const [ano, mes, dia] = isoDate.split('-')
  return `${dia}/${mes}/${ano}`
}

const stats = ref({})
const periodoTexto = ref('')

const graficoSubtemas = ref({ labels: [], values: [], cores: [] })
const graficoStatus = ref({ labels: [], values: [] })
const graficoTemporal = ref({ labels: [], values: [] })
const graficoTemasTempo = ref({ labels: [], series: [] })

onMounted(async () => {
  try {
    const [data, temas] = await Promise.all([
      fetchEstatisticas(),
      fetchTemas().catch(() => [])
    ])

    stats.value = data.resumo ?? {}

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

    const temporalSubtema = data.temporal_por_subtema ?? { labels: [], series: [] }
    graficoTemasTempo.value = {
      labels: temporalSubtema.labels,
      series: (temporalSubtema.series ?? []).map(serie => ({
        ...serie,
        cor: corPorNome.get(serie.nome) || null
      }))
    }
  } catch {
    erro.value = 'Não foi possível carregar as estatísticas. Verifique a conexão com o servidor.'
  } finally {
    carregando.value = false
  }
})
</script>

<style scoped>
.analises {
  padding: 28px 20px;
}

.analises-header {
  margin-bottom: var(--gap);
}

.analises-title {
  font-size: 24px;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.02em;
  margin-bottom: 4px;
}

.analises-desc {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.6;
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
  min-width: 0;
}

.stats-value {
  font-size: 28px;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1;
  letter-spacing: -0.02em;
}

.stats-value--periodo {
  font-size: 15px;
  white-space: nowrap;
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

.grafico-subtitulo {
  font-size: 12px;
  color: var(--text-secondary);
  margin-top: -12px;
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

.nota-futura {
  margin-top: var(--gap);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  font-size: 14px;
  color: var(--primary-dark);
  background: #EFF6FF;
  padding: 18px 20px;
  border-left: 4px solid var(--primary);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
}

.nota-futura svg {
  flex-shrink: 0;
  color: var(--primary);
}

.nota-futura strong {
  font-weight: 700;
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
  .stats-grid {
    gap: 12px;
  }
}
</style>
