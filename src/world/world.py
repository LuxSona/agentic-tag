from ..utils import constants


class World():
    def __init__(self, quadtree, size=constants.DEFAULT_WORLD_SIZE):
        self.size = size
        self.quadtree = quadtree
        self.agents = []

    def addAgent(self, agent):
        #Adds an agent to the world.
        self.agents.append(agent)

    def getNeighbors(self, position, radius=constants.VISIBLE_RADIUS):
        #Use the quadtree algorithm to get neighbors within a certain radius of a position.
        #Query the tree with our quadtree. 
        neighbors = self.quadtree.queryFromPoint(position, radius, [])
        #Neighbors is a list of Point objects, so we need to extract the agent data from each Point object and return a list of agents.
        neighbors = [p.data for p in neighbors]
        return neighbors
        
    def setTree(self, quadtree):
        self.quadtree = quadtree