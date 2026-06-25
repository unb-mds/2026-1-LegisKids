---
name: chartjs-visualization
description: Use this skill whenever creating or editing data visualizations with Chart.js in the LegisKids frontend — charts showing proposições by theme, status distribution, trends over time, or any new Chart() / <canvas> based chart, including Vue wrappers around Chart.js. Triggers on "gráfico", "chart", "visualização de dados", Chart.js config objects, or canvas elements meant for charting.
---

# Chart.js — Visualizações do LegisKids

## Quando cada tipo de gráfico é apropriado

- **Barras** — comparar quantidade de proposições por tema, por autor, ou por estado.
- **Linha** — evolução de proposições/aprovações ao longo do tempo (tendência).
- **Pizza/Doughnut** — distribuição percentual de status (tramitando/aprovada/rejeitada) — use só quando há poucas categorias (até ~5), senão fica ilegível.
- Evite gráfico 3D ou excesso de cores decorativas — prioriza legibilidade, já que parte do público (dado o nome do projeto) pode ser jovem/não especialista.

## Setup básico

```javascript
import { Chart, BarController, BarElement, CategoryScale, LinearScale, Tooltip, Legend } from "chart.js";

Chart.register(BarController, BarElement, CategoryScale, LinearScale, Tooltip, Legend);
```

Registre apenas os componentes usados (tree-shaking) em vez de `import "chart.js/auto"` em produção — reduz o tamanho do bundle.

## Gráfico de barras: proposições por tema

```javascript
const ctx = document.getElementById("grafico-temas");

new Chart(ctx, {
  type: "bar",
  data: {
    labels: dados.map((d) => d.tema),
    datasets: [
      {
        label: "Proposições por tema",
        data: dados.map((d) => d.quantidade),
        backgroundColor: "#1d4ed8",
        borderRadius: 4,
      },
    ],
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      y: { beginAtZero: true, ticks: { precision: 0 } },
    },
    plugins: {
      legend: { display: false },
      tooltip: { callbacks: { label: (ctx) => `${ctx.raw} proposições` } },
    },
  },
});
```

- `beginAtZero: true` no eixo de quantidade — nunca deixe o eixo Y começar em um valor arbitrário em gráfico de barras, distorce a percepção de proporção.
- `ticks: { precision: 0 }` quando o valor é uma contagem inteira (não faz sentido mostrar "3.5 proposições").
- `maintainAspectRatio: false` + container CSS com altura definida, para o gráfico se adaptar bem em mobile.

## Integração com Vue

Encapsule o Chart.js em um componente reutilizável em vez de manipular o canvas diretamente em cada tela:

```vue
<script setup>
import { ref, onMounted, onUnmounted, watch } from "vue";
import { Chart } from "chart.js/auto";

const props = defineProps({
  labels: { type: Array, required: true },
  valores: { type: Array, required: true },
  titulo: { type: String, default: "" },
});

const canvasRef = ref(null);
let instanciaChart = null;

function renderizar() {
  if (instanciaChart) instanciaChart.destroy();
  instanciaChart = new Chart(canvasRef.value, {
    type: "bar",
    data: {
      labels: props.labels,
      datasets: [{ label: props.titulo, data: props.valores }],
    },
    options: { responsive: true, maintainAspectRatio: false },
  });
}

onMounted(renderizar);
watch([() => props.labels, () => props.valores], renderizar);
onUnmounted(() => instanciaChart?.destroy());
</script>

<template>
  <div style="position: relative; height: 320px;">
    <canvas ref="canvasRef"></canvas>
  </div>
</template>
```

Ponto crítico: **sempre destrua a instância anterior** (`instanciaChart.destroy()`) antes de criar uma nova e no `onUnmounted` — esquecer isso é a causa mais comum de memory leak e gráficos "fantasma" sobrepostos ao navegar entre páginas em apps Vue.

## Acessibilidade e dados subjacentes

- Sempre disponibilize os dados também em uma forma textual/tabular próxima ao gráfico (uma tabela escondida ou um resumo em texto) — gráficos em `<canvas>` não são acessíveis a leitores de tela por padrão.
- Use `aria-label` descritivo no container do gráfico: `aria-label="Gráfico de barras: quantidade de proposições por tema"`.

## Performance

- Não recrie o gráfico em cada pequena mudança de prop não relacionada a dados — use `update()` para mudanças de dados quando possível, em vez de `destroy()` + `new Chart()`, se a estrutura (tipo, eixos) não mudou:

```javascript
instanciaChart.data.datasets[0].data = novosValores;
instanciaChart.update();
```

- Para listas grandes de pontos (séries temporais longas), considere `decimation` plugin do Chart.js em vez de plotar milhares de pontos brutos.

## Checklist

1. Tipo de gráfico escolhido de acordo com a pergunta que ele responde (comparação, tendência, distribuição).
2. Eixo numérico começando em zero quando for gráfico de barras.
3. Instância destruída antes de recriar e no unmount do componente Vue.
4. Dados também acessíveis em formato textual/tabular.
5. Apenas os módulos do Chart.js necessários registrados (sem `chart.js/auto` em produção).
