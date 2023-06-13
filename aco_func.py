import random
import matplotlib.pyplot as plt

#Função de leitura do arquivo contendo as cidades
def ler_arquivo_tsp(nome_arquivo):
    with open(nome_arquivo, 'r') as arquivo:
        
        linhas = arquivo.readlines()[6:58] #Define que as linhas a serem lidas serão da linha 7 à linha 58
        cidades = [] #Vetor que irá armazenar as coordenadas das cidades
        
        #Divisão das coordenadas x e y para criação do vetor
        for linha in linhas:
            cidade = linha.strip().split(' ')
            cidades.append((float(cidade[1]), float(cidade[2])))
    
    return cidades

#Função responsavél por calcular a distância entre as cidades
def calcular_distancia(cidade1, cidade2):
    x1, y1 = cidade1 #Recebe as coordenadas da cidade atual
    x2, y2 = cidade2 #Recebe as coordenadas da próxima cidade

    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5 #retorna a distância euclidiana entre as cidades

#Função responsavel pelo calculo da distância total
def calcular_distancia_total(cidades, rota):

    distancia_total = 0
    
    #Para cada aresta dentro da rota, menos a cidade atual 
    for i in range(len(rota) - 1):
        
        #Cidade atual recebe a cidade atual i e a próxima cidade é i + 1
        cidade_atual = rota[i]
        prox_cidade = rota[i + 1]
        
        #A distância total recebe o calculo da distância entre a cidade atual e a proxima cidade
        distancia_total += calcular_distancia(cidades[cidade_atual], cidades[prox_cidade])
    
    #Calulada a distância entre a ultima cidade e a primeira
    distancia_total += calcular_distancia(cidades[rota[-1]], cidades[rota[0]])
    
    return distancia_total

#Função para inicialização dos feromônios Permitindo uma distribuição uniforme de feromonio inicial
def inicializar_feromonios(num_cidades, valor_inicial):

    #Multiplica o valor inicial pelo numero de cidade para cada elemento dentro da cidade
    #isso garante uma uniformização dos dados na matriz
    return [[valor_inicial] * num_cidades for _ in range(num_cidades)]

#Função de avaliação e e construção da solução pela otimização ACO
def construir_solucao(cidades, feromonios, alpha, beta, formigas_elite, Q):
    
    #Num de cidades é igual ao tamanho do vetor de cidades
    num_cidades = len(cidades) 
    
    #A cidade inicial é definida aleatoriamente nos valores de 0 ao comprimento total menos 1
    #cidade_inicial = 1 #Caso queira iniciar a partir de uma cidade especifica
    cidade_inicial = random.randint(0, num_cidades-1) 
    
    #Aramazena a cidade inicial escolhida no vetor solução, que irá agregar as demais cidades no decorrer do laço
    solucao = [cidade_inicial] 

    #preenche todas as cidades como não visitadas, ou seja como visitado = False
    visitados = [False] * num_cidades 
    
    #A cidade inicial recebe o valor de TRUE
    visitados[cidade_inicial] = True 

    #Enquanto o tamanho do vetor de solução for menor que o numero de cidades o algoritmo será executado
    while len(solucao) < num_cidades:

        #Preenche o vetor de probabilidade com 0 em todos os valores equivelente ao tamanho do vetor do num de cidades
        probabilidade = [0] * num_cidades
        
        #Iterage nas cidades
        for prox_cidade in range(num_cidades):

            #Valida se a proxima cidade não foi visitada
            if not visitados[prox_cidade]:
                
                #Verifica se é uma formiga eletista, caso seja o feromonio é reforçado
                if prox_cidade in formigas_elite:
                    probabilidade[prox_cidade] = ((feromonios[cidade_inicial][prox_cidade] ** alpha)
                                                   * ((1.0 / calcular_distancia(cidades[cidade_inicial], cidades[prox_cidade])) ** beta)) * Q
                else:
                    probabilidade[prox_cidade] = ((feromonios[cidade_inicial][prox_cidade] ** alpha)
                                                   * ((1.0 / calcular_distancia(cidades[cidade_inicial], cidades[prox_cidade])) ** beta))

        #Soma das probabilidades
        probabilidade_total = sum(probabilidade)

        #Caso a probabilidade seja igual a 0 defini-se uma probabilidade uniforme para as cidades que serão visitadas
        if probabilidade_total == 0:
            probabilidade = [1 / num_cidades] * num_cidades
        #Caso contrario noramaliza as probabilidades através da divisãso de cada probabilidade pela probabilidade total
        else:
            probabilidade = [p / probabilidade_total for p in probabilidade]

        #Escolhe de forma aleatória a próxima cidade baseado na probabilidade
        escolha = random.choices(range(num_cidades), weights=probabilidade)[0]
        solucao.append(escolha)
        
        #A cidade escolhidade recebe TRUE e a proxima cidade se torna a cidade inicial 
        visitados[escolha] = True
        cidade_inicial = escolha

        # Atualizar feromônio na trilha percorrida pela formiga
        feromonios[escolha][cidade_inicial] += Q

    return solucao

