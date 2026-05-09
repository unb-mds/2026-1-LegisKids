from services.camara_api import listar_proposicoes
from datetime import datetime

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

proposicoes = listar_proposicoes(qntItens, dataInicio["dataInput"], dataFim["dataInput"], ordem, ordenacao)

for proposicao in proposicoes:
    print("ID:", proposicao.get("id"))
    print("Tipo:", proposicao.get("siglaTipo"))
    print("Número:", proposicao.get("numero"))
    print("Ano:", proposicao.get("ano"))
    print("Data de apresentação:", proposicao.get("dataApresentacao"))
    print("Ementa:", proposicao.get("ementa"))
    print("------ # -------")