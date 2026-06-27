import logging
import os
import time
from datetime import date, datetime, timezone

import requests
from tenacity import (
    RetryError,
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

from src.backend.models import Proposicao, SyncExecution
from src.backend.repository import camara_repository as repo

logger = logging.getLogger(__name__)

URL_BASE = "https://dadosabertos.camara.leg.br/api/v2"

PALAVRAS_CHAVE = [
    "crianças",
    "adolescentes",
    "internet",
    "redes sociais",
    "proteção de dados",
    "segurança digital",
    "abuso infantil",
    "exploração sexual infantil",
    "crimes virtuais",
    "cyberbullying",
    "plataformas digitais",
    "jogos online",
    "conteúdo impróprio",
    "regulação digital",
]

# 8 categorias fixas — sem "outros". Irrelevantes são descartadas antes de persistir.
CATEGORIAS_FIXAS = [
    "cyberbullying",
    "exploração sexual infantil online",
    "proteção de dados de menores",
    "segurança digital infantil",
    "regulação de plataformas digitais",
    "conteúdos nocivos para menores",
    "crimes virtuais contra crianças",
    "privacidade de menores",
]

RESULTADO_IRRELEVANTE = "irrelevante"

STATUS_VALIDOS_SITUACAO = {
    "Em tramitação",
    "Aprovado",
    "Arquivado",
    "Encerrado",
}

_CAMPOS_OBRIGATORIOS = ("id", "siglaTipo", "numero", "ano", "ementa", "dataApresentacao")


# ── Helpers de API da Câmara ──────────────────────────────────────────────────

def _is_retryable(exc: BaseException) -> bool:
    if isinstance(exc, requests.HTTPError):
        return exc.response is not None and exc.response.status_code >= 500
    return isinstance(exc, (requests.Timeout, requests.ConnectionError))


@retry(
    retry=retry_if_exception(_is_retryable),
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    reraise=True,
)
def _buscar_proposicoes_api(pagina: int, itens: int = 100) -> list[dict]:
    params = {
        "itens": itens,
        "pagina": pagina,
        "ordem": "DESC",
        "ordenarPor": "id",
    }
    response = requests.get(
        f"{URL_BASE}/proposicoes",
        params=params,
        headers={"Accept": "application/json"},
        timeout=20,
    )
    response.raise_for_status()
    return response.json().get("dados", [])


def _normalizar_data(valor: str | None) -> date | None:
    if not valor:
        return None
    for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M", "%Y-%m-%d"):
        try:
            return datetime.strptime(valor[:19], fmt).date()
        except ValueError:
            continue
    return None


def _validar_proposicao(dado: dict) -> dict | None:
    for campo in _CAMPOS_OBRIGATORIOS:
        if dado.get(campo) is None:
            logger.warning("Proposição %s: campo obrigatório ausente '%s'. Ignorando.", dado.get("id"), campo)
            return None

    ementa = str(dado["ementa"]).strip()
    if not ementa:
        logger.warning("Proposição %s: ementa vazia. Ignorando.", dado.get("id"))
        return None

    data_apresentacao = _normalizar_data(dado.get("dataApresentacao"))
    if data_apresentacao is None:
        logger.warning(
            "Proposição %s: dataApresentacao inválida '%s'. Ignorando.",
            dado.get("id"), dado.get("dataApresentacao"),
        )
        return None

    descricao_situacao = dado.get("descricaoSituacao") or "Em tramitação"
    if descricao_situacao not in STATUS_VALIDOS_SITUACAO:
        descricao_situacao = "Em tramitação"

    return {
        "id": int(dado["id"]),
        "sigla_tipo": str(dado["siglaTipo"])[:20],
        "numero": int(dado["numero"]),
        "ano": int(dado["ano"]),
        "ementa": ementa,
        "data_apresentacao": data_apresentacao,
        "descricao_situacao": descricao_situacao,
        "sigla_partido": str(dado.get("siglaPartido") or "")[:20],
        "data_coleta": datetime.now(timezone.utc),
        "classificacao_status": Proposicao.CLASSIFICACAO_PENDENTE,
    }


def _filtrar_por_palavras_chave(dados: list[dict]) -> list[dict]:
    palavras = [p.lower() for p in PALAVRAS_CHAVE]
    return [
        d for d in dados
        if any(
            p in " ".join([str(d.get("ementa", "")), str(d.get("ementaDetalhada", ""))]).lower()
            for p in palavras
        )
    ]


# ── Gemini ────────────────────────────────────────────────────────────────────

def _is_rate_limit_error(exc: Exception) -> bool:
    exc_str = str(exc).lower()
    return (
        "429" in exc_str
        or "resourceexhausted" in type(exc).__name__.lower()
        or "quota" in exc_str
    )


def _classificar_via_gemini(ementa: str) -> str:
    """Chama o Gemini e retorna "irrelevante" ou o nome exato de uma categoria.

    Lança exceção se a API falhar após retentativas — o chamador trata o fallback.
    """
    try:
        from google import genai
        from google.genai import types as genai_types
    except ImportError:
        raise RuntimeError("google-genai não instalado. Execute: pip install google-genai")

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("GOOGLE_API_KEY não configurada.")

    client = genai.Client(api_key=api_key)

    categorias_str = "\n".join(f"- {c}" for c in CATEGORIAS_FIXAS)
    prompt = (
        "Você é um classificador de proposições legislativas brasileiras.\n\n"
        "Analise a ementa abaixo e responda com UMA das seguintes opções:\n"
        '- "irrelevante" → se NÃO tratar de proteção de crianças ou adolescentes '
        "no ambiente digital/internet\n"
        "- Um dos temas abaixo → se a proposta tratar do tema\n\n"
        f"Temas válidos:\n{categorias_str}\n\n"
        "Responda SOMENTE com a palavra ou frase exata. Sem explicação.\n\n"
        f"Ementa: {ementa[:600]}"
    )

    response = None
    for tentativa in range(2):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
                config=genai_types.GenerateContentConfig(
                    http_options=genai_types.HttpOptions(timeout=30000),
                ),
            )
            break
        except Exception as exc:
            if tentativa == 0 and _is_rate_limit_error(exc):
                logger.warning("Gemini 429 ResourceExhausted: aguardando 60s antes de re-tentar.")
                time.sleep(60)
                continue
            raise

    resultado = response.text.strip().lower()

    if resultado == RESULTADO_IRRELEVANTE:
        return RESULTADO_IRRELEVANTE

    if resultado not in CATEGORIAS_FIXAS:
        raise ValueError(f"Gemini retornou resultado inválido: '{resultado}'")

    return resultado


