-- ============================================================
-- LegisKids — Criação das tabelas principais
-- Schema baseado na documentação de arquitetura do projeto
-- ============================================================

-- ── partidos ──────────────────────────────────────────────────────────────────
-- Partidos políticos associados às proposições.
-- IDs vindos diretamente da API da Câmara dos Deputados.
CREATE TABLE IF NOT EXISTS partidos (
    id    INTEGER      PRIMARY KEY,
    sigla VARCHAR(20)  NOT NULL UNIQUE,
    nome  VARCHAR(150) NOT NULL
);

-- ── proposicoes ───────────────────────────────────────────────────────────────
-- Proposições legislativas relacionadas à segurança da criança na internet.
-- Apenas dados necessários para os dashboards são persistidos.
CREATE TABLE IF NOT EXISTS proposicoes (
    id                  INTEGER      PRIMARY KEY,
    sigla_tipo          VARCHAR(20)  NOT NULL,
    numero              INTEGER      NOT NULL,
    ano                 INTEGER      NOT NULL,
    ementa              TEXT         NOT NULL,
    data_apresentacao   DATE         NOT NULL,
    descricao_situacao  VARCHAR(150) NOT NULL,
    partido_id          INTEGER      REFERENCES partidos(id) ON DELETE SET NULL,
    sigla_partido       VARCHAR(20)  NOT NULL,
    categoria           VARCHAR(100),           -- classificação temática derivada das palavras-chave
    data_coleta         TIMESTAMP    NOT NULL DEFAULT NOW(),
    UNIQUE (sigla_tipo, numero, ano)
);

-- ── tramitacoes ───────────────────────────────────────────────────────────────
-- Histórico simplificado de tramitação legislativa.
CREATE TABLE IF NOT EXISTS tramitacoes (
    id                    SERIAL       PRIMARY KEY,
    proposicao_id         INTEGER      NOT NULL REFERENCES proposicoes(id) ON DELETE CASCADE,
    data_hora             TIMESTAMP    NOT NULL,
    id_situacao           INTEGER      NOT NULL,
    descricao_situacao    VARCHAR(150) NOT NULL,
    descricao_tramitacao  TEXT         NOT NULL,
    sigla_orgao           VARCHAR(50)  NOT NULL
);

-- ── usuarios ──────────────────────────────────────────────────────────────────
-- Usuários autenticados via Google OAuth.
CREATE TABLE IF NOT EXISTS usuarios (
    id           SERIAL       PRIMARY KEY,
    nome         VARCHAR(100) NOT NULL,
    email        VARCHAR(150) NOT NULL UNIQUE,
    google_id    VARCHAR(100) NOT NULL UNIQUE,
    data_criacao TIMESTAMP    NOT NULL DEFAULT NOW()
);

-- ── favoritos ─────────────────────────────────────────────────────────────────
-- Proposições salvas por usuários (N:N com restrição de unicidade).
CREATE TABLE IF NOT EXISTS favoritos (
    id            SERIAL    PRIMARY KEY,
    usuario_id    INTEGER   NOT NULL REFERENCES usuarios(id)    ON DELETE CASCADE,
    proposicao_id INTEGER   NOT NULL REFERENCES proposicoes(id) ON DELETE CASCADE,
    data_favorito TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE (usuario_id, proposicao_id)
);

-- ── historico_consultas ───────────────────────────────────────────────────────
-- Histórico de pesquisas realizadas pelos usuários.
CREATE TABLE IF NOT EXISTS historico_consultas (
    id            SERIAL       PRIMARY KEY,
    usuario_id    INTEGER      NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    termo_busca   VARCHAR(255) NOT NULL,
    data_consulta TIMESTAMP    NOT NULL DEFAULT NOW()
);

-- ── requisicoes_api ───────────────────────────────────────────────────────────
-- Monitoramento e auditoria das coletas da API da Câmara.
CREATE TABLE IF NOT EXISTS requisicoes_api (
    id                   SERIAL       PRIMARY KEY,
    endpoint             VARCHAR(255) NOT NULL,
    data_requisicao      TIMESTAMP    NOT NULL DEFAULT NOW(),
    quantidade_registros INTEGER      NOT NULL,
    status_requisicao    VARCHAR(50)  NOT NULL,
    tempo_execucao_ms    INTEGER
);

-- ── Índices ───────────────────────────────────────────────────────────────────
CREATE INDEX IF NOT EXISTS idx_proposicoes_ano          ON proposicoes(ano);
CREATE INDEX IF NOT EXISTS idx_proposicoes_partido      ON proposicoes(partido_id);
CREATE INDEX IF NOT EXISTS idx_proposicoes_situacao     ON proposicoes(descricao_situacao);
CREATE INDEX IF NOT EXISTS idx_tramitacoes_proposicao   ON tramitacoes(proposicao_id);
CREATE INDEX IF NOT EXISTS idx_tramitacoes_data         ON tramitacoes(data_hora);
CREATE INDEX IF NOT EXISTS idx_favoritos_usuario        ON favoritos(usuario_id);
CREATE INDEX IF NOT EXISTS idx_historico_usuario        ON historico_consultas(usuario_id);
CREATE INDEX IF NOT EXISTS idx_requisicoes_data         ON requisicoes_api(data_requisicao);