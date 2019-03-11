from Person import Person
from random import randint
import collections

class Population:
    def __init__(self):
        self.persons = []
        self.step = 0

    def add_person(self, person):
        self.persons.append(person)

    def init_random_population(self, size, num_zones):
        for _ in range(size):
            p = Person(randint(1, num_zones))
            self.add_person(p)

    def __str__(self):
        length = len(self.persons)

        od = {}

        for person in self.persons:
            origin = person.get_origin()
            if origin in od:
                od[origin] += 1
            else:
                od[origin] = 1

        od = collections.OrderedDict(sorted(od.items()))
        
        print(od)
        ret = 'Step {} - Population contains {} persons'.format(self.step, length)
        return ret

    def evolve(self):
        for person in self.persons:
            person.evolve()

        self.step += 1

        print(self)