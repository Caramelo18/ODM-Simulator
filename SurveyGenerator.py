import shapefile
import shapely
import random
import numpy as np
from shapely.geometry import Point, shape
from pandas import pandas, ExcelWriter

import PopulationGenerator

basepath = 'data/' 

class SurveyGenerator:
    def __init__(self):
        self.init_shapefile()
        self.schools = {'ESC1': [], 'ESC2': [], 'ESC3': [], 'ESCSEC': []}
        self.workplaces = {'Primary': [], 'Secondary': [], 'Tertiary': []}
        self.read_schools()
        self.read_workplaces()
        self.get_population_distribution()
        self.calculate_surveys_to_generate()
        self.read_survey_template()
        self.fill_students_surveys()
        self.fill_workers_surveys()

    def init_shapefile(self):
        filepath = 'data/pombal.shp'
        shape_file = shapefile.Reader(filepath)

        self.all_shapes = shape_file.shapes() # get all the polygons
        self.all_records = shape_file.records()

    def get_point_zone(self, lat, lon):
        point = (lon, lat)
        point = Point(point)

        zone = None
        for i, sh in enumerate(self.all_shapes):
            polygon = shape(sh)
            if polygon.contains(point):
                zone = self.all_records[i][8]
                # print(zone)
                break

        return zone

    def read_schools(self):
        filepath = basepath + "schools.csv"
        df = pandas.read_csv(filepath)

        for _, row in df.iterrows():
            lat = row['Lat']
            lon = row['Lon']
            name = row['School Name']
            school_type = row['School Type']
            zone = self.get_point_zone(lat, lon)
            if zone is not None:
                obj = {'name': name, 'zone': zone, 'type': school_type}
                self.schools[school_type].append(obj)

        # print(self.schools)
        # print(self.schools, len(self.schools))

    def read_workplaces(self):
        filepath = basepath + "workplaces.csv"
        df = pandas.read_csv(filepath)

        for _, row in df.iterrows():
            lat = row['Lat']
            lon = row['Lon']
            name = row['Name']
            work_type = row['Work Type']
            size = row['Size']
            zone = self.get_point_zone(lat, lon)
            if zone is not None:
                obj = {'name': name, 'zone': zone, 'type': work_type, 'size': size}
                self.workplaces[work_type].append(obj)

        # print(self.workplaces)

    def get_population_distribution(self):
        filepath = basepath + "pombal-detailed.csv"
        df = pandas.read_csv(filepath)

        resize_ratio = PopulationGenerator.get_resize_ratio()
        
        for i, row in df.iterrows():
            tot = int(round(row['Total'] * resize_ratio, 0))
            pens_num = int(round(row['Pensionistas'] * resize_ratio, 0))
            stud_num = int(round(row['Estudantes'] * resize_ratio, 0))
            prim_num = int(round(row['Setor primário'] * resize_ratio, 0))
            sec_num = int(round(row['Secundário'] * resize_ratio, 0))
            tert_num = int(round(row['Terciário'] * resize_ratio, 0))
            df.loc[i, 'Total'] = tot
            df.loc[i, 'Pensionistas'] = pens_num
            df.loc[i, 'Estudantes'] = stud_num
            df.loc[i, 'Setor primário'] = prim_num
            df.loc[i, 'Secundário'] = sec_num
            df.loc[i, 'Terciário'] = tert_num

        df = df.drop(df.index[47])
        
        self.population_distibution = df

    def calculate_surveys_to_generate(self):
        surveys_to_generate = []
        occupations = ['Estudantes', 'Setor primário', 'Secundário', 'Terciário']
        for _, row in self.population_distibution.iterrows():
            obj = {'from': row['Localidade']}
            for occupation in occupations:
                rand_perc = np.random.normal(30, 5) / 100
                num = int(round(row[occupation] * rand_perc, 0))
                obj[occupation] = num

            surveys_to_generate.append(obj)
        self.surveys_to_generate = surveys_to_generate
        # print(surveys_to_generate)

    def read_survey_template(self):
        filepath = basepath + "registo-od-clean.xlsx"
        df = pandas.read_excel(filepath)

        self.columns = df.columns.tolist()

    def fill_students_surveys(self):
        print("Generating students surveys")
        filepath = basepath + "registo-od-generated-students.xlsx"

        row_list = []

        students_columns = self.columns + ['SCHOOL-TYPE']

        for place in self.surveys_to_generate:
            origin = place['from']
            number = place['Estudantes']
            
            schools = self.generate_zone_schools()
            
            for _ in range(number):
                d = dict.fromkeys(self.columns, '')
                d['ORG-LUG'] = origin
                school = schools[random.randint(0, len(schools) - 1)]
                d['DEST-LUG'] = school['zone']
                d['SCHOOL-TYPE'] = school['type']
                row_list.append(d)

        random.shuffle(row_list)

        df = pandas.DataFrame(row_list, columns=students_columns)

        with ExcelWriter(filepath) as writer:
            df.to_excel(writer)

    def fill_workers_surveys(self):
        print("Generating workers surveys")

        filepath = basepath + "registo-od-generated-workers.xlsx"

        row_list = []

        workers_columns = self.columns + ['WORK-TYPE']

        for place in self.surveys_to_generate:
            origin = place['from']
            prim_number = place['Setor primário']
            sec_number = place['Secundário']
            tert_number = place['Terciário']
            workplaces = self.generate_zone_workplaces(prim_number, sec_number, tert_number)
            for workplace in workplaces:
                d = dict.fromkeys(self.columns, '')
                d['ORG-LUG'] = origin
                d['DEST-LUG'] = workplace['zone']
                d['WORK-TYPE'] = workplace['type']
                row_list.append(d)

        random.shuffle(row_list)

        df = pandas.DataFrame(row_list, columns=workers_columns)

        with ExcelWriter(filepath) as writer:
            df.to_excel(writer)

    def generate_zone_schools(self):
        zone_schools = []

        schools_list = self.schools.copy()
        
        random.shuffle(schools_list['ESC1'])
        random.shuffle(schools_list['ESC2'])
        random.shuffle(schools_list['ESC3'])
        random.shuffle(schools_list['ESCSEC'])

        zone_schools.append(schools_list['ESC1'][0])
        zone_schools.append(schools_list['ESC2'][0])
        zone_schools.append(schools_list['ESC3'][0])
        zone_schools.append(schools_list['ESCSEC'][0])

        return zone_schools

    def generate_zone_workplaces(self, n_prim, n_sec, n_tert):
        prim_weights = []
        sec_weights = []
        tert_weights = []

        for workplace in self.workplaces['Primary']:
            prim_weights.append(self.get_weight_by_size(workplace['size']))
        for workplace in self.workplaces['Secondary']:
            sec_weights.append(self.get_weight_by_size(workplace['size']))
        for workplace in self.workplaces['Tertiary']:
            tert_weights.append(self.get_weight_by_size(workplace['size']))
        
        prim_workplaces = random.choices(self.workplaces['Primary'], weights=prim_weights, k=n_prim)
        sec_workplaces = random.choices(self.workplaces['Secondary'], weights=sec_weights, k=n_sec)
        tert_workplaces = random.choices(self.workplaces['Tertiary'], weights=tert_weights, k=n_tert)

        workplaces = prim_workplaces + sec_workplaces + tert_workplaces

        return workplaces

    def get_weight_by_size(self, size):
        if size is 1:
            return 5
        elif size is 2:
            return 15
        elif size is 3:
            return 80
        elif size is 4:
            return 200

survey_generator = SurveyGenerator()