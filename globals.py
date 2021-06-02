#to not every time iterate the whole graph only node which have zombies are iterated. This brings good performance especially for early stages of the simulation
global nodes_with_zombies
nodes_with_zombies = []

#a metric accessed in several places
global humans_killled
humans_killled=0

#helper object to iterate through all zombies (of all age) of a node
global ttl
ttl = ['z_1', 'z_2', 'z_3', 'z_4', 'z_5', 'z_6', 'z_7', 'z_8', 'z_9', 'z_10', 'z_11', 'z_12', 'z_13', 'z_14', 'z_15']