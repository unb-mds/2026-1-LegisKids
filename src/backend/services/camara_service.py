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
    data_inicio = os.getenv("CAMARA_DATA_INICIO", "2022-01-01")
    params = {
        "itens": itens,
        "pagina": pagina,
        "ordem": "DESC",
        "ordenarPor": "id",
        "dataApresentacaoInicio": data_inicio,
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


def _classificar_lote_via_gemini(ementas: list[str]) -> list[list[str]]:
    """Classifica um lote de ementas em uma única chamada ao Gemini.

    Retorna lista de listas na mesma ordem das ementas:
    - ["irrelevante"]              → descartar
    - ["cyberbullying", "privacidade de menores"] → categorias que realmente se aplicam
    Lança exceção se a API falhar — o chamador trata o fallback.
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
    ementas_formatadas = "\n".join(f"{i + 1}: {e[:400]}" for i, e in enumerate(ementas))
    prompt = (
        "Você é um classificador de proposições legislativas brasileiras.\n\n"
        "Para cada ementa abaixo, responda com as categorias que realmente se aplicam.\n"
        "Seja conservador: só inclua uma categoria se a ementa tratar direta e explicitamente do tema.\n\n"
        "Opções de resposta por ementa:\n"
        '- "irrelevante" → se NÃO tratar de proteção de crianças ou adolescentes '
        "no ambiente digital/internet\n"
        "- Uma ou mais categorias da lista abaixo, separadas por vírgula, "
        "somente as que realmente se aplicam (sem exagerar)\n\n"
        f"Categorias válidas:\n{categorias_str}\n\n"
        "Formato de resposta (uma linha por ementa):\n"
        "1: <categoria1> ou <categoria1>, <categoria2> ou irrelevante\n"
        "2: ...\n\n"
        f"Ementas:\n{ementas_formatadas}"
    )

    for tentativa in range(2):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=genai_types.GenerateContentConfig(
                    http_options=genai_types.HttpOptions(timeout=60000),
                ),
            )
            break
        except Exception as exc:
            if tentativa == 0 and _is_rate_limit_error(exc):
                logger.warning("Gemini 429 ResourceExhausted: aguardando 60s antes de re-tentar.")
                time.sleep(60)
                continue
            raise

    resultados: list[list[str]] = [[RESULTADO_IRRELEVANTE]] * len(ementas)
    for linha in response.text.strip().splitlines():
        if ":" not in linha:
            continue
        prefixo, _, valor = linha.partition(":")
        try:
            idx = int(prefixo.strip()) - 1
        except ValueError:
            continue
        if not (0 <= idx < len(ementas)):
            continue
        partes = [p.strip().lower() for p in valor.split(",")]
        if partes == [RESULTADO_IRRELEVANTE]:
            resultados[idx] = [RESULTADO_IRRELEVANTE]
        else:
            categorias_validas = [p for p in partes if p in CATEGORIAS_FIXAS]
            resultados[idx] = categorias_validas if categorias_validas else [RESULTADO_IRRELEVANTE]

    return resultados


# ── Service ───────────────────────────────────────────────────────────────────

class CamaraService:
    def __init__(self):
        self._batch_size = int(os.getenv("GEMINI_BATCH_SIZE", "10"))

    def _classificar_lote(self, dtos: list[dict]) -> list[tuple[dict, list[str] | None]]:
        """Classifica um lote de DTOs em uma única chamada ao Gemini.

        Retorna lista de (dto, resultado) onde resultado é:
        - list[str] com categorias → relevante, deve persistir e vincular todas
        - [RESULTADO_IRRELEVANTE]  → descartar, não persistir
        - None                     → Gemini falhou, persistir como pendente_classificacao
        """
        if not dtos:
            return []

        logger.info("Gemini: classificando lote de %d proposições.", len(dtos))
        ementas = [dto["ementa"] for dto in dtos]
        try:
            resultados = _classificar_lote_via_gemini(ementas)
        except Exception as exc:
            logger.warning("Falha na classificação em lote via Gemini: %s. Marcando como pendentes.", exc)
            for dto in dtos:
                dto["classificacao_status"] = Proposicao.CLASSIFICACAO_PENDENTE
            return [(dto, None) for dto in dtos]

        saida = []
        for dto, categorias in zip(dtos, resultados):
            if categorias == [RESULTADO_IRRELEVANTE]:
                saida.append((dto, [RESULTADO_IRRELEVANTE]))
            else:
                dto["classificacao_status"] = Proposicao.CLASSIFICACAO_CLASSIFICADO
                saida.append((dto, categorias))
        return saida

    def _classificar_e_filtrar(self, dto: dict) -> tuple[dict, list[str] | None]:
        """Wrapper single-item para compatibilidade interna."""
        return self._classificar_lote([dto])[0]

    def _retentar_pendentes(self) -> None:
        """Re-classifica proposições com status pendente_classificacao em lotes."""
        pendentes = repo.get_proposicoes_pendentes(limite=50)
        if not pendentes:
            return
        logger.info("Re-tentando classificação de %d proposições pendentes.", len(pendentes))

        for i in range(0, len(pendentes), self._batch_size):
            lote = pendentes[i:i + self._batch_size]
            dtos = [{"id": p.id, "ementa": p.ementa, "classificacao_status": p.classificacao_status} for p in lote]
            try:
                pares = self._classificar_lote(dtos)
            except Exception as exc:
                logger.warning("Falha ao re-tentar lote de pendentes: %s.", exc)
                continue
            for dto, categorias in pares:
                if categorias == [RESULTADO_IRRELEVANTE]:
                    repo.deletar_proposicao(dto["id"])
                    logger.info("Proposição pendente %d era irrelevante — removida.", dto["id"])
                elif categorias is not None:
                    repo.vincular_categorias_lote(dto["id"], categorias)
                    repo.atualizar_classificacao_status(dto["id"], Proposicao.CLASSIFICACAO_CLASSIFICADO)
                    logger.info("Proposição pendente %d classificada como %s.", dto["id"], categorias)

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

                # Filtro 1: early-stop — se todos os IDs da página já estão no banco,
                # as páginas seguintes (IDs menores, ordem DESC) também estarão.
                ids_brutos = [d["id"] for d in dados_brutos]
                ids_conhecidos = repo.get_ids_existentes(ids_brutos)
                if len(ids_conhecidos) == len(ids_brutos):
                    logger.info(
                        "Página %d: todos os %d IDs já no banco — paginação encerrada.",
                        pagina, len(ids_brutos),
                    )
                    break

                filtrados = _filtrar_por_palavras_chave(dados_brutos)
                logger.info(
                    "Página %d: %d recebidos, %d após filtro de palavras-chave.",
                    pagina, len(dados_brutos), len(filtrados),
                )

                # Valida todos primeiro, depois classifica em lotes
                dtos_validos: list[dict] = []
                for dado in filtrados:
                    dto = _validar_proposicao(dado)
                    if dto is None:
                        total_erros += 1
                    else:
                        dtos_validos.append(dto)

                # Filtro 2: skip de IDs já conhecidos — evita rechamar o Gemini
                # para proposições já salvas (classificadas ou pendentes).
                # Pendentes são tratadas por _retentar_pendentes no início do run.
                novos = len(dtos_validos)
                dtos_validos = [dto for dto in dtos_validos if dto["id"] not in ids_conhecidos]
                pulados = novos - len(dtos_validos)
                if pulados:
                    logger.debug("Página %d: %d proposição(ões) já no banco — ignoradas.", pagina, pulados)

                dtos_com_resultado: list[tuple[dict, str | None]] = []
                for i in range(0, len(dtos_validos), self._batch_size):
                    lote = dtos_validos[i:i + self._batch_size]
                    if cota_gemini_esgotada:
                        for dto in lote:
                            dto["classificacao_status"] = Proposicao.CLASSIFICACAO_PENDENTE
                        dtos_com_resultado.extend((dto, None) for dto in lote)
                        continue
                    try:
                        pares = self._classificar_lote(lote)
                        dtos_com_resultado.extend(pares)
                    except Exception:
                        cota_gemini_esgotada = True
                        for dto in lote:
                            dto["classificacao_status"] = Proposicao.CLASSIFICACAO_PENDENTE
                        dtos_com_resultado.extend((dto, None) for dto in lote)

                # Filtra irrelevantes e persiste o restante
                para_persistir = []
                for dto, categorias in dtos_com_resultado:
                    if categorias == [RESULTADO_IRRELEVANTE]:
                        total_descartados += 1
                    else:
                        para_persistir.append((dto, categorias))

                if para_persistir:
                    dtos_apenas = [d for d, _ in para_persistir]
                    contadores = repo.upsert_proposicoes_lote(dtos_apenas)
                    total_inseridos += contadores["inseridos"]
                    total_atualizados += contadores["atualizados"]

                    for dto, categorias in para_persistir:
                        if categorias:
                            repo.vincular_categorias_lote(dto["id"], categorias)

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
