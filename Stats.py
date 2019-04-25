from Population import Population
from matplotlib import pyplot as plt
from Enums import PersonClass

class Stats:
    def __init__(self, population):
        self.population = population

    def get_persons_by_class(self, person_class):
        persons = []
        for person in self.population.get_persons():
            if person.get_person_class() == person_class:
                persons.append(person)
        
        return (len(persons), persons)

    def get_population_classes_stats(self):
        for person_class in PersonClass:
            (size, _) = self.get_persons_by_class(person_class)
            print(person_class, size, sep = " - ")

    def plot_population_by_age(self):
        ages = []
        for person in self.population.get_persons():
            ages.append(person.get_age())

        plt.hist(ages, bins=100)
        plt.xlabel("Age")
        plt.ylabel("Number of Persons")
        plt.show()

    def show_histogram(self, data):
        plt.hist(data)
        plt.show()