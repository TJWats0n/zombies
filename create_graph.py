import networkx as nx
import matplotlib.pyplot as plt
from imageprocessing import import_population_as_array, import_elevation_as_array
import numpy as np

def graph_stats(G):
    print(nx.info(G))
    #print("Nodes: ", G.nodes())

def draw_graph(G):
    print('draw_graph')
    #needed for grid representation
    positions = {}
    for node in G.nodes:
        positions[node] = [node[0], node[1]]
    pos = nx.spring_layout(G, pos=positions, fixed=positions.keys())
    print('pos done')
    plt.figure()
    print('drawing')
    nx.draw_networkx(G, pos, node_size=2, width=0.1, with_labels=False)
    print('drawing done')
    plt.show()

def create_nodes(rows = 3, columns = 3):
    print('create_nodes()')
    nodes = [(x,y) for x in range(columns) for y in range(rows)]

    G = nx.DiGraph()
    G.add_nodes_from(nodes)
    nx.set_node_attributes(G, 0, name='z_count')
    nx.set_node_attributes(G, 0, name='h_count')
    nx.set_node_attributes(G, {}, name='z_population')

    #create dictionary of positions to stick graph to a grid (2,1): [2,1]
    positions = {}
    for node in G.nodes:
        positions[node] = [node[0], node[1]]
    nx.set_node_attributes(G, positions, "pos")
    #graph_stats(G)
    #draw_graph(G)
    return G

def create_edges(G, rows, columns):
    print('create_edges()')
    edges = []
    for node in G.nodes:
        #G.add_edges_from(edges)
        #draw_graph(G)
        #print(node)
        #get neighbours
        if node[0] > 0 and node[0] <columns-1 and node[1]>0 and node[1]<rows-1: #middle points
            #start left, then clockwise
            edges.append((node, (node[0]-1, node[1])))#left
            edges.append((node, (node[0]-1, node[1]+1)))
            edges.append((node, (node[0], node[1]+1)))#upper
            edges.append((node, (node[0]+1, node[1]+1)))
            edges.append((node, (node[0]+1, node[1])))#right
            edges.append((node, (node[0]+1, node[1]-1)))
            edges.append((node, (node[0], node[1]-1)))#bottom
            edges.append((node, (node[0]-1, node[1]-1)))
            continue

        if node[0] == 0 and node[1]>0 and node[1]<rows-1: #left border
            edges.append((node, (node[0], node[1] + 1)))  # upper
            edges.append((node, (node[0] + 1, node[1] + 1)))
            edges.append((node, (node[0] + 1, node[1])))  # right
            edges.append((node, (node[0] + 1, node[1] - 1)))
            edges.append((node, (node[0], node[1] - 1)))  # bottom
            continue

        if node[0] == columns-1 and node[1]>0 and node[1]<rows-1: #right border
            edges.append((node, (node[0], node[1] - 1)))  # bottom
            edges.append((node, (node[0] - 1, node[1] - 1)))
            edges.append((node, (node[0] - 1, node[1])))  # left
            edges.append((node, (node[0] - 1, node[1] + 1)))
            edges.append((node, (node[0], node[1] + 1)))  # upper
            continue

        if node[0] > 0 and node[0] <columns-1 and node[1] == 0: #lower border
            edges.append((node, (node[0] - 1, node[1])))  # left
            edges.append((node, (node[0] - 1, node[1] + 1)))
            edges.append((node, (node[0], node[1] + 1)))  # upper
            edges.append((node, (node[0] + 1, node[1] + 1)))
            edges.append((node, (node[0] + 1, node[1])))  # right
            continue

        if node[0] > 0 and node[0] < columns - 1 and node[1] == rows-1: #upper border
            edges.append((node, (node[0] + 1, node[1])))  # right
            edges.append((node, (node[0] + 1, node[1] - 1)))
            edges.append((node, (node[0], node[1] - 1)))  # bottom
            edges.append((node, (node[0] - 1, node[1] - 1)))
            edges.append((node, (node[0] - 1, node[1])))  # left
            continue

        if node[0] == 0 and node[1] == 0: #ll corner
            edges.append((node, (node[0], node[1] + 1)))  # upper
            edges.append((node, (node[0] + 1, node[1] + 1)))
            edges.append((node, (node[0] + 1, node[1])))  # right
            continue

        if node[0] == 0 and node[1] == rows-1: #ul corner
            edges.append((node, (node[0] + 1, node[1])))  # right
            edges.append((node, (node[0] + 1, node[1] - 1)))
            edges.append((node, (node[0], node[1] - 1)))  # bottom
            continue

        if node[0] == columns-1 and node[1]==rows-1: #ur corner
            edges.append((node, (node[0], node[1] - 1)))  # bottom
            edges.append((node, (node[0] - 1, node[1] - 1)))
            edges.append((node, (node[0] - 1, node[1])))  # left
            continue

        if node[0] == columns-1 and node[1] == 0: #lr corner
            edges.append((node, (node[0] - 1, node[1])))  # left
            edges.append((node, (node[0] - 1, node[1] + 1)))
            edges.append((node, (node[0], node[1] + 1)))  # upper
            continue

    G.add_edges_from(edges)
    return G

