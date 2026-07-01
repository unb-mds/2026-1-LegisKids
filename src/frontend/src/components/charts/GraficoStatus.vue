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
import { Chart, DoughnutController, ArcElement, Tooltip, Legend } from 'chart.js'

Chart.register(DoughnutController, ArcElement, Tooltip, Legend)

const CORES = [
  '#2563EB',
  '#059669',
  '#EA580C',
  '#7C3AED',
  '#DC2626',
  '#0891B2'
]

const props = defineProps({
  labels: { type: Array, default: () => [] },
  values: { type: Array, default: () => [] },
  ariaLabel: { type: String, default: 'Gráfico de rosca: distribuição por status' }
})

const canvasRef = ref(null)
let chart = null

const temDados = computed(() => props.labels.length > 0 && props.values.length > 0)

function criarGrafico() {
  if (!canvasRef.value || !temDados.value) return
  chart?.destroy()
  chart = new Chart(canvasRef.value, {
    type: 'doughnut',
    data: {
      labels: props.labels,
      datasets: [{
        data: props.values,
        backgroundColor: CORES.slice(0, props.labels.length),
        borderWidth: 2,
        borderColor: '#fff'
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: '65%',
      plugins: {
        legend: { position: 'bottom' },
        tooltip: { mode: 'index', intersect: false }
      }
    }
  })
}

watch(() => [props.labels, props.values], () => {
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
