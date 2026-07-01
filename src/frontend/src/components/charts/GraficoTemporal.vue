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
import { Chart, LineController, LineElement, PointElement, CategoryScale, LinearScale, Tooltip, Legend, Filler } from 'chart.js'

Chart.register(LineController, LineElement, PointElement, CategoryScale, LinearScale, Tooltip, Legend, Filler)

const props = defineProps({
  meses: { type: Array, default: () => [] },
  contagens: { type: Array, default: () => [] },
  ariaLabel: { type: String, default: 'Gráfico de linha: evolução temporal de proposições' }
})

const canvasRef = ref(null)
let chart = null

const temDados = computed(() => props.meses.length > 0 && props.contagens.length > 0)

function criarGrafico() {
  if (!canvasRef.value || !temDados.value) return
  chart?.destroy()
  chart = new Chart(canvasRef.value, {
    type: 'line',
    data: {
      labels: props.meses,
      datasets: [{
        label: 'Proposições',
        data: props.contagens,
        borderColor: '#2563EB',
        backgroundColor: 'rgba(37, 99, 235, 0.08)',
        borderWidth: 2,
        pointRadius: 4,
        pointHoverRadius: 6,
        fill: true,
        tension: 0.3
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: { mode: 'index', intersect: false }
      },
      scales: {
        y: { beginAtZero: true, ticks: { stepSize: 1 } }
      }
    }
  })
}

watch(() => [props.meses, props.contagens], () => {
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
  height: 260px;
}

.grafico-vazio {
  text-align: center;
  padding: 40px 20px;
  color: var(--text-secondary);
  font-size: 14px;
}
</style>
