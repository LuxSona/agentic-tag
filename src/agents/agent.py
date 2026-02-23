import numpy as np
from ..utils import constants
import logging 

logger = logging.getLogger(__name__)

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
        #LOGGING: If the agent has a heading of (0,0), log a warning that the agent is not moving.
        if np.linalg.norm(self.heading) == 0:
            logger.warning(f"Agent {self.id} has a heading of (0,0) and is not moving.")
        #If the agent's position is NAN, log an error.

        requestedPosition =  self.position + (self.heading * self.velocity)
        #Check if requested position is NAN, and if so log an error.
        if np.isnan(self.position).any():
            logger.error(f"WARN: Agent {self.id}, IT: {self.it} is requesting a position of {requestedPosition} which contains NAN.")
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
            logger.info(f"INFO: Neighbors for IT is {neighbors}")
            #If there are no neighbors, just keep doing what we're doing. Mutate the heading a little bit to add some randomness.
            if len(neighbors) <= 1:
                self.heading += (np.random.rand(2) - 0.5) * 0.1
                self.heading = self.heading / np.linalg.norm(self.heading)
                return
            self.velocity = 1 + np.random.random()
            #Here's the problem: When we get our neighbors, we get the absolute closest one, which is ourselves
            closestNeighbor = None
            closestDistance = float("inf")
            for neighbor in neighbors:
                if neighbors is self:
                    pass
                else:
                    closestNeighbor = neighbor if np.linalg.norm(neighbor.position - self.position) < closestDistance else closestNeighbor
            

            #Choose that neighbor and run towards them. If linalg.norm is 0, just pick a random direction, the agent is on top of the neighbor and should be able to tag them (which is handled in the simulation controller).
            if np.linalg.norm(closestNeighbor.position - self.position) == 0:
                self.heading = np.random.rand(2) - 0.5
                self.heading = self.heading / np.linalg.norm(self.heading)
            else:
                self.heading = (closestNeighbor.position - self.position) / np.linalg.norm(closestNeighbor.position - self.position)
            self.velocity = 2+np.random.random()
            logger.info(f"INFO: Agent {self.id} is in CHASE MODE.")


            


if __name__ == "__main__":
    print(constants.VISIBLE_RADIUS)