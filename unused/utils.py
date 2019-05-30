import pandas
import random
import numpy as np

basepath = 'data/'

#
# 
# UNUSED
#
#

def merge_ss():
    filepath = basepath + 'subsections.csv'
    df = pandas.read_csv(filepath)
    df['SEC-SS'] = df['SEC11'].map(str) + "-" + df['SS11'].map(str)

    places = {}
    for _, row in df.iterrows():
        place_id = row['LUG11']
        if place_id in places:
            places[place_id].append(row['SEC-SS'])
        else:
            places[place_id] = [row['SEC-SS']]

    filepath = basepath + '2011census-full.csv'
    df = pandas.read_csv(filepath, encoding="latin1")

    for index, row in df.iterrows():
        cod = row['GEO_COD']
        cod = cod[1:]
        fr = cod[4:6]
        sec = str(int(cod[6:9]))
        subsec = str(int(cod[9:11]))
        df.loc[index, 'GEO_COD'] = cod
        df.loc[index, 'FR'] = fr
        df.loc[index, 'SEC-SS'] = sec + "-" + subsec
    
    df = df[df['FR'] == '09'] 

    df['LUG11'] = 'def'

    for place in places:
        subsections = places[place]
        for subsection in subsections:
            df.loc[df['SEC-SS'] == subsection, ['LUG11']] = place
    
    df = df.drop('ANO', 1)
    df = df.drop('NIVEL', 1)
    df = df.groupby(['LUG11']).sum()

    df.to_csv('data/census-lug11.csv')
    
    print(df)

def roulette(probabilites):
    length = len(probabilites)
    prob = probabilites.copy()

    for i in range(1, length):
        prob[i] = prob[i - 1] + prob[i]
        
    rand = random.random()

    d = 0
    for i in range(1, len(prob)):
        if rand >= prob[i - 1] and rand <= prob[i]:
            d = i
            break
    
    return d

def generate_ages_by_probabilites(probabilites, k=1):
    age_range = np.arange(len(probabilites))
    ages = random.choices(age_range, probabilites, k = k)
    return ages


def main():
    merge_ss()

if __name__== "__main__":
    main()