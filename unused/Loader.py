from pandas import pandas
import shapefile
import shapely
from shapely.geometry import Point, shape
from Section import Section

basepath = 'data/' 

def load_sections(filename):
    filepath = basepath + filename
    df = pandas.read_csv(filepath)

    sections = {}
    for _, row in df.iterrows():
        section = Section(row['SEC11'], row['lat'], row['lon'])
        sections[row['SEC11']] = section
    
    return sections

def load_population_data(filename):
    filepath = basepath + filename
    df = pandas.read_csv(filepath)

    sections = {}

    for _, row in df.iterrows():
        section_id, fensino_1bas, fensino_2bas = row['SEC'], row['N_IND_RESIDENT_FENSINO_1BAS'], row['N_IND_RESIDENT_FENSINO_2BAS']
        fensino_3bas, fensino_sec, fensino_possec = row['N_IND_RESIDENT_FENSINO_3BAS'], row['N_IND_RESIDENT_FENSINO_SEC'], row['N_IND_RESIDENT_FENSINO_POSSEC']
        reform, desemp = row['N_IND_RESID_PENS_REFORM'], row['N_IND_RESID_DESEMP']

        sections[section_id] = {'fensino_1bas': fensino_1bas, 'fensino_2bas': fensino_2bas, 'fensino_3bas': fensino_3bas, 'fensino_sec': fensino_sec, 'fensino_possec': fensino_possec, 'reform': reform, 'desemp': desemp}
        # print(sections[section_id])
        # print(section_id, fensino_1bas, fensino_2bas, fensino_3bas, fensino_sec, fensino_possec, reform, desemp, sep = ' - ')

    return sections

def load_shapefile(filename, lat, lon):
    filepath = basepath + filename
    shape_file = shapefile.Reader(filepath)

    all_shapes = shape_file.shapes() # get all the polygons
    all_records = shape_file.records()

    # point = (-8.65429, 39.87083) # Valeira
    point = (-8.64149, 39.88365) # Casalinho
    point = (-8.63600, 39.90731) # Pombal
    point = (-8.571673, 39.897888) # Vale
    point = (lon, lat)
    point = Point(point)

    zone = None
    for i, sh in enumerate(all_shapes):
        polygon = shape(sh)
        if polygon.contains(point):
            zone = all_records[i][8]
            # print(zone)

    return zone

    