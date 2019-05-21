import shapefile
import shapely
import numpy as np
from shapely.geometry import Point, shape
from pandas import pandas

import DataGenerator

basepath = 'data/' 

class SurveyGenerator:
    def __init__(self):
        self.init_shapefile()
        self.schools = []
        self.workplaces = []
        self.read_schools()
        self.read_workplaces()
        self.get_population_distribution()
        self.calculate_surveys_to_generate()

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
                self.schools.append(obj)

        # print(self.schools, len(self.schools))

    def read_workplaces(self):
        filepath = basepath + "workplaces.csv"
        df = pandas.read_csv(filepath)

        for _, row in df.iterrows():
            lat = row['Lat']
            lon = row['Lon']
            name = row['Name']
            work_type = row['Work Type']
            zone = self.get_point_zone(lat, lon)
            if zone is not None:
                obj = {'name': name, 'zone': zone, 'type': work_type}
                self.workplaces.append(obj)

        # print(self.workplaces, len(self.workplaces))

    def get_population_distribution(self):
        filepath = basepath + "pombal-detailed.csv"
        df = pandas.read_csv(filepath)

        resize_ratio = DataGenerator.get_resize_ratio()
        
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
                rand_perc = np.random.normal(20, 5) / 100
                num = int(round(row[occupation] * rand_perc, 0))
                obj[occupation] = num


            surveys_to_generate.append(obj)

        print(surveys_to_generate)


survey_generator = SurveyGenerator()