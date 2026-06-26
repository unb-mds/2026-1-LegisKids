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

CATEGORIAS_FIXAS = [
    "cyberbullying",
    "exploração sexual infantil online",
    "proteção de dados de menores",
    "segurança digital infantil",
    "regulação de plataformas digitais",
    "conteúdos nocivos para menores",
    "crimes virtuais contra crianças",
    "privacidade de menores",
    "outros",
]

STATUS_VALIDOS_SITUACAO = {
    "Em tramitação",
    "Aprovado",
    "Arquivado",
    "Encerrado",
}

_CAMPOS_OBRIGATORIOS = ("id", "siglaTipo", "numero", "ano", "ementa", "dataApresentacao")


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
    """Busca uma página de proposições na API da Câmara com retry automático."""
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
    for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(valor[:19], fmt).date()
        except ValueError:
            continue
    return None


def _validar_proposicao(dado: dict) -> dict | None:
    """Valida e normaliza um dado bruto da API. Retorna DTO ou None se inválido."""
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
        logger.warning("Proposição %s: dataApresentacao inválida '%s'. Ignorando.", dado.get("id"), dado.get("dataApresentacao"))
        return None

    descricao_situacao = dado.get("descricaoSituacao") or "Em tramitação"
    if descricao_situacao not in STATUS_VALIDOS_SITUACAO:
        descricao_situacao = "Em tramitação"

    sigla_partido = dado.get("siglaPartido") or ""

    return {
        "id": int(dado["id"]),
        "sigla_tipo": str(dado["siglaTipo"])[:20],
        "numero": int(dado["numero"]),
        "ano": int(dado["ano"]),
        "ementa": ementa,
        "data_apresentacao": data_apresentacao,
        "descricao_situacao": descricao_situacao,
        "sigla_partido": sigla_partido[:20],
        "data_coleta": datetime.now(timezone.utc),
        "classificacao_status": Proposicao.CLASSIFICACAO_PENDENTE,
    }


def _filtrar_por_palavras_chave(dados: list[dict]) -> list[dict]:
    palavras = [p.lower() for p in PALAVRAS_CHAVE]
    resultado = []
    for d in dados:
        texto = " ".join([
            str(d.get("ementa", "")),
            str(d.get("ementaDetalhada", "")),
        ]).lower()
        if any(p in texto for p in palavras):
            resultado.append(d)
    return resultado


def _categorizar_via_gemini(ementa: str) -> str:
    """Envia a ementa ao Gemini e retorna a categoria. Lança exceção em falha."""
    try:
        import google.generativeai as genai
    except ImportError:
        raise RuntimeError("google-generativeai não instalado.")

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("GOOGLE_API_KEY não configurada.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    categorias_str = "\n".join(f"- {c}" for c in CATEGORIAS_FIXAS)
    prompt = (
        f"Classifique a seguinte ementa legislativa em UMA das categorias abaixo.\n"
        f"Responda SOMENTE com o nome exato da categoria, sem explicações.\n\n"
        f"Categorias válidas:\n{categorias_str}\n\n"
        f"Ementa: {ementa[:500]}"
    )

    response = model.generate_content(prompt, request_options={"timeout": 5})
    categoria = response.text.strip().lower()

    if categoria not in CATEGORIAS_FIXAS:
        logger.warning("Gemini retornou categoria inválida: '%s'", categoria)
        raise ValueError(f"Categoria inválida: {categoria}")

    return categoria


class CamaraService:
    def __init__(self):
        self._rpm = int(os.getenv("GEMINI_RATE_LIMIT_RPM", "15"))
        self._min_interval = 60.0 / self._rpm if self._rpm > 0 else 0
        self._last_gemini_call = 0.0

    def _categorizar_com_rate_limit(self, ementa: str) -> str:
        """Aplica rate limit antes de chamar o Gemini."""
        agora = time.monotonic()
        espera = self._min_interval - (agora - self._last_gemini_call)
        if espera > 0:
            logger.info("Gemini rate limit: aguardando %.1fs.", espera)
            time.sleep(espera)
        self._last_gemini_call = time.monotonic()
        return _categorizar_via_gemini(ementa)

    def _categorizar_com_fallback(self, dto: dict) -> dict:
        """Categoriza a proposição via Gemini; em falha, define pendente_classificacao."""
        try:
            categoria = self._categorizar_com_rate_limit(dto["ementa"])
            dto["classificacao_status"] = Proposicao.CLASSIFICACAO_CLASSIFICADO
            logger.debug("Proposição %d categorizada como '%s'.", dto["id"], categoria)
        except Exception as exc:
            logger.warning(
                "Falha ao categorizar proposição %d via Gemini: %s. Marcando como pendente.",
                dto["id"],
                exc,
            )
            dto["classificacao_status"] = Proposicao.CLASSIFICACAO_PENDENTE
        return dto

    def run_sync(self) -> dict:
        """Executa a sincronização completa. Registra tudo em sync_executions."""
        logger.info("=== Sincronização da Câmara iniciada ===")
        execucao = repo.criar_sync_execution()

        total_processados = 0
        total_inseridos = 0
        total_atualizados = 0
        total_erros = 0
        status_final = SyncExecution.STATUS_CONCLUIDO
        mensagem_erro = None
        cota_gemini_esgotada = False

        try:
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
                logger.info("Página %d: %d recebidos, %d após filtro.", pagina, len(dados_brutos), len(filtrados))

                dtos = []
                for dado in filtrados:
                    dto = _validar_proposicao(dado)
                    if dto is None:
                        total_erros += 1
                        continue

                    if not cota_gemini_esgotada:
                        try:
                            dto = self._categorizar_com_fallback(dto)
                        except Exception:
                            cota_gemini_esgotada = True
                            dto["classificacao_status"] = Proposicao.CLASSIFICACAO_PENDENTE

                    dtos.append(dto)

                if dtos:
                    contadores = repo.upsert_proposicoes_lote(dtos)
                    total_inseridos += contadores["inseridos"]
                    total_atualizados += contadores["atualizados"]

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
        }
        logger.info(
            "=== Sincronização concluída: %s | processados=%d inseridos=%d atualizados=%d erros=%d ===",
            status_final,
            total_processados,
            total_inseridos,
            total_atualizados,
            total_erros,
        )
        return resumo
