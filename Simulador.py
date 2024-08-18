import ndlib.models.ModelConfig as mc
import ndlib.models.CompositeModel as gc
import ndlib.models.compartments as es
from sklearn.metrics import mean_squared_error


def simulacao(infectados_dados_reais, recuperados_dados_reais, grafo, dias, beta, gamma, nos_infectados,
              nos_recuperados):
    # Simula a difusão da doença e retorna o erro da simulação em relação aos dados.
    sucetiveis_simulacao = []
    infectados_simulacao = []
    recuperados_simulacao = []

    # Instanciando o Modelo
    modelo = gc.CompositeModel(grafo)

    # Definindo os estados
    modelo.add_status("Susceptible")
    modelo.add_status("Infected")
    modelo.add_status("Removed")

    # Definindo a regra de infecção
    c1 = es.EdgeStochastic(triggering_status="Infected")
    c2 = es.NodeStochastic(gamma)

    # Definindo as regras de mudança de estado
    modelo.add_rule("Susceptible", "Infected", c1)
    modelo.add_rule("Infected", "Removed", c2)

    # Configuração Inicial do Modelo
    config = mc.Configuration()

    # Threshold specs
    for i, j, k in grafo.edges.data():
        threshold = beta * round(sum(k.values()), 2)
        config.add_edge_configuration("threshold", (i, j), threshold)

    # Inicializando os nos infectados
    config.add_model_initial_configuration("Infected", nos_infectados)
    config.add_model_initial_configuration("Removed", nos_recuperados)

    # Simulation execution
    modelo.set_initial_status(config)
    iteracoes = modelo.iteration_bunch(dias)

    # Obtendo o número de suscetiveis, infectados e recuperados a cada iteração
    for i in iteracoes:
        sucetiveis_simulacao.append(i['node_count'][0])
        infectados_simulacao.append(i['node_count'][1])
        recuperados_simulacao.append(i['node_count'][2])

    mse_i = round(mean_squared_error(infectados_dados_reais, infectados_simulacao), 5)
    mse_r = round(mean_squared_error(recuperados_dados_reais, recuperados_simulacao), 5)

    # Condicional para lidar com estouro de memória provocado pelo mean square error
    if mse_i < 0:
        mse_i = 10_000_000

    if mse_r < 0:
        mse_r = 10_000_000

    return mse_i, mse_r, sucetiveis_simulacao, infectados_simulacao, recuperados_simulacao