# ── Service ───────────────────────────────────────────────────────────────────

class CamaraService:
    def __init__(self):
        self._rpm = int(os.getenv("GEMINI_RATE_LIMIT_RPM", "15"))
        self._min_interval = 60.0 / self._rpm if self._rpm > 0 else 0
        self._last_gemini_call = 0.0

    def _classificar_com_rate_limit(self, ementa: str) -> str:
        agora = time.monotonic()
        espera = self._min_interval - (agora - self._last_gemini_call)
        if espera > 0:
            logger.debug("Gemini rate limit: aguardando %.1fs.", espera)
            time.sleep(espera)
        self._last_gemini_call = time.monotonic()
        return _classificar_via_gemini(ementa)

    def _classificar_e_filtrar(self, dto: dict) -> tuple[dict, str | None]:
        """Classifica a proposição via Gemini.

        Retorna (dto, resultado) onde resultado é:
        - nome da categoria  → relevante, deve persistir e vincular
        - RESULTADO_IRRELEVANTE → descartar, não persistir
        - None               → Gemini falhou, persistir como pendente_classificacao
        """
        try:
            resultado = self._classificar_com_rate_limit(dto["ementa"])
            if resultado == RESULTADO_IRRELEVANTE:
                return dto, RESULTADO_IRRELEVANTE
            dto["classificacao_status"] = Proposicao.CLASSIFICACAO_CLASSIFICADO
            return dto, resultado
        except Exception as exc:
            logger.warning(
                "Falha ao classificar proposição %d via Gemini: %s. Marcando como pendente.",
                dto["id"], exc,
            )
            dto["classificacao_status"] = Proposicao.CLASSIFICACAO_PENDENTE
            return dto, None

    def _retentar_pendentes(self) -> None:
        """Re-classifica proposições com status pendente_classificacao."""
        pendentes = repo.get_proposicoes_pendentes(limite=50)
        if not pendentes:
            return
        logger.info("Re-tentando classificação de %d proposições pendentes.", len(pendentes))
        for prop in pendentes:
            dto_pendente = {
                "id": prop.id,
                "ementa": prop.ementa,
                "classificacao_status": prop.classificacao_status,
            }
            try:
                _, resultado = self._classificar_e_filtrar(dto_pendente)
                if resultado == RESULTADO_IRRELEVANTE:
                    repo.deletar_proposicao(prop.id)
                    logger.info("Proposição pendente %d era irrelevante — removida.", prop.id)
                elif resultado is not None:
                    repo.vincular_categoria(prop.id, resultado)
                    repo.atualizar_classificacao_status(prop.id, Proposicao.CLASSIFICACAO_CLASSIFICADO)
                    logger.info("Proposição pendente %d classificada como '%s'.", prop.id, resultado)
                # resultado None → continua pendente, será re-tentada no próximo run
            except Exception as exc:
                logger.warning("Falha ao re-tentar proposição %d: %s.", prop.id, exc)

    def run_sync(self) -> dict:
        """Executa a sincronização completa. Registra tudo em sync_executions."""
        logger.info("=== Sincronização da Câmara iniciada ===")
        execucao = repo.criar_sync_execution()

        total_processados = 0
        total_inseridos = 0
        total_atualizados = 0
        total_erros = 0
        total_descartados = 0
        status_final = SyncExecution.STATUS_CONCLUIDO
        mensagem_erro = None
        cota_gemini_esgotada = False

        try:
            # Re-tentar pendentes de runs anteriores antes de buscar novas proposições
            self._retentar_pendentes()

            pagina = 1
            while True:
                logger.info("Buscando página %d da API da Câmara...", pagina)
                try:
                    dados_brutos = _buscar_proposicoes_api(pagina)
                except (RetryError, requests.HTTPError, requests.RequestException) as exc:
                    logger.error("Falha na API da Câmara após retries: %s", exc)
                    status_final = SyncExecution.STATUS_ERRO_API
                    mensagem_erro = str(exc)
                    break

                if not dados_brutos:
                    logger.info("Página %d vazia — fim da paginação.", pagina)
                    break

                filtrados = _filtrar_por_palavras_chave(dados_brutos)
                logger.info(
                    "Página %d: %d recebidos, %d após filtro de palavras-chave.",
                    pagina, len(dados_brutos), len(filtrados),
                )

                # Lista de (dto, categoria_nome | "irrelevante" | None)
                dtos_com_resultado: list[tuple[dict, str | None]] = []

                for dado in filtrados:
                    dto = _validar_proposicao(dado)
                    if dto is None:
                        total_erros += 1
                        continue

                    if not cota_gemini_esgotada:
                        try:
                            dto, resultado = self._classificar_e_filtrar(dto)
                        except Exception:
                            cota_gemini_esgotada = True
                            dto["classificacao_status"] = Proposicao.CLASSIFICACAO_PENDENTE
                            resultado = None
                    else:
                        dto["classificacao_status"] = Proposicao.CLASSIFICACAO_PENDENTE
                        resultado = None

                    if resultado == RESULTADO_IRRELEVANTE:
                        total_descartados += 1
                        continue  # não persistir

                    dtos_com_resultado.append((dto, resultado))

                if dtos_com_resultado:
                    dtos_apenas = [d for d, _ in dtos_com_resultado]
                    contadores = repo.upsert_proposicoes_lote(dtos_apenas)
                    total_inseridos += contadores["inseridos"]
                    total_atualizados += contadores["atualizados"]

                    for dto, categoria_nome in dtos_com_resultado:
                        if categoria_nome:
                            repo.vincular_categoria(dto["id"], categoria_nome)

                total_processados += len(filtrados)
                pagina += 1

        except Exception as exc:
            logger.exception("Erro interno inesperado na sincronização.")
            status_final = SyncExecution.STATUS_ERRO_INTERNO
            mensagem_erro = str(exc)

        if cota_gemini_esgotada and status_final == SyncExecution.STATUS_CONCLUIDO:
            status_final = SyncExecution.STATUS_CONCLUIDO_PARC

        repo.atualizar_sync_execution(
            execucao.id,
            finalizado_em=datetime.now(timezone.utc),
            status=status_final,
            total_processados=total_processados,
            total_inseridos=total_inseridos,
            total_atualizados=total_atualizados,
            total_erros=total_erros,
            mensagem_erro=mensagem_erro,
        )

        resumo = {
            "status": status_final,
            "total_processados": total_processados,
            "total_inseridos": total_inseridos,
            "total_atualizados": total_atualizados,
            "total_erros": total_erros,
            "total_descartados": total_descartados,
        }
        logger.info(
            "=== Sincronização concluída: %s | processados=%d inseridos=%d "
            "atualizados=%d erros=%d descartados=%d ===",
            status_final, total_processados, total_inseridos,
            total_atualizados, total_erros, total_descartados,
        )
        return resumo
