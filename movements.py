from createGraph import create_nodes
import random
import globals
from globals import nodes_with_zombies
from globals import ttl
import numpy as np
from tqdm import tqdm

def total_zombies(G, node):
    total_z = 0
    for time in ttl:
        total_z += G.nodes[node][time]
    return total_z

def define_dist(G, node, total_zombies):
    weights = []
    for i in range(1,16):
        weights.append(G.nodes[node]['z_{}'.format(i)])
    weights = np.array(weights)/total_zombies
    return list(weights)

def zombie_move_helper(G, come_from, go_to, contrib):
    if go_to not in nodes_with_zombies:
        nodes_with_zombies.append(go_to)
    weights = define_dist(G, come_from, total_zombies(G, come_from))
    for index, weight in enumerate(weights):
        G.nodes[come_from][ttl[index]] -= int(weight * int(contrib))
        G.nodes[go_to][ttl[index]] += int(weight * int(contrib))
    return G

def zombie_destroy_helper(G, cell, quantity):
    weights = define_dist(G, cell, total_zombies(G, cell))
    for index, weight in enumerate(weights):
        G.nodes[cell][ttl[index]] -= int(weight * int(quantity))
    return G

def zombie_creation_helper(G, cell, quantity):
    G.nodes[cell]['z_15'] += quantity
    if cell not in nodes_with_zombies:
        nodes_with_zombies.append(cell)
    return G

def initial_zombies(G, node, population=117321): #node = rize in graph coordinates
    G.nodes[node]['z_15'] = population
    nodes_with_zombies.append(node)
    #G.nodes[node]['h_count'] -= population
    return G

def step_1(G_old, G_new, nodes_with_zombies):
    nwz = list(nodes_with_zombies) #avoid "changed size during iteration"
    for node in nwz:
        sum_H_j = 0
        for neighbor in G_old.neighbors(node):
            sum_H_j += G_old.nodes[neighbor]['h_count']

            # i=0
        if sum_H_j == 0:  #2nd & 4th line: nothing changes
            continue

        for neighbor in G_old.neighbors(node): # i!=0
            #1st line
            H_j = G_old.nodes[neighbor]['h_count']
            Z_j = total_zombies(G_old, node)
            lambda_0_i = G_old[node][neighbor]['lambda_d']

            contrib = H_j / sum_H_j * Z_j * lambda_0_i
            if int(np.floor(contrib)) == 0:
                continue

            # if G_old.nodes[node]['z_count'] <= contrib:
            #     G_new.nodes[node]['z_count'] = 0
            #     G_new.nodes[neighbor]['z_count'] += G_old.nodes[node]['z_count']
            #     zombie_move_helper(node, neighbor, np.floor(G_old.nodes[node]['z_count']))
            # else:

            G_new = zombie_move_helper(G_new, node, neighbor, contrib)
            #G_new = zombie_destroy_helper(G_new, node, contrib)

            # G_new.nodes[node]['z_count'] -= contrib
            # G_new.nodes[neighbor]['z_count'] += contrib

    return G_new


def step_2(G, nodes_with_zombies):
    nwz = list(nodes_with_zombies)  # avoid "changed size during iteration"
    for node in nwz:
        killed = total_zombies(G, node)*10
        if killed > G.nodes[node]['h_count']:
            G = zombie_creation_helper(G, node, G.nodes[node]['h_count'])
            G.nodes[node]['h_count'] = 0
            globals.humans_killled += G.nodes[node]['h_count']
        else:
            G = zombie_creation_helper(G, node, killed)
            G.nodes[node]['h_count'] -= killed
            globals.humans_killled += killed

    return G


def step_3(G, nodes_with_zombies):
    nwz = list(nodes_with_zombies)  # avoid "changed size during iteration"
    for node in nwz:
        destroyed = G.nodes[node]['h_count']*10

        if int(destroyed) == 0:
            continue
        if destroyed > total_zombies(G, node):
            for time in ttl:
                G.nodes[node][time] = 0
        else:
            G = zombie_destroy_helper(G, node, destroyed)
    return G


def manage_zombie_age(G, nodes_with_zombies):
    current_alive = 0
    nwz = list(nodes_with_zombies)  # avoid "changed size during iteration"
    for node in nwz:
        for i in range(1,15):
            G.nodes[node]['z_{}'.format(i)] = G.nodes[node]['z_{}'.format(i+1)]
        G.nodes[node]['z_15'] = 0
        current_alive += total_zombies(G, node)
    return G, int(current_alive)
