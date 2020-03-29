import math
from collections import defaultdict
import itertools
import numpy as np
from matplotlib import pyplot as plt
import networkx as nx

# I. Write the Barabasi-Albert model to generate a graph

# total number of nodes will be n
# create m0 < n initial nodes that represent a fully connected graph
# add n-m0 nodes one by one with m < m0 links
# links are attahced to the existing ones with probability proportional to their degree
# space is 40 x 40
dim = 40
m0 = 3
m = 3
n = 30

# generate coordinates for nodes
x = np.random.randint(dim, size=n)
y = np.random.randint(dim, size=n)

def get_distance(x, y, start, end):
    distance = math.sqrt((x[start] - x[end])**2 + (y[start] - y[end])**2)
    return distance

# create initial nodes and edges making a fully connected graph
nodes = defaultdict(list)
links = {}
for comb in itertools.combinations(range(m0), 2):
    nodes[comb[0]].append(comb[1])
    nodes[comb[1]].append(comb[0])
    links[frozenset(comb)] = get_distance(x, y, comb[0], comb[1])

for i in range(m0, n):
    # K is the total number of edges currently
    K = sum([len(value) for key, value in nodes.items()])
    nodes_ordered_list = sorted(nodes.items(),  key=lambda (kk,v): len(v), reverse=True)
    while True:
        rand = np.random.randint(K+1)
        ssum = 0
        # instead of generating random number and random node multiple times
        # probability is defined by the range the edges of a particular node occupies in range(K)
        for node, edges in nodes_ordered_list:
            chosen_node = node
            ssum += len(edges)
            if ssum >= rand:
                break
        pair = frozenset([chosen_node, i])
        if links.get(pair):
            continue
        nodes[chosen_node].append(i)
        nodes[i].append(chosen_node)
        links[pair] = get_distance(x, y, chosen_node, i)
        if len(nodes[i]) == m:
            break

# II. Write the Dijkstra's algorithm
inf = 1e8
distance_sum = 0.0
distances = []
pairs = 0
while True:
    if pairs == 100:
        break
    starting_point = np.random.randint(n)
    end_point = np.random.randint(n)
    if starting_point == end_point:
        continue
    pairs += 1
    unvisited_dict = {}
    previous = []
    for key, value in nodes.items():
        unvisited_dict[key] = inf
    unvisited_dict[starting_point] = 0
    # This is the actual starting point
    while True:
        current_node = min(unvisited_dict, key=unvisited_dict.get)
        if current_node == end_point:
            break
        dist_so_far = unvisited_dict[current_node]
        del unvisited_dict[current_node]
        for neighbour in nodes[current_node]:
            pair = frozenset([current_node, neighbour])
            dist = dist_so_far + links[pair]
            # Since this is an unordered graph and the array "nodes" is symmetric
            # We get keyerror if neighbour has been already visited
            try:
                if dist < unvisited_dict[neighbour]:
                    unvisited_dict[neighbour] = dist
                    previous.append(current_node)
            except KeyError as e:
                continue
    previous.append(end_point)
    final_distance = unvisited_dict[end_point]
    distance_sum += final_distance
    print("START: {} FINAL: {} DISTANCE: {}".format(starting_point, end_point, final_distance))
    distances.append((starting_point, end_point, final_distance, previous))

print("Average: {}".format(distance_sum / 100))

min_tup = min(distances, key=lambda x: x[2])
min_start = min_tup[0]
min_end = min_tup[1]
min_dist = min_tup[2]
min_nodes = min_tup[3]
min_edges = zip(min_nodes, min_nodes[1:])
min_labels = {i: i for i in min_nodes}

max_tup = max(distances, key=lambda x: x[2])
max_start = max_tup[0]
max_end = max_tup[1]
max_dist = max_tup[2]
max_nodes = max_tup[3]
max_edges = zip(max_nodes, max_nodes[1:])
max_labels = {i: i for i in max_nodes}

print("Min distance between {} and {} is {}".format(min_start, min_end, min_dist))
print("Max distance between {} and {} is {}".format(max_start, max_end, max_dist))

G = nx.from_dict_of_lists(nodes)
pos = nx.spring_layout(G)
nx.draw_networkx(G, pos)
nx.draw_networkx_nodes(G,pos,nodelist=min_nodes,node_color='r')
nx.draw_networkx_nodes(G,pos,nodelist=max_nodes,node_color='b')
nx.draw_networkx_edges(G,pos,edgelist=min_edges,edge_color='r',width=4)
nx.draw_networkx_edges(G,pos,edgelist=max_edges,edge_color='b',width=2)
nx.draw_networkx_labels(G,pos,labels=max_labels)
nx.draw_networkx_labels(G,pos,labels=min_labels)
plt.axis('off')
plt.show()