def insert_human_pop(G, agg_factor, height, img):
    print('insert_human_pop()')
    for node in G.nodes:
        x_pos = node[0] * agg_factor
        y_pos = node[1] * agg_factor
        # needs some conversion as array index starts top left and graph index starts bottom left
        G.nodes[node]['h_count'] = np.sum(
            img[height - agg_factor - y_pos:height - y_pos, x_pos:x_pos + agg_factor])
    return G

def insert_elevation(G, agg_factor, height, img):
    print('insert_elevation()')
    for node in G.nodes:
        x_pos = node[0] * agg_factor
        y_pos = node[1] * agg_factor
        # needs some conversion as array index starts top left and graph index starts bottom left
        avg_elevation = np.average(img[height - agg_factor - y_pos:height - y_pos, x_pos:x_pos + agg_factor]) #across 15x15 px

        if avg_elevation == -1:
            #assumption: all pixels aggregated to on node in graph are water
            #with this we avoid deleting important pixels of cities at the coast e.g. Brest
            G.nodes[node]['elevation'] = 'water' #mark for later removal
        else:
            G.nodes[node]['elevation'] = avg_elevation
    return G

def remove_water(G):
    print('remove_water()')
    nodes = [n for n in G.nodes] #avoid "dictionary changed size during iteration"
    for node in nodes:
        if G.nodes[node]['elevation'] == 'water':
            G.remove_node(node)
    return G

def calc_lambda(G):
    print('calc_slope()')
    for node in G.nodes:
        for neighbor in G.neighbors(node):
            # arctan(y/x), x is distance between middle point of aggregated node (15x15px 1px=1km)
            slope = np.arctan((G.nodes[node]['elevation'] - G.nodes[neighbor]['elevation']) / 15)
            sign = np.sign(slope)
            if slope > 10:
                lambda_d = 0
            elif slope < 0:
                lambda_d = 1
            else:
                lambda_d = 1-slope * 0.1
            G[node][neighbor]['lambda_d'] = lambda_d
    return G


def main():
    test = False

    if test == True: #use test case for quicker dev
        agg_factor = 2
        height, width = 6,6
        rows, columns = int(height/agg_factor), int(width/agg_factor)
        population_img = np.random.randint(0, 10, (6, 6))
    else:
        population_img, width, height = import_population_as_array("population-density-map.bmp")
        # for now we assume that picture dimensions/15 results in integer values
        agg_factor = 15
        rows = int(height/agg_factor)
        columns = int(width/agg_factor)

    G = create_nodes(rows, columns)
    G = create_edges(G, rows, columns)
    elevation_img = import_elevation_as_array("elevation1x1_new-mer-bleue.bmp")
    G = insert_elevation(G, agg_factor, height, elevation_img)
    G = remove_water(G)
    G = insert_human_pop(G, agg_factor, height, population_img)
    G = calc_lambda(G)

    draw_graph(G)

    #y axis needs to be calculated from the bottom up as graph grid origin is lower left and not upper left as pictures
    brest_x, brest_y = np.floor(669/agg_factor), np.floor(28511306/agg_factor)
    rize_x, rize_y = np.floor(4426/agg_factor), np.floor(2851-2108/agg_factor)
    #https: // stackoverflow.com / questions / 27030473 / how - to - set - colors -
    #for -nodes - in -networkx


    # # G has format (col, row) because drawing function interprets first tuple value as x-axis position which corresponds to column
    # # (0,0) is the bottom left corner
    # # draw_graph(G)
    #
    # G = insert_human_pop(G, height, population_img)



    print('')



if __name__ == '__main__':
    main()







