from Person import Person
from random import randint
from Enums import PersonClass, Schools
import collections
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt


class Population:
    def __init__(self, num_places):
        self.persons = []
        self.num_places = num_places
        self.step = 0

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

    def evolve(self):
        for person in self.persons:
            person.evolve()

        self.step += 1

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

    def get_person_class_by_school(self, school):
        if school == Schools.SCH_1:
            return PersonClass.CLASS2
        elif school == Schools.SCH_SUP:
            return PersonClass.CLASS4
        
        return PersonClass.CLASS3

    def get_persons_by_class(self, person_class):
        persons = []
        for person in self.persons:
            if person.get_person_class() == person_class:
                persons.append(person)
        
        return (len(persons), persons)

    def get_population_classes_stats(self):
        for person_class in PersonClass:
            (size, _) = self.get_persons_by_class(person_class)
            print(person_class, size, sep = " - ")