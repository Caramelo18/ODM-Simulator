from random import randint

class Person:
    def __init__(self, origin, destination, person_class):
        self.origin = origin
        self.destination = destination
        self.person_class = person_class
        self.step = 0

    def __str__(self):
        return 'Oi'

    def __repr__(self):
        return 'Person from {} to {}'.format(self.origin, self.destination)

    def evolve(self):
        self.step += 1
    
    def get_origin(self):
        return self.origin

    def get_destination(self):
        return self.destination
    
    def get_step(self):
        return self.step
    
    def get_person_class(self):
        return self.person_class