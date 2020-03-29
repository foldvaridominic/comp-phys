# There is one main data collector at (0,0)
# Intermediate collectors can be installed
# Number of sensors: N
# An individual (sequence) is a list of 0s and 1s
# 1: the sensor is connected directly to the main collector
# 0: the sensor is connected through an intermediate collector
# Intermediate collector of a particular sensor:
# another sensor connected directly to the main collector and being closest to our sensor
# S is the size of population, e.g. the number of individuals
# Fitness function is the sum of distances (the smaller the better)

# START
# Order the individuals based on fitness
# After ordering generate probabilities equally based on rank
# Select a parent based on rank (although randomly)
# Do not remove the parent from the list even after selecting it
# Use single point crossover with probability pc
# If crossover:
    # select another parent as before
    # do not remove the parent from the list even after selecting it
    # get a child:
        # randomly select a point for crossover
        # up to that point contribution to the child comes from first parent
        # from that point contribution to the child  comes from second parent
# Use mutation (bit-flip) with probability pm if crossover and always if not crossover
# Get the same size of population (new generation)
# GOTO START

import math
import numpy as np
import matplotlib.pyplot as plt

def get_closest(seq, idx, x, y):
    dmin = 1e100
    ddx = 0
    ddy = 0
    for idx2, gene2 in enumerate(seq):
        if gene2 == 1:
            dx = x[idx2] - x[idx]
            dy = y[idx2] - y[idx]
            d = math.sqrt(dx**2 + dy**2)
            if d < dmin:
                dmin = d
                closest = idx2
                ddx = dx
                ddy = dy
    return dmin, ddx, ddy


def get_fitness(population, x, y):
    fitness = []
    for seq in population:
        dist = 0.0
        for idx, gene in enumerate(seq):
            if gene == 1: # directly connected
                dist += math.sqrt(x[idx]**2 + y[idx]**2)
            else:
                dmin, _1, _2 = get_closest(seq, idx, x, y)
                dist += dmin
        fitness.append(dist)
    return fitness

def get_probabilities(S):
    prob  = np.linspace(0, 1, S)
    prob = [p / sum(prob) for p in prob]
    return prob

def order_by_fitness(population, fitness):
    population = [seq for _, seq in sorted(zip(fitness, population), key=lambda x: x[0])]
    return population

def create_new_child(population, probabilities, pc, pm, N):
    parent_idx = np.random.choice(range(len(population)), p=probabilities)
    parent = population[parent_idx]

    if np.random.random() < pc:
        child = []
        parent2_idx = np.random.choice(range(len(population)), p=probabilities)
        parent2 = population[parent2_idx]
        crossover_pt = np.random.randint(N)
        for i in range(crossover_pt):
            child.append(parent[i])
        for i in range(crossover_pt, N):
            child.append(parent2[i])

        if np.random.random() < pm:
            mutation_pt = np.random.randint(N)
            if child[mutation_pt] == 0:
                child[mutation_pt] = 1
            if child[mutation_pt] == 1:
                child[mutation_pt] = 0
    else:
        child = parent
    #    mutation_pt = np.random.randint(N)
    #    if child[mutation_pt] == 0:
    #        child[mutation_pt] = 1
    #    if child[mutation_pt] == 1:
    #        child[mutation_pt] = 0

    return child

def create_new_generation(x, y, population, N, S, pc=0.9, pm=0.1):
    new_generation = []
    fitness = get_fitness(population, x, y)
    population = order_by_fitness(population, fitness)
    probabilities = get_probabilities(S)
    for i in range(S):
        child = create_new_child(population, probabilities, pc, pm, N)
        new_generation.append(child)
    return new_generation

def display_figure(population, x, y, generation):
    fitness = get_fitness(population, x, y)
    population = order_by_fitness(population, fitness)
    seq = population[0]
    colors = []
    for idx, gene in enumerate(seq):
        if gene == 1:
            colors.append('red')
            plt.arrow(x[idx], y[idx], -x[idx], -y[idx])
        if gene == 0:
            colors.append('blue')
            _, dx, dy = get_closest(seq, idx, x, y)
            plt.arrow(x[idx], y[idx], dx, dy)
    xx = np.insert(x, 0, 0)
    yy = np.insert(y, 0, 0)
    colors.insert(0, 'green')
    plt.axis('off')
    plt.scatter(xx, yy, c=colors)
    plt.title('Generation {}'.format(generation))
    plt.show()


if __name__ == '__main__':
    dim = 18
    N = 32
    S = 100
    x = np.random.randint(dim, size=N)
    y = np.random.randint(dim, size=N)
    population = []
    for i in range(S):
        seq = np.random.randint(2, size=N)
        population.append(seq)
    #display_figure(population, x, y, generation=0)
    for i in range(50):
        population = create_new_generation(x, y, population, N=N, S=S)
    display_figure(population, x, y, generation=i+1)
