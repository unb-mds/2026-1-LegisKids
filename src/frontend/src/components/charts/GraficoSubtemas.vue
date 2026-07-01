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
import { Chart, BarController, BarElement, CategoryScale, LinearScale, Tooltip, Legend } from 'chart.js'

Chart.register(BarController, BarElement, CategoryScale, LinearScale, Tooltip, Legend)

const COR_PADRAO = '#2563EB'

const props = defineProps({
  subtemas: { type: Array, default: () => [] },
  totais: { type: Array, default: () => [] },
  cores: { type: Array, default: () => [] },
  ariaLabel: { type: String, default: 'Gráfico de barras: proposições por subtema' }
})

const canvasRef = ref(null)
let chart = null

const temDados = computed(() => props.subtemas.length > 0 && props.totais.length > 0)

function criarGrafico() {
  if (!canvasRef.value || !temDados.value) return
  chart?.destroy()

  const cores = props.subtemas.map((_, i) => props.cores[i] || COR_PADRAO)

  chart = new Chart(canvasRef.value, {
    type: 'bar',
    data: {
      labels: props.subtemas,
      datasets: [{
        label: 'Proposições',
        data: props.totais,
        backgroundColor: cores,
        borderColor: cores,
        borderWidth: 1,
        borderRadius: 4
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

watch(() => [props.subtemas, props.totais, props.cores], () => {
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
