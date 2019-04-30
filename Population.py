from Person import Person
from random import randint
from Enums import PersonClass, Schools
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
import utils
import random
from Stats import Stats

# Data from 2017 for "freguesia de Pombal" 
DEATHS_PER_YEAR = 183
DEATHS_PER_YEAR_M = 99
DEATHS_PER_YEAR_F = 84

# Data from 2017 for "Pombal" municipality - use yearly data because fluctuations during months
BIRTHS_PER_YEAR = 336
BIRTHS_PER_YEAR_M = 166
BIRTHS_PER_YEAR_F = 170

# Data from 2011 to 2017 for "Pombal" municipality
MIGRATORY_BALANCE = {'2011': -109, '2012': -91, '2013': -82, '2014': -99, '2015': 161, '2016': -217, '2017': -250}

# Data from 2011 for "freguesia de Pombal" (Proporção da população residente que 1 ano antes residia noutra unidade territorial (%) por Local de residência)
INCOMING_POP_PERC_PER_YEAR = 10.68

REG_LEIRIA_POP = 294632
MUN_POMB_POP = 55217
FREG_POMB_POP = 17187

BIRTH_RANGES = [(10,14), (15,19), (20,24), (25,29), (30,34), (35,39), (40,44), (45,49), (50,120)]

class Population:
    def __init__(self, num_places):
        self.persons = []
        self.num_places = num_places
        self.step_num = 0

        self.stats = Stats(self)

    def get_persons(self):
        return self.persons
    
    def get_population_size(self):
        return len(self.persons)

    def get_stats(self):
        return self.stats

    def set_mortality(self, data):
        self.mortality_probabilites = data

    def set_natality(self, data):
        keys = list(data)
        total_births = int(data[keys[0]])
        probabilities = []
        
        for i in range(1, len(keys)):
            num_births = int(data[keys[i]])
            prob = num_births/total_births
            probabilities.append(prob)

        self.natality_probabilites = probabilities

    def add_person(self, person):
        self.persons.append(person)

    def add_batch(self, size, origin, destination, person_class = PersonClass.CLASS1):
        for _ in range(size):
            p = Person(origin, destination, person_class)
            self.add_person(p)

    def remove_person(self, person):
        self.persons.remove(person)

    def __str__(self):
        length = len(self.persons)

        ret = 'Step {} - Population contains {} persons'.format(self.step_num, length)
        return ret

    def step(self):
        for person in self.persons:
            person.evolve()

        self.simulate_mortality()
        self.simulate_natality()
        self.simulate_migrations()

        print(self)
        self.step_num += 1

        self.stats.get_population_age_stats()

    def simulate_mortality(self):
        try:
            self.mortality_probabilites
        except AttributeError:
            print("ERROR: No mortality data loaded")
            exit(1)

        death_percentage = DEATHS_PER_YEAR / FREG_POMB_POP
        num_deaths = int(self.get_population_size() * death_percentage)

        rand = int(np.random.normal(0, int(num_deaths * 0.05)))
        num_deaths += rand

        death_ages = utils.generate_ages_by_probabilites(self.mortality_probabilites, num_deaths)
        
        for i in range(len(death_ages)):
            age = death_ages[i]
            d_person = self.get_random_person_by_age(age)
            while d_person is None:
                age = utils.generate_ages_by_probabilites(self.mortality_probabilites)[0]
                d_person = self.get_random_person_by_age(age)
                if d_person is not None:
                    death_ages[i] = age 
            self.remove_person(d_person)        

        self.stats.add_mortality_stats(self.step_num, death_ages)

        print("Step {} - {} persons are now dead".format(self.step_num, len(death_ages)))
        # plt.hist(death_ages, bins="auto")
        # plt.xlabel("Age")
        # plt.ylabel("Number of Persons")
        # plt.show()

    def simulate_natality(self):
        try:
            self.natality_probabilites
        except AttributeError:
            print("ERROR: No natality data loaded")
            exit(1)
            
        births = int(BIRTHS_PER_YEAR * self.get_population_size() / MUN_POMB_POP)
        rand = int(np.random.normal(0, int(births * 0.05)))
        
        births += rand
        
        newborns_places = []
        mothers_ages = []

        mothers_age_ranges = utils.generate_ages_by_probabilites(self.natality_probabilites, births)

        for age_range in mothers_age_ranges:
            (min_age, max_age) = BIRTH_RANGES[age_range]
            mother = self.get_random_person_in_age_range(min_age, max_age)
            mother_place = mother.get_origin()
            destination = 32
            newborns_places.append(mother_place)
            mothers_ages.append(mother.get_age())
            person = Person(mother_place, destination, PersonClass.CLASS1, 0)
            self.add_person(person)

        self.stats.add_natality_stats(self.step_num, {'places': newborns_places, 'ages': mothers_ages})

        print("Step {} - {} persons were born".format(self.step_num, len(mothers_age_ranges)))

    def simulate_migrations(self):
        num_income_people = int(INCOMING_POP_PERC_PER_YEAR * 0.01 * self.get_population_size())
        num_outcome_people = num_income_people - MIGRATORY_BALANCE['2017']

        rand_inc = int(np.random.normal(0, int(num_income_people * 0.05)))
        rand_out = int(np.random.normal(0, int(num_outcome_people * 0.05)))

        num_income_people += rand_inc
        num_outcome_people += rand_out

        migr_bal = num_income_people - num_outcome_people
        # print(num_income_people, num_outcome_people, migr_bal)


    def get_random_person_by_age(self, age):
        possible_persons = []
        for person in self.persons:
            if person.get_age() == age:
                possible_persons.append(person)
        
        random.shuffle(possible_persons)
        
        if len(possible_persons) is 0:
            return None

        return possible_persons[0]
    
    def get_random_person_in_age_range(self, min_age, max_age):
        possible_persons = []
        for person in self.persons:
            if person.get_age() >= min_age and person.get_age() <= max_age:
                possible_persons.append(person)

        random.shuffle(possible_persons)
        
        if len(possible_persons) is 0:
            return None

        return possible_persons[0]
        
    
    def get_odm(self):
        od = [[0 for i in range(self.num_places + 1)] for j in range(self.num_places + 1)]

        for i in range(len(od)):
            od[0][i] = i
            od[i][0] = i

        for person in self.persons:
            origin = person.get_origin()
            destination = person.get_destination()
            od[origin][destination] += 1
            
        # for line in od:
        #     print(line)
    
        plt.imshow(od, interpolation='nearest')
        plt.show()

