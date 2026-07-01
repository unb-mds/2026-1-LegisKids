<template>
  <div class="sobre-page">
    <section class="hero">
      <div class="container">
        <span class="hero__eyebrow">Sobre o projeto</span>
        <h1 class="hero__title">Acompanhar as leis que protegem crianças na internet não devia ser difícil</h1>
        <p class="hero__desc">
          O LegisKids acompanha, organiza e classifica proposições legislativas da Câmara dos Deputados
          focadas em proteção de crianças e adolescentes no ambiente digital — para que qualquer pessoa
          consiga entender o que está tramitando, sem precisar garimpar o site oficial.
        </p>
      </div>
    </section>

    <div class="container">
      <section class="temas">
        <h2 class="section-title">Temas que acompanhamos</h2>
        <div class="temas-grid">
          <div class="tema-card" style="background:#EDE9FE">
            <span class="tema-card__dot" style="background:#7C3AED"></span>
            Cyberbullying
          </div>
          <div class="tema-card" style="background:#FEE2E2">
            <span class="tema-card__dot" style="background:#DC2626"></span>
            Exploração sexual infantil online
          </div>
          <div class="tema-card" style="background:#DBEAFE">
            <span class="tema-card__dot" style="background:#2563EB"></span>
            Proteção de dados de menores
          </div>
          <div class="tema-card" style="background:#D1FAE5">
            <span class="tema-card__dot" style="background:#059669"></span>
            Segurança digital infantil
          </div>
          <div class="tema-card" style="background:#FFEDD5">
            <span class="tema-card__dot" style="background:#EA580C"></span>
            Regulação de plataformas digitais
          </div>
        </div>
      </section>

      <section class="como-funciona">
        <h2 class="section-title">Como funciona</h2>
        <div class="passos">
          <div class="passo">
            <div class="passo__numero">1</div>
            <div>
              <h3 class="passo__titulo">Coleta</h3>
              <p class="passo__desc">
                Buscamos proposições diretamente da
                <a href="https://dadosabertos.camara.leg.br" target="_blank" rel="noopener noreferrer">API de Dados Abertos da Câmara dos Deputados</a>,
                de forma periódica e sem duplicatas.
              </p>
            </div>
          </div>
          <div class="passo">
            <div class="passo__numero">2</div>
            <div>
              <h3 class="passo__titulo">Classificação por tema</h3>
              <p class="passo__desc">
                Cada proposição é analisada e associada a um ou mais subtemas de proteção infantil digital,
                para facilitar a busca e a visualização por assunto.
              </p>
            </div>
          </div>
          <div class="passo">
            <div class="passo__numero">3</div>
            <div>
              <h3 class="passo__titulo">Disponibilização</h3>
              <p class="passo__desc">
                As proposições ficam disponíveis para busca, filtro e acompanhamento — com link direto
                para a ficha oficial de cada projeto na Câmara.
              </p>
            </div>
          </div>
        </div>
      </section>

      <section class="card card--info">
        <h2 class="card__title">Uma promessa sobre os dados</h2>
        <p>
          Nem toda informação sobre uma proposição está disponível na fonte pública — quando um dado
          não existe (como o autor de um projeto, por exemplo), a plataforma mostra isso de forma
          explícita em vez de simular ou inventar um valor.
        </p>
      </section>

      <section class="card">
        <h2 class="card__title">Contexto acadêmico</h2>
        <p>
          O LegisKids é um projeto acadêmico desenvolvido para a disciplina de Métodos de Desenvolvimento
          de Software (MDS) da Universidade de Brasília (UnB), turma 2026/1.
        </p>
      </section>
    </div>
  </div>
</template>

<style scoped>
.sobre-page {
  padding-bottom: 40px;
}

.hero {
  background: var(--primary);
  padding: 48px 20px 40px;
  margin-bottom: var(--gap);
}

.hero__eyebrow {
  display: inline-block;
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: rgba(255, 255, 255, 0.75);
  margin-bottom: 12px;
}

.hero__title {
  font-size: 30px;
  font-weight: 700;
  color: #fff;
  line-height: 1.25;
  max-width: 760px;
  margin-bottom: 16px;
  letter-spacing: -0.01em;
}

.hero__desc {
  font-size: 15px;
  color: rgba(255, 255, 255, 0.88);
  line-height: 1.7;
  max-width: 640px;
}

.container {
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 0 32px;
}

.section-title {
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 16px;
}

.temas {
  margin-bottom: var(--gap);
}

.temas-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.tema-card {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border-radius: 999px;
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary);
}

.tema-card__dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}

.como-funciona {
  margin-bottom: var(--gap);
}

.passos {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.passo {
  display: flex;
  gap: 14px;
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  padding: 20px;
}

.passo__numero {
  flex-shrink: 0;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--secondary);
  color: var(--primary);
  font-weight: 700;
  font-size: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.passo__titulo {
  font-size: 14px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 6px;
}

.passo__desc {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.6;
}

.card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  padding: 20px;
  margin-bottom: 16px;
}

.card--info {
  border-left: 4px solid var(--primary);
}

.card__title {
  font-size: 16px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 10px;
}

.card p {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.7;
}

.card a,
.passo__desc a {
  color: var(--primary);
  font-weight: 500;
}

@media (max-width: 900px) {
  .passos {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .hero {
    padding: 36px 16px 28px;
  }

  .hero__title {
    font-size: 24px;
  }

  .container {
    padding: 0 16px;
  }
}
</style>
