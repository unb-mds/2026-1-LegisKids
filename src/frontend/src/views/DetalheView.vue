<template>
  <div class="detalhe">
    <div class="container">

      <RouterLink to="/busca" class="back-link">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true">
          <polyline points="15,18 9,12 15,6"/>
        </svg>
        Voltar à busca
      </RouterLink>

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

        <article class="proposicao-detalhe" aria-label="Detalhes da proposição">
          <header class="detalhe-header">
            <div class="detalhe-badges">
              <span class="detalhe-codigo">{{ proposicao.id }}</span>
              <StatusBadge :status="proposicao.status || 'Em tramitação'" />
              <span v-if="proposicao.subtema || proposicao.categoria" class="detalhe-subtema">
                {{ proposicao.subtema || proposicao.categoria }}
              </span>
            </div>
            <h1 class="detalhe-titulo">{{ proposicao.titulo || proposicao.ementa }}</h1>
          </header>

          <div class="detalhe-meta">
            <div class="meta-grupo">
              <span class="meta-label">Autor</span>
              <span class="meta-valor">{{ proposicao.autor || proposicao.nome_autor || 'Não informado' }}</span>
            </div>
            <div class="meta-grupo">
              <span class="meta-label">Partido</span>
              <span class="meta-valor">{{ proposicao.partido || proposicao.sigla_partido || '—' }}</span>
            </div>
            <div class="meta-grupo">
              <span class="meta-label">Data de Apresentação</span>
              <span class="meta-valor">{{ dataFormatada }}</span>
            </div>
          </div>

          <section class="detalhe-ementa">
            <h2 class="section-label">Ementa</h2>
            <p class="ementa-texto">{{ proposicao.ementa || proposicao.titulo || 'Ementa não disponível.' }}</p>
          </section>

          <div v-if="proposicao.url_documento || proposicao.url" class="detalhe-link">
            <a
              :href="proposicao.url_documento || proposicao.url"
              target="_blank"
              rel="noopener noreferrer"
              class="btn btn-primary"
            >
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true">
                <path d="M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6"/>
                <polyline points="15,3 21,3 21,9"/>
                <line x1="10" y1="14" x2="21" y2="3"/>
              </svg>
              Ver documento oficial
            </a>
          </div>

          <section v-if="tramitacoes.length" class="detalhe-tramitacao">
            <h2 class="section-label">Histórico de Tramitação</h2>
            <ol class="timeline" aria-label="Histórico de tramitação">
              <li v-for="(t, i) in tramitacoes" :key="i" class="timeline-item">
                <div class="timeline-dot" aria-hidden="true"></div>
                <div class="timeline-content">
                  <span class="timeline-data">{{ formatarData(t.data || t.dataHora) }}</span>
                  <p class="timeline-desc">{{ t.descricao || t.descricaoSituacao || t.despacho }}</p>
                  <span v-if="t.orgao || t.siglaOrgao" class="timeline-orgao">{{ t.orgao || t.siglaOrgao }}</span>
                </div>
              </li>
            </ol>
          </section>
        </article>

      </template>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import StatusBadge from '@/components/StatusBadge.vue'
import { fetchProposicao } from '@/services/proposicoes'

const route = useRoute()
const carregando = ref(true)
const erro = ref(null)
const proposicao = ref(null)
const tramitacoes = ref([])

const dataFormatada = computed(() => {
  const d = proposicao.value?.data || proposicao.value?.data_apresentacao
  if (!d) return 'Não informada'
  try { return new Date(d).toLocaleDateString('pt-BR') } catch { return d }
})

function formatarData(d) {
  if (!d) return '—'
  try { return new Date(d).toLocaleDateString('pt-BR') } catch { return d }
}

onMounted(async () => {
  try {
    const data = await fetchProposicao(route.params.id)
    proposicao.value = data.proposicao ?? data
    tramitacoes.value = data.tramitacoes ?? []
  } catch (e) {
    erro.value = e.message?.includes('404')
      ? 'Proposição não encontrada.'
      : 'Não foi possível carregar a proposição. Verifique a conexão com o servidor.'
  } finally {
    carregando.value = false
  }
})
</script>

<style scoped>
.detalhe {
  padding: 28px 20px;
}

.back-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  font-weight: 500;
  color: var(--text-secondary);
  margin-bottom: 24px;
  transition: color var(--transition);
}

.back-link:hover {
  color: var(--primary);
}

.proposicao-detalhe {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow);
  overflow: hidden;
}

.detalhe-header {
  padding: 28px;
  border-bottom: 1px solid var(--border);
}

.detalhe-badges {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 12px;
}

.detalhe-codigo {
  font-size: 13px;
  font-weight: 700;
  color: var(--primary-dark);
  background: #DBEAFE;
  padding: 4px 12px;
  border-radius: 999px;
  font-family: 'IBM Plex Mono', monospace;
}

.detalhe-subtema {
  font-size: 12px;
  font-weight: 600;
  padding: 4px 12px;
  border-radius: 999px;
  background: var(--purple-bg);
  color: var(--purple-text);
}

.detalhe-titulo {
  font-size: 22px;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1.3;
}

.detalhe-meta {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
  padding: 24px 28px;
  border-bottom: 1px solid var(--border);
  background: var(--bg);
}

.meta-grupo {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.meta-label {
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-caption);
}

.meta-valor {
  font-size: 15px;
  font-weight: 500;
  color: var(--text-primary);
}

.detalhe-ementa {
  padding: 24px 28px;
  border-bottom: 1px solid var(--border);
}

.section-label {
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--text-caption);
  margin-bottom: 12px;
}

.ementa-texto {
  font-size: 15px;
  color: var(--text-secondary);
  line-height: 1.7;
}

.detalhe-link {
  padding: 20px 28px;
  border-bottom: 1px solid var(--border);
}

.detalhe-tramitacao {
  padding: 24px 28px;
}

.timeline {
  list-style: none;
  position: relative;
  padding-left: 28px;
}

.timeline::before {
  content: '';
  position: absolute;
  left: 7px;
  top: 8px;
  bottom: 8px;
  width: 2px;
  background: var(--border);
}

.timeline-item {
  position: relative;
  padding-bottom: 24px;
}

.timeline-item:last-child {
  padding-bottom: 0;
}

.timeline-dot {
  position: absolute;
  left: -24px;
  top: 4px;
  width: 14px;
  height: 14px;
  background: var(--primary);
  border: 2px solid #fff;
  border-radius: 50%;
  box-shadow: 0 0 0 2px var(--border);
}

.timeline-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.timeline-data {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-caption);
}

.timeline-desc {
  font-size: 14px;
  color: var(--text-primary);
  line-height: 1.5;
}

.timeline-orgao {
  font-size: 12px;
  font-weight: 600;
  color: var(--primary-dark);
  background: #DBEAFE;
  padding: 2px 8px;
  border-radius: 4px;
  align-self: flex-start;
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
</style>
