import numpy as np
from ..utils import constants

class Agent():
    def __init__(self,id,world):
        #Initialize some variables.
        self.id = id
        self.it = False 
        self.position = np.array([0,0])
        self.heading  = np.array([0,0])
        self.velocity = 1
        #Reference to world.
        self.world = world
    
    def requestMove(self):
        requestedPosition =  self.position + (self.heading * self.velocity)
        return requestedPosition
    
    def decideMovement(self):
        if not self.it:
            neighbors = self.world.getNeighbors(self.position, radius=constants.VISIBLE_RADIUS)
            if any(n.it for n in neighbors):
                #Neighbor is it! We run away.
                #We're basically going to scatter here. Get all neighbors's positions and scatter in the average opposite direction.
                neighborPositions = np.array([n.position for n in neighbors])
                averageNeighborPosition = np.mean(neighborPositions, axis=0)
                directionAwayFromNeighbors = self.position - averageNeighborPosition
                #Normalize the direction vector and set it as the new heading.
                if np.linalg.norm(directionAwayFromNeighbors) > 0:
                    self.heading = directionAwayFromNeighbors / np.linalg.norm(directionAwayFromNeighbors)
                else:
                    #If we're exactly on top of the average neighbor position, just pick a random direction.
                    self.heading = np.random.rand(2) - 0.5
                    self.heading = self.heading / np.linalg.norm(self.heading)
                
                self.velocity = 2 + np.random.random() 
            #Else, we're not it and no neighbors are it, so just keep doing what we're doing. Mutate the heading a little bit to add some randomness.
            self.heading += (np.random.rand(2) - 0.5) * 0.1
            self.heading = self.heading / np.linalg.norm(self.heading)

        else:
            #We're it, so get neighbors.
            neighbors = self.world.getNeighbors(self.position, radius=constants.VISIBLE_RADIUS)
            #If there are no neighbors, just keep doing what we're doing. Mutate the heading a little bit to add some randomness.
            if len(neighbors) == 0:
                self.heading += (np.random.rand(2) - 0.5) * 0.1
                self.heading = self.heading / np.linalg.norm(self.heading)
                return
            
            closestNeighbor = min(neighbors, key=lambda n: np.linalg.norm(n.position - self.position))
            #Choose that neighbor and run.
            self.heading = (closestNeighbor.position - self.position) / np.linalg.norm(closestNeighbor.position - self.position)
            self.velocity = 2+np.random.random()
            

            


if __name__ == "__main__":
    print(constants.VISIBLE_RADIUS)