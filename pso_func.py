import numpy as np

# Definir função objetivo
def objective_function(x, y):
    return (1 - x) ** 2 + 100 * (y - x ** 2) ** 2

# Definir classe Particle
class Particle:
    def __init__(self, x_range, y_range):
        # Inicializar a posição e velocidade da partícula com valores aleatórios dentro do intervalo
        self.position = np.random.uniform(x_range[0], x_range[1], size=2)
        self.velocity = np.random.uniform(y_range[0], y_range[1], size=2)
        self.best_position = self.position.copy()  # Definir a melhor posição inicial como a posição atual
        self.best_cost = float('inf')  # Definir o melhor custo inicial como infinito

    def update_velocity(self, global_best_position, inertia_weight, cognitive_weight, social_weight):
        r1 = np.random.rand()  # Gerar um número aleatório entre 0 e 1
        r2 = np.random.rand()  # Gerar um número aleatório entre 0 e 1
        # Atualizar a velocidade da partícula usando a fórmula do PSO
        self.velocity = (inertia_weight * self.velocity +
                         cognitive_weight * r1 * (self.best_position - self.position) +
                         social_weight * r2 * (global_best_position - self.position))

    def update_position(self):
        # Atualizar a posição da partícula adicionando a velocidade atual
        self.position += self.velocity
        # Limitar a posição dentro do intervalo definido
        self.position = np.clip(self.position, -5, 5)

    def evaluate(self):
        # Avaliar o custo da função objetivo para a posição atual da partícula
        cost = objective_function(self.position[0], self.position[1])
        if cost < self.best_cost:
            # Atualizar a melhor posição e o melhor custo se o custo atual for menor
            self.best_position = self.position.copy()
            self.best_cost = cost
        return cost

# Definir algoritmo PSO
def particle_swarm_optimization(x_range, y_range, num_particles, num_iterations):
    inertia_weight = 0.729  # Peso da inércia
    cognitive_weight = 1.49445  # Peso cognitivo
    social_weight = 1.49445  # Peso social
    global_best_cost = float('inf')  # Melhor custo global inicial como infinito
    global_best_position = None  # Melhor posição global inicial como vazia
    best_costs = []  # Lista para armazenar o melhor custo em cada iteração
    mean_costs = []  # Lista para armazenar o custo médio em cada iteração

    # Criar uma lista de partículas com posições e velocidades aleatórias
    particles = [Particle(x_range, y_range) for _ in range(num_particles)]

    # Loop pelas iterações do algoritmo PSO
    for iteration in range(num_iterations):
        costs = []  # Lista para armazenar os custos das partículas em cada iteração
        for particle in particles:
            # Avaliar o custo da função objetivo para a posição da partícula
            cost = particle.evaluate()
            costs.append(cost)

            if cost < global_best_cost:
                # Atualizar a melhor posição global e o melhor custo se o custo atual for menor
                global_best_cost = cost
                global_best_position = particle.position.copy()

        best_cost = min(costs)  # Obter o melhor custo na iteração atual
        mean_cost = np.mean(costs)  # Calcular o custo médio na iteração atual
        best_costs.append(best_cost)  # Adicionar o melhor custo à lista de melhores custos
        mean_costs.append(mean_cost)  # Adicionar o custo médio à lista de custos médios

        for particle in particles:
            # Atualizar a velocidade e posição das partículas usando o PSO
            particle.update_velocity(global_best_position, inertia_weight, cognitive_weight, social_weight)
            particle.update_position()

    return global_best_position, best_costs, mean_costs