#Função de evaporação de feromônio
def evaporar_feromonios(feromonios, evaporacao, formigas_elite):

    #Passsa por todos os elementos da matriz i, j que representam as arestas entre as cidades
    for i in range(len(feromonios)):
        for j in range(len(feromonios[i])):
           
            #Verifica se esse local pertence a uma formiga de elite para definir a regra de evaporação
            if (i, j) not in formigas_elite:
                feromonios[i][j] *= (1 - evaporacao)
            else:
                feromonios[i][j] *= (1 - (evaporacao/2))

#Algoritmo de otimização ACO
def aco(cidades, num_formigas, num_iteracoes, alpha, beta, evaporacao, Q, num_formigas_elite):
    
    
    num_cidades = len(cidades) #Recebe o numero de elementos das cidades
    melhor_distancia = float('inf') #Inicia a melhor como infinito para ser atualizado
    melhor_rota = [] #Inicia o vetor de Melhor rota
    aptidao_maxima_iteracoes = [] #Incia o vetor de aptidao maxima por iteção

    #Incializa o feromonio para uniformização dos dados
    feromonios = inicializar_feromonios(num_cidades, 1.0)

    #Inicia as listas de melhor distancia e iterações
    lista_melhor_distancia = []
    lista_iteracoes = []


    for iteracao in range(num_iteracoes):

        #Seleciona aleatoriamente um conjunto de formigas elitistas
        formigas_elite = random.sample(range(num_cidades), num_formigas_elite)
        
        formigas = []
        
        #Cada formiga executa sua caminhada
        for _ in range(num_formigas):

            formiga = construir_solucao(cidades, feromonios, alpha, beta, formigas_elite, Q)
            formigas.append(formiga)

        #Calcula a distancia e guarda a melhor distancia
        for formiga in formigas:
            distancia = calcular_distancia_total(cidades, formiga)

            if distancia < melhor_distancia:
                melhor_distancia = distancia
                melhor_rota = formiga

            #Inicia a evaporação do feromônio
            evaporar_feromonios(feromonios, evaporacao, formigas_elite)
        
        #Armazena os valores de aptidade maxima da iterações, melhores distâncias e iterações
        aptidao_maxima_iteracoes.append(melhor_distancia)
        lista_melhor_distancia.append(melhor_distancia)
        lista_iteracoes.append(iteracao)

    return melhor_rota, lista_iteracoes, lista_melhor_distancia, formigas, melhor_distancia

#Função de plotagem dos gráficos
def plotar_grafico(cidades, melhor_solucao,lista_iteracoes, lista_melhor_distancia, num_formigas, formigas):
    
    plt.plot(lista_iteracoes, lista_melhor_distancia)
    plt.xlabel('Iteração')
    plt.ylabel('Melhor Distância')
    plt.title('Convergência do ACO')
    plt.show()

    plt.figure(figsize=(10, 6))
    for i in range(num_formigas):
        rota_x = [cidades[j][0] for j in formigas[i]]
        rota_y = [cidades[j][1] for j in formigas[i]]
        plt.plot(rota_x, rota_y, marker='o', linestyle='-', label='Formiga {}'.format(i+1))
    plt.xlabel('Coordenada X')
    plt.ylabel('Coordenada Y')
    plt.title('Deslocamento Final das Formigas')
    plt.legend()
    plt.show()

    custos = [calcular_distancia_total(cidades, formiga) for formiga in formigas]
    menor_custo = min(custos)
    iteracao_menor_custo = custos.index(menor_custo)

    plt.plot(range(num_formigas), custos, marker='o', linestyle='-', color='b')
    plt.xlabel('Formiga')
    plt.ylabel('Custo')
    plt.title('Custo de cada Formiga')
    plt.xticks(range(num_formigas))
    plt.axvline(x=iteracao_menor_custo, color='r', linestyle='--', label='Menor Custo')
    plt.legend()
    plt.show()
    
    # Extrair as coordenadas X e Y das cidades
    x = [cidade[0] for cidade in cidades]
    y = [cidade[1] for cidade in cidades]

    # Plotar as cidades no gráfico
    plt.scatter(x, y, color='red', label='Cidades')

    # Plotar a linha da melhor solução encontrada pelas formigas
    x_melhor = [cidades[i][0] for i in melhor_solucao]
    y_melhor = [cidades[i][1] for i in melhor_solucao]
    x_melhor.append(cidades[melhor_solucao[0]][0])  # Adicionar a primeira cidade novamente para formar um ciclo
    y_melhor.append(cidades[melhor_solucao[0]][1])
    plt.plot(x_melhor, y_melhor, color='blue', linewidth=1.5, label='Melhor Solução')

    # Plotar as ligações entre as cidades na melhor solução
    for i in range(len(melhor_solucao) - 1):
        cidade_atual = melhor_solucao[i]
        prox_cidade = melhor_solucao[i + 1]
        x_coords = [cidades[cidade_atual][0], cidades[prox_cidade][0]]
        y_coords = [cidades[cidade_atual][1], cidades[prox_cidade][1]]
        plt.plot(x_coords, y_coords, color='green', linewidth=0.5)

    # Definir os rótulos das cidades
    for i, cidade in enumerate(cidades):
        plt.annotate(str(i), (cidade[0], cidade[1]), textcoords="offset points", xytext=(0,10), ha='center')

    # Configurar o gráfico
    plt.title('Cidades e Melhor Solução')
    plt.xlabel('Coordenada X')
    plt.ylabel('Coordenada Y')
    plt.legend()

    # Exibir o gráfico
    plt.show()