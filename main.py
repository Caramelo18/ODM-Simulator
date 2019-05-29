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
    population.get_stats().get_population_age_stats()
    for _ in range(NUM_STEPS):
        #TODO: store age distribution for each step
        print(population.get_population_age_distribution())
        population.step()

    # population.get_stats().show_natality_chart()
    # population.get_stats().show_mortality_chart()

def main():
    # population = Population(NUM_SECTIONS)
    # data = Loader.load_population_data('2011census.csv')
    # population.init_population(data)

    # sections = Loader.load_sections('sections.csv')
    # print(sections)

    # population.init_random_population(POPULATION_SIZE)
    # print(population)
    
    # Loader.load_shapefile('pombal.shp')

    
    # population = DataGenerator.load_od_reg("fake-data.csv")

    # population = DataGenerator.init_population("fake-data.csv")
    # print(population.get_population_age_distribution())


    mortality_data = Parser.get_mortality_data()
    natality_data = Parser.get_natality_data()
    migrations_ages = [0, 0, 0, 0, 111, 44, 206, 71, 0, 28, 49, 0, 75, 0, 0, 0, 0, 0]

    population = DataGenerator.init_population_census_2011()
    population.set_mortality(mortality_data)
    population.set_natality(natality_data)
    population.set_migrations(migrations_ages)
    population.train_predictiors()

    # population.get_population_age_distribution()
    
    # stats.get_population_classes_stats()
    simulate(population)
    # stats.plot_population_by_age()

  
if __name__== "__main__":
    main()
