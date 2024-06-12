import numpy as np
import matplotlib.pyplot as plt
import random

# Definimos las constantes y parámetros del modelo
GRID_SIZE = 50  # Tamaño de la cuadrícula
INITIAL_COLORS = [1, 2, 3, 0]  # Red, Green, Blue, Black
SWAP_RATE_EXPONENT = 0.33
REPRODUCE_RATE_EXPONENT = 0.33
SELECT_RATE_EXPONENT = 0.33

def initialize_grid(size):
    return np.random.choice(INITIAL_COLORS, (size, size))

def rate_from_exponent(exponent):
    return 10 ** exponent

def swap_rate():
    return rate_from_exponent(SWAP_RATE_EXPONENT)

def reproduce_rate():
    return rate_from_exponent(REPRODUCE_RATE_EXPONENT)

def select_rate():
    return rate_from_exponent(SELECT_RATE_EXPONENT)

def percentage(rate):
    return 100 * rate / (swap_rate() + reproduce_rate() + select_rate())

def get_neighbors4(grid, x, y):
    neighbors = []
    if x > 0:
        neighbors.append((x-1, y))
    if x < grid.shape[0] - 1:
        neighbors.append((x+1, y))
    if y > 0:
        neighbors.append((x, y-1))
    if y < grid.shape[1] - 1:
        neighbors.append((x, y+1))
    return neighbors

def swap(grid, x, y, target):
    tx, ty = target
    grid[x, y], grid[tx, ty] = grid[tx, ty], grid[x, y]

def reproduce(grid, x, y, target):
    tx, ty = target
    if grid[tx, ty] == 0:
        grid[tx, ty] = grid[x, y]
    elif grid[x, y] == 0:
        grid[x, y] = grid[tx, ty]

def select(grid, x, y, target):
    tx, ty = target
    if beat(grid[x, y], grid[tx, ty]):
        grid[tx, ty] = 0
    elif beat(grid[tx, ty], grid[x, y]):
        grid[x, y] = 0

def beat(color1, color2):
    return (color1 == 1 and color2 == 2) or (color1 == 2 and color2 == 3) or (color1 == 3 and color2 == 1)

def run_simulation(grid, steps):
    for _ in range(steps):
        repetitions = grid.size // 3
        events = [0] * np.random.poisson(repetitions * swap_rate()) + \
                 [1] * np.random.poisson(repetitions * reproduce_rate()) + \
                 [2] * np.random.poisson(repetitions * select_rate())
        random.shuffle(events)
        
        for event in events:
            x, y = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
            neighbors = get_neighbors4(grid, x, y)
            if not neighbors:
                continue
            target = random.choice(neighbors)
            if event == 0:
                swap(grid, x, y, target)
            elif event == 1:
                reproduce(grid, x, y, target)
            elif event == 2:
                select(grid, x, y, target)

def plot_grid(grid, step):
    plt.imshow(grid, cmap='nipy_spectral', interpolation='nearest')
    plt.title(f'Step {step}')
    plt.colorbar()
    plt.show()

# Inicializamos el grid y ejecutamos la simulación
grid = initialize_grid(GRID_SIZE)
steps = 100  # Número de pasos de la simulación

for step in range(steps):
    run_simulation(grid, 1)
    plot_grid(grid, step)
