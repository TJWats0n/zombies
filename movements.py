from createGraph import create_nodes
import random
import globals
from globals import zombie_population
import numpy as np
from tqdm import tqdm

def zombie_move_helper(come_from, go_to, quantity):
    if quantity > len(zombie_population[come_from]):
        quantity = len(zombie_population[come_from])
    moving_zombies = random.sample(list(zombie_population[come_from].items()), k=int(quantity))
    for zombie, ttl in moving_zombies:
        if go_to not in zombie_population:
            zombie_population[go_to] = {}
        zombie_population[go_to][zombie] = ttl
        zombie_population[come_from].pop(zombie)

def zombie_destroy_helper(cell, quantity):
    if quantity > len(zombie_population[cell]):
        quantity = len(zombie_population[cell])
    destroyed_zombies = random.sample(list(zombie_population[cell].items()), k=int(quantity))
    for zombie, ttl in destroyed_zombies:
        zombie_population[cell].pop(zombie, None)

def zombie_creation_helper(cell, quantity):
    i = 0
    while (i <= quantity):
        if cell not in zombie_population:
            zombie_population[cell] = {}
        zombie_population[cell][globals.global_id_counter] = 15
        globals.global_id_counter += 1
        i += 1

def initial_zombies(G, node, population=117321): #node = rize in graph coordinates
    G.nodes[node]['z_count'] = population
    G.nodes[node]['h_count'] -= population
    zombie_creation_helper(node, population)
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
            Z_j = G_old.nodes[node]['z_count']
            lambda_0_i = G_old[node][neighbor]['lambda_d']

            contrib = H_j / sum_H_j * Z_j * lambda_0_i
            if int(np.floor(contrib)) == 0:
                continue

            if int(np.floor(contrib)) == 108636.0:
                print('stop')
            if G_old.nodes[node]['z_count'] <= contrib:
                G_new.nodes[node]['z_count'] = 0
                G_new.nodes[neighbor]['z_count'] += G_old.nodes[node]['z_count']
                zombie_move_helper(node, neighbor, np.floor(G_old.nodes[node]['z_count']))
            else:
                G_new.nodes[node]['z_count'] -= contrib
                G_new.nodes[neighbor]['z_count'] += contrib
                zombie_move_helper(node, neighbor, np.floor(contrib))

    return G_new


def step_2(G, nodes_with_zombies):
    nwz = list(nodes_with_zombies)  # avoid "changed size during iteration"
    for node in nwz:
        killed = G.nodes[node]['z_count']*10
        globals.humans_killled += killed
        if killed > G.nodes[node]['h_count']:
            G.nodes[node]['z_count'] += G.nodes[node]['h_count'] #killed humans become zombies
            zombie_creation_helper(node, G.nodes[node]['h_count'])
            G.nodes[node]['h_count'] = 0
        else:
            G.nodes[node]['z_count'] += killed
            G.nodes[node]['h_count'] -= killed
            zombie_creation_helper(node, killed)

    return G


def step_3(G, nodes_with_zombies):
    nwz = list(nodes_with_zombies)  # avoid "changed size during iteration"
    for node in nwz:
        destroyed = G.nodes[node]['h_count']*10
        if destroyed > G.nodes[node]['z_count']:
            G.nodes[node]['z_count'] = 0
            zombie_destroy_helper(node, np.floor(G.nodes[node]['z_count']))
        else:
            G.nodes[node]['z_count'] -= destroyed
            zombie_destroy_helper(node, np.floor(destroyed))

    return G


def manage_zombie_age(nodes_with_zombies):
    current_alive = 0
    nwz = list(nodes_with_zombies)  # avoid "changed size during iteration"
    for node in nwz:
        current_alive += len(zombie_population[node])
        nwz_ = list(zombie_population[node].items())  # avoid "changed size during iteration"
        for id, age in nwz_:
            if age == 0:
                zombie_population[node].pop(id, None)
            else:
                zombie_population[node][id] -= 1
    return current_alive
