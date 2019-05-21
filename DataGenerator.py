from pandas import pandas
import shapefile
import shapely
from shapely.geometry import Point, shape
from Section import Section
from random import randint
from Person import Person
from Population import Population
from Enums import PersonClass
import Parser
import Loader
import random

basepath = 'data/' 
schools = [2, 13, 17, 18, 33, 41, 57]
workplaces = [7, 21, 47, 54, 38, 12, 9, 64]
elder_locs = [4, 18, 27, 32]

def load_od_reg(filename):
    filepath = basepath + filename
    df = pandas.read_csv(filepath)

    num_places = len(df)
    df = df.drop(df.columns[0], axis = 1)
    

    # GENERATE SCHOOL LOCATIONS
    # for i, row in df.iterrows():
    #     df.loc[i, 'SCH_1_M'] = schools[randint(0, len(schools) - 1)]
    #     df.loc[i, 'SCH_2_M'] = schools[randint(0, len(schools) - 1)]
    #     df.loc[i, 'SCH_3_M'] = schools[randint(0, len(schools) - 1)]
    #     df.loc[i, 'SCH_SEC_M'] = schools[randint(0, len(schools) - 1)]
    #     df.loc[i, 'SCH_1_S'] = schools[randint(0, len(schools) - 1)]
    #     df.loc[i, 'SCH_2_S'] = schools[randint(0, len(schools) - 1)]
    #     df.loc[i, 'SCH_3_S'] = schools[randint(0, len(schools) - 1)]
    #     df.loc[i, 'SCH_SEC_S'] = schools[randint(0, len(schools) - 1)]
    #     df.loc[i, 'SCH_M_S_DIST'] = round(random.uniform(0, 1),2)
    #     pop_1 = round(random.uniform(0,0.5), 2)
    #     pop_2 = round(random.uniform(0, 1 - pop_1), 2)
    #     pop_3 = round(random.uniform(0, 1 - pop_1 - pop_2), 2)
    #     pop_sec = round(1 - pop_1 - pop_2 - pop_3, 2)
    #     df.loc[i, 'SCH_1'] = pop_1
    #     df.loc[i, 'SCH_2'] = pop_2
    #     df.loc[i, 'SCH_3'] = pop_3
    #     df.loc[i, 'SCH_SEC'] = pop_sec

    # df.to_csv(basepath + "fake-data1.csv")
    
    population = Population(num_places)
    chld_pop = 0.15
    stud_pop = 0.3
    work_pop = 0.4
    ret_pop = 0.15

    for _, row in df.iterrows():
        num_pop = row['POPULATION']
        num_chld = int(num_pop * chld_pop)
        num_stud = int(num_pop * stud_pop)
        num_work = int(num_pop * work_pop)
        num_ret = int(num_pop * ret_pop)

        home_loc = row['PLACE_ID']
        
        num_sch_1_m = int(num_stud * row['SCH_M_S_DIST'] * row['SCH_1'])
        num_sch_1_s = int(num_stud * (1 - row['SCH_M_S_DIST']) * row['SCH_1'])
        num_sch_2_m = int(num_stud * row['SCH_M_S_DIST'] * row['SCH_2'])
        num_sch_2_s = int(num_stud * (1 - row['SCH_M_S_DIST']) * row['SCH_2'])
        num_sch_3_m = int(num_stud * row['SCH_M_S_DIST'] * row['SCH_3'])
        num_sch_3_s = int(num_stud * (1 - row['SCH_M_S_DIST']) * row['SCH_3'])
        num_sch_sec_m = int(num_stud * row['SCH_M_S_DIST'] * row['SCH_SEC'])
        num_sch_sec_s = int(num_stud * (1 - row['SCH_M_S_DIST']) * row['SCH_SEC'])
        # print(num_sch_1_m, num_sch_1_s, num_sch_2_m, num_sch_2_s, num_sch_3_m, num_sch_3_s, num_sch_SEC_m, num_sch_SEC_s)
        population.add_batch(size = num_sch_1_m, origin = home_loc, destination = int(row['SCH_1_M']), person_class=PersonClass.CLASS2)
        population.add_batch(size = num_sch_1_s, origin = home_loc, destination = int(row['SCH_1_S']), person_class=PersonClass.CLASS2)
        population.add_batch(size = num_sch_2_m, origin = home_loc, destination = int(row['SCH_2_M']), person_class=PersonClass.CLASS3)
        population.add_batch(size = num_sch_2_s, origin = home_loc, destination = int(row['SCH_2_S']), person_class=PersonClass.CLASS3)
        population.add_batch(size = num_sch_3_m, origin = home_loc, destination = int(row['SCH_3_M']), person_class=PersonClass.CLASS3)
        population.add_batch(size = num_sch_3_s, origin = home_loc, destination = int(row['SCH_3_S']), person_class=PersonClass.CLASS3)
        population.add_batch(size = num_sch_sec_m, origin = home_loc, destination = int(row['SCH_SEC_M']), person_class=PersonClass.CLASS3)
        population.add_batch(size = num_sch_sec_s, origin = home_loc, destination = int(row['SCH_SEC_S']), person_class=PersonClass.CLASS3)

        population.add_batch(size = num_chld, origin = home_loc, destination = home_loc, person_class = PersonClass.CLASS1)

        wrk_a = random.uniform(0, 0.6)
        wrk_b = random.uniform(0, 1 - wrk_a)
        wrk_c = 1 - wrk_a - wrk_b
        random.shuffle(workplaces)
        wrk_pl = workplaces[0:3]
        wrk_a = int(num_work * wrk_a)
        wrk_b = int(num_work * wrk_b)
        wrk_c = int(num_work * wrk_c)

        population.add_batch(size = wrk_a, origin = home_loc, destination = wrk_pl[0], person_class=PersonClass.CLASS4)
        population.add_batch(size = wrk_b, origin = home_loc, destination = wrk_pl[1], person_class=PersonClass.CLASS5)
        population.add_batch(size = wrk_c, origin = home_loc, destination = wrk_pl[2], person_class=PersonClass.CLASS6)

        random.shuffle(elder_locs)
        population.add_batch(size = num_ret, origin = home_loc, destination = elder_locs[0], person_class=PersonClass.CLASS7)


    return population


