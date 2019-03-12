from Person import Person
from Population import Population
import Loader

from random import randint

POPULATION_SIZE = 100
NUM_SECTIONS = 5
NUM_STEPS = 5

def simulate(population):
    for _ in range(NUM_STEPS):
        population.evolve()

def main():
    population = Population(NUM_SECTIONS)
    sections = Loader.load_sections('sections.csv')
    print(sections)

    population.init_random_population(POPULATION_SIZE)
    print(population)
    population.get_odm()
    #simulate(population)
  
if __name__== "__main__":
    main()
