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

def load_population_data(filename):
    filepath = 'data/' + filename
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