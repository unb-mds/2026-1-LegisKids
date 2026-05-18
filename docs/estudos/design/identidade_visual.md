# Identidade Visual do Projeto

**Documento:** v1.0 — Proposta Inicial  
**Data:** 17/04/2026

Link do Figma: https://www.figma.com/design/AnQaZLh3I0PuwHrCeWATfy/Identidade-Visual-Projeto-MDS?node-id=0-1&t=qyLGSw2rnOed27WN-1

---

## Propósito e público-alvo

### Propósito

Sistema de monitoramento legislativo dedicado a acompanhar, analisar e alertar sobre propostas de lei, regulamentações e políticas públicas relacionadas à proteção de crianças e adolescentes no ambiente digital.

### Público-alvo

- **Primário** — ONGs de defesa dos direitos da criança, advogados especializados, pesquisadores, formuladores de políticas públicas
- **Secundário** — educadores, pais, jornalistas especializados em direitos digitais
- **Perfil** — profissionais sérios e engajados que buscam informação confiável e ferramentas eficientes

---

## Personalidade da marca

### Atributos principais

- **Confiável** — fonte segura de informação legislativa
- **Protetora** — foco em salvaguardar direitos das crianças
- **Profissional** — abordagem séria e técnica
- **Acessível** — interface clara, sem ser infantilizada
- **Vigilante** — atenção constante às mudanças legislativas
- **Esperançosa** — tom positivo sobre mudanças possíveis

### Tom de comunicação

Sério mas humano, técnico mas compreensível, protetor sem ser alarmista.

---

## Paleta de cores

### Cores principais

**Azul Confiança — `#2563EB`** (cor primária)
Representa segurança, profissionalismo e estabilidade. Uso: cabeçalhos, CTAs principais, navegação.

**Azul Autoridade — `#1E40AF`** (cor secundária)
Representa seriedade, expertise e instituições. Uso: textos importantes, bordas, estados ativos.

### Cores de suporte

**Verde Guardião — `#059669`**
Representa proteção ativa, aprovação e segurança garantida. Uso: indicadores positivos, confirmações.

**Roxo Governança — `#7C3AED`**
Representa legislação, poder público e formalidade. Uso: tags legislativas, categorias, destaques de lei.

**Laranja Vigilância — `#EA580C`**
Representa atenção necessária e urgência moderada. Uso: notificações importantes, prazos próximos.

**Vermelho Urgente — `#DC2626`**
Representa ameaças, prazos críticos e ação imediata. Uso: alertas críticos (uso moderado).

### Cores neutras

- `#0F172A` — Grafite (texto principal)
- `#475569` — Cinza Médio (texto secundário)
- `#CBD5E1` — Cinza Claro (bordas)
- `#F1F5F9` — Gelo (backgrounds)
- `#FFFFFF` — Branco (fundos principais)

### Gradientes (uso opcional)

```css
/* Gradiente Institucional */
background: linear-gradient(135deg, #2563EB 0%, #1E40AF 100%);

/* Gradiente Proteção */
background: linear-gradient(135deg, #059669 0%, #047857 100%);
```

---

## Tipografia

### Família principal — Inter (sans-serif)

Uso em toda a interface e textos gerais. Clean, legível, profissional e humanista.

```css
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
```

Pesos: 400 Regular (corpo), 500 Medium (subtítulos, labels), 600 Semibold (títulos secundários), 700 Bold (títulos principais, CTAs).

### Família secundária — IBM Plex Mono (monospace)

Uso em códigos de lei, números de processos e dados técnicos.

```css
font-family: 'IBM Plex Mono', 'Courier New', monospace;
```

### Hierarquia tipográfica

```css
H1:      32px / 700 / Inter / #0F172A  / line-height: 1.2
H2:      24px / 600 / Inter / #0F172A  / line-height: 1.3
H3:      20px / 600 / Inter / #1E40AF  / line-height: 1.4
Body:    16px / 400 / Inter / #475569  / line-height: 1.6
Small:   14px / 400 / Inter / #64748B  / line-height: 1.5
Caption: 12px / 500 / Inter / #64748B  / uppercase / letter-spacing: 0.05em
```

---

## Estilo visual

### Conceito geral

"Vigilância Profissional com Propósito Humano" — interface limpa e moderna que equilibra seriedade institucional com acessibilidade, inspirada em dashboards governamentais modernos, plataformas de advocacy digital e design systems de organizações de direitos humanos.

### Características de design

**Minimalismo funcional** — layouts limpos sem excesso de ornamentação, foco no conteúdo, espaçamento generoso.

**Estrutura clara** — hierarquia visual evidente, grids bem definidos, organização lógica da informação.

**Elementos de proteção** — ícones de escudo e vigilância usados com moderação, bordas sutis para separar conteúdo crítico, cards com sombras suaves.

**Feedback visual claro** — estados hover bem definidos, transições suaves (200–300ms), indicadores de status coloridos e legíveis.

---

## Componentes visuais

### Iconografia

Biblioteca recomendada: **Lucide Icons** (moderna, consistente, código aberto).

Estilo: outline, stroke width 2px, tamanho padrão 20px ou 24px, cor herdada da tipografia ou cor de destaque.

Ícones-chave: Shield (proteção), ClipboardList (legislação), Bell (alertas), Eye (monitoramento), Scale (justiça), Building (instituições), BarChart (análises), Search (busca), Clock (prazos), CheckCircle (aprovação).

### Cards e containers

```css
/* Card Padrão */
background: #FFFFFF;
border: 1px solid #E2E8F0;
border-radius: 8px;
padding: 24px;
box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
transition: all 0.2s ease;

/* Card Hover */
box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
border-color: #2563EB;

/* Card de Alerta */
border-left: 4px solid #EA580C;
background: #FFF7ED;
```

### Botões

```css
/* Primário */
background: #2563EB; color: #FFFFFF;
padding: 12px 24px; border-radius: 6px; font-weight: 600;
hover: background: #1D4ED8;

/* Secundário */
background: transparent; color: #2563EB;
border: 2px solid #2563EB; padding: 10px 22px;
hover: background: #EFF6FF;

/* Alerta */
background: #DC2626; color: #FFFFFF;
hover: background: #B91C1C;
```

### Badges e tags

```css
padding: 4px 12px; border-radius: 12px;
font-size: 12px; font-weight: 600;

.ativo    { background: #DCFCE7; color: #166534; }
.analise  { background: #DBEAFE; color: #1E40AF; }
.urgente  { background: #FEE2E2; color: #991B1B; }
.arquivado{ background: #F1F5F9; color: #475569; }
```

---

## Referências

### Sistemas similares

- **GovTrack.us** — excelência em apresentar informação legislativa complexa com interface limpa
- **ProPublica** — jornalismo investigativo com design sério e visualização de dados clara
- **UNICEF Digital Reports** — equilíbrio entre seriedade e acessibilidade, uso de cores com propósito
- **Electronic Frontier Foundation (EFF)** — advocacy digital com hierarquia de informação exemplar
- **EU Digital Services Act Tracker** — monitoramento legislativo com dashboard profissional

### Referências de estilo

- **Cores** — paletas institucionais de ONGs e azuis governamentais
- **Layout** — Gov.uk design system, U.S. Web Design System
- **Componentes** — Tailwind UI, Shadcn/ui
- **Tipografia** — sistemas open-source governamentais

---

## Proposta de logo

### Conceito 1 — Escudo Legislativo
Ícone de escudo estilizado com integração sutil de documento. Cores: `#2563EB` + `#7C3AED`. Estilo: geométrico, moderno, confiável.

### Conceito 2 — Guardião Digital
Combinação de escudo e ícone de conectividade, representando proteção no ambiente digital. Cores: `#2563EB` + `#059669`. Estilo: minimalista, tech, protetor.

### Conceito 3 — Olhar Vigilante
Símbolo de vigilância e legislação com formas limpas. Cores: gradiente azul institucional. Estilo: sério, observador, ativo.

Para desenvolvimento final do logo, recomenda-se trabalho com designer profissional.

---

## Aplicação em interface

### Cores em contexto

- **Navegação** — fundo `#2563EB`, texto branco
- **Backgrounds** — `#F1F5F9` (geral), `#FFFFFF` (cards)
- **Texto principal** — `#0F172A`
- **Texto secundário** — `#475569`
- **Links** — `#2563EB`, hover `#1D4ED8`
- **Alertas** — borda `#EA580C`, fundo `#FFF7ED`
- **Tags legislativas** — fundo `#EDE9FE`, texto `#7C3AED`
- **Proteção ativa** — fundo `#D1FAE5`, texto `#065F46`

---

## Acessibilidade

### Contraste (WCAG 2.1 — Nível AA)

- Azul `#2563EB` em branco: 4,5:1
- Texto `#0F172A` em branco: 15:1
- Texto `#475569` em branco: 7:1

### Considerações adicionais

- não usar apenas cor para transmitir informação (incluir ícones ou texto)
- garantir áreas clicáveis mínimas de 44×44px
- fornecer feedback visual em todos os estados interativos
- suportar navegação por teclado
- incluir textos alternativos em todas as imagens

---

## Diretrizes de uso

### Fazer

- usar azuis para elementos institucionais e navegação
- manter hierarquia tipográfica consistente
- aplicar espaçamento generoso entre elementos
- usar ícones outline com moderação
- priorizar legibilidade e clareza
- usar verde para indicadores positivos
- manter acessibilidade (contraste WCAG AA mínimo)

### Evitar

- infantilizar o design (o sistema é sobre proteção de crianças, não para crianças)
- ilustrações fofas ou desenhos cartoon
- muitas cores simultâneas
- gradientes excessivos ou efeitos pesados
- vermelho como cor decorativa
- fontes informais

---

## Próximos passos

### Fase 1 — Validação (atual)

- Definir propósito e público *(concluído)*
- Criar paleta de cores *(concluído)*
- Escolher tipografia *(concluído)*
- Documentar estilo visual *(concluído)*
- Revisar com stakeholders *(pendente)*

### Fase 2 — Desenvolvimento

- Criar componentes base no Figma/código
- Desenvolver logo profissional
- Criar library de ícones personalizada (opcional)
- Desenvolver design system completo

### Fase 3 — Implementação

- Aplicar identidade na UI do sistema
- Criar guia de estilo completo
- Documentar padrões de uso
- Treinar equipe

---

## Conclusão

Esta identidade visual foi criada para transmitir seriedade, confiança e propósito de proteção, adequada ao tema sensível de proteção de crianças na internet e ao contexto profissional de monitoramento legislativo.

A paleta equilibra azuis institucionais (confiança), verdes (proteção), roxos (legislação) e alertas controlados (laranja/vermelho), sempre priorizando clareza e profissionalismo. A tipografia Inter garante modernidade e legibilidade, enquanto o estilo visual minimalista mantém o foco no conteúdo crítico.