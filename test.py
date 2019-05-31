import PopulationGenerator
import time

population = PopulationGenerator.init_population_census_2011()

dynamics = population.dynamics
dynamics.get_od_matrix()