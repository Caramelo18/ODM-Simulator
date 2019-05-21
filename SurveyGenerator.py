import shapefile
import shapely
from shapely.geometry import Point, shape
from pandas import pandas


basepath = 'data/' 

class SurveyGenerator:
    def __init__(self):
        self.init_shapefile()

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

        return zone

    def read_schools(self):
        filepath = basepath + "schools.csv"
        df = pandas.read_csv(filepath)

        print(df)
        for _, row in df.iterrows():
            lat = row['Lat']
            lon = row['Lon']
            name = row['School Name']
            zone = self.get_point_zone(lat, lon)
            if zone is not None:
                print(name, zone)

    def read_workplaces(self):
        filepath = basepath + "workplaces.csv"
        df = pandas.read_csv(filepath)

        print(df)
        for _, row in df.iterrows():
            lat = row['Lat']
            lon = row['Lon']
            name = row['Name']
            zone = self.get_point_zone(lat, lon)
            if zone is not None:
                print(name, zone)

survey_generator = SurveyGenerator()