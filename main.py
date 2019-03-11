from Person import Person
from Population import Population
from random import randint

POPULATION_SIZE = 100
NUM_ZONES = 29
NUM_STEPS = 5

def simulate(population):
    for _ in range(NUM_STEPS):
        population.evolve()

def main():
    population = Population()

    population.init_random_population(POPULATION_SIZE, NUM_ZONES)
    print(population)

    simulate(population)
  
if __name__== "__main__":
    main()
