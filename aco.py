import aco_func as aco

# Ler o arquivo tsp
cidades = aco.ler_arquivo_tsp('berlin52.tsp')

# Parâmetros
num_formigas = len(cidades) #Numero de formigas na colônia
num_iteracoes = 400 #Máximo de iterações
alpha = 1.0 #Importância do ferômonio
beta = 5.0 #Importância das informações Heurísticas (Como a distância entre as cidades)
evaporacao = 0.5 #Taxa de evaporação do ferômonio que reduz a instensidade do feromônio nas arestas 
Q = 100.0 #Valor do feromônio que será depositado por cada formiga em uma aresta
b = 5 #Formigas elitistas, cuja função é reforçar as arestas da melhor rota

# Executar o algoritmo ACO
melhor_rota, lista_iteracoes, lista_melhor_distancia, formigas, melhor_distancia = aco.aco(cidades, num_formigas, num_iteracoes, alpha, beta, evaporacao, Q, b)

print('Melhor Distância: ', melhor_distancia)
print('Melhor Rota: ', melhor_rota)

#Chama a plotagem dos gráficos
aco.plotar_grafico(cidades, melhor_rota,lista_iteracoes, lista_melhor_distancia, num_formigas, formigas)

