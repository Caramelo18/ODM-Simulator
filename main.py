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
NUM_STEPS = 3

def simulate(population):
    for _ in range(NUM_STEPS):
        population.step()


def main():
    print("Loading natality and mortality data")
    mortality_data = Parser.get_mortality_data()
    natality_data = Parser.get_natality_data()
    migrations_ages = [0, 0, 0, 0, 111, 44, 206, 71, 0, 28, 49, 0, 75, 0, 0, 0, 0, 0]

    population = DataGenerator.init_population_census_2011()
    population.set_mortality(mortality_data)
    population.set_natality(natality_data)
    population.set_migrations(migrations_ages)
    population.train_predictiors()
    
    simulate(population)
     
if __name__== "__main__":
    main()
