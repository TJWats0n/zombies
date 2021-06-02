import networkx as nx
import matplotlib.pyplot as plt
from imageprocessing import import_population_as_array, import_elevation_as_array
import numpy as np
from globals import ttl
import pickle

def total_zombies(G, node):
    total_z = 0
    for time in ttl:
        total_z += G.nodes[node][time]
    return total_z

def gen_color_map(G, pop_nodes):
    color_map = []
    for node in G.nodes:
        if node in pop_nodes:
            color_map.append('red')
        elif  total_zombies(G, node)> 0:
            color_map.append('yellow')
        elif total_zombies(G, node) == 0 and G.nodes[node]['h_count'] == 0:
            color_map.append('black')
        else:
            color_map.append('green')
    return color_map

def draw_graph(G,title, pop_nodes):
    print('draw_graph')
    #needed for grid representation
    positions = {}
    for node in G.nodes:
        positions[node] = [node[0], node[1]]
    pos = nx.spring_layout(G, pos=positions, fixed=positions.keys())


    #draw only nodes of full graph
    plt.figure()
    color_map = gen_color_map(G, pop_nodes)
    plt.title(title)
    print('drawing')
    nx.draw_networkx_nodes(G, pos, node_color=color_map, node_size=5, linewidths=0)
    plt.show()


def get_max_h_population(G):
    pop = []
    for node in G.nodes:
        pop.append((node, G.nodes[node]['h_count']))

    top_20 = sorted(pop, key=lambda i: i[1])[-20:]
    return top_20


file_name_3 = '/Users/juliankopp/PycharmProjects/zombieapocalypse/results/graph_2019-10-18'

with open(file_name_3, 'rb') as input:
    G = pickle.load(input)

top20=get_max_h_population(G)
nodes = []
for tup in top20:
    nodes.append(tup[0])

print(nodes)

# file_name_1 = '/Users/juliankopp/PycharmProjects/zombieapocalypse/results/graph_2019-08-18'
# file_name_2 = '/Users/juliankopp/PycharmProjects/zombieapocalypse/results/graph_2019-09-18'
# file_name_3 = '/Users/juliankopp/PycharmProjects/zombieapocalypse/results/graph_2019-10-18'
# file_name_4 = '/Users/juliankopp/PycharmProjects/zombieapocalypse/results/graph_2019-11-18'
# file_name_5 = '/Users/juliankopp/PycharmProjects/zombieapocalypse/results/graph_2019-12-18'
# file_name_6 = '/Users/juliankopp/PycharmProjects/zombieapocalypse/results/graph_2020-01-19'
#
file = file_name_3
# with open(file, 'rb') as input:
#     G = pickle.load(input)
title = file.split('/')[-1]
draw_graph(G, title, nodes)