from models.guitar_factory import factory_simulation
from constants import default_constants
from simulation_params import SimulationParams


def simulate(params):
    constants = SimulationParams(params)
    sim_result = factory_simulation(constants)
    
    return sim_result

def main():
    sim_result = simulate(default_constants)
    
    for log in sim_result['logs']:
        print(log)


if __name__ == "__main__":
    main()
