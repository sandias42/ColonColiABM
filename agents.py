"""

agents.py

Contains the definintions of agents which will populate the world. The behavior
of each class should not be defined by their __init__() arguments, but rather by
the methods and values of the class itself.

"""

import numpy as np
import pydispatch
# BZ - For the time being I've left script import statements 
# in this format to distinguish them from actual packages/modules
from main import *


class Agent:
    # An agent has a unique position and id to interact with World
    def __init__(self,pos,ID):
        self.ID = ID
        def getID(self):
            return self.ID
        self.pos=pos

class Cell(Agent):
    # A cell is an agent who can reproduce and will eventually die
    def __init__(self,pos,ID,Colon,child=True):
        super(Cell,self,pos,ID).__init__()
        # The value at which a cell will die()
        self.lifespan = 100 #arbitrary
        # The age at which a Cell should attempt to replicate()
        self.puberty = 50 #arbitrary
        self.colon = Colon
        # A counter which will determine the Cell's proximity to lifespan and
        # Counter to measure the time since last cell division, random at the
        # start of the simulation and 0 otherwise
        if child == False:
            self.treplicate = np.random.randint(self.puberty)
            self.age = np.random.randint(self.age)
        else:
            self.trplicate = 0
            self.age = 0
    # A function which checks if the cells environment is appropriate for
    # growth and returns a Bool, True if Cell should live False otherwise
    # Should be overwritten in subclasses!
    def lifeCondition(self):
        return True
    def getAge(self):
        return self.age
    def die(self):
        self.colon.remove(self)
    # Helper to return the list of empty neighbors
    def emptyNeighbors(self):
        # as used here, neighbors should be a dictionary
        neighbors = self.colon.getNeighbors(self.pos)
        emptyNeighbors= []
        for pos, obj in neighbors.iteritems():
            if obj == None:
                emptyNeighbors.append(pos)  
        # If the Cell is on the edge of the colon add the corresponding "exterior" 
        # spaces that it can replicate to
        if len(neighbors) < 26:
            for i in range(26-len(neighbors)):
                emptyNeighbors.append(None)
    # Creates a child object of the same type as parent in a random adjacent
    # empty space. As defined here, the Cell won't replicate if all adjacent
    # occupied but will continue to check each tick. Cancer cells should 
    # override
    def replicate(self):
        if self.emptyNeighbors().len() == 0:
            return
        else:
            # Colon function which generates a new Cell a random empty space 
            # as the first argument, and takes the Cell itself as the second 
            # so the function can make child cell the same type as parent 
            # (and track reproduction later if desired)
            self.colon.spawnNew(myshuffle(self.emptyNeighbors())[0], self)
            self.treplicate = 0
    # Moves cell into the space which is in the same direction as the calling
    # object. If that space is empty, it asks colon to update its position, if
    # it contains an object then it asks colon for the object and makes move()
    def move(self, posPrev):
        empties = self.emptyNeighbors()
        if empties.len() != 0:
            nxt = myshuffle(empties)[0]
        else:
            # Does this work?
            nxt = tuple(np.add(
                np.subtract(self.pos.values(),posPrev.values()),
                self.pos.values()))
            z,x,y = nxt
            nxt = Space(layer=z,x=x,y=y)
        # Get the current resident of a Space by position
        o = self.colon.objByPos(nxt)
        if o != None:
            o.move(self.pos)
        # Puts the agent specified by the first argument in the space specified
        # by the second argument provided the space is empty        
        self.colon.moveAgent(posPrev,nxt,self)
    # A defined behavior to be executed each timestep and overridden in subclass
    def behavior(self):
        return
    # Handles the timestep event 
    # TODO figure out pydispatcher and listeners
    def doAction(self, sender):
        if not self.lifeCondition() or self.age >= self.lifespan:
            self.die()
        else:
            if self.treplicate >= self.puberty:
                self.replicate()
            self.behavior()
            self.age += 1
            self.treplicate += 1

