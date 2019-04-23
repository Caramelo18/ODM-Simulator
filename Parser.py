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
