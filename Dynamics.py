from collections import Counter
from pandas import pandas
from ShapefileHelper import ShapefileHelper
from Distribution import Distribution
import numpy as np
import copy
import random
import sys
import Parser

basepath = 'data/'

class Dynamics:
    def __init__(self, population, student_surveys, worker_surveys):
        self.population = population
        self.zones = []
        self.shapefile_helper = ShapefileHelper()
        
        np.set_printoptions(threshold=np.inf, linewidth=250)

        self.read_student_surveys(student_surveys)
        self.read_workers_surveys(worker_surveys)

        self.load_unemployment()
             
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

        data = {}

        for _, row in df.iterrows():
            origin = row['ORG-LUG']
            workplace_zone = row['DEST-LUG']
            if 'Casal Fern' in workplace_zone:
                workplace_zone = 'Casal Fernão João' 
            workplace_type = row['WORK-TYPE']
            if origin not in data:
                data[origin] = {'dest': [], 'type': []}
            data[origin]['dest'].append(workplace_zone)
            data[origin]['type'].append(workplace_type)

        self.workers_data = data

        self.process_workers_data()

    def load_unemployment(self):
        data = Parser.get_unemployment_rates()

        # r = []
        # for (a, b) in data:
        #     unemployment = int(round(data[(a,b)],0))
        #     for i in range(unemployment):
        #         for age in range(a,b+1):
        #             r.append(age)
        
        # dist = Distribution(custom_dist=False)
        # dist.Fit(r)
        # dist.Plot(r)
        self.unemployment_rates = data

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

    def process_workers_data(self):
        workplaces_distribution = {}

        for origin in self.workers_data:
            zone_data = self.workers_data[origin]['dest']
            counts = Counter(zone_data)
            num_answers = len(zone_data)
            zone_destinations = {}
            for zone in counts:
                zone_destinations[zone] = counts[zone] / num_answers
            workplaces_distribution[origin] = zone_destinations
        
        self.workplaces_distribution = workplaces_distribution
        
    def correct_students_data(self):
        for zone in self.zones:
            if zone not in self.schools_distribution:
                self.schools_distribution[zone] = {'ESC1': {}, 'ESC2': {}, 'ESC3': {}, 'ESCSEC': {}}

        closest_zones = self.shapefile_helper.find_nearest_points()
        
        for origin in self.schools_distribution:
            zone_data = self.schools_distribution[origin]
            for school_type in zone_data:
                num_schools = len(zone_data[school_type])
                closest_zone = None
                closest_zone_schools = None
                i = 0
                if num_schools is not 0:
                    continue
                while num_schools is 0:
                    closest_zones_indexes = closest_zones[self.get_zone_index(origin)]
                    (_, index) = closest_zones_indexes[i]
                    closest_zone = self.zones[index]
                    closest_zone_schools = self.schools_distribution[closest_zone][school_type]
                    num_schools = len(closest_zone_schools)
                    i += 1

                self.schools_distribution[origin][school_type] = closest_zone_schools

    def correct_workers_data(self):
        for zone in self.zones:
            if zone not in self.workplaces_distribution:
                self.workplaces_distribution[zone] = {}
                    
    def init_od_matrix(self):
        self.zones = self.population.zones
        
        self.correct_students_data()
        self.correct_workers_data()

        self.reset_matrices()

    def reset_matrices(self):
        num_zones = len(self.zones)
        
        types = ['ESC1', 'ESC2', 'ESC3', 'ESCSEC', 'WORKERS']

        self.matrices = {}

        for matrix_cat in types:
            self.matrices[matrix_cat] = np.zeros(shape=(num_zones, num_zones), dtype=int)

    def fill_matrix_students(self):
        try: 
            self.matrices
        except AttributeError:
            self.init_od_matrix()
            
        for person in self.population.get_persons():
            school_type = self.get_school_type_by_age(person.get_age())
            if school_type is not None:
                origin = person.get_origin()
                origin_index = self.get_zone_index(origin)
                schools = self.schools_distribution[origin][school_type]
                
                zones = list(schools.keys())
                probabilites = list(schools.values())
                dest = self.choose_destination(zones, probabilites)
                dest_index = self.get_zone_index(dest)
                self.matrices[school_type][origin_index][dest_index] += 1

    def fill_matrix_workers(self):
        try: 
            self.matrices
        except AttributeError:
            self.init_od_matrix()

        for person in self.population.get_persons():
            age = person.get_age()
            if age > 19 and age < 65:
                if not self.is_employed(age):
                    continue
                origin = person.get_origin()
                origin_index = self.get_zone_index(origin)

                zone_workplaces = self.workplaces_distribution[origin]
                zones = list(zone_workplaces.keys())
                probabilites = list(zone_workplaces.values())
                dest = self.choose_destination(zones, probabilites)
                dest_index = self.get_zone_index(dest)
                self.matrices['WORKERS'][origin_index][dest_index] += 1


    def get_od_matrix(self, step=None):
        self.fill_matrix_students()
        self.fill_matrix_workers()

        self.append_zones_totals()

        self.save_matrices_to_csv(step=step)

        matrices = self.matrices

        self.reset_matrices()
        
        return matrices

    def get_zone_index(self, zone):
        return self.zones.index(zone)

    def choose_destination(self, dest, probabilites):
        destination = random.choices(population=dest, weights=probabilites)
        return destination[0]

    def append_zones_totals(self):
        
        for matrix_type in self.matrices:
            matrix = self.matrices[matrix_type]
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
            self.matrices[matrix_type] = new_matrix 

    def save_matrices_to_csv(self, step=None):
        print("Saving matrix to CSV")
        basepath = 'matrices/'
        filepath = basepath + 'odm-{}'
        if step is not None:
            filepath = filepath + '-step{}'.format(step)
        filepath = filepath + '.csv'

        matrix_size = len(self.matrices['ESC1'])
        aggregate_matrix = np.zeros(shape=(matrix_size, matrix_size), dtype=int)

        labels = self.zones + ['Total']

        for matrix_type in self.matrices:
            filename = filepath.format(matrix_type)
            aggregate_matrix = np.add(aggregate_matrix, self.matrices[matrix_type], dtype=int)
            pandas.DataFrame(self.matrices[matrix_type], index=labels, columns=labels).to_csv(filename)
        
        self.matrices['AGG'] =  aggregate_matrix
        filename = filepath.format('aggregate')
        pandas.DataFrame(aggregate_matrix, index=labels, columns=labels).to_csv(filename)
    
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
    
    def is_employed(self, age):
        perc = None

        for (a, b) in self.unemployment_rates:
            if age >= a and age <= b:
                perc = self.unemployment_rates[(a,b)]

        perc /= 100

        rand = random.random()

        employed = perc <= rand
        
        return employed
