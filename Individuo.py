import Funcoes
import Simulador
from random import random, sample


class Individuo:
    # Cada indivíduo é uma possível solução para o problema.

    def __init__(self, nro_bits, geracao=0):
        # Construtor da classe, responsável por inicializar aleatoriamente os parâmetros beta e gamma
        self.beta = ["0", "0"]
        self.gamma = ["0", "0"]
        self.nota_avaliacao_beta = 0
        self.nota_avaliacao_gamma = 0
        self.nota_avaliacao = 0
        self.sucetiveis_simulacao = []
        self.infectados_simulacao = []
        self.recuperados_simulacao = []
        self.geracao = geracao

        # Inicialização aleatória dos cromossomos beta e gamma
        for i in range(nro_bits - 2):
            self.beta.append("0") if random() < 0.5 else self.beta.append("1")
            self.gamma.append("0") if random() < 0.5 else self.gamma.append("1")

    def fitness(self, infectados_sjdr, recuperados_sjdr, nro_bits, grafo, dias, nos_infectados, nos_recuperados):
        # Obtém-se o valor decimal referente aos cromossomos beta e gamma.
        beta = Funcoes.converter_cromossomo_para_decimal(self.beta)
        gamma = Funcoes.converter_cromossomo_para_decimal(self.gamma)

        # Interpolamos esses valores para o intervalo entre 0 e 1.
        beta = Funcoes.interpolar_valor(beta, 0, ((2 ** nro_bits) - 1), 0, 1)
        gamma = Funcoes.interpolar_valor(gamma, 0, ((2 ** nro_bits) - 1), 0, 1)

        # Simulação
        mse_beta, mse_gamma, suce, inf, rec = Simulador.simulacao(infectados_sjdr, recuperados_sjdr, grafo, dias, beta,
                                                                  gamma,
                                                                  nos_infectados, nos_recuperados)

        # A nota final é dada pela média dos erros de beta e gamma. Quanto menor esse erro, melhor é a solução!
        media = (mse_beta + mse_gamma) / 2

        self.nota_avaliacao_beta = mse_beta
        self.nota_avaliacao_gamma = mse_gamma

        self.sucetiveis_simulacao = suce.copy()
        self.infectados_simulacao = inf.copy()
        self.recuperados_simulacao = rec.copy()
        self.nota_avaliacao = round((1000000 / media), 5)
        return self

    def crossover(self, outro_individuo):
        # Realiza o crossover "de um único ponto" nos cromossomos beta e gamma.
        nro_bits = len(self.beta)
        corte_beta = round(random() * len(self.beta))

        # Crossover Beta.
        filho1_beta = outro_individuo.beta[0:corte_beta] + self.beta[corte_beta::]
        filho2_beta = self.beta[0:corte_beta] + outro_individuo.beta[corte_beta::]

        corte_gamma = round(random() * len(self.gamma))

        # Crossover Gamma.
        filho1_gamma = outro_individuo.gamma[0:corte_gamma] + self.gamma[corte_gamma::]
        filho2_gamma = self.gamma[0:corte_gamma] + outro_individuo.gamma[corte_gamma::]

        # Criação de dois novos indivíduos que herdaram os genes dos "pais".
        filhos = [Individuo(nro_bits, (self.geracao + 1)),
                  Individuo(nro_bits, (self.geracao + 1))]

        filhos[0].beta = filho1_beta
        filhos[1].beta = filho2_beta
        filhos[0].gamma = filho1_gamma
        filhos[1].gamma = filho2_gamma
        return filhos

    def mutacao(self, taxa_mutacao):
        # Realiza a mutação nos cromossomos.
        for i in range(len(self.beta)):
            if random() < taxa_mutacao:
                if self.beta[i] == '1':
                    self.beta[i] = '0'
                else:
                    self.beta[i] = '1'

            if random() < taxa_mutacao:
                if self.gamma[i] == '1':
                    self.gamma[i] = '0'
                else:
                    self.gamma[i] = '1'
        return self
