import Parser
from pandas import pandas
from Population import Population

basepath = 'data/' 

AGE_RANGES = ['[0-4] ', '[5-9] ', '[10-13] ', '[14-19] ', '[20-24] ', '[25-64] ', '[>64] '] 
AGE_RANGES_NUM = [(0,4), (5,9), (10,13), (14,19), (20,24), (25,64), (65,100)]

def get_resize_ratio():
    MUN_2011_POP = 55018
    MUN_2017_POP = 52324
    # FREG_2011_POP = total['Total'][47]
    ratio = MUN_2017_POP / MUN_2011_POP

    return ratio

def init_population_census_2011(custom_origin_index=None):
    print("Initializing population")

    filepath = basepath + "pombal-detailed.csv"
    df = pandas.read_csv(filepath)

    # total = df.iloc[[47]]
    
    df = df.drop(df.index[47])

    ratio = get_resize_ratio()
    
    zones = df['Localidade'].tolist()
    population = Population()
    population.set_zones(zones)
    
    for index, row in df.iterrows():
        new_num_pop = 0
        for rng in AGE_RANGES:
            age_num = int(round(row[rng] * ratio, 0))
            new_num_pop += age_num
            df.loc[index, rng] = age_num
        df.loc[index, 'Total'] = new_num_pop
        
    
    for _, row in df.iterrows():
        lugar = row['Localidade']
        if custom_origin_index is not None:
            lugar = zones[custom_origin_index]
        for i in range(len(AGE_RANGES) - 2):
            key = AGE_RANGES[i]
            (a, b) = AGE_RANGES_NUM[i]
            num = row[key]
            population.add_batch_age_range(num, lugar, a, b)
        adult_range_num = row[len(AGE_RANGES)]
        senior_range_num = row[len(AGE_RANGES) + 1]
        adult_distribution = get_adult_age_distribution(adult_range_num)
        senior_distribution = get_senior_age_distribution(senior_range_num)
        for (a, b) in adult_distribution:
            num_age_range = adult_distribution[(a,b)]
            population.add_batch_age_range(num_age_range, lugar, a, b)
        for (a,b) in senior_distribution:
            num_age_range = senior_distribution[(a,b)]
            population.add_batch_age_range(num_age_range, lugar, a, b)

    population.get_stats().add_age_distribution_stats(0, population.get_population_age_distribution())
    print("Population initialized - Total population: {}".format(population.get_population_size()))
    population.get_stats().print_population_age_stats()

    return population

def get_adult_age_distribution(total_adult):
    ranges = Parser.get_age_ranges()[5:13]
    ages_distribution = list(Parser.get_population_data()[2017].values())[5:13]
    total = sum(ages_distribution)
    ages_distribution = [x / total for x in ages_distribution]
    
    ret = {}
    for i in range(len(ages_distribution)):
        key = ranges[i]
        num_people = int(round(ages_distribution[i]*total_adult,0))
        ret[key] = num_people

    return ret

def get_senior_age_distribution(total_senior):
    ranges = Parser.get_age_ranges()[13:]
    ages_distribution = list(Parser.get_population_data()[2017].values())[13:]
    total = sum(ages_distribution)
    ages_distribution = [x / total for x in ages_distribution]
    
    ret = {}

    for i in range(len(ages_distribution)):
        key = ranges[i]
        num_people = int(round(ages_distribution[i] * total_senior,0))
        ret[key] = num_people
    
    return ret

