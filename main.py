import Funcoes
import time
import matplotlib
import networkx as nx
import matplotlib.pyplot as plt
from random import random, sample
from Algoritmo_Genetico import AlgoritmoGenetico


def executar(nome_arq, nome_graph, nro_simul):
    inicio = time.time()

    # Lendo os dados e gerando o grafo
    suce, inf, rec = Funcoes.leitura_dados(nome_arq)

    # Variáveis de controle
    tamanho_populacao = 4
    nro_bits = 10
    nro_geracoes = 100
    taxa_mutacao = 0.1
    dias = len(suce)
    elitismo = 2
    quantidade_infec = inf[0]
    quantidade_rec = rec[0]

    """
    # Gerando Grafo
    grafo = nx.erdos_renyi_graph(nos, probabilidade_criacao_aresta)
    path = str(nro_simul) + "grafo.graphml"
    nx.write_graphml(grafo, path)
    """
    grafo = nx.read_graphml(nome_graph)
    nos = len(grafo.nodes())

    # Sorteia um conjunto de nós que será os nós infectados e recuperados da simulação
    aux = sample(grafo.nodes(), (quantidade_infec + quantidade_rec))

    # Seleciona aleatoriamente quais nós serão os nós infectados na simulação
    nos_infectados = sample(aux, quantidade_infec)
    nos_recuperados = []

    for i in aux:
        if i not in nos_infectados:
            nos_recuperados.append(i)

    deg = nx.degree(grafo)
    media_grau = 0

    for _, j in deg:
        media_grau += j

    media_grau = media_grau / nos
    ag = AlgoritmoGenetico(tamanho_populacao)
    ag.evoluir_solucao(taxa_mutacao, nro_bits, nro_geracoes, inf, rec, grafo, dias, elitismo, nos_infectados,
                       nos_recuperados)

    nome_arq_result = str(nro_simul) + '_resultados.txt'
    dados = open(nome_arq_result, 'w')
    dados.write('########################################\n')
    dados.write('            Configuração AG\n')
    dados.write('########################################\n')
    dados.write('\nTamanho População: ' + str(tamanho_populacao))
    dados.write('\nNúmero de Gerações: ' + str(nro_geracoes))
    dados.write('\nBits Cromossomo: ' + str(nro_bits))
    dados.write('\nDias: ' + str(dias))
    dados.write('\nTaxa de Mutação: ' + str(taxa_mutacao))
    dados.write('\nQuantidade de nós: ' + str(nos))
    dados.write('\nNós infectados: ' + str(nos_infectados))
    dados.write('\nNome do arquivo de amostra: ' + str(nome_arq))
    dados.write('\nGrau médio dos nós: ' + str(media_grau))
    dados.write('\n\n')

    dados.write('########################################\n')
    dados.write('     Evolução da solução encontrada\n')
    dados.write('########################################\n')

    for i in range(len(ag.melhores_solucoes)):
        beta = Funcoes.converter_cromossomo_para_decimal(ag.melhores_solucoes[i].beta)
        gamma = Funcoes.converter_cromossomo_para_decimal(ag.melhores_solucoes[i].gamma)
        beta = round(Funcoes.interpolar_valor(beta, 0, ((2 ** nro_bits) - 1), 0, 1), 8)
        gamma = round(Funcoes.interpolar_valor(gamma, 0, ((2 ** nro_bits) - 1), 0, 1), 8)
        r0 = 0
        if gamma != 0:
            r0 = beta / gamma

        dados.write('\nGeração: ' + str(ag.melhores_solucoes[i].geracao))
        dados.write('\nBeta : ' + str(beta))
        dados.write('\nGamma: ' + str(gamma))
        dados.write('\nAvaliação Beta: ' + str(ag.melhores_solucoes[i].nota_avaliacao_beta))
        dados.write('\nAvaliação Gamma: ' + str(ag.melhores_solucoes[i].nota_avaliacao_gamma))
        dados.write('\nNOTA: ' + str(ag.melhores_solucoes[i].nota_avaliacao))
        dados.write('\nNúmero Básico de Reprodução (R0): ' + str(r0))
        dados.write('\nSucetiveis Simulação: ' + str(ag.melhores_solucoes[i].sucetiveis_simulacao))
        dados.write('\nInfectados Simulação: ' + str(ag.melhores_solucoes[i].infectados_simulacao))
        dados.write('\nRecuperados Simulação: ' + str(ag.melhores_solucoes[i].recuperados_simulacao))
        dados.write('\n')

    beta = Funcoes.converter_cromossomo_para_decimal(ag.melhor_solucao.beta)
    gamma = Funcoes.converter_cromossomo_para_decimal(ag.melhor_solucao.gamma)
    beta = round(Funcoes.interpolar_valor(beta, 0, ((2 ** nro_bits) - 1), 0, 1), 8)
    gamma = round(Funcoes.interpolar_valor(gamma, 0, ((2 ** nro_bits) - 1), 0, 1), 8)

    dados.write('\n\nMelhor Solução Encontrada:')
    dados.write('\nGeração: ' + str(ag.melhor_solucao.geracao))
    dados.write('\nBeta : ' + str(beta))
    dados.write('\nGamma: ' + str(gamma))
    dados.write('\nAvaliação Beta: ' + str(ag.melhor_solucao.nota_avaliacao_beta))
    dados.write('\nAvaliação Gamma: ' + str(ag.melhor_solucao.nota_avaliacao_gamma))
    dados.write('\nNOTA: ' + str(ag.melhor_solucao.nota_avaliacao))
    dados.write('\nSucetiveis Simulação: ' + str(ag.melhor_solucao.sucetiveis_simulacao))
    dados.write('\nInfectados Simulação: ' + str(ag.melhor_solucao.infectados_simulacao))
    dados.write('\nRecuperados Simulação: ' + str(ag.melhor_solucao.recuperados_simulacao))
    dados.write('\n\n')

    resultados = open("resultados_simulacao.txt", 'w')
    for i in range(dias):
        resultados.write(str(ag.melhor_solucao.sucetiveis_simulacao[i]) + ',' +
                         str(ag.melhor_solucao.infectados_simulacao[i]) + ',' +
                         str(ag.melhor_solucao.recuperados_simulacao[i]) + '\n')
    resultados.close()

    lista_de_dias = []
    for i in range(1, dias + 1):
        lista_de_dias.append(i)

    # Plotando o gráfico de Infectados
    plt.plot(lista_de_dias, inf, label='Infectados Reais', linestyle='-')
    plt.plot(lista_de_dias, ag.melhor_solucao.infectados_simulacao, label='Infectados Simulados', linestyle='--')

    fig1 = plt.gcf()
    matplotlib.pyplot.xlabel('Dias')
    matplotlib.pyplot.ylabel('Número de Pessoas')
    plt.title("Comparação Infectados")
    plt.legend()
    plt.close()
    # plt.show()

    # Salvando o gráfico
    nome_figura_inf = str(nro_simul) + '_Figura_Infectados.pdf'
    fig1.savefig(nome_figura_inf, format='pdf')

    # Plotando o gráfico de Recuperados
    plt.plot(lista_de_dias, rec, label='Recuperados Reais', linestyle='-')
    plt.plot(lista_de_dias, ag.melhor_solucao.recuperados_simulacao, label='Recuperados Simulados', linestyle='--')

    fig2 = plt.gcf()
    matplotlib.pyplot.xlabel('Dias')
    matplotlib.pyplot.ylabel('Número de Pessoas')
    plt.title("Comparação Recuperados")
    plt.legend()
    plt.close()
    # plt.show()

    # Salvando o gráfico
    nome_figura_rec = str(nro_simul) + '_Figura_Recuperados.pdf'
    fig2.savefig(nome_figura_rec, format='pdf')

    fim = time.time()
    dados.write('Tempo de Execução: ' + str(fim - inicio) + ' segundos')
    dados.close()


if __name__ == '__main__':
    # main("dados_sjdr_12_03_2021__22_04_2021.csv", 0.00007, 1)
    executar("dados_sjdr_12_03_2021__22_04_2021.csv", "SJDR.graphml", 1)
