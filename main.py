import matplotlib.pyplot as plt
import itertools
import random
import copy
import math
import numpy as np
from agents import * # BZ - For the time being I've left script import statements in this format to distinguish them from actual packages/modules
from pydispatch import dispatcher

#Record object for each space in the colon, xcoord is height position, ycoord is width position
class Space(object):
    def __init__(self, layer=None, x=None, y=None):
        self.layer = layer
        self.x = x
        self.y = y
    def values(self):
        return tuple(self.layer,self.x,self.y)

#CELL COORDINATES ARE (LAYER, WIDTH (HORIZONTAL), HEIGHT (VERTICAL)) S.O. to Ethan Alley
class Colon:
    def __init__(self, layers, width, height, innerWidth, innerHeight, cancerRatio, occupiedRatio):
        self.layers = layers
        self.width = width
        self.height = height
        self.innerWidth = innerWidth # Inner describes the inner colon cavity dimensions
        self.innerHeight = innerHeight
        self.cancerRatio = cancerRatio # Proportion of cells that are cancerous
        self.occupiedRatio = occupiedRatio # Proportion of all spaces in the COLON WALL that are occupied
        self.spaces = {} # Spaces contains the positions and types of all cells currently in the colon
        self.ids = xrange(100000000) # Cell ID generator, TODO: Figure out how to endlessly generate unique IDs without breaking the bank
        self.current_id = 0 # Tracks current index of id generated from self.ids
        self.sender = self # The sender of a timestep signal is identified as the Colon object itself

    # Randomly distributes cells in the colon, final spaces tuple format will contain a Space record object followed by a Cell object or None if the Space is empty
    def populate(self):
        self.innerSpaces = list(itertools.product(xrange(self.layers),xrange(int((self.width-self.innerWidth)/2), int(self.width-(self.width-self.innerWidth)/2)),xrange(int((self.height-self.innerHeight)/2),int(self.height-(self.height-self.innerHeight)/2))))
        
        for i in len(self.innerSpaces):
            self.innerSpaces[i] = Space(*self.innerSpaces[i])

        # Assign unoccupied spaces in inner tube of colon
        for pos in self.innerSpaces:
            self.spaces = dict(self.spaces, **dict(pos, None))

        self.outerSpaces = list(itertools.product(xrange(self.layers),self.width,itertools.chain(xrange(int((self.height-self.innerHeight)/2)),xrange(int(self.height-(self.height-self.innerHeight)/2),self.height))))+list(itertools.product(xrange(self.layers),itertools.chain(xrange(int((self.width-self.innerWidth)/2)),xrange(int(self.width-(self.width-self.innerWidth)/2))),xrange(int((self.height-self.innerHeight)/2),int(self.height-(self.height-self.innerHeight)/2))))
        random.shuffle(self.outerSpaces)

            for i in len(self.outerSpaces):
            self.outerSpaces[i] = Space(*self.outerSpaces[i])

        # Assign unoccupied spaces in colon wall region
        self.n_occupied = int(self.occupiedRatio*len(self.outerSpaces))
        for pos in itertools.islice(self.outerSpaces, self.n_occupied, None):
            self.spaces = dict(self.spaces, **dict(pos, None))

        # Assign spaces in colon wall region to each cell type
        self.n_cancer = int(self.cancerRatio*self.n_occupied)
        for pos in itertools.islice(self.outerSpaces, self.n_cancer):
            self.spaces = dict(self.spaces, **dict(pos, Cancer(pos, self.ids[self.current_id], self, False)))
                self.current_id += 1
            )
        for pos in itertools.islice(self.outerSpaces, self.n_cancer, self.n_occupied):
            self.spaces = dict(self.spaces, **dict(pos, Healthy(pos, self.ids[self.current_id], self, False)))
                self.current_id += 1
            )

    # Returns a dictionary of neighboring spaces and their current occupants for a given Space pos
    def getNeighbors(self, pos):
        neighbors = {}
        for t in self.spaces.iteritems():
            if (abs(t[0].layer - pos.layer) <= 1) and (abs(t[0].x - pos.x) <=1 ) and (abs(t[0].y - pos.y) <= 1) and (t[0] != pos):
                neighbors = dict(neighbors, **dict(t))
                # edges tracks the number of sides of a space that are in contact with the "edge" of the colon (i.e. on the outer surface of the colon wall)
                edges = abs(t[0].layer%layers) + abs(t[0].x%width) + abs(t[0].y%height)
                if edges < 3:
                    if len(neighbors) == 7 + int(math.ceil(float(edges)/2.0))*4 + int(math.floor(float(edges)/2.0))*6:
                        return neighbors
                elif len(neighbors) == 26:
                    return neighbors

    # Removes a Cell from its current Space pos (e.g. when a cell dies)
    def remove(self, pos):
        self.spaces[pos] = None

    # Spawns a new Cell in Space pos (e.g. when a cell reproduces)
    def spawnNew(self, pos, cell):
        if isinstance(obj,Healthy):
            self.spaces[pos] = Healthy(pos, self.ids[self.current_id], self, True)
            self.current_id += 1
        elif isinstance(obj,Cancer):
            self.spaces[pos] = Cancer(pos, self.ids[self.current_id], self, True)
            self.current_id += 1
        else:
            print ("Error: Cell type is neither Healthy nor Cancer!")
            raise TypeError

    def is_unsatisfied(self, x, y):
        race = self.agents[(x,y)]
        count_similar = 0
        count_different = 0

        if x > 0 and y > 0 and (x-1, y-1) not in self.empty_houses:
            if self.agents[(x-1, y-1)] == race:
                count_similar += 1
            else:
                count_different += 1
        if y > 0 and (x,y-1) not in self.empty_houses:
            if self.agents[(x,y-1)] == race:
                count_similar += 1
            else:
                count_different += 1
        if x < (self.width-1) and y > 0 and (x+1,y-1) not in self.empty_houses:
            if self.agents[(x+1,y-1)] == race:
                count_similar += 1
            else:
                count_different += 1
        if x > 0 and (x-1,y) not in self.empty_houses:
            if self.agents[(x-1,y)] == race:
                count_similar += 1
            else:
                count_different += 1        
        if x < (self.width-1) and (x+1,y) not in self.empty_houses:
            if self.agents[(x+1,y)] == race:
                count_similar += 1
            else:
                count_different += 1
        if x > 0 and y < (self.height-1) and (x-1,y+1) not in self.empty_houses:
            if self.agents[(x-1,y+1)] == race:
                count_similar += 1
            else:
                count_different += 1        
        if x > 0 and y < (self.height-1) and (x,y+1) not in self.empty_houses:
            if self.agents[(x,y+1)] == race:
                count_similar += 1
            else:
                count_different += 1        
        if x < (self.width-1) and y < (self.height-1) and (x+1,y+1) not in self.empty_houses:
            if self.agents[(x+1,y+1)] == race:
                count_similar += 1
            else:
                count_different += 1

        if (count_similar+count_different) == 0:
            return False
        else:
            return float(count_similar)/(count_similar+count_different) < self.happy_threshold

    def update(self):
        for i in range(self.n_iterations):
        self.old_agents = copy.deepcopy(self.agents)
        n_changes = 0
        for agent in self.old_agents:
            if self.is_unhappy(agent[0], agent[1]):
                agent_race = self.agents[agent]
                empty_house = random.choice(self.empty_houses)
                self.agents[empty_house] = agent_race
                del self.agents[agent]
                self.empty_houses.remove(empty_house)
                self.empty_houses.append(agent)
                n_changes += 1
        print n_changes
        if n_changes == 0:
            break

    def move_to_empty(self, x, y):
        race = self.agents[(x,y)]
    empty_house = random.choice(self.empty_houses)
    self.updated_agents[empty_house] = race
    del self.updated_agents[(x, y)]
    self.empty_houses.remove(empty_house)
    self.empty_houses.append((x, y))

    def plot(self):
        fig, ax = plt.subplots()
        #If you want to run the simulation with more than 7 colors, you should set agent_colors accordingly
        agent_colors = {1:'b', 2:'r', 3:'g', 4:'c', 5:'m', 6:'y', 7:'k'}
        for agent in self.agents:
            ax.scatter(agent[0]+0.5, agent[1]+0.5, color=agent_colors[self.agents[agent]])

        ax.set_title(title, fontsize=10, fontweight='bold')
        ax.set_xlim([0, self.width])
        ax.set_ylim([0, self.height])
        ax.set_xticks([])
        ax.set_yticks([])
        plt.savefig(file_name)

# Implementation goes here
c = Colon(500, 500, 500, 100, 100, 0.3, 0.85)
c.populate()
# TODO: Write method that returns true if at least one E. coli object is alive in colon
while(Coli.is_alive()):
    dispatcher.send( signal="r", sender=c.sender )