# Generate a random lattice with p=0.59 occupation probability (size 256x256).
# Write the Hoshen-Kopelman algorithm to identify the clusters.
# Measure the fractal dimension of the clusters using box method.

import matplotlib.pyplot as plt
import numpy as np
import math

def find_clusters(size=256, p=0.59):
    p = float(p)
    size = int(size)
    link = []
    # Sizes list will contain lists of tuples of the elements of a cluster
    sizes = []
    # Generate random lattice with certain probability of occupation
    lattice = np.random.choice((1, 0), size=(size, size), p=(p,1-p))
    vis = np.copy(lattice)

    i = 0
    # Go through the elements
    for row in range(size):
        for col in range(size):
            # If originally it is occupied (True)
            if lattice[row][col]:
                # Try to reach the upper neighbour's link
                try:
                    if row-1 < 0:
                        raise IndexError("Does not have upper neighbour")
                    # Overwrite value to the link of its group
                    lattice[row][col] = link[lattice[row-1][col]]
                    # If succeeded check whether there is an occupied neighbour from the left
                    # In this case link conflicts need to be resolved
                    try:
                        if col-1 < 0:
                            raise IndexError("Does not have neighbour from the left")
                        # Choose the neighbour having lower index
                        chosen_link = min(link[lattice[row][col-1]], link[lattice[row-1][col]])
                        unchosen_link = max(link[lattice[row][col-1]], link[lattice[row-1][col]])
                        # Overwrite the links and aggregate sizes
                        if chosen_link != unchosen_link:
                            for ll,l in enumerate(link):
                                if l == unchosen_link:
                                    link[ll] = chosen_link
                            link[lattice[row][col-1]] = chosen_link
                            link[lattice[row-1][col]] = chosen_link
                            sizes[chosen_link] = sizes[chosen_link] + sizes[unchosen_link]
                            sizes[unchosen_link] = None
                        # Overwrite value to the link of its group
                        lattice[row][col] = chosen_link
                        # Now sizes is incremented
                        sizes[chosen_link].append((row, col))
                        #DEBUG
                        #print("upper and left neighbour too")
                    # In case only upper neighbour had to be taken into account
                    except IndexError as e1:
                        # Extend sizes
                        sizes[lattice[row][col]].append((row, col))
                        #DEBUG
                        #print("upper neighbour")
                # If there is no upper neighbour or it was not occuplied
                except IndexError as e2:
                    # Check the neighbour from the left
                    try:
                        if col-1 < 0:
                            raise IndexError("Does not have neighbour from the left")
                        # Overwrite value to the link of its group
                        lattice[row][col] = link[lattice[row][col-1]]
                        # Extend sizes
                        sizes[lattice[row][col]].append((row, col))
                        #DEBUG
                        #print("left neighbour")
                    # In case neither of these neighbours are occupied, or simply they do not exist
                    except IndexError as e3:
                        # Introduce a new number written on the lattice
                        lattice[row][col] = i
                        # Add one more element to the link list
                        link.append(i)
                        # Add one more element to the sizes list
                        sizes.append([(row, col)])
                        i += 1
                        #DEBUG
                        #print("new group")
            # In case it is not occupied
            else:
                # Make sure index on the lattice is large enough to generate IndexError when it is called
                lattice[row][col] = 99999
                #DEBUG
                #print("not occ.")
    sizes = filter(None, sizes)
    print("Number of clusters: {}".format(len(sizes)))
    return sizes, vis

def get_fractal_dimensions(sizes, vis, size=256):
    fractal_dimensions = []
    boxes_all = []
    parameters = []
    size = int(size)
    epsilons = [2**i for i in range(1,8)]
    log_epsilons = [math.log(ep) for ep in epsilons]
    for cluster in sizes:
        boxes = [0 for i in range(7)]
        for jj, j in enumerate(epsilons):
            for k in range(j):
                for kk in range(j):
                    _break = False
                    for row in range(0 + size/j*k, size/j*(k+1)):
                        for col in range(0 + size/j*kk, size/j*(kk+1)):
                            if (row, col) in cluster:
                                boxes[jj] += 1
                                _break = True
                                break
                        if _break:
                            break
        boxes = [math.log(N) for N in boxes]
        z = np.polyfit(log_epsilons, boxes, 1)
        boxes_all.append(boxes)
        fractal_dimensions.append(z[0])
        parameters.append(z)

    sizes = [len(size) for size in sizes]
    max_index = sizes.index(max(sizes))
    boxes = boxes_all[max_index]
    z = parameters[max_index]
    print("Largest cluster size: {}".format(sizes[max_index]))

    # plot diagram of box method for the largest cluster
    p = np.poly1d(z)
    xp = np.linspace(1, 200, 100)
    xp = [math.log(x) for x in xp]
    plt.title('Box method for one cluster')
    plt.xlabel('log Epsilon')
    plt.ylabel('log $N$')
    plt.plot(log_epsilons, boxes, '.', xp, p(xp), '-')
    plt.show()


    # plot correlation of sizes and fractal dimensions
    plt.title('Fractal dimensions and sizes')
    plt.xlabel('Size')
    plt.ylabel('Fractal dimension')
    plt.plot(sizes, fractal_dimensions, '.')
    plt.show()

    plt.imshow(vis)
    plt.show()



if __name__ == '__main__':

    sizes, vis = find_clusters()
    get_fractal_dimensions(sizes, vis)
