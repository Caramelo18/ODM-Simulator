from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

soup = BeautifulSoup(open("data/emvida.html"), 'html.parser')

table = soup.find_all(class_="dados")[0]
table = table.find("tbody")
table = table.find_all(class_=["TRow1", "TRow0"])

data = {}

for i, line in enumerate(table):
    num = line.find_all("td", attrs={'style': 'width:9%'})[2].text
    num = num.replace(" ", "")
    num = int(num)
    data[i] =  num

print(data)

# plt.bar(data.keys(), data.values(), 0.75, color='g')
# plt.show()

# data = np.round(np.random.normal(5, 2, 100))
# print(data)
# plt.hist(data, bins=10, range=(0,10), edgecolor='black')
# plt.show()
values = []
for key in data:
    num = data[key]
    i = 0
    while i < num:
        values.append(key)
        i += 1
        

mean = np.mean(values)
sd = np.std(values)


x = np.linspace(0,120,1000)
y = stats.norm.pdf(x, loc=mean, scale=sd)    # for example
#plt.hist(values, bins=100, range=(0,100), width=0.75)
print(mean, sd)
plt.plot(x, y)
plt.show()
