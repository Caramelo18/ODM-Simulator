from matplotlib import pyplot as plt
import numpy as np
from Enums import PersonClass
import statistics
import collections


class Stats:
    def __init__(self, population):
        self.population = population
        self.natality_stats = {}
        self.mortality_stats = {}
        self.migration_stats = {}

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

    def get_population_age_stats(self):
        ages = []

        for person in self.population.get_persons():
            ages.append(person.get_age())

        mean_age = round(statistics.mean(ages), 2)
        median_age = statistics.median(ages)

        print("Mean Age: {} - Median Age: {}".format(mean_age, median_age))


    def show_histogram(self, data):
        plt.hist(data)
        plt.show()

    def add_natality_stats(self, step, data):
        self.natality_stats[step] = data
    
    def add_mortality_stats(self, step, data):
        self.mortality_stats[step] = data
    
    def add_migration_stats(self, step, data):
        self.migration_stats[step] = data

    def show_natality_chart(self):
        steps = self.natality_stats.keys()
        bar_width = 0.9 / len(steps)
        
        ages = np.arange(15, 50)

        for step in steps:
            ages_data = self.natality_stats[step]['ages']
            counts = collections.Counter(ages_data)
            frequencies = []
            for age in ages:
                if age in counts:
                    frequencies.append(counts[age])
                else:
                    frequencies.append(0)
                    
            offset = step * bar_width
            label_str = "Step {}".format(step)
            plt.bar(ages + offset, frequencies, width=bar_width, label=label_str)

        plt.xlabel("Ages")
        plt.ylabel("Mothers Ages")
        plt.xticks(ages + bar_width, ages)
        plt.legend()
        plt.tight_layout()
        plt.show()
    
    def show_mortality_chart(self):
        steps = self.mortality_stats.keys()
        bar_width = 0.9 / len(steps)
        
        ages = np.arange(0, 101)

        for step in steps:
            ages_data = self.mortality_stats[step]
            counts = collections.Counter(ages_data)
            frequencies = []
            for age in ages:
                if age in counts:
                    frequencies.append(counts[age])
                else:
                    frequencies.append(0)

            offset = step * bar_width
            label_str = "Step {}".format(step)
            plt.bar(ages + offset, frequencies, width=bar_width, label=label_str)
        
        plt.xlabel("Ages")
        plt.ylabel("Number of Deaths")
        plt.xticks(ages + bar_width, ages)
        plt.legend()
        plt.tight_layout()
        plt.show()