from ..agents import agent
from ..world import world
from ..utils import quadtree, constants
import numpy as np
import logging
logger = logging.getLogger(__name__)

class SimulationController():

    def __init__(self, numAgents=constants.DEFAULT_NUM_AGENTS, worldSize=constants.DEFAULT_WORLD_SIZE):
        #When we initialize, we create a number of agents. We add each agent to the world, and insert them (wrapped in a Point object) into the quadtree.
        self.currentTick = 0
        self.worldSize = worldSize
        #Set up a quadtree
        boundary = quadtree.boundingBox(np.array([0,0]), np.array(worldSize))
        self.qt = quadtree.QuadTree(boundary, 4)
        #Set up the world.
        self.world = world.World(self.qt, size=worldSize)
        #Create agents and add them to both the world and our quadtree.
        self.agents = []
        for i in range(numAgents):
            newAgent = agent.Agent(i, self.world)
            #Randomize the agent's initial position and heading.
            newAgent.position = np.random.rand(2) * worldSize
            newAgent.heading = np.random.rand(2) - 0.5
            newAgent.heading = newAgent.heading / np.linalg.norm(newAgent.heading)
        
            self.world.addAgent(newAgent)
            self.qt.insert(quadtree.Point(newAgent.position, data=newAgent))
        self.agents = self.world.agents
        #Randomly choose one agent to be it at the start.
        randomItAgent = np.random.choice(self.agents)
        randomItAgent.it = True
        self.it = [randomItAgent]

    def regenerateQuadtree(self):
        #Make a new quadtree and reinsert all agents based on their new positions.
        boundary = quadtree.boundingBox(np.array(self.worldSize)/2, np.array(self.worldSize))
        self.qt = quadtree.QuadTree(boundary, 4)
        for agent in self.world.agents:
            self.qt.insert(quadtree.Point(agent.position, data=agent))
        self.world.setTree(self.qt)
        
    def tick(self):
        self.currentTick += 1
        #Regenerate the quadtree based on agents' new positions.
        self.regenerateQuadtree()
        #Update agent movements u
        self.updateAgentMovements()
        #Handle interactions between agents.
        self.updateItStatus()
    
    def updateItStatus(self):
        #Check neighbors of the it agent. If any are within the tagging radius, they become it and the old it agent is no longer it.
        for it in self.it:
            neighbors = self.world.getNeighbors(it.position, radius=constants.VISIBLE_RADIUS)
            for neighbor in neighbors:
                logger.info(f"Neighbor position: {neighbor.position}, It Position: {it.position}")
                if neighbor in self.it:
                    pass 
                if neighbor not in self.it and np.linalg.norm(neighbor.position - it.position) <= constants.TAGGING_RADIUS:
                    #Tagging occurs! Neighbor becomes it, old it is no longer it.
                    logger.info(f"Tick {self.currentTick}: Agent {it.id} tagged Agent {neighbor.id}.")
                    neighbor.it = True
                    self.it.append(neighbor)
                    print(it.id)
                    break

    
    def updateAgentMovements(self):
        '''
        For each agent, call decideMovement to update their heading and velocity based on their neighbors.
        For each agent, call requestMove to get their requested new position and update their position.
        '''
        for agent in self.agents:
            agent.decideMovement()
        for agent in self.agents:
            requestedPosition = agent.requestMove()
            #Wrap around the world boundaries.
            requestedPosition = requestedPosition % self.worldSize
            agent.position = requestedPosition
        
        