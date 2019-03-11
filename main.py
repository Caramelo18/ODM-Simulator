from Person import Person
from Population import Population
from random import randint

POPULATION_SIZE = 100
NUM_ZONES = 5
NUM_STEPS = 5

def simulate(population):
    for _ in range(NUM_STEPS):
        population.evolve()

def main():
    population = Population(NUM_ZONES)

    population.init_random_population(POPULATION_SIZE)
    print(population)
    population.get_odm()
    #simulate(population)
  
if __name__== "__main__":
    main()
