from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

import random


def get_mortality_data():
    soup = BeautifulSoup(open("data/emvida.html"), 'html.parser')

    table = soup.find_all(class_="dados")[0]
    table = table.find("tbody")
    table = table.find_all(class_=["TRow1", "TRow0"])

    data = {}
    total = 0

    for i, line in enumerate(table):
        num = line.find_all("td", attrs={'style': 'width:9%'})[2].text
        num = num.replace(" ", "")
        num = int(num)
        data[i] =  num
        total += num

    probabilites = []
    
    return data
    
    for age in data:
        probabilites.append(data[age]/total)

    # indexes = np.arange(len(data))
    # plt.bar(indexes, probabilites)
    # plt.show()

    return probabilites

    values = []
    total = 0
    for key in data:
        num = data[key]
        i = 0
        while i < num:
            values.append(key)
            i += 1
            total += 1
            
    print(total)
    mean = np.mean(values)
    sd = np.std(values)


    x = np.linspace(0,120,100)
    y = stats.norm.pdf(x, loc=mean, scale=sd)    # for example
    #plt.hist(values, bins=100, range=(0,100), width=0.75)
    print(mean, sd)
    plt.plot(x, y)
    plt.show()

def get_natality_data():
    soup = BeautifulSoup(open("data/natalidade_simple.html"), 'html.parser')

    table = soup.find_all(class_="dados")[0]
    table = table.find("tbody")
    table = table.find_all(class_=["TRow1"])[0]
    table = table.find_all("td")

    total_births = table[2].text
    births_10_14 = table[3].text
    births_15_19 = table[4].text
    births_20_24 = table[5].text
    births_25_29 = table[6].text
    births_30_34 = table[7].text
    births_35_39 = table[8].text
    births_40_44 = table[9].text
    births_45_49 = table[10].text
    births_50_more = table[11].text

    data = {'total_births': total_births, 'births_10_14': births_10_14, 'births_15_19': births_15_19, 'births_20_24': births_20_24, 'births_25_29': births_25_29, 'births_30_34': births_30_34, 'births_35_39': births_35_39, 'births_40_44': births_40_44, 'births_45_49': births_45_49, 'births_50_more': births_50_more}
    
    return data

def get_age_ranges():
    ranges = []
    for i in range(0, 86, 5):
        rng = (i, i + 4)
        ranges.append(rng)

    return ranges

def get_population_data():
    soup = BeautifulSoup(open("data/popres.html"), 'html.parser')
    
    table = soup.find_all(class_="dados")[0]
    table = table.find("tbody")
    table = table.find_all(class_=["TRow1", "TRow0"])

    ranges = get_age_ranges()
    data = {}
    
    year = 2017
    i = 2
    j = 0
    for i in range(i, len(table), 3):
        row = table[i]
        values = row.find_all("td")[2:]
        year_data = {}
        for i in range(len(values)):
            rng = ranges[i]
            num = values[i].text.replace(" ", "")
            num = int(num)
            year_data[rng] = num
        data[year - j] = year_data
        j += 1

    # print(data)
    return data


def get_natality_data_2011_2018():
    soup = BeautifulSoup(open("data/natalidade_2011_2018.html"), 'html.parser')
    
    table = soup.find_all(class_="dados")[0]
    table = table.find("tbody")
    table = table.find_all(class_=["TRow1", "TRow0"])

    data = {}
    year = 2018
    for i in range(len(table)):
        row = table[i].find_all("td")[2].text
        data[year - i] = int(row)

    return data

def get_mortality_data_2011_2018():
    soup = BeautifulSoup(open("data/mortalidade_2011_2018.html"), 'html.parser')
    
    table = soup.find_all(class_="dados")[0]
    table = table.find("tbody")
    table = table.find_all(class_=["TRow1", "TRow0"])
    
    data = {}
    year = 2018
    for i in range(len(table)):
        row1 = int(table[i].find_all("td")[2].text)
        row2 = int(table[i].find_all("td")[4].text)
        data[year - i] = row1 + row2        

    # print(data)
    return data
        

# get_population_data()
# get_natality_data_2011_2018()
get_mortality_data_2011_2018()