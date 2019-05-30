from collections import Counter
from pandas import pandas
import numpy as np
import copy
import random
import sys
basepath = 'data/'

class Dynamics:
    def __init__(self, population):
        self.population = population
        self.zones = []
        self.read_student_surveys('registo-od-generated-students.xlsx')
        np.set_printoptions(threshold=np.inf, linewidth=250)
        # self.read_workers_surveys('registo-od-generated-workers.xlsx')
         
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
    
    def read_student_surveys(self, filename):
        filepath = basepath + filename
        
        df = pandas.read_excel(filepath)
        zone_schools = {'ESC1': [], 'ESC2': [], 'ESC3': [], 'ESCSEC': []}
        data = {}

        for _, row in df.iterrows():
            origin = row['ORG-LUG']
            school_type = row['SCHOOL-TYPE']
            school_zone = row['DEST-LUG']
            if origin not in data:
                data[origin] = copy.deepcopy(zone_schools)
            data[origin][school_type].append(school_zone)

        self.sudents_data = data
        self.process_students_data()
        
    
    def read_workers_surveys(self, filename):
        filepath = basepath + filename

        df = pandas.read_excel(filepath)

    def process_students_data(self):
        schools_distribution = {}
        for origin in self.sudents_data:
            zone_data = self.sudents_data[origin]
            schools_distribution[origin] = {}
            for school_type in zone_data:
                schools = zone_data[school_type]
                num_school_surveys = len(schools)
                schools_count = Counter(schools)
                schools_perc = {} 
                for zone in schools_count:
                    schools_perc[zone] = schools_count[zone] / num_school_surveys
                schools_distribution[origin][school_type] = schools_perc

        self.schools_distribution = schools_distribution
        
    def init_od_matrix(self):
        self.zones = self.population.zones
        num_zones = len(self.zones)

        self.matrix = np.zeros(shape=(num_zones, num_zones), dtype=int)

    def fill_matrix_students(self):
        for person in self.population.get_persons():
            school_type = self.get_school_type_by_age(person.get_age())
            if school_type is not None:
                origin = person.get_origin()
                origin_index = self.get_zone_index(origin)
                schools = self.schools_distribution[origin][school_type]
                if len(schools) is 0: #TODO: GET THE CLOSEST ZONE WITH SCHOOL
                    continue
                zones = list(schools.keys())
                probabilites = list(schools.values())
                dest = self.choose_destination(zones, probabilites)
                dest_index = self.get_zone_index(dest)
                self.matrix[origin_index][dest_index] += 1

                
    def fill_matrix_workers(self):
        print("Workers")

    def get_od_matrix(self):
        self.init_od_matrix()
        self.fill_matrix_students()
        # self.fill_matrix_workers()
        self.append_zones_totals()

    def get_zone_index(self, zone):
        return self.zones.index(zone)

    def choose_destination(self, dest, probabilites):
        destination = random.choices(population=dest, weights=probabilites)
        return destination[0]

    def append_zones_totals(self):
        matrix = self.matrix
        new_len = len(matrix) + 1
        new_matrix = np.zeros(shape=(new_len, new_len), dtype=int)
        new_matrix = new_matrix.astype(int)
        
        for i in range(len(matrix)):
            line = matrix[i]
            total = sum(line)
            total = np.array([total])
            new_line = np.concatenate((line, total), axis=0)
            new_matrix[i] = new_line
        
        attraction = np.sum(new_matrix, axis = 0)
        new_matrix[len(matrix)] = attraction

        self.matrix = new_matrix
        print(self.matrix)
        

    #TODO: save matrix to csv
    
    def get_school_type_by_age(self, age):
        if age > 5 and age < 10:
            return 'ESC1'
        elif age > 9 and age < 12:
            return 'ESC2'
        elif age > 11 and age < 15:
            return 'ESC3' 
        elif age > 14 and age < 19:
            return 'ESCSEC'
        else:
            return None