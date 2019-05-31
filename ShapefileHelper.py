import shapely
import shapefile
import sys
import heapq
from shapely.geometry import Point, shape

class ShapefileHelper:
    def __init__(self):
        filepath = 'data/pombal.shp'
        shape_file = shapefile.Reader(filepath, encoding='utf-8')

        self.shape_records = shape_file.shapeRecords()
        self.all_records = shape_file.records()

        self.get_centroids()
        self.find_nearest_points()
            
    def get_centroids(self):
        centers = {}
        names = []
        
        for i in range(len(self.shape_records)):
            shape_record = self.shape_records[i]
            shape_geom = shape(shape_record.__geo_interface__['geometry'])
            center_coords = shape_geom.centroid
            name = self.all_records[i][8]
            names.append(name)
            centers[name] = center_coords
            
        self.zones_names = sorted(names)
        self.centers = centers

    def find_nearest_points(self):
        nearest_zones = {}

        for point_a_name in self.centers:
            point_a = self.centers[point_a_name]
            min_dist_list = []
            for point_b_name in self.centers:
                point_b = self.centers[point_b_name]
                point_b_index = self.get_zone_index(point_b_name)
                dist = point_a.distance(point_b)
                if dist > 0:
                    heapq.heappush(min_dist_list, (dist, point_b_index))
                
            nearest_zones[self.get_zone_index(point_a_name)] = min_dist_list

        return nearest_zones
    
    def get_zone_index(self, zone):
        return self.zones_names.index(zone)
                
