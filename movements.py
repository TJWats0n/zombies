from createGraph import create_nodes
import random
nodes_with_zombies = []
rows, columns = 3,3
import datetime

G = create_nodes(rows, columns)

def zombie_move_helper(G, come_from, go_to, quantity):
    moving_zombies = random.choices(list(G.nodes[come_from]['z_population'].items()), k=quantity)
    for zombie, ttl in moving_zombies:
        G.nodes[go_to]['z_population'][zombie] = ttl
        G.nodes[come_from]['z_population'].pop(zombie, None)
    return G

def zombie_destroy_helper(G, cell, quantity):
    destroyed_zombies = random.choices(list(G.nodes[cell]['z_population'].items()), k=quantity)
    for zombie, ttl in destroyed_zombies:
        G.nodes[cell]['z_population'].pop(zombie, None)
    return G

def zombie_creation_helper(G, cell, quantity, ):
    global global_id_counter
    i = 0
    while (i <= quantity):
        G.nodes[cell]['z_population'][global_id_counter] = 15
        global_id_counter += 1
        i += 1
    return G

def initial_zombies(G, nodes_with_zombies, node=(49,295)): #node = rize in graph coordinates
    rize_population = 117.321 #wikipedia
    G.nodes[node]['z_count'] = rize_population
    G.nodes[node]['h_count'] -= rize_population
    G = zombie_creation_helper(G, node)
    nodes_with_zombies.append(node)
    return G, nodes_with_zombies

def step_1(G, nodes_with_zombies):
    for node in nodes_with_zombies:
        sum_H_j = 0
        for neighbor in G.neighbors(node):
            nodes_with_zombies.append(neighbor)
            sum_H_j += G.nodes[neighbor]['h_count']

        for neighbor in G.neighbors(node): # i!=0
            if sum_H_j == 0:#2nd line
                continue #no contribution to cell neighbor
            else:#1st line
                H_j = G.nodes[neighbor]['h_count']
                Z_j = G.nodes[node]['z_count']
                lambda_0_i = G[node][neighbor]['lambda_d']

                contrib = H_j / sum_H_j * Z_j * lambda_0_i
                G.nodes[neighbor]['z_count'] += contrib

                G = zombie_move_helper(G, node, neighbor, contrib)

        #i=0
        if sum_H_j == 0: #4th line
            contrib = G.nodes[node]['z_count']
            G.nodes[node]['z_count'] += contrib

    return G, nodes_with_zombies


def step_2(G, nodes_with_zombies):
    for node in nodes_with_zombies:
        killed = G.nodes[node]['z_count']*10
        if killed > G.nodes[node]['h_count']:
            G.nodes[node]['z_count'] += G.nodes[node]['h_count']
            G = zombie_creation_helper(G, node, G.nodes[node]['h_count'])
            G.nodes[node]['h_count'] = 0
        else:
            G.nodes[node]['h_count'] -= killed
            G.nodes[node]['z_count'] += killed
            G = zombie_creation_helper(G, node, killed)

    return G


def step_3(G, nodes_with_zombies):
    for node in nodes_with_zombies:
        destroyed = G.nodes[node]['h_count']*10
        if destroyed > G.nodes[node]['z_count']:
            G.nodes[node]['z_count'] = 0
            G = zombie_destroy_helper(G, node, G.nodes[node]['z_count'])
        else:
            G.nodes[node]['z_count'] -= destroyed
            G = zombie_destroy_helper(G, node, destroyed)

    return G


def manage_zombie_age(G, nodes_with_zombies):
    current_alive = 0
    for node in nodes_with_zombies:
        current_alive += len(G.nodes[node]['z_population'])
        for id, age in G.nodes[node]['z_population']:
            if age == 0:
                G.nodes[node]['z_population'].pop(id, None)
            else:
                G.nodes[node]['z_population'][id] -= 1
    return G, current_alive

if __name__ == '__main__':
    #gets executed when movements.py is imported, gets changed from within zombie_creation_helper()
    global global_id_counter
    global_id_counter = 0

    nodes_with_zombies = []
    init_date = datetime.date.fromisoformat('2019-08-18')

    #iteration start
    i=0
    #while i<end:
    cur_date = init_date + datetime.timedelta(days=i)
    G = create_nodes(rows, columns)
    G, nodes_with_zombies = initial_zombies(G, nodes_with_zombies)
    G = step_1(G, nodes_with_zombies)
    G = step_2(G, nodes_with_zombies)
    G = step_3(G, nodes_with_zombies)
    G, current_alive = manage_zombie_age(G, nodes_with_zombies)

    perc_died = current_alive/global_id_counter

    #save G for current iteration
    #iteration end
