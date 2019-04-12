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
    indexes = np.arange(len(data))
    
    for age in data:
        probabilites.append(data[age]/total)

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
