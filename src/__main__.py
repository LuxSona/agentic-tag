from .simulation import simulationController
from .visualization import visualizer
import logging
import pygame 

def main():
    simController = simulationController.SimulationController()
    visualize = visualizer.Visualizer(simController)
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        simController.tick()
        visualize.render()
        clock.tick(60)  # Limit to 60 FPS

if __name__ == "__main__":
    main()
