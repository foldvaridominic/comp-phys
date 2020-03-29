import sys
import matplotlib.pyplot as plt
import numpy as np
import math

def flip_spins(size=8, beta=0.48, **kwargs):
    beta = float(beta)
    size = int(size)
    p = 1-math.exp(-2*beta)
    active_spins = set()
    selected_spins = set()
    unselected_spins = set()
    init_lattice = kwargs.get('init_lattice')
    if init_lattice is not None:
        lattice = init_lattice
        vis = np.copy(lattice)
    else:
        # Generate random lattice with zeros and ones
        lattice = np.random.choice((1, 0), size=(size, size))
        vis = np.copy(lattice)

    init_0 = np.random.randint(0,size-1)
    init_1 = np.random.randint(0,size-1)
    init = (init_0, init_1)
    init_spin = lattice[init[0]][init[1]]
    if init_spin == 0:
        next_spin = 1
    else:
        next_spin = 0
    active_spins.add(init)
    selected_spins.add(init)

    # Go until active spin list is empty
    while active_spins:
        spin = active_spins.pop()
        neighbours = []
        neighbours.append((max(0, spin[0] - 1), spin[1]))
        neighbours.append((min(size - 1, spin[0] + 1), spin[1]))
        neighbours.append((spin[0], max(0, spin[1] - 1)))
        neighbours.append((spin[0], min(size - 1, spin[1] + 1)))
        for neighbour in neighbours:
            treshold = np.random.random()
            if neighbour != spin and neighbour not in unselected_spins and treshold <= p and \
                lattice[spin[0]][spin[1]] == lattice[neighbour[0]][neighbour[1]]:
                active_spins.add(neighbour)
                selected_spins.add(neighbour)
            elif neighbour != spin:
                unselected_spins.add(neighbour)
    for spin in selected_spins:
        lattice[spin[0]][spin[1]] = next_spin
    coverage = 0.0
    for row in range(size):
        for col in range(size):
            if lattice[row][col] == next_spin:
                coverage += 1
    coverage = int(round(coverage / (float((size * size))) * 100.0))

    return vis, lattice, coverage



if __name__ == '__main__':

    for beta in np.linspace(0.4, 0.48, 9):
        vis, lattice, coverage = flip_spins(beta=beta)
        ax = plt.subplot(3, 5, 1)
        ax.set_title("Initial")
        plt.imshow(vis)
        plt.axis('off')
        ax = plt.subplot(3, 5, 2)
        ax.set_title("Step 1, {} %".format(coverage))
        plt.imshow(lattice)
        plt.axis('off')
        for i in range(2,15):
            _, lattice, coverage = flip_spins(beta=beta, init_lattice=lattice)
            ax = plt.subplot(3, 5, i+1)
            ax.set_title("Step {}, {} %".format(i, coverage))
            plt.imshow(lattice)
            plt.axis('off')
        plt.suptitle("Beta = {}".format(beta))
        plt.show()
