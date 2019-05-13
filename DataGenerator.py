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


def guess_age(person_class):
    return 1