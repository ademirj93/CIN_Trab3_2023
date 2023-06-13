import numpy as np
import matplotlib.pyplot as plt
import pso_func as pso

# Executar o algoritmo PSO
x_range = [-5, 5]  # Intervalo para a variável x
y_range = [-5, 5]  # Intervalo para a variável y
num_particles = 50  # Número de partículas
num_iterations = 100  # Número de iterações

# Chamar a função do algoritmo PSO para obter a melhor posição, melhores custos e custos médios
best_position, best_costs, mean_costs = pso.particle_swarm_optimization(x_range, y_range, num_particles, num_iterations)

# Plotar o gráfico com o valor mínimo e médio da função ao longo das iterações
iterations = np.arange(num_iterations)
plt.figure(figsize=(10, 5))
plt.plot(iterations, best_costs, label='Mínimo')
plt.plot(iterations, mean_costs, label='Médio')
plt.xlabel('Iteração')
plt.ylabel('Valor da função')
plt.legend()
plt.title('Valor mínimo e médio da função ao longo das iterações')
plt.show()

print('Melhor posição:', best_position)
print('Melhor custo:', pso.objective_function(best_position[0], best_position[1]))
