<template>
  <div class="grafico-wrapper">
    <p v-if="!temDados" class="grafico-vazio">Nenhum dado disponível</p>
    <canvas
      v-else
      ref="canvasRef"
      :aria-label="ariaLabel"
      role="img"
    ></canvas>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { Chart, LineController, LineElement, PointElement, CategoryScale, LinearScale, Tooltip, Legend } from 'chart.js'

Chart.register(LineController, LineElement, PointElement, CategoryScale, LinearScale, Tooltip, Legend)

const CORES_FALLBACK = ['#2563EB', '#059669', '#EA580C', '#7C3AED', '#DC2626', '#0891B2', '#DB2777', '#65A30D']

const props = defineProps({
  labels: { type: Array, default: () => [] },
  series: { type: Array, default: () => [] },
  ariaLabel: { type: String, default: 'Gráfico de linhas interativo: proposições por subtema ao longo do tempo' }
})

const canvasRef = ref(null)
let chart = null

const temDados = computed(() => props.labels.length > 0 && props.series.length > 0)

function criarGrafico() {
  if (!canvasRef.value || !temDados.value) return
  chart?.destroy()

  chart = new Chart(canvasRef.value, {
    type: 'line',
    data: {
      labels: props.labels,
      datasets: props.series.map((serie, i) => {
        const cor = serie.cor || CORES_FALLBACK[i % CORES_FALLBACK.length]
        return {
          label: serie.nome,
          data: serie.values,
          borderColor: cor,
          backgroundColor: cor,
          borderWidth: 2,
          pointRadius: 3,
          pointHoverRadius: 5,
          tension: 0.3
        }
      })
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { mode: 'index', intersect: false },
      plugins: {
        legend: { position: 'bottom', labels: { boxWidth: 12, font: { size: 11 } } },
        tooltip: { mode: 'index', intersect: false }
      },
      scales: {
        y: { beginAtZero: true, ticks: { stepSize: 1 } }
      }
    }
  })
}

watch(() => [props.labels, props.series], () => {
  if (temDados.value) criarGrafico()
  else chart?.destroy()
}, { deep: true })

onMounted(() => { if (temDados.value) criarGrafico() })
onUnmounted(() => chart?.destroy())
</script>

<style scoped>
.grafico-wrapper {
  position: relative;
  width: 100%;
  height: 340px;
}

.grafico-vazio {
  text-align: center;
  padding: 40px 20px;
  color: var(--text-secondary);
  font-size: 14px;
}
</style>
