import Parser
import DataGenerator


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

artificial_population = DataGenerator.init_population("fake-data.csv", year = 2011)
mortality_data = Parser.get_mortality_data()
natality_data = Parser.get_natality_data()

artificial_population.set_mortality(mortality_data)
artificial_population.set_natality(natality_data)

init_age_dist = artificial_population.get_population_age_distribution()

num_years = 0
for year in range(2011, 2018):
    artificial_population.step_people()
    artificial_population.simulate_mortality()
    artificial_population.simulate_natality()
    num_years += 1

fin_age_dist = artificial_population.get_population_age_distribution()

print(init_age_dist)
print(fin_age_dist)

real_pop = DataGenerator.init_population("fake-data.csv", year = 2017)
real_age_dist = real_pop.get_population_age_distribution()
print(real_age_dist)

test(fin_age_dist, real_age_dist, num_years)
