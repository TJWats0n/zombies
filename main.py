from createGraph import generate_graph,draw_graph
import datetime
from movements import initial_zombies, step_1, step_2, step_3, manage_zombie_age
import numpy as np
import pickle
import globals
import copy

def iter_stats(day, date, total_zombies, current_zombies):

    print("====== Day:{} =========".format(day))
    print("date: {}".format(date))
    print("total zombies: {}".format(total_zombies))
    print("current alive zombies: {}".format(current_zombies))
    print("humans killed: {}".format(globals.global_id_counter + 117000))

def simulation(G_old, G_new, i=0):
    init_date = datetime.date.fromisoformat('2019-08-18')
    while i < 150:
        cur_date = init_date + datetime.timedelta(days=i)

        G_new = step_1(G_old, G_new, globals.zombie_population.keys())
        G_new = step_2(G_new, globals.zombie_population.keys())
        G_new = step_3(G_new, globals.zombie_population.keys())
        current_alive = manage_zombie_age(globals.zombie_population.keys())

        perc_died = current_alive/globals.global_id_counter

        if G_new.nodes[(brest_x, brest_y)]['z_count'] > 0:
            print("Zombies arrived in Brest at {}".format(cur_date))
            break

        iter_stats(i, cur_date, globals.global_id_counter, current_alive)

        file_name = "results/graph_{}".format(cur_date)
        with open(file_name, 'wb') as out_file:
            pickle.dump(G_new, out_file)

        i += 1
        #new is the next old
        with open(file_name, 'rb') as in_file:
            G_old = pickle.load(in_file)

if __name__ == '__main__':
    agg_factor = 15
    # G = generate_graph()
    #
    # with open('base_graph.pickle', 'wb') as out_file:
    #     pickle.dump(G, out_file)

    with open('base_graph.pickle', 'rb') as in_file:
        G = pickle.load(in_file)

    #height of cropped picture = 2970, other values (city positions) are printed from import_population_as_array
    #y-axis conversion needed as picture (0,0) is top left while graph (0,0) is bottom left
    brest_x, brest_y = np.floor(686/agg_factor), np.floor((2970 - 1245)/agg_factor) #686,1245 x,y
    rize_x, rize_y = np.floor(4412/agg_factor), np.floor((2970 - 2178) /agg_factor) #4412,2178 x,y

    G.nodes[(brest_x, brest_y)]['h_count'] = 139.163 #data from 2015

    G = initial_zombies(G, (rize_x, rize_y), 117321)

    G_old = G
    #G_new = copy.deepcopy(G_old)

    #for dev, much faster than deepcopy
    with open('base_graph.pickle', 'rb') as in_file:
        G_new = pickle.load(in_file)
    G_new.nodes[(rize_x, rize_y)]['z_count'] = 117321
    G_new.nodes[(rize_x, rize_y)]['h_count'] -= 117321
    G_new.nodes[(brest_x, brest_y)]['h_count'] = 139.163  # data from 2015

    simulation(G_old, G_new, 0)