import requests
import time

URL_BASE = "https://dadosabertos.camara.leg.br/api/v2"


def listar_proposicoes(qntItens, dataInicio, dataFim, ordem, ordenacao):
    url = f"{URL_BASE}/proposicoes"

    for _ in range(3):
        resposta = requests.get(
            url,
            params={"itens": qntItens, 
                    "dataApresentacaoInicio": dataInicio, 
                    "dataApresentacaoFim": dataFim, 
                    "ordem": ordem,
                    "ordenarPor": ordenacao},

            headers={"Accept": "application/json"},
            timeout=20
        )

        #print("Status:", resposta.status_code)
        #print("Resposta:", resposta.text)

        if resposta.status_code == 200:
            dados = resposta.json()
            if (dados["dados"] == []):
                print("Não foram econtrados os dados com base nos filtros!")

            return dados["dados"]

        if resposta.status_code == 504:
            print("A API demorou para responder. Tentando novamente...")
            time.sleep(2)
        

    print("Não foi possível acessar a API.")
    return []