from .simulation import simulationController

def main():
    simController = simulationController.SimulationController()
    for _ in range(5000):
        simController.tick()

if __name__ == "__main__":
    main()
