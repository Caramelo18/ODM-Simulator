from Person import Person
from random import randint
import collections

class Population:
    def __init__(self, num_zones):
        self.persons = []
        self.num_zones = num_zones
        self.step = 0

    def add_person(self, person):
        self.persons.append(person)

    def init_random_population(self, size):
        for _ in range(size):
            p = Person(randint(1, self.num_zones))
            self.add_person(p)
    
    def init_population(self, data):
        for section_id in data:
            section_data = data[section_id]
            for classes in section_data:
                amount = section_data[classes]
                for _ in range(amount):
                    p = Person(section_id)
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
        od = [[0 for i in range(self.num_zones + 1)] for j in range(self.num_zones + 1)]

        for i in range(len(od)):
            od[0][i] = i
            od[i][0] = i

        for person in self.persons:
            origin = person.get_origin()
            destination = person.get_destination()
            od[origin][destination] += 1
            
        for line in od:
            print(line)