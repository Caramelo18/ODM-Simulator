import scipy
import scipy.stats

import matplotlib
import matplotlib.pyplot as plt

import Parser
from collections import Counter


# Source: http://www.insightsbot.com/blog/WEjdW/fitting-probability-distributions-with-python-part-1
class Distribution(object):
    
    def __init__(self,dist_names_list = []):
        self.dist_names = ['norm','lognorm','expon']
        self.dist_results = []
        self.params = {}
        
        self.DistributionName = ""
        self.PValue = 0
        self.Param = None
        
        self.isFitted = False

        self.min_val = 9999999
        self.max_val = -9999999
        
        
    def Fit(self, y):
        self.dist_results = []
        self.params = {}
        for dist_name in self.dist_names:
            dist = getattr(scipy.stats, dist_name)
            print(dist)
            param = dist.fit(y)
            
            self.params[dist_name] = param
            #Applying the Kolmogorov-Smirnov test
            D, p = scipy.stats.kstest(y, dist_name, args=param);
            self.dist_results.append((dist_name,p))

        #select the best fitted distribution
        sel_dist,p = (max(self.dist_results,key=lambda item:item[1]))
        #store the name of the best fit and its p value
        self.DistributionName = sel_dist
        self.PValue = p
        
        self.isFitted = True
        self.min_val = min(y)
        self.max_val = max(y)

        print(self.min_val)
        print(self.max_val)
        return self.DistributionName,self.PValue
    
    def Random(self, n = 1, integer = True):
        if self.isFitted:
            dist_name = self.DistributionName
            param = self.params[dist_name]
            #initiate the scipy distribution
            dist = getattr(scipy.stats, dist_name)
            num = dist.rvs(*param[:-2], loc=param[-2], scale=param[-1], size=n)
            if integer:
                num = num.astype(int)
            return self.Filter(num)
        else:
            raise ValueError('Must first run the Fit method.')
    
    def Filter(self, values):
        init_len = len(values)
        min_val = min(values)
        max_val = max(values)
        print(min_val, max_val, len(values))
        filtered_values = values
        while min_val < self.min_val or max_val > self.max_val:
            for i in range(len(filtered_values)):
                if filtered_values[i] > self.max_val:
                    filtered_values[i] = self.Random()[0]
                if filtered_values[i] < self.min_val:
                    filtered_values[i] = self.Random()[0]

            min_val = min(filtered_values)
            max_val = max(filtered_values)
            

        print(min_val, max_val, len(filtered_values))
        return filtered_values
            
    def Plot(self,y):
        x = self.Random(n=len(y))
        plt.hist(x, alpha=0.5, label='Fitted')
        plt.hist(y, alpha=0.5, label='Actual')
        plt.legend(loc='upper right')
        plt.show()

dist = Distribution()

data = Parser.get_natality_data()
data.pop('total_births', None)
print(data)
r = []
for i in range(len(data)):
    key = list(data.keys())[i]
    num = int(data[key])
    for _ in range(num):
        rng = i + 1
        r.append(i + 1)

dist.Fit(r)
dist.Plot(r)

true = Counter(r)
fit = Counter(dist.Random(len(r)))
print(true)
print(fit)