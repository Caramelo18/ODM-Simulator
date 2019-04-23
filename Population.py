from Person import Person
from random import randint
from Enums import PersonClass, Schools
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
import utils
import random

# Data from January 2019 for "Região de Leiria"
DEATHS_PER_MONTH = 383
DEATHS_PER_MONTH_M = 196
DEATHS_PER_MONTH_F = 187

# Data from 2017 for "Pombal" municipality - use yearly data because fluctuations during years
BIRTHS_PER_YEAR = 336
BIRTHS_PER_YEAR_M = 166
BIRTHS_PER_YEAR_F = 170

REG_LEIRIA_POP = 294632
MUN_POMB_POP = 55217
FREG_POMB_POP = 17187

class Population:
    def __init__(self, num_places):
        self.persons = []
        self.num_places = num_places
        self.step_num = 0

    def get_persons(self):
        return self.persons
    
    def get_population_size(self):
        return len(self.persons)

    def set_mortality(self, data):
        print(data)
        self.mortality_probabilites = data

    def set_natality(self, data):
        self.natality_probabilites = data

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

        print(self)
        self.step_num += 1

    def simulate_mortality(self):
        if self.mortality_probabilites is None:
            print("No mortality data loaded")
            exit(1)

        deaths_per_year = DEATHS_PER_MONTH * 12
        death_percentage = deaths_per_year/REG_LEIRIA_POP
        num_deaths = int(self.get_population_size() * death_percentage)

        death_ages = []
        while num_deaths > 0:
            age = None
            d_person = None
            while d_person is None:
                age = utils.roulette(self.mortality_probabilites)
                d_person = self.get_random_person_by_age(age)
            
            self.remove_person(d_person)
            death_ages.append(age)
            num_deaths -= 1

        print("Step {} - {} persons are now dead".format(self.step_num, len(death_ages)))
        # plt.hist(death_ages, bins="auto")
        # plt.xlabel("Age")
        # plt.ylabel("Number of Persons")
        # plt.show()

    def simulate_natality(self):
        births_per_year = int(BIRTHS_PER_YEAR * self.get_population_size() / MUN_POMB_POP)

        for _ in range(births_per_year):
            origin = randint(0, 20)
            destination = 32
            person = Person(origin, destination, PersonClass.CLASS1, 0)
            self.add_person(person)

        print("Step {} - {} persons were born".format(self.step_num, births_per_year))

    def get_random_person_by_age(self, age):
        possible_persons = []
        for person in self.persons:
            if person.get_age() == age:
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

