"""

agents.py

Contains the definintions of agents which will populate the world. The behavior
of each class should not be defined by their __init__() arguments, but rather by
the methods and values of the class itself.

"""

import numpy as np
import pydispatch
from main import * # BZ - For the time being I've left script import statements in this format to distinguish them from actual packages/modules

class Agent:
    # An agent has a unique position and id to interact with World
    def __init__(self,pos,ID):
        self.ID = ID
        def getID(self):
            return self.ID
        self.pos=pos

class Cell(Agent):
    # A cell is an agent who can reproduce and will eventually die
    def __init__(self,pos,ID,Colon,child):
        super(Cell,self,pos,ID).__init__()
        # The value at which a cell will die()
        self.lifespan = 100 #arbitrary
        # A counter which will determine the Cell's proximity to lifespan
        self.age = np.random.randint(100)
        # The age at which a Cell should attempt to replicate()
        self.puberty = 50 #arbitrary
        # Counter to measure the time since last cell division
        self.treplicate = np.random.randint(self.puberty) #arbitrary
        self.colon = Colon
        if child == True:
            self.treplicate = 0
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
            self.colon.spawnNew(np.random.shuffle(self.emptyNeighbors())[0], self)
            self.treplicate = 0
    # Moves cell into the space which is in the same direction as the calling
    # object. If that space is empty, it asks colon to update its position, if
    # it contains an object then it asks colon for the object and makes move()
    def move(self, posPrev):
        empties = self.emptyNeighbors()
        if empties.len() != 0:
            nxt = np.random.shuffle(empties)[0]
        else:
            # Does this work?
            nxt = tuple(np.add(
                np.subtract(self.pos.values(),posPrev.values()),
                self.pos.values()))
            z,x,y = nxt
            nxt = Space(layer=z,x=x,y=y)
        # Get the current resident of a Space by position
        o = colon.objByPos(nxt)
        if o != None:
            o.move(self.pos)
        # Puts the agent specified by the first argument in the space specified
        # by the second argument provided the space is empty        
        colon.moveAgent(self,nxt)
    # Handles the timestep event 
    # TODO figure out pydispatcher and listeners
    def doAction(self, sender):
        if not self.lifeCondition() or self.age >= self.lifespan:
            self.die()
        else:
            if self.treplicate >= self.puberty:
                self.replicate()
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
        o, nxtpos = numpy.random.shuffle(
            self.colon.getNeighbors(self.pos).items())[0]
        if o != None:
            o.move(self.pos)
        colon.spawnNew(self, nxtpos)
        self.treplicate = 0
        
        
        
        
        
