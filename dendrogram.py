import math
import itertools
import numpy as np
from scipy.cluster.hierarchy import dendrogram
import matplotlib.pyplot as plt

def calculate_distance_of_cities(city1, city2, data):
    city1 = data[city1]
    city2 = data[city2]
    distance = math.sqrt(sum(
        [(month1 - month2)**2
        for month1, month2 in zip(city1, city2)
        ]
        ))
    return distance

def calculate_distance_of_groups(group1, group2, data):
    distance = min(
            [calculate_distance_of_cities(city1, city2, data)
            for city1 in group1
            for city2 in group2
            ]
            )
    return distance

def merge_groups(groups, city_in_group, linkage, data, new_group_idx):
    pairs = list(itertools.combinations(groups,2))
    distances = [(pair, calculate_distance_of_groups(group1, group2, data))
                for pair, (group1, group2) in enumerate(pairs)
                ]
    min_value = min(distances, key=lambda tup: tup[1])
    chosen_pair = pairs[min_value[0]]

    distance = min_value[1]
    group_idx1 = city_in_group[chosen_pair[0][0]]
    group_idx2 = city_in_group[chosen_pair[1][0]]
    cities_to_merge = tuple([city for group in chosen_pair for city in group])

    # update city_in_group
    for city in cities_to_merge:
        city_in_group[city] = new_group_idx

    # update groups
    groups.remove(chosen_pair[0])
    groups.remove(chosen_pair[1])
    groups.add(cities_to_merge)

    # add new row to linkage
    new_line = [group_idx1, group_idx2, distance, len(cities_to_merge)]
    linkage = np.append(linkage, [new_line], axis=0)

    return groups, city_in_group, linkage

if __name__ == "__main__":
    with open ("town.dat", 'r') as f:
        data = {}
        for line in f.readlines():
            values = line.strip().split()
            data[values[0]] = map(int, values[1:])
    f.close()

    n = len(data)
    # Initialize groups, which will be a set of groups of cities
    # Gets updated at every iteration based on group merges
    groups = set()
    # Initialize city_in_group, which tells a city's group currently
    # Gets updated at every iteration by new group indexes
    city_in_group = {}

    for group_idx, city in enumerate(data.keys()):
        city_in_group[city] = group_idx
        groups.add((city,))

    # Initialize linkage, which is the required format of merging history for visualization
    linkage = np.array(np.empty((1,4)))

    # Iterate n-1 times, at that point all city's belong to the same big group
    for i in range(n-1):
        new_group_idx = n + i
        groups, city_in_group, linkage = \
                merge_groups(groups, city_in_group, linkage, data, new_group_idx)

    # Delete first row which is a result of the initialization
    linkage = linkage[1:]
    # Shorten city names
    labels = [name[:5] for name in data.keys()]

    dendrogram(linkage, labels=labels)
    plt.show()

