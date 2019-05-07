from collections import Counter

class Dynamics:
    def __init__(self, population):
        self.population = population
         
    def get_persons_by_class_and_zone(self, person_class, origin_zone):
        persons = []

        for person in self.population.get_persons():
            if person.get_person_class() == person_class and person.get_origin() == origin_zone:
                persons.append(person)
        
        print(persons)
        dest_zones = []
        for person in persons:
            dest_zones.append(person.get_destination())
        
        dest_zones_counter = Counter(dest_zones)
        print(dest_zones_counter)
        print(len(persons))