class Healthy(Cell):
    def __init__(self,pos,ID,colon,child):
        # Keeping arbitrary Cell defaults
        super(Healthy,self,pos,ID,colon,child).__init__()
        # Change this to change how many neighbors are necessary for survival
        self.numNeighborsReq = 13
    def lifeCondition(self):
        neighbors = self.colon.getNeighbors(self.pos)
        numhealthy = 0
        for obj in neighbors.itervalues():
            if isinstance(obj,Healthy):
                numhealthy += 1
        if numhealthy >= self.numNeighborsReq:
            return True
        else:
            return False
            
class Cancer(Cell):
    def __init__(self,pos,ID,colon,child):
        # Keeping super methods
        super(Cancer,self,pos,ID,colon,child).__init__()
        self.lifespan = 1000
        self.puberty = 20
    def lifeCondition(self):
        return True
    def replicate(self):
        neighbors = self.colon.getNeighbors(self.pos)
        exts = 26-len(neighbors)
        if len(neighbors) < 26:
            for i in range(exts):
                neighbors.append(None)
        space = myshuffle(
            neighbors.items())[0]
        if space = None:
            self.treplicate = 0
        else:
            if space[1] != None:
                space[1].move(self.pos)
            colon.spawnNew(space[0], self)
            self.treplicate = 0
        
class Ecoli(Cell)
    def __init__(self,pos,ID,colon):
        # Keeping super methods
        super(Ecoli,self,pos,ID,colon).__init__()
        self.lifespan = 20 # TODO- FIND NUMBERS THAT AREN'T STUPID
        self.puberty = 10
        # % Chance of sticking to a healthy cell
        self.healthyBinding = 20, # arbitrary
        # % Chance of sticking to a cancer cell
        self.cancerBinding = 50 # arbitrary      
        # % Chance of falling off a healthy cell when already stuck
        self.healthyDissoc = 80 #arbitrary
        # % Chance of falling off a cancer cell when already stuck
        self.cancerDissoc = 5 #arbitrary
        self.isStuck = False
        self.stuckTo = None
    def behavior(self):
        neighbors = myshuffle(self.colon.getNeighbors(self.pos))
        empties = []
        def stick(pos,obj):
            # To keep things simple for now, Ecoli can't stick to themselves
            if isinstance(obj, Ecoli):
                pass
            elif isinstance(obj, Cancer) 
            && np.random.randint(100) <= self.cancerBinding:
                self.isStuck = True
                self.stuckTo = obj
            elif isinstance(obj, Healthy) 
            && np.random.randint(100) <= self.healthyBinding:
                self.isStuck = True
                self.stuckTo = obj
            elif obj == None:
                empties.append(pos)
            else:
                print "Illegal object in colon.getNeighbors!"
                raise TypeError
                
        if not self.isStuck:
            # This filter relies on the rule that the next frame (ie the
            # direction of colon flow) is always counting up from zero, or one
            # greater than the frame before
            for pos, obj in neighbors:
                stick(pos,obj)
            empties = filter((lambda pos: 
            True if pos.layer == (self.pos.layer + 1) else False), empties)
            # Will only move down because of the above filter
            if empties.len() > 0:
                colon.moveAgent(self.pos,myshuffle(empties)[0],self)
            else:
                pass
        elif isinstance(self.stuckTo, Cancer) 
        && np.random.randint(100) <= self.cancerDissoc
            self.isStuck = False
            self.stuckTo = None
        elif isinstance(self.stuckTo, Healthy) 
        && np.random.randint(100) <= self.healthyDissoc
            self.isStuck = False
            self.stuckTo = None
        else:
            print "Ecoli is stuck to an illegal object type"
            raise TypeError
        

            
            
        
        
# A more sensible, functional implementation of shuffle
def myshuffle(seq):
    myshuffle(seq)
    return seq
        
        
        
