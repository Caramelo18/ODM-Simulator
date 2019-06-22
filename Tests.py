from Population import Population
from Stats import Stats
from SurveyGenerator import SurveyGenerator
from pandas import pandas
import PopulationGenerator
import Parser
import numpy as np

NUM_STEPS = 5

def simulate(population):
    resulting_matrices = {}
    for i in range(NUM_STEPS):
        population.step()
        matrices = population.dynamics.get_od_matrix(step=population.step_num)
        resulting_matrices[i+1] = matrices
    # matrices_info(resulting_matrices)
    # age_dist(population)

def control_test():
    mortality_data = Parser.get_mortality_data()
    natality_data = Parser.get_natality_data()
    migrations_ages = [0, 0, 0, 0, 111, 44, 206, 71, 0, 28, 49, 0, 75, 0, 0, 0, 0, 0]

    population = PopulationGenerator.init_population_census_2011()
    population.init_dynamics()
    population.set_mortality(mortality_data)
    population.set_natality(natality_data)
    population.set_migrations(migrations_ages)
    population.train_predictiors()
    
    simulate(population)

def double_natality_test():
    mortality_data = Parser.get_mortality_data()
    natality_data = Parser.get_natality_data()

    migrations_ages = [0, 0, 0, 0, 111, 44, 206, 71, 0, 28, 49, 0, 75, 0, 0, 0, 0, 0]

    natality_data = Parser.get_natality_data_2011_2018()
    natality_data.pop(2018, None)

    for year in natality_data:
        natality_data[year] *= 2

    population = PopulationGenerator.init_population_census_2011()
    population.init_dynamics()
    population.set_mortality(mortality_data)
    population.set_natality(natality_data)
    population.set_migrations(migrations_ages)
    population.train_predictiors(custom_natality=natality_data)
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
    population.init_dynamics()
    population.set_mortality(mortality_data)
    population.set_natality(natality_data)
    population.set_migrations(migrations_ages)
    population.train_predictiors(custom_mortality=deaths_py)
    
    simulate(population)

def custom_population_origin_test():

    mortality_data = Parser.get_mortality_data()
    natality_data = Parser.get_natality_data()
    migrations_ages = [0, 0, 0, 0, 111, 44, 206, 71, 0, 28, 49, 0, 75, 0, 0, 0, 0, 0]

    custom_index = 25
    population = PopulationGenerator.init_population_census_2011(custom_origin_index=custom_index)
    print("All population initiated on", population.zones[custom_index])
    
    population.init_dynamics()
    population.set_mortality(mortality_data)
    population.set_natality(natality_data)
    population.set_migrations(migrations_ages)
    population.train_predictiors()
    
    simulate(population)

def custom_popualation_schools_test():
    students_filepath = "fake-students-survey.xlsx"
    _ = SurveyGenerator(schools_list="schools-outeiro-das-galegas.csv", students_filepath=students_filepath)

    mortality_data = Parser.get_mortality_data()
    natality_data = Parser.get_natality_data()
    migrations_ages = [0, 0, 0, 0, 111, 44, 206, 71, 0, 28, 49, 0, 75, 0, 0, 0, 0, 0]

    population = PopulationGenerator.init_population_census_2011()
    population.init_dynamics(student_surveys=students_filepath)
    population.set_mortality(mortality_data)
    population.set_natality(natality_data)
    population.set_migrations(migrations_ages)
    population.train_predictiors()
    
    simulate(population)


def custom_popualation_workplaces_test():
    workers_filepath = "fake-workers-survey.xlsx"
    _ = SurveyGenerator(workplaces_list="workplaces-aldeia-redondos.csv", workers_filepath=workers_filepath)

    mortality_data = Parser.get_mortality_data()
    natality_data = Parser.get_natality_data()
    migrations_ages = [0, 0, 0, 0, 111, 44, 206, 71, 0, 28, 49, 0, 75, 0, 0, 0, 0, 0]

    population = PopulationGenerator.init_population_census_2011()
    population.init_dynamics(workers_survey=workers_filepath)
    population.set_mortality(mortality_data)
    population.set_natality(natality_data)
    population.set_migrations(migrations_ages)
    population.train_predictiors()
    
    simulate(population)

def flatten_mortality_test():
    mortality_data = Parser.get_mortality_data()
    for age in mortality_data:
        mortality_data[age] = 20
    
    natality_data = Parser.get_natality_data()
    migrations_ages = [0, 0, 0, 0, 111, 44, 206, 71, 0, 28, 49, 0, 75, 0, 0, 0, 0, 0]

    population = PopulationGenerator.init_population_census_2011()
    population.init_dynamics()
    population.set_mortality(mortality_data) # BEST = "ksone"
    population.set_natality(natality_data)
    population.set_migrations(migrations_ages)
    population.train_predictiors()
    
    simulate(population)

def matrices_info(matrices):
    to_csv = []
    origins_data = []
    dests_data = []
    for step in matrices:
        for mat_type in matrices[step]:
            matrix = matrices[step][mat_type]
            size = len(matrix) - 1
            destinations = list(matrix[size])
            origins = list(matrix[:,size])
            label = "STEP{}-{}".format(step, mat_type)
            org_row = [label + "-ORG"]
            dest_row = [label + "-DEST"]
            org_row = org_row + origins
            dest_row = dest_row +  destinations
            origins_data.append(org_row)
            dests_data.append(dest_row)

    to_csv = origins_data +  dests_data
    pandas.DataFrame(to_csv).to_csv("teste.csv", header=None, index=None)

def age_dist(population):
    age_distributions = population.stats.age_distributions
    
    to_csv = []
    for step in age_distributions:
        dist = age_distributions[step]
        label = "STEP{}".format(step)
        label = [label]
        row = label + dist
        to_csv.append(row)

    pandas.DataFrame(to_csv).to_csv("age_dists.csv", header=None, index=None)

# control_test()
# double_natality_test()
# double_mortality_test()
# custom_population_origin_test()
# custom_popualation_schools_test()
# custom_popualation_workplaces_test()
flatten_mortality_test()