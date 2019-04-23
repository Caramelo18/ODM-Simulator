from Person import Person
from Population import Population
from Stats import Stats
import Loader
import DataGenerator
from random import randint
import Parser
import utils
import matplotlib.pyplot as plt

POPULATION_SIZE = 100
NUM_SECTIONS = 29
NUM_STEPS = 1

def simulate(population):
    for _ in range(NUM_STEPS):
        population.step()

def main():
    # population = Population(NUM_SECTIONS)
    # data = Loader.load_population_data('2011census.csv')
    # population.init_population(data)

    # sections = Loader.load_sections('sections.csv')
    # print(sections)

    # population.init_random_population(POPULATION_SIZE)
    # print(population)
    
    # Loader.load_shapefile('pombal.shp')

    mortality_data = Parser.get_mortality_data()
    natality_data = Parser.get_natality_data()
    
    population = DataGenerator.load_od_reg("fake-data.csv")
    population.set_mortality(mortality_data)

    stats = Stats(population)
    
    # stats.get_population_classes_stats()

    simulate(population)
    stats.plot_population_by_age()

  
if __name__== "__main__":
    main()
