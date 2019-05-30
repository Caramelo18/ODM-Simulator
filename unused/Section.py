class Section:
    def __init__(self, section, lat, lon):
        self.section = section
        self.lat = lat
        self.lon = lon
    
    def __repr__(self):
        return 'Section {} -  Lat: {} - Lon: {}'.format(self.section, self.lat, self.lon)