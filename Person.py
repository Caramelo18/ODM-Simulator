from random import randint
from Enums import *
import numpy as np

class Person:
    def __init__(self, origin, destination, person_class, age=None):
        self.origin = origin
        self.destination = destination
        self.person_class = person_class
        self.step = 0
        self.age = age if age is not None else self.guess_age()

    def __str__(self):
        return 'Person with {} year(s) ({}) that lives in zone {}.'.format(self.age, self.person_class, self.origin)
    
    def __repr__(self):
        return 'A {} - C {} - O {}'.format(self.age, self.person_class, self.origin)

    def evolve(self):
        self.step += 1
        self.update_age_and_class()
    
    def get_origin(self):
        return self.origin

    def get_destination(self):
        return self.destination
    
    def get_step(self):
        return self.step
    
    def get_person_class(self):
        return self.person_class

    def get_age(self):
        return self.age

    def guess_age(self):
        if self.person_class == PersonClass.CLASS1:
            return randint(0, 5)
        elif self.person_class == PersonClass.CLASS2:
            return randint(6, 9)
        elif self.person_class == PersonClass.CLASS3:
            return randint(10, 18)
        elif self.person_class == PersonClass.CLASS4:
            return randint(19, 35)
        elif self.person_class == PersonClass.CLASS5:
            return randint(36, 50)
        elif self.person_class == PersonClass.CLASS6:
            return randint(51, 64)
        return int(np.random.normal(80, 10))

    def update_age_and_class(self):
        self.age += 1
        
        if self.age == 6:
            self.person_class = PersonClass.CLASS2
        elif self.age == 10:
            self.person_class = PersonClass.CLASS3
        elif self.age == 19:
            self.person_class = PersonClass.CLASS4
        elif self.age == 36:
            self.person_class = PersonClass.CLASS5
        elif self.age == 51:
            self.person_class = PersonClass.CLASS6
        elif self.age == 65:
            self.person_class = PersonClass.CLASS7