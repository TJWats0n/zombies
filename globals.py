# gets executed when movements.py is imported, gets changed from within zombie_creation_helper()
global global_id_counter
global_id_counter = 0


#graph cannot take a dictionary as node attribute. Therefore we use a global object with format node_key: {zombie_id: time_to_live}
#changed from: zombie_move_helper(), zombie_destroy_helper(), zombie_creation_helper()
global zombie_population
zombie_population = {}

global humans_killled
humans_killled=0