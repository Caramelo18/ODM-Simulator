from Person import Person
from Population import Population
import Loader
import DataGenerator

from random import randint

POPULATION_SIZE = 100
NUM_SECTIONS = 29
NUM_STEPS = 5

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
    DataGenerator.load_od_reg("fake-data.csv")
  
if __name__== "__main__":
    main()
