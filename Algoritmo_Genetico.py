import Funcoes
from Individuo import Individuo
from random import random
import multiprocessing

class AlgoritmoGenetico:
    # Definição da classe AG, responsável por "resolver" o problema.

    def __init__(self, tamanho_populacao):
        # Construtor da classe.
        self.tamanho_populacao = tamanho_populacao
        self.populacao = []
        self.geracao = 0
        self.melhor_solucao = 0
        self.melhores_solucoes = []

    def inicializar_populacao(self, nro_bits):
        # Inicializa a população inicial. Basicamente gera soluções aleatórias, que serão "evoluidas" posteriormente.
        for i in range(self.tamanho_populacao):
            self.populacao.append(Individuo(nro_bits))

        self.melhor_solucao = self.populacao[0]

    def seleciona_pai(self, soma_avaliacao):
        # Simulação da roleta viciada
        pai = -1
        valor_sorteado = random() * soma_avaliacao
        soma = 0
        i = 0

        while i < len(self.populacao) and soma < valor_sorteado:
            soma += self.populacao[i].nota_avaliacao
            pai += 1
            i += 1

        return pai

    def soma_avaliacoes(self):
        soma = 0
        for individuo in self.populacao:
            soma += individuo.nota_avaliacao

        return soma

    def ordenar_populacao(self):
        self.populacao = sorted(self.populacao, key=lambda populacao: populacao.nota_avaliacao, reverse=True)

    def melhor_individuo(self, individuo):
        # Compara a nota desses indivíduos. Quanto menor a nota, melhor é a solução. Ela representa o erro da simulação
        if self.melhor_solucao.nota_avaliacao < individuo.nota_avaliacao:
            self.melhor_solucao = individuo
            self.melhores_solucoes.append(individuo)

    def visualizar_geracao(self, nro_bits, geracao):
        # Imprime o melhor indivíduo da geração. Ele sempre estará na posição zero.
        melhor = self.populacao[0]

        # Obtém-se o valor decimal referente aos cromossomos beta e gamma.
        beta = Funcoes.converter_cromossomo_para_decimal(melhor.beta)
        gamma = Funcoes.converter_cromossomo_para_decimal(melhor.gamma)

        # Interpolamos esses valores para o intervalo entre 0 e 1.
        beta = Funcoes.interpolar_valor(beta, 0, ((2 ** nro_bits) - 1), 0, 1)
        gamma = Funcoes.interpolar_valor(gamma, 0, ((2 ** nro_bits) - 1), 0, 1)

        print(f'\nGeração Atual: {geracao}'
              f'\nGeração do Individuo: {self.populacao[0].geracao}'
              f'\nBeta : {beta}'
              f'\nGamma: {gamma}'
              f'\nAvaliação Beta: {melhor.nota_avaliacao_beta}'
              f'\nAvaliação Gamma: {melhor.nota_avaliacao_gamma}'
              f'\nNOTA: {melhor.nota_avaliacao}')

    def evoluir_solucao(self, taxa_mutacao, nro_bits, nro_geracoes, inf, rec, grafo, dias, elitismo, nos_infectados,
                        nos_recuperados):

        # Gera a população inicial
        self.inicializar_populacao(nro_bits)

        # Avalia os individuos na população
        """for individuo in self.populacao:
            individuo.fitness(inf, rec, nro_bits, grafo, dias, nos_infectados, nos_recuperados)"""

        with multiprocessing.Pool(processes=4) as pool:
            self.populacao = pool.starmap(Individuo.fitness, [(individuo, inf, rec, nro_bits, grafo, dias, nos_infectados,
                                                               nos_recuperados) for individuo in self.populacao])

        self.ordenar_populacao()
        self.visualizar_geracao(nro_bits, 0)

        # Execução do loop responsável pela convergência dos parâmetros
        for i in range(1, nro_geracoes + 1):
            soma_avaliacao = self.soma_avaliacoes()
            nova_populacao = []

            # Os dois melhores indivíduos da população são selecionados como "pais" da nova população.
            for individuo_gerados in range(0, self.tamanho_populacao - elitismo, 2):
                # Seleção dos pais
                pai1 = self.seleciona_pai(soma_avaliacao)
                pai2 = self.seleciona_pai(soma_avaliacao)

                # Aplicação do crossover, gerando novos filhos com os genes dos pais
                filhos = self.populacao[pai1].crossover(self.populacao[pai2])

                # Aplicação do processo de mutação nos filhos.
                nova_populacao.append(filhos[0].mutacao(taxa_mutacao))
                nova_populacao.append(filhos[1].mutacao(taxa_mutacao))

            # Realiza o elitismo na nova população
            for indice in range(elitismo):
                nova_populacao.append(self.populacao[indice])

            # A população antiga é substituida pela nova população, que foi criada anteriormente.
            self.populacao = list(nova_populacao)

            with multiprocessing.Pool(processes=4) as pool:
                self.populacao = pool.starmap(Individuo.fitness, [(individuo, inf, rec, nro_bits, grafo, dias, nos_infectados,
                                                                   nos_recuperados) for individuo in self.populacao])

            self.ordenar_populacao()
            self.visualizar_geracao(nro_bits, i)

            melhor = self.populacao[0]
            self.melhor_individuo(melhor)
