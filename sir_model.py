import random
import math
from collections import defaultdict
import itertools
import numpy as np
from matplotlib import pyplot as plt
import networkx as nx

# I. Write the Barabasi-Albert model to generate a graph

# total number of nodes will be n
# create m0 < n initial nodes that represent a fully connected graph
# add n-m0 nodes one by one with m <= m0 links
# links are attahced to the existing ones with probability proportional to their degree

m0 = 3
m = 3
n = 30
# create initial nodes and edges making a fully connected graph
nodes = defaultdict(list)
links = set()
for comb in itertools.combinations(range(m0), 2):
    # symmetric graph
    nodes[comb[0]].append(comb[1])
    nodes[comb[1]].append(comb[0])
    links.add(frozenset(comb))

for i in range(m0, n):
    # K is the total number of edges currently
    K = sum([len(value) for key, value in nodes.items()])
    nodes_ordered_list = sorted(nodes.items(),  key=lambda (kk,v): len(v), reverse=True)
    while True:
        rand = np.random.randint(K+1)
        ssum = 0
        # instead of generating random number and random node multiple times
        # probability is defined by the range of sum series of nodes occupied in range(K)
        # for the last node of the actual series this is the probability
        # although if biggest node has already more edges than random number --> new cyle (not efficient)
        for node, edges in nodes_ordered_list:
            chosen_node = node
            ssum += len(edges)
            if ssum >= rand:
                break
        pair = frozenset((chosen_node, i))
        if pair in links:
            continue
        nodes[chosen_node].append(i)
        nodes[i].append(chosen_node)
        links.add(pair)
        if len(nodes[i]) == m:
            break

G = nx.from_dict_of_lists(nodes)
pos = nx.spring_layout(G)
nx.draw(G, pos)

# II. SIR model

# now beta is defined differently, the probability for one node to get infected
# is proportional to the number of infected neighbours
# max probability is max_edge * beta, so the smaller the beta is the higher the probability is for infection
# with this implementation, I found it impossible not to get the first infected recovered after step 1
# and on the other hand not to get all nodes infected either after multiple steps
gamma = 0.5
beta = 0.4
# initial conditions: all but one node is susceptible
# the missing one is infected
susceptable = set((range(n)))
infected = set()
random_node = random.sample(range(n), 1)[0]
susceptable.remove(random_node)
infected.add(random_node)
recovered = set()

len_nodes_list = [len(edges) for node, edges in nodes.items()]
max_edge = max(len_nodes_list)
max_chance = max_edge * beta
edgelist = {tuple(pair) for pair in links}
print("max chance: {}".format(max_chance))
step = 0

while True:
    step += 1
    if len(infected) == 0:
        break
    random_node = random.sample(infected, 1)[0]
    chance_for_infection = max_chance * np.random.random_sample()
    chance_to_recover = np.random.random()
    for neighbour in nodes[random_node]:
        if neighbour in susceptable:
            chance = sum([1 for node in nodes[neighbour] if node in infected])
            # this is the official beta
            # provided the definition of max_chance, chance can be higher than max_chance
            # for instance if more than beta part of its neighbours are infected
            print("chance: {}".format(chance))
            if chance > chance_for_infection:
                susceptable.remove(neighbour)
                infected.add(neighbour)
    if gamma > chance_to_recover:
        infected.remove(random_node)
        recovered.add(random_node)

    nx.draw_networkx_nodes(G,pos,nodelist=infected,node_color='r')
    nx.draw_networkx_nodes(G,pos,nodelist=recovered,node_color='b')
    nx.draw_networkx_nodes(G,pos,nodelist=susceptable,node_color='g')
    nx.draw_networkx_edges(G,pos,edgelist=edgelist)
    plt.axis('off')
    plt.title('Step {} G: Susceptable, R: Infected, B: Recovered'.format(step))
    plt.show()
