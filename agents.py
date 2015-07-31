"""

agents.py

Contains the definintions of agents which will populate the world. The behavior
of each class should not be defined by their __init__() arguments, but rather by
the methods and values of the class itself.

"""

import numpy as np
from main import Colon

class Agent:
    # An agent has a unique position and id to interact with World
    def __init__(self,pos,ID):
        self.__ID = ID
        def getID(self):
            return self.ID
        self.pos=pos

class Cell(Agent):
    # A cell is an agent who can reproduce and will eventually die
    def __init__(self,pos,ID):
        super(Cell,self,pos,ID).__init__()
        # The value at which a cell will die()
        self.__lifespan = 100 #arbitrary
        # A counter which will determine the Cell's proximity to lifespan
        self.__age = np.random.randint(100)
        def getAge(self):
            return self.age
        def die(self):
            # Colon function which deletes the Cell instance and replaces it
            # None
            Colon.removeme(self)
        # Counter to measure the time since last cell division
        self.__treplicate = 0 #arbitrary          
        # The age at which a Cell should attempt to replicate()
        self.__puberty = 50
        def __replicate():
            # as used here, neighbors should be a dictionary
            neighbors = Colon.getneighbors(self.pos)
            emptyneighbors= []
            for pos, obj in neighbors.items():
                if obj == None:
                    emptyneighbors.append(pos)
            # Colon function which generates a new Cell in the space of the
            # first argument, and takes the Cell itself as the second so the
            # function can make child cell the same type as parent (and track
            # reproduction later if desired)
            Colon.spawnNew(np.random.shuffle(emptyneighbors)[0],self)
            self.__treplicate = 0
        # Condition to determine whether a Cell's environment is suitable for
        # life. To be overwritten by subclasses so that, for example, Healthy
        # cells check if they have the correct number of Healthy neighbors
        self.lifecondition = True
        # Handles the timestep event 
        # TODO figure out pydispatcher and listeners
        def doAction():
            if not self.lifecondition or self.__age >= self.__lifespan:
                self.die()
            else:
                if self.__treplicate >= self.__puberty:
                    self.__replicate()
                self.__age += 1
                self.__treplicate += 1


                    
                
        
            
        
            
            
        
        
        
