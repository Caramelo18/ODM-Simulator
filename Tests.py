from Population import Population
from Stats import Stats
from SurveyGenerator import SurveyGenerator
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

    population = PopulationGenerator.init_population_census_2011()
    population.init_dynamics()
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

# control_test()
# double_natality_test()
# double_mortality_test()
# custom_population_origin_test()
# custom_popualation_schools_test()
# custom_popualation_workplaces_test()