def init_population(filename, year = 2017):
    filepath = basepath + filename
    df = pandas.read_csv(filepath)

    num_places = len(df)
    df = df.drop(df.columns[0], axis = 1)
    # print(df)

    population = Population(num_places)
    age_ranges = Parser.get_age_ranges()
    population_ages = Parser.get_population_data()[year]
    
    total_pop = sum(population_ages.values())
    for pop in population_ages:
        percentage = population_ages[pop]/total_pop
        population_ages[pop] = percentage

    for _, row in df.iterrows():
        lug_pop = row['POPULATION']
        home_loc = row['PLACE_ID']
        
        for (a, b) in population_ages:
            percentage = population_ages[(a, b)]
            pop_in_range = int(round(percentage * lug_pop, 0))
            population.add_batch_age_range(pop_in_range, home_loc, a, b)
                
    return population

AGE_RANGES = ['[0-4] ', '[5-9] ', '[10-13] ', '[14-19] ', '[20-24] ', '[25-64] ', '[>64] '] 
AGE_RANGES_NUM = [(0,4), (5,9), (10,13), (14,19), (20,24), (25,64), (65,100)]

def init_population_census_2011():
    filepath = basepath + "pombal-detailed.csv"
    df = pandas.read_csv(filepath)

    total = df.iloc[[47]]
    
    df = df.drop(df.index[47])
    num_places = len(df)

    MUN_2011_POP = 55018
    MUN_2017_POP = 52324
    FREG_2011_POP = total['Total'][47]
    ratio = MUN_2017_POP / MUN_2011_POP
    
    for index, row in df.iterrows():
        new_num_pop = 0
        for rng in AGE_RANGES:
            age_num = int(round(row[rng] * ratio, 0))
            new_num_pop += age_num
            df.loc[index, rng] = age_num
        df.loc[index, 'Total'] = new_num_pop
        
    population = Population(num_places)

    for _, row in df.iterrows():
        lugar = row['Localidade']
        for i in range(len(AGE_RANGES) - 2):
            key = AGE_RANGES[i]
            (a, b) = AGE_RANGES_NUM[i]
            num = row[key]
            population.add_batch_age_range(num, lugar, a, b)
        adult_range_num = row[len(AGE_RANGES)]
        senior_range_num = row[len(AGE_RANGES) + 1]
        adult_distribution = get_adult_age_distribution(adult_range_num)
        senior_distribution = get_senior_age_distribution(senior_range_num)
        for (a, b) in adult_distribution:
            num_age_range = adult_distribution[(a,b)]
            population.add_batch_age_range(num_age_range, lugar, a, b)
        for (a,b) in senior_distribution:
            num_age_range = senior_distribution[(a,b)]
            population.add_batch_age_range(num_age_range, lugar, a, b)

    print(population)
    print(population.get_population_age_distribution())
    # get_senior_age_distribution()

    return population

def get_adult_age_distribution(total_adult):
    ranges = Parser.get_age_ranges()[5:13]
    ages_distribution = list(Parser.get_population_data()[2017].values())[5:13]
    total = sum(ages_distribution)
    ages_distribution = [x / total for x in ages_distribution]
    
    ret = {}
    for i in range(len(ages_distribution)):
        key = ranges[i]
        num_people = int(round(ages_distribution[i]*total_adult,0))
        ret[key] = num_people

    return ret

def get_senior_age_distribution(total_senior):
    ranges = Parser.get_age_ranges()[13:]
    ages_distribution = list(Parser.get_population_data()[2017].values())[13:]
    total = sum(ages_distribution)
    ages_distribution = [x / total for x in ages_distribution]
    
    ret = {}

    for i in range(len(ages_distribution)):
        key = ranges[i]
        num_people = int(round(ages_distribution[i] * total_senior,2))
        ret[key] = num_people
    
    return ret




