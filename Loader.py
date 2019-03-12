from pandas import pandas
from Section import Section

def load_sections(filename):
    filepath = 'data/' + filename
    df = pandas.read_csv(filepath)

    sections = {}
    for _, row in df.iterrows():
        section = Section(row['SEC11'], row['lat'], row['lon'])
        sections[row['SEC11']] = section
    
    return sections