from backend.services.camara_api import listar_proposicoes
from backend.services.camara_api import buscarCodTema
from datetime import datetime

# Lista de palavras-chave para filtrar proposições
FILTROS_PALAVRAS_CHAVE = [
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

def lerData(mensagem):
    while True:
        dataTexto = input(mensagem)
        tiposData = {"dataInput": dataTexto, 
                     "dataFormatada": None}
        
        try:
            dataFormatada = datetime.strptime(dataTexto, "%Y-%m-%d")
            tiposData["dataFormatada"] = dataFormatada
            return tiposData
        
        except ValueError:
            print("Formato de dado escrito errado, digite no formato pedido!")

def verificarData(dataInicio, dataFim):
    dataHoje = datetime.today()
    difData = dataFim - dataInicio

    if (dataFim - dataInicio).days > 92:
        print("O limite máximo entre datas é de 3 meses")
        return True
    
    elif (dataHoje < dataFim):        
        print("Data inválida, use a dataFim até no máximo o dia de hoje")
        return True
    
    elif (difData.days < 0):
        print("A data final não pode ser menor que a data de início")
        return True

    else:
        return False


def listarDadosTema():
    resposta = buscarCodTema()
    if resposta is None:
        print("Erro ao buscar temas.")
        return []

    if resposta.status_code != 200:
        print("Erro ao buscar temas. Código de status:", resposta.status_code)
        return []

    dadosDeTemas = resposta.json().get("dados", [])
    listaCodigos = []

    for tema in dadosDeTemas:
        cod = tema.get("cod")
        nome = tema.get("nome")

        if cod is not None:
            print("Código:", cod)
            listaCodigos.append(str(cod))
        if nome:
            print("Tema:", nome, "\n")

    return listaCodigos


def selecionarCodTema(listaCodTemas):
    if not listaCodTemas:
        return None

    print("\n--- Escolha o Tema ---")
    print("0. Buscar em TODOS os temas (sem filtro de tema)")
    for idx, cod in enumerate(listaCodTemas, start=1):
        print(f"{idx}. Tema {cod}")
    
    while True:
        escolha = input("\nEscolha o tema (0 para todos, ou número do tema): ")
        
        if escolha.strip() == "0":
            return None  # Retorna None para buscar em todos os temas
        
        if escolha in listaCodTemas:
            return escolha
        
        print("Escolha um código válido, escreva novamente corretamente")


def listarFiltrosTema():
    print("\n--- Filtros de Palavras-chave ---")
    for idx, termo in enumerate(FILTROS_PALAVRAS_CHAVE, start=1):
        print(f"{idx}. {termo}")
    print("0. Nenhum filtro")


def selecionarFiltrosTema():
    listarFiltrosTema()
    while True:
        escolha = input("\nEscolha os filtros (exemplo: 1,3,5 ou 0): ")
        
        if escolha.strip() == "0":
            return []

        try:
            numeros = [int(x.strip()) for x in escolha.split(",")]
            selecionados = []
            
            for num in numeros:
                if 1 <= num <= len(FILTROS_PALAVRAS_CHAVE):
                    selecionados.append(FILTROS_PALAVRAS_CHAVE[num - 1])
                else:
                    print(f"Número {num} inválido!")
                    raise ValueError

            return selecionados
        
        except ValueError:
            print("Digite números válidos separados por vírgula")


controleLoop = True
qntItens = int(input("Digite qnt de proposições: "))

while controleLoop:
    dataInicio = lerData("Digite a data de início em AAAA-MM-DD: ")
    dataFim = lerData("Digite a data final em AAAA-MM-DD: ")

    controleLoop = verificarData(dataInicio["dataFormatada"], dataFim["dataFormatada"])

controleLoop = True
while controleLoop:
    ordem = input("Quer em Ascendente (ASC) ou Descendente (DESC): ")
    if ordem in ["ASC", "DESC"]:
        controleLoop = False
    else:
        print("Ordem errada, escreva a sigla correta")

controleLoop = True
while controleLoop:
    ordenacao = input("Quer ordenar a partir de qual: id, codTipo, siglaTipo, numero ou ano? ")
    if ordenacao in ["id", "codTipo", "siglaTipo", "numero", "ano"]:
        controleLoop = False
    else:
        print("Ordenacao escrita errada, escreva novamente corretamente")

listaCodTemas = listarDadosTema()
if not listaCodTemas:
    print("Não foi possível carregar os temas. Encerrando o programa.")
    raise SystemExit(1)

codTema = selecionarCodTema(listaCodTemas)
# codTema pode ser None (buscar em todos) ou um código específico

if codTema is None:
    print("\nBuscando em TODOS os temas...\n")
else:
    print(f"\nBuscando no tema: {codTema}\n")

# Agora o usuário seleciona filtros de palavras-chave
palavras_chave = selecionarFiltrosTema()

if palavras_chave:
    print(f"Filtros selecionados: {', '.join(palavras_chave)}\n")
else:
    print("Nenhum filtro de palavras-chave selecionado\n")

proposicoes = listar_proposicoes(
    qntItens,
    dataInicio["dataInput"],
    dataFim["dataInput"],
    codTema,
    ordem,
    ordenacao,
    palavras_chave,
)

for proposicao in proposicoes:
    print("ID:", proposicao.get("id"))
    print("Tipo:", proposicao.get("siglaTipo"))
    print("Número:", proposicao.get("numero"))
    print("Ano:", proposicao.get("ano"))
    print("Data de apresentação:", proposicao.get("dataApresentacao"))
    print("Ementa:", proposicao.get("ementa"))
    print("------ # -------")