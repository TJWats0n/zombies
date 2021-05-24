# zombies

You need python 3.7 to show the graph on a correct grid.
then use: conda install --file requirements.txt
pygraphviz could need some more of your attention (it also requires python 3.7)

Code:
create_graph.py has all the functions to build the base graph. Needed attributes are included, edges generated and water removed. There is an issue with the resolution of 15x15px for one node. As you can see the canal between france and england is connected in the graph even though zombies are not allowed to progagate through water. This comes from the assumption that a graph node which represents water is only discarded if all 225 pixels of this node are water. With this we don't loose sea cities (as e.g. Brest) by accident but have the mentioned advantage. Solution would be to have finer resolution.

The graph looks like this, but is very slow to generate (~15 Minutes)

[First Graph Represenation](graph.png)


imageprocessing.py imports and transforms the bit map images. Here the elevation file is interesting as it is converted to HVE colorspace where we can then use the 'hue' value as linear mapping. 

movements.py has all the logic for the movements of zombies, their creation, their destruction and the managemtn of their age. On the bottom there is rudimentary code for the main loop where one loop is one day and is the heart of the simulation. This is not yet tested.

What is missing:
- color editing in graph representation where the zombies are
- the main loop
- statistics
- a main file as entry point to the simulation from which the graph is created and the main loop is executed
- a naming and saving convention for each new graph (ideally the main loop takes the graph from the previous day and saves after calculations. With this we can analyse everyday without being dependent on the runtime)



