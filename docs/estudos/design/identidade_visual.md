# Identidade Visual do Projeto
## Monitoramento Legislativo – Proteção de Crianças na Internet
---
## Exemplo Figma

Abaixo, segue um estudo realizado no site Figma com detalhes visuais e testes feitos para melhor visualização:

[![Título da Imagem](https://play-lh.googleusercontent.com/hoVBnPBRehmXsCqESLXRH2E3OTxklkwKZlb1psn7imm0VUSobn2nevS9RRFWb9GM4-o=w240-h480-rw)](https://www.figma.com/design/AnQaZLh3I0PuwHrCeWATfy/Identidade-Visual-Projeto-MDS?node-id=0-1&t=qyLGSw2rnOed27WN-1)
---

## 1. Propósito e Público-Alvo

### Propósito
Sistema de monitoramento legislativo dedicado a acompanhar, analisar e alertar sobre propostas de lei, regulamentações e políticas públicas relacionadas à proteção de crianças e adolescentes no ambiente digital.

### Público-Alvo
- **Primário**: ONGs de defesa dos direitos da criança, advogados especializados, pesquisadores, formuladores de políticas públicas
- **Secundário**: Educadores, pais, jornalistas especializados em direitos digitais
- **Perfil**: Profissionais sérios, engajados, que buscam informação confiável e ferramentas eficientes

---

## 2. Personalidade da Marca

### Atributos Principais
- **Confiável**: Fonte segura de informação legislativa
- **Protetora**: Foco em salvaguardar direitos das crianças
- **Profissional**: Abordagem séria e técnica
- **Acessível**: Interface clara, sem ser infantilizada
- **Vigilante**: Atenção constante às mudanças legislativas
- **Esperançosa**: Tom positivo sobre mudanças possíveis

### Tom de Comunicação
Sério mas humano, técnico mas compreensível, protetor sem ser alarmista.

---

## 3. Paleta de Cores

### Cores Principais

#### Azul Institucional (Cor Primária)
- **#2563EB** - Azul Confiança
- Representa: Segurança, profissionalismo, estabilidade
- Uso: Cabeçalhos, CTAs principais, elementos de navegação

#### Azul Profundo (Cor Secundária)
- **#1E40AF** - Azul Autoridade
- Representa: Seriedade, expertise, instituições
- Uso: Textos importantes, bordas, estados ativos

### Cores de Suporte

#### Verde Proteção
- **#059669** - Verde Guardião
- Representa: Proteção ativa, aprovação, segurança garantida
- Uso: Indicadores positivos, confirmações, proteções ativas

#### Roxo Legislativo
- **#7C3AED** - Roxo Governança
- Representa: Legislação, poder público, formalidade
- Uso: Tags legislativas, categorias, destaques de lei

#### Laranja Alerta
- **#EA580C** - Laranja Vigilância
- Representa: Atenção necessária, urgência moderada
- Uso: Notificações importantes, prazos próximos

#### Vermelho Crítico
- **#DC2626** - Vermelho Urgente
- Representa: Ameaças, prazos críticos, ação imediata
- Uso: Alertas críticos, projetos ameaçadores (uso moderado)

### Cores Neutras

- **#0F172A** - Grafite (texto principal)
- **#475569** - Cinza Médio (texto secundário)
- **#CBD5E1** - Cinza Claro (bordas)
- **#F1F5F9** - Gelo (backgrounds)
- **#FFFFFF** - Branco (fundos principais)

### Gradientes (Uso Opcional)

```css
/* Gradiente Institucional */
background: linear-gradient(135deg, #2563EB 0%, #1E40AF 100%);

/* Gradiente Proteção */
background: linear-gradient(135deg, #059669 0%, #047857 100%);
```

---

## 4. Tipografia

### Família Tipográfica Principal

#### **Inter** (Sans-serif moderna)
- **Uso**: Toda a interface, textos gerais
- **Características**: Clean, legível, profissional, humanista
- **Pesos sugeridos**:
  - 400 (Regular) - Corpo de texto
  - 500 (Medium ) - Subtítulos, labels
  - 600 (Semibold) - Títulos secundários
  - 700 (Bold) - Títulos principais, CTAs

```css
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
```

### Família Tipográfica Secundária

#### **IBM Plex Mono** (Monospace)
- **Uso**: Códigos de lei, números de processos, dados técnicos
- **Características**: Confiável, técnica, distinguível
- **Peso**: 400 (Regular), 600 (Semibold)

```css
font-family: 'IBM Plex Mono', 'Courier New', monospace;
```

### Hierarquia Tipográfica

```css
/* Títulos Principais */
H1: 32px / 700 / Inter / #0F172A / line-height: 1.2

/* Títulos de Seção */
H2: 24px / 600 / Inter / #0F172A / line-height: 1.3

/* Subtítulos */
H3: 20px / 600 / Inter / #1E40AF / line-height: 1.4

/* Corpo de Texto */
Body: 16px / 400 / Inter / #475569 / line-height: 1.6

/* Texto Pequeno */
Small: 14px / 400 / Inter / #64748B / line-height: 1.5

/* Labels e Metadados */
Caption: 12px / 500 / Inter / #64748B / uppercase / letter-spacing: 0.05em
```

---

## 5. Estilo Visual

### Conceito Geral
**"Vigilância Profissional com Propósito Humano"**

Interface limpa e moderna que equilibra seriedade institucional com acessibilidade, inspirada em:
- Dashboards governamentais modernos
- Plataformas de advocacy digital
- Sistemas de monitoramento profissional
- Design system de organizações de direitos humanos

### Características de Design

#### Minimalismo Funcional
- Layouts limpos sem excesso de ornamentação
- Foco no conteúdo e na informação
- Espaçamento generoso (white space)

#### Estrutura Clara
- Hierarquia visual evidente
- Grids bem definidos
- Organização lógica da informação

#### Elementos de Proteção
- Ícones de escudo, cadeado, vigilância (uso moderado)
- Bordas sutis para separar conteúdo crítico
- Cards com sombras suaves para elevação

#### Feedback Visual Claro
- Estados hover bem definidos
- Transições suaves (200-300ms)
- Indicadores de status coloridos e legíveis

---

## 6. Componentes Visuais

### Iconografia

#### Biblioteca Recomendada
**Lucide Icons** - moderna, consistente, código aberto

#### Ícones-Chave do Sistema
- 🛡️ **Shield**: Proteção, segurança
- 📋 **ClipboardList**: Legislação, projetos de lei
- 🔔 **Bell**: Alertas, notificações
- 👁️ **Eye**: Monitoramento, vigilância
- ⚖️ **Scale**: Justiça, legislação
- 🏛️ **Building**: Instituições governamentais
- 📊 **BarChart**: Análises, estatísticas
- 🔍 **Search**: Busca, investigação
- ⏰ **Clock**: Prazos, temporalidade
- ✓ **CheckCircle**: Aprovação, proteção ativa

#### Estilo de Ícones
- **Stroke width**: 2px
- **Tamanho padrão**: 20px ou 24px
- **Estilo**: Outline (não filled)
- **Cor**: Herda da tipografia ou cor de destaque

### Cards e Containers

```css
/* Card Padrão */
background: #FFFFFF;
border: 1px solid #E2E8F0;
border-radius: 8px;
padding: 24px;
box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);

/* Card com Hover */
transition: all 0.2s ease;
hover: {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  border-color: #2563EB;
}

/* Card de Alerta */
border-left: 4px solid #EA580C;
background: #FFF7ED;
```

### Botões

```css
/* Botão Primário */
background: #2563EB;
color: #FFFFFF;
padding: 12px 24px;
border-radius: 6px;
font-weight: 600;
hover: background: #1D4ED8;

/* Botão Secundário */
background: transparent;
color: #2563EB;
border: 2px solid #2563EB;
padding: 10px 22px;
hover: background: #EFF6FF;

/* Botão de Alerta */
background: #DC2626;
color: #FFFFFF;
hover: background: #B91C1C;
```

### Badges e Tags

```css
/* Badge de Status */
padding: 4px 12px;
border-radius: 12px;
font-size: 12px;
font-weight: 600;

/* Variações */
.ativo { background: #DCFCE7; color: #166534; }
.analise { background: #DBEAFE; color: #1E40AF; }
.urgente { background: #FEE2E2; color: #991B1B; }
.arquivado { background: #F1F5F9; color: #475569; }
```

---

## 7. Moodboard e Referências

### Referências de Sistemas Similares

#### 1. **GovTrack.us**
- Excelência em apresentar informação legislativa complexa
- Interface limpa e funcional
- Sistema de alertas bem implementado

#### 2. **ProPublica**
- Jornalismo investigativo com design sério
- Visualização de dados clara
- Tipografia profissional

#### 3. **UNICEF Digital Reports**
- Equilíbrio entre seriedade e acessibilidade
- Uso de cores com propósito
- Design centrado em crianças sem infantilizar

#### 4. **Electronic Frontier Foundation (EFF)**
- Advocacy digital bem apresentado
- Visual moderno mas confiável
- Hierarquia de informação exemplar

#### 5. **EU Digital Services Act Tracker**
- Monitoramento legislativo europeu
- Interface dashboard profissional
- Timeline e visualizações eficientes

### Referências de Estilo Visual

- **Cores**: Paletas institucionais de ONGs + azuis governamentais
- **Layout**: Gov.uk design system, U.S. Web Design System
- **Componentes**: Tailwind UI, Shadcn/ui (profissionais e modernos)
- **Tipografia**: Sistemas open-source governamentais

### Moodboard (Conceitos Visuais)

```
┌─────────────────────────────────────────────┐
│  CONFIANÇA + PROTEÇÃO + MODERNIDADE        │
│                                             │
│  [Azul Institucional]  [Estrutura Clara]   │
│  [Tipografia Limpa]    [Ícones Precisos]   │
│  [White Space]         [Dados Visuais]     │
│  [Hierarquia Forte]    [Feedback Claro]    │
└─────────────────────────────────────────────┘
```

---

## 8. Proposta de Logo (Conceito Inicial)

### Conceito 1: "Escudo Legislativo"
- Ícone de escudo estilizado
- Integração sutil de um livro/documento
- Cores: Azul #2563EB + Roxo #7C3AED
- Estilo: Geométrico, moderno, confiável

### Conceito 2: "Guardião Digital"
- Combinação de escudo + ícone de conectividade
- Representa proteção no ambiente digital
- Cores: Azul #2563EB + Verde #059669
- Estilo: Minimalista, tech, protetor

### Conceito 3: "Olhar Vigilante"
- Símbolo de vigilância + legislação
- Formas limpas e profissionais
- Cores: Gradiente azul institucional
- Estilo: Sério, observador, ativo

**Nota**: Para desenvolvimento final do logo, recomenda-se trabalho com designer profissional.

---

## 9. Aplicação em Interface

### Estrutura de Página Típica

```
┌─────────────────────────────────────────────────┐
│ HEADER [Azul #2563EB]                           │
│ Logo + Navegação [Branco]                       │
├─────────────────────────────────────────────────┤
│                                                 │
│ TÍTULO PRINCIPAL [H1 - #0F172A]                │
│ Subtítulo explicativo [Body - #475569]         │
│                                                 │
│ ┌──────────────┐  ┌──────────────┐             │
│ │ Card Alerta  │  │ Card Status  │             │
│ │ [Laranja]    │  │ [Verde]      │             │
│ └──────────────┘  └──────────────┘             │
│                                                 │
│ LISTA DE PROJETOS DE LEI                       │
│ ┌─────────────────────────────────────┐        │
│ │ [Badge Roxo] PL 1234/2026          │        │
│ │ Título do projeto...                │        │
│ │ [Ícones de metadata]               │        │
│ └─────────────────────────────────────┘        │
│                                                 │
└─────────────────────────────────────────────────┘
```

### Exemplo de Cores em Contexto

- **Navegação**: Fundo #2563EB, texto branco
- **Backgrounds**: #F1F5F9 (geral), #FFFFFF (cards)
- **Texto principal**: #0F172A
- **Texto secundário**: #475569
- **Links**: #2563EB, hover #1D4ED8
- **Alertas importantes**: Borda #EA580C, fundo #FFF7ED
- **Tags legislativas**: Fundo #EDE9FE, texto #7C3AED
- **Status proteção ativa**: Fundo #D1FAE5, texto #065F46

---

## 10. Diretrizes de Uso

### O que FAZER ✅

- Usar azuis para elementos institucionais e navegação
- Manter hierarquia tipográfica consistente
- Aplicar espaçamento generoso entre elementos
- Usar ícones outline de forma moderada
- Priorizar legibilidade e clareza
- Usar verde para indicadores positivos/proteção
- Aplicar vermelho/laranja com parcimônia (apenas alertas reais)
- Manter acessibilidade (contraste WCAG AA mínimo)

### O que EVITAR ❌

- Não infantilizar o design (não é para crianças, é sobre proteção delas)
- Não usar ilustrações fofas ou desenhos cartoon
- Não sobrecarregar com muitas cores simultâneas
- Não usar gradientes excessivos ou efeitos pesados
- Não comprometer legibilidade por estética
- Não usar vermelho como cor decorativa
- Não criar interfaces complexas ou confusas
- Não usar Comic Sans ou fontes informais

---

## 11. Acessibilidade

### Contraste de Cores (WCAG 2.1 - Nível AA)

Todas as combinações principais atendem aos requisitos:
- Azul #2563EB em branco: ✅ 4.5:1
- Texto #0F172A em branco: ✅ 15:1
- Texto #475569 em branco: ✅ 7:1

### Considerações Adicionais

- Não usar apenas cor para transmitir informação (incluir ícones/texto)
- Garantir áreas clicáveis mínimas de 44x44px
- Fornecer feedback visual em todos os estados interativos
- Suportar navegação por teclado
- Incluir textos alternativos em todas as imagens

---

## 12. Próximos Passos

### Fase 1: Validação (Atual)
- ✅ Definir propósito e público
- ✅ Criar paleta de cores
- ✅ Escolher tipografia
- ✅ Documentar estilo visual
- ⏳ Revisar com stakeholders

### Fase 2: Desenvolvimento
- [ ] Criar componentes base no Figma/código
- [ ] Desenvolver logo profissional
- [ ] Criar library de ícones personalizada (opcional)
- [ ] Desenvolver design system completo

### Fase 3: Implementação
- [ ] Aplicar identidade na UI do sistema
- [ ] Criar guia de estilo completo
- [ ] Documentar padrões de uso
- [ ] Treinar equipe

---

## 13. Conclusão

Esta identidade visual foi criada para transmitir **seriedade, confiança e propósito de proteção**, adequada ao tema sensível de proteção de crianças na internet e ao contexto profissional de monitoramento legislativo.

A paleta equilibra **azuis institucionais** (confiança), **verdes** (proteção), **roxos** (legislação) e **alertas controlados** (laranja/vermelho), sempre priorizando clareza e profissionalismo.

A tipografia **Inter** garante modernidade e legibilidade, enquanto o estilo visual minimalista mantém o foco no conteúdo crítico: as leis e políticas que protegem crianças no ambiente digital.

---

**Documento criado em**: 17/04/2026  
**Versão**: 1.0  
**Status**: Proposta Inicial/Estudo da Identidade Visual
