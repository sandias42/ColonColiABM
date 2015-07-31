"""

agents.py

Contains the definintions of agents which will populate the world. The behavior
of each class should not be defined by their __init__() arguments, but rather by
the methods and values of the class itself.

"""

import numpy as np
import pydispatch

class Agent:
    # An agent has a unique position and id to interact with World
    def __init__(self,pos,ID):
        self.ID = ID
        def getID(self):
            return self.ID
        self.pos=pos

class Cell(Agent):
    # A cell is an agent who can reproduce and will eventually die
    def __init__(self,pos,ID,Colon):
        super(Cell,self,pos,ID).__init__()
        # The value at which a cell will die()
        self.lifespan = 100 #arbitrary
        # A counter which will determine the Cell's proximity to lifespan
        self.age = np.random.randint(100)
        # Counter to measure the time since last cell division
        self.puberty = 50 #arbitrary
        self.treplicate = np.random.randint(self.puberty)#arbitrary
        self.Colon = Colon
    # A function which checks if the cells environment is appropriate for
    # growth and returns a Bool, True if Cell should live False otherwise
    # Should be overwritten in subclasses!
    def lifeCondition(self):
        return True        
    def getAge(self):
        return self.age
    def die(self):
        # TODO Colon function which deletes the Cell instance and replaces it
        # None
        self.Colon.removeme(self)
    # The age at which a Cell should attempt to replicate()
    def replicate(self):
        # as used here, neighbors should be a dictionary
        neighbors = self.Colon.getneighbors(self.pos)
        emptyneighbors= []
        for pos, obj in neighbors.iteritems():
            if obj == None:
                emptyneighbors.append(pos)
        # Colon function which generates a new Cell in the space of the
        # first argument, and takes the Cell itself as the second so the
        # function can make child cell the same type as parent (and track
        # reproduction later if desired)
        if emptyneighbors.len() == 0:
            return
        else:
            self.Colon.spawnNew(np.random.shuffle(emptyneighbors)[0],self)
            self.treplicate = 0
    # Handles the timestep event 
    # TODO figure out pydispatcher and listeners
    def doAction(self):
        if not self.lifeCondition() or self.age >= self.lifespan:
            self.die()
        else:
            if self.treplicate >= self.puberty:
                self.replicate()
            self.age += 1
            self.treplicate += 1

class Healthy(Cell):
    def __init__(self,pos,ID,Colon):
        # Keeping arbitrary Cell defaults
        super(Healthy,self,pos,ID,Colon).__init__()
        # Change this to change how many neighbors are necessary for survival
        self.numNeighborsReq = 13
    def lifeCondition(self):
        neighbors = self.Colon.getneighbors(self.pos)
        numhealthy = 0
        for obj in neighbors.itervalues():
            if isinstance(obj,Healthy):
                numhealthy += 1
        if numhealthy >= self.numNeighborsReq:
            return True
        else:
            return False
            
class Cancer(Cell):
    def __init__(self,pos,ID,Colon):
        # Keeping super methods
        super(Cancer,self,pos,ID,Colon).__init__()
        self.lifespan = 1000
        self.puberty = 20
    
    
        
    
        
        
        
    
        
        
        
        
                    
                
        
            
        
            
            
        
        
        
