from Population import Population
from Stats import Stats
import PopulationGenerator
import Parser

NUM_STEPS = 5

def simulate(population):
    for _ in range(NUM_STEPS):
        population.step()
        population.dynamics.get_od_matrix(step=population.step_num)

def control_test():
    mortality_data = Parser.get_mortality_data()
    natality_data = Parser.get_natality_data()
    migrations_ages = [0, 0, 0, 0, 111, 44, 206, 71, 0, 28, 49, 0, 75, 0, 0, 0, 0, 0]

    population = PopulationGenerator.init_population_census_2011()
    population.set_mortality(mortality_data)
    population.set_natality(natality_data)
    population.set_migrations(migrations_ages)
    population.train_predictiors()
    
    simulate(population)

def double_natality_test():
    mortality_data = Parser.get_mortality_data()
    natality_data = Parser.get_natality_data()

    migrations_ages = [0, 0, 0, 0, 111, 44, 206, 71, 0, 28, 49, 0, 75, 0, 0, 0, 0, 0]

    population = PopulationGenerator.init_population_census_2011()
    population.set_mortality(mortality_data)
    population.set_natality(natality_data)
    population.set_migrations(migrations_ages)
    population.train_predictiors()
    population.BIRTHS_PER_YEAR = population.BIRTHS_PER_YEAR * 2
    
    simulate(population)

def double_mortality_test():
    mortality_data = Parser.get_mortality_data()
    natality_data = Parser.get_natality_data()
    migrations_ages = [0, 0, 0, 0, 111, 44, 206, 71, 0, 28, 49, 0, 75, 0, 0, 0, 0, 0]

    deaths_py = Parser.get_mortality_data_2011_2018()
    deaths_py.pop(2018, None)

    for year in deaths_py:
        deaths_py[year] = deaths_py[year] * 2

    population = PopulationGenerator.init_population_census_2011()
    population.set_mortality(mortality_data)
    population.set_natality(natality_data)
    population.set_migrations(migrations_ages)
    population.train_predictiors(custom_mortality=deaths_py)
    
    simulate(population)

# control_test()
# double_natality_test()
double_mortality_test()