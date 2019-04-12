from Person import Person
from Population import Population
import Loader
import DataGenerator
from random import randint
from Enums import *
import Parser
import utils

POPULATION_SIZE = 100
NUM_SECTIONS = 29
NUM_STEPS = 1

def simulate(population):
    for _ in range(NUM_STEPS):
        population.evolve()

def main():
    # population = Population(NUM_SECTIONS)
    # data = Loader.load_population_data('2011census.csv')
    # population.init_population(data)

    # sections = Loader.load_sections('sections.csv')
    # print(sections)

    # population.init_random_population(POPULATION_SIZE)
    # print(population)
    # population.get_odm()
    # simulate(population)
    # Loader.load_shapefile('pombal.shp')
    mortality_data = Parser.get_mortality_data()
    print(mortality_data)
    utils.roulette(mortality_data)
    population = DataGenerator.load_od_reg("fake-data.csv")
    
    population.get_population_classes_stats()

    # population.plot_population_by_age()
    simulate(population)

  
if __name__== "__main__":
    main()
