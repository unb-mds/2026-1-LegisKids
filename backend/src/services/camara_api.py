import requests
import time

URL_BASE = "https://dadosabertos.camara.leg.br/api/v2"

def listar_proposicoes(qntItens, dataInicio, dataFim, codTema, ordem, ordenacao, palavras_chave=None):
    url = f"{URL_BASE}/proposicoes"
    
    # Se temos filtros de palavras-chave, pegamos mais itens da API
    # porque precisamos filtrar depois
    itens_requisicao = qntItens
    if palavras_chave:
        itens_requisicao = min(qntItens * 3, 100)
    
    params = {
        "itens": itens_requisicao,
        "dataApresentacaoInicio": dataInicio,
        "dataApresentacaoFim": dataFim,
        "ordem": ordem,
        "ordenarPor": ordenacao,
    }

    if codTema:
        params["codTema"] = codTema

    for _ in range(3):
        resposta = requests.get(
            url,
            params=params,
            headers={"Accept": "application/json"},
            timeout=20,
        )

        if resposta.status_code == 200:
            dados = resposta.json()
            resultados = dados.get("dados", [])
            
            # Aplica filtro de palavras-chave se foi fornecido
            if palavras_chave:
                resultados = filtrar_por_palavras_chave(resultados, palavras_chave)
            
            if not resultados:
                print("Não foram encontrados dados com base nos filtros!")
            
            return resultados[:qntItens]

        if resposta.status_code == 504:
            print("A API demorou para responder. Tentando novamente...")
            time.sleep(2)

    print("Não foi possível acessar a API.")
    return []


def filtrar_por_palavras_chave(proposicoes, palavras_chave):
    if not palavras_chave:
        return proposicoes
    
    # Converte todas as palavras para minúsculas para comparação
    palavras_chave_lower = [p.lower() for p in palavras_chave]
    
    resultados = []
    for prop in proposicoes:
        # Procura em múltiplos campos para ter mais confiança
        texto_busca = " ".join([
            str(prop.get("ementa", "")),                    # Descrição curta
            str(prop.get("ementaDetalhada", "")),           # Descrição completa
            str(prop.get("explicitacao", "")),              # Explicação adicional
            str(prop.get("siglaTipo", "")),                 # Tipo (PL, PEC, etc)
            str(prop.get("numero", "")),                    # Número da proposição
            str(prop.get("ano", "")),                       # Ano
        ]).lower()
        
        # Verifica se alguma palavra-chave está em qualquer um dos campos
        if any(palavra in texto_busca for palavra in palavras_chave_lower):
            resultados.append(prop)
    
    return resultados


def buscarCodTema():
    url_codTema = f"{URL_BASE}/referencias/proposicoes/codTema"

    try:
        resposta = requests.get(url_codTema, headers={"Accept": "application/json"}, timeout=20)
        return resposta
    except requests.RequestException:
        print("Erro ao acessar a API de temas.")
        return None

    