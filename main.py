import matplotlib.pyplot as plt
import itertools
import random
import copy
#import numpy as np
from cell import *
from pydispatch import dispatcher

#Record object for each space in the colon, xcoord is height position, ycoord is width position
class Space(object):
    # TODO argument names don't match variable assignments -EA Why not x, y z? Less typing
    def __init__(self, layer=None, xcoord=None, ycoord=None):
        self.layer = layer
        self.width = width
        self.height = height

#CELL COORDINATES ARE (LAYER, WIDTH (HORIZONTAL), HEIGHT (VERTICAL)) S.O. to Ethan Alley
class Colon:
    def __init__(self, layers, width, height, inner_width, inner_height, cancer_ratio, occupied_ratio):
        self.layers = layers
        self.width = width
        self.height = height
        self.inner_width = inner_width # Inner describes the inner colon cavity dimensions
        self.inner_height = inner_height
        self.cancer_ratio = cancer_ratio # Proportion of cells that are cancerous
        self.occupied_ratio = occupied_ratio # Proportion of all spaces in the COLON WALL that are occupied
        self.spaces = {} # Spaces contains the positions and types of all cells currently in the colon
        self.ids = xrange(100000000) # Cell ID generator, TODO: Figure out how to endlessly generate unique IDs without breaking the bank
        self.current_id = 0 #Tracks current index of id generated from self.ids

    # Randomly distributes cells in the colon, final spaces tuple formal will contain a Space record object followed by a "u", "c" or "h" designating unoccupied, cancer or healthy cekk location respectively
    # Why not a tuple with space and then an instance of the Cell object itself? How will the instances be stored if not in the spaces -EA (Actually I see below)
    def populate(self):
        self.inner_spaces = list(itertools.product(xrange(self.layers),xrange(int((self.width-self.inner_width)/2), int(self.width-(self.width+self.inner_width)/2)),xrange(int((self.height-self.inner_height)/2),int(self.height-(self.height+self.inner_height)/2))))
        
        for i in len(self.inner_spaces):
            self.inner_spaces[i] = Space(*self.inner_spaces[i])

        # Assign unoccupied spaces in inner tube of colon
        for pos in self.inner_spaces:
            self.spaces = dict(
                self.spaces.items() +
                dict(pos, None)
            )

        self.outer_spaces = list(itertools.product(xrange(self.layers),itertools.chain(xrange(int((self.width-self.inner_width)/2)),xrange(int(self.width-(self.width+self.inner_width)/2), self.width)),itertools.chain(xrange(int((self.height-self.inner_height)/2)),xrange(int(self.height-(self.height+self.inner_height)/2),self.height))))
        random.shuffle(self.outer_spaces)

            for i in len(self.outer_spaces):
            self.outer_spaces[i] = Space(*self.outer_spaces[i])

        # Assign unoccupied spaces in colon wall region
        self.n_occupied = int(self.occupied_ratio*len(self.outer_spaces))
        for pos in itertools.islice(self.outer_spaces, self.n_occupied, None):
            self.spaces = dict(
                self.spaces.items() +
                dict(pos, None)
            )

        # Assign spaces in colon wall region to each cell type
        self.n_cancer = int(self.cancer_ratio*self.n_occupied)
        for pos in itertools.islice(self.outer_spaces, self.n_cancer):
            self.spaces = dict(
                self.spaces.items() +
                dict(pos, Cancer(pos, self.ids[self.current_id]))
                self.current_id += 1
            )
        for pos in itertools.islice(self.outer_spaces, self.n_cancer, self.n_occupied):
            self.spaces = dict(
                self.spaces.items() +
                dict(pos, Healthy(pos, self.ids[self.current_id]))
                self.current_id += 1
            )

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