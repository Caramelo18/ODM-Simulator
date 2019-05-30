from random import randint
from Enums import PersonClass, Schools
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
import random
from Person import Person
from Stats import Stats
from Dynamics import Dynamics
from Predictor import Predictor
from Distribution import Distribution
import Parser

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

# Data from 21/03/2011 for "freguesia de Pombal" (relative to 31/12/2009)
MIGR_NO_CHANGE = 15160
MIGR_FROM_SAME = 1143
MIGR_FROM_OUT = 692

REG_LEIRIA_POP = 294632
MUN_POMB_POP = 55217
FREG_POMB_POP = 17187

BIRTH_RANGES = [(10,14), (15,19), (20,24), (25,29), (30,34), (35,39), (40,44), (45,49), (50,120)]

class Population:
    def __init__(self):
        self.persons = []
        self.zones = []
        self.step_num = 0
        self.dynamics = Dynamics(self)
        self.stats = Stats(self)
        self.predictor = Predictor()

    def get_dynamics(self):
        self.dynamics.get_persons_by_class_and_zone(PersonClass.CLASS3, 57)

    def get_persons(self):
        return self.persons
    
    def get_population_size(self):
        return len(self.persons)

    def get_stats(self):
        return self.stats

    def set_zones(self, zones):
        self.zones = zones

    def set_mortality(self, data):
        print("Fitting mortality distribution")
        mortality_data = list(data.values())
        r = []
        for i in range(len(mortality_data)):
            deaths = mortality_data[i]
            for _ in range(deaths):
                r.append(i)
                
        dist = Distribution()
        dist.Fit(r)

        self.mortality_distribution = dist
                
    def set_natality(self, data):
        print("Fitting natality distribution")
        data.pop('total_births', None)
        
        r = []
        for i in range(len(data)):
            key = list(data.keys())[i]
            num = int(data[key])
            for _ in range(num):
                r.append(i + 1)

        dist = Distribution()
        dist.Fit(r)
        
        self.natality_distribution = dist
    
    def set_migrations(self, data):
        print("Fitting migration distribution")
        
        r = []
        for i in range(len(data)):
            num = data[i]
            for _ in range(num):
                r.append(i)

        dist = Distribution(in_range=False)
        dist.Fit(r)
        
        self.migrations_distribution = dist
    
    def train_predictiors(self):
        print("Initializing predictors")
        self.predictor.init_mortality_predictor()
        # self.predictor.init_natality_predictor()
        self.predictor.init_migration_predictor()

    def add_person(self, person):
        self.persons.append(person)

    def add_batch(self, size, origin, destination = None, person_class = PersonClass.CLASS1):
        for _ in range(size):
            p = Person(origin, destination, person_class)
            self.add_person(p)

    def add_batch_age_range(self, size, origin, min_age, max_age):
        for _ in range(size):
            age = randint(min_age, max_age)
            p = Person(origin, PersonClass.CLASS1, age = age)
            self.add_person(p)


    def remove_person(self, person):
        self.persons.remove(person)

    def __str__(self):
        length = len(self.persons)

        ret = 'Step {} - Population contains {} persons'.format(self.step_num, length)
        return ret

    def step(self):
        self.step_num += 1
        self.step_people()
            
        self.simulate_mortality()
        self.simulate_natality()
        self.simulate_migrations()

        self.stats.add_age_distribution_stats(self.step_num, self.get_population_age_distribution())

        print(self)
        self.stats.print_population_age_stats()

    def step_people(self):
        for person in self.persons:
            person.evolve()
        
    def simulate_mortality(self):
        try:
            self.mortality_distribution
        except AttributeError:
            print("ERROR: No mortality data loaded")
            exit(1)
            
        # death_percentage = DEATHS_PER_YEAR / FREG_POMB_POP
        # num_deaths = int(self.get_population_size() * death_percentage)

        # rand = int(np.random.normal(0, int(num_deaths * 0.05)))
        # num_deaths += rand
        age_distibution = self.get_population_age_distribution()
        num_deaths = self.predictor.predict_mortality(age_distibution)

        death_ages = self.mortality_distribution.Random(n=num_deaths)
        
        for i in range(len(death_ages)):
            age = death_ages[i]
            d_person = self.get_random_person_by_age(age)
            while d_person is None:
                age = self.mortality_distribution.Random()[0]
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
            self.natality_distribution
        except AttributeError:
            print("ERROR: No natality data loaded")
            exit(1)
            
        births = int(BIRTHS_PER_YEAR * self.get_population_size() / MUN_POMB_POP)
        rand = int(np.random.normal(0, int(births * 0.05)))
        
        births += rand
        
        newborns_places = []
        mothers_ages = []

        mothers_age_ranges = self.natality_distribution.Random(n = births)

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
        num_persons_out = self.predictor.predict_migrations(self.get_population_size())
        num_persons_out = abs(num_persons_out)
        
        migration_age_ranges = self.migrations_distribution.Random(n=num_persons_out)
        age_ranges = Parser.get_age_ranges()

        outcome_ages = []
        
        for i in range(len(migration_age_ranges)):
            age_range = migration_age_ranges[i]

            if age_range >= len(age_ranges):
                migration_age_ranges[i] = self.migrations_distribution.Random(n=1)[0]
                age_range = migration_age_ranges[i]

            (a, b) = age_ranges[age_range]
            
            person = self.get_random_person_in_age_range(a, b)
            outcome_ages.append(person.get_age())
            self.remove_person(person)

        self.stats.add_migration_stats(self.step_num, outcome_ages)

        print("Step {} - {} persons left".format(self.step_num, num_persons_out))

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
    
    def get_num_persons_in_age_range(self, min_age, max_age):
        possible_persons = []
        for person in self.persons:
            if person.get_age() >= min_age and person.get_age() <= max_age:
                possible_persons.append(person)
        
        return len(possible_persons)

    def get_population_age_distribution(self):
        age_ranges = Parser.get_age_ranges()
        (min_a, max_a) = age_ranges[len(age_ranges) - 1]
        max_a = 120
        age_ranges[len(age_ranges) - 1] = (min_a, max_a)

        info = []

        for (min_a, max_a) in age_ranges:
            num = self.get_num_persons_in_age_range(min_a, max_a)
            info.append(num)
        
        return info
        
    
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

