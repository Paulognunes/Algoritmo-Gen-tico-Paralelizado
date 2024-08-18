import csv


def converter_cromossomo_para_decimal(cromossomo):
    # Obtém o valor decimal referente ao cromossomo. Basicamente transforma o cromossomo "binário" em decimal.
    cromossomo.reverse()
    potencia = 0
    valor = 0
    for i in cromossomo:
        if i == '1':
            valor = valor + (2 ** potencia)
        potencia += 1
    cromossomo.reverse()
    return valor


def interpolar_valor(n, start1, stop1, start2, stop2):
    # Interpolação de valores. Converte um valor contido em um intervalo para outro intervalo.
    return ((n - start1) / (stop1 - start1)) * (stop2 - start2) + start2


def leitura_dados(nome_arquivo):
    # Leitura dos dados
    sucetiveis_sjdr = []
    infectados_sjdr = []
    recuperados_sjdr = []

    arq = open(nome_arquivo)
    dados_sjdr = csv.DictReader(arq, fieldnames=["S", "I", "R"])

    for row in dados_sjdr:
        sucetiveis_sjdr.append(int(row['S']))
        infectados_sjdr.append(int(row['I']))
        recuperados_sjdr.append(int(row['R']))

    arq.close()
    return sucetiveis_sjdr, infectados_sjdr, recuperados_sjdr
