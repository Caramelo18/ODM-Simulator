from Person import Person
from random import randint
from Enums import PersonClass, Schools
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt

# Data from January 2019 for "Região de Leiria"
DEATHS_PER_MONTH = 383
DEATHS_PER_MONTH_M = 196
DEATHS_PER_MONTH_F = 187
REG_LEIRIA_POP = 294632

class Population:
    def __init__(self, num_places):
        self.persons = []
        self.num_places = num_places
        self.step_num = 0

    def get_persons(self):
        return self.persons

    def add_person(self, person):
        self.persons.append(person)

    def add_batch(self, size, origin, destination, person_class = PersonClass.CLASS1):
        for i in range(size):
            p = Person(origin, destination, person_class)
            self.add_person(p)                

    def __str__(self):
        length = len(self.persons)

        ret = 'Step {} - Population contains {} persons'.format(self.step, length)
        return ret

    def step(self):
        for person in self.persons:
            person.evolve()

        self.step_num += 1

        print(self)
    
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

