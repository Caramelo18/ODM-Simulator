import Parser
import DataGenerator
from Population import Population

def test(pop_a, pop_b, num_years):
    if len(pop_a) is not len(pop_b):
        print("Different sizes")
        return

    comp = []
    for i in range(len(pop_a)):
        n_pop_a = pop_a[i]
        n_pop_b = pop_b[i]
        dif = n_pop_a - n_pop_b
        comp.append(dif)
    comp[:] = [int(x / num_years) for x in comp]
    print(comp, sum(comp))

# artificial_population = DataGenerator.init_population("fake-data.csv", year = 2011)
# mortality_data = Parser.get_mortality_data()
# natality_data = Parser.get_natality_data()

# artificial_population.set_mortality(mortality_data)
# artificial_population.set_natality(natality_data)
# artificial_population.train_predictiors()

# init_age_dist = artificial_population.get_population_age_distribution()

# num_years = 0
# for year in range(2011, 2017):
#     artificial_population.step_people()
#     artificial_population.simulate_mortality()
#     artificial_population.simulate_natality()
#     num_years += 1

# fin_age_dist = artificial_population.get_population_age_distribution()

# print(init_age_dist)
# print(fin_age_dist)

# real_pop = DataGenerator.init_population("fake-data.csv", year = 2017)
# real_age_dist = real_pop.get_population_age_distribution()
# print(real_age_dist)

# test(fin_age_dist, real_age_dist, num_years)

def init_mun_pombal_population(data, year):
    age_dist = data[year]
    population = Population(1)
    for (a, b) in age_dist:
        num = age_dist[(a,b)]
        if b == 89:
            b = 100
        population.add_batch_age_range(num, "A", a, b)
    
    return population

pombal_age_dist = Parser.get_population_data()
pombal_natality = Parser.get_natality_data_2011_2018()
pombal_mortality = Parser.get_mortality_data_2011_2018()
mortality_data = Parser.get_mortality_data()

artificial_population = init_mun_pombal_population(pombal_age_dist, 2011)
artificial_population.set_mortality(mortality_data)
final_population = init_mun_pombal_population(pombal_age_dist, 2017)

print(artificial_population.get_population_age_distribution())


num_years = 0
for year in range(2011, 2018):
    num_years += 1
    num_births = pombal_natality[year]
    num_deaths = pombal_mortality[year]
    
    #population aging
    artificial_population.step_people()
    #population natality
    artificial_population.add_batch_age_range(num_births, "A", 0, 0)
    #population mortality
    death_ages = artificial_population.mortality_distribution.Random(n=num_deaths)
    for i in range(len(death_ages)):
        age = death_ages[i]
        d_person = artificial_population.get_random_person_by_age(age)
        while d_person is None:
            age = artificial_population.mortality_distribution.Random()[0]
            d_person = artificial_population.get_random_person_by_age(age)
            if d_person is not None:
                death_ages[i] = age 
        artificial_population.remove_person(d_person)
    print(year)

print(num_years)

print(artificial_population.get_population_age_distribution())
print(final_population.get_population_age_distribution())
test(final_population.get_population_age_distribution(), artificial_population.get_population_age_distribution(), 7)