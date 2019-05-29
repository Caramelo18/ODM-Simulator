import scipy
import scipy.stats

import matplotlib
import matplotlib.pyplot as plt

import Parser
from collections import Counter

import warnings


# Source: http://www.insightsbot.com/blog/WEjdW/fitting-probability-distributions-with-python-part-1
class Distribution(object):
    
    def __init__(self,dist_names_list = [], custom_dist = True, in_range = True):
        if custom_dist:
            self.dist_names = ["genlogistic", "johnsonsu", "moyal"]
        else:
            self.dist_names = [d for d in dir(scipy.stats) if isinstance(getattr(scipy.stats, d), scipy.stats.rv_continuous)] # ['norm','lognorm','expon']
            
        self.dist_results = []
        self.params = {}
        
        self.DistributionName = ""
        self.PValue = 0
        self.Param = None
        
        self.isFitted = False

        self.min_val = 9999999
        self.max_val = -9999999

        self.in_range = in_range
        
        
    def Fit(self, y):
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        self.dist_results = []
        self.params = {}
        for dist_name in self.dist_names:
            dist = getattr(scipy.stats, dist_name)
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
        # print("BEST: ", self.DistributionName)
        self.isFitted = True
        self.min_val = min(y)
        self.max_val = max(y)

        warnings.filterwarnings("always", category=RuntimeWarning)
        warnings.filterwarnings("always", category=DeprecationWarning)

        return self.DistributionName,self.PValue
    
    def Random(self, n = 1, integer = True):
        if self.isFitted:
            dist_name = self.DistributionName
            param = self.params[dist_name]
            #initiate the scipy distribution
            dist = getattr(scipy.stats, dist_name)
            num = dist.rvs(*param[:-2], loc=param[-2], scale=param[-1], size=n)
            if integer:
                for i in range(len(num)):
                    num[i] = round(num[i], 0)
                num = num.astype(int)
            if self.in_range:
                return self.Filter(num)
            else:
                return num
        else:
            raise ValueError('Must first run the Fit method.')
    
    def Filter(self, values):
        init_len = len(values)
        min_val = min(values)
        max_val = max(values)
        filtered_values = values
        while min_val < self.min_val or max_val > self.max_val:
            for i in range(len(filtered_values)):
                if filtered_values[i] > self.max_val:
                    filtered_values[i] = self.Random()[0]
                if filtered_values[i] < self.min_val:
                    filtered_values[i] = self.Random()[0]

            min_val = min(filtered_values)
            max_val = max(filtered_values)
            
        return filtered_values
            
    def Plot(self,y):
        x = self.Random(n=len(y))
        plt.hist(x, alpha=0.5, label='Fitted')
        plt.hist(y, alpha=0.5, label='Actual')
        plt.legend(loc='upper right')
        plt.show()

# dist = Distribution()

# data = Parser.get_natality_data()
# data.pop('total_births', None)
# print(data)
# r = []
# for i in range(len(data)):
#     key = list(data.keys())[i]
#     num = int(data[key])
#     for _ in range(num):
#         rng = i + 1
#         r.append(i + 1)

# dist.Fit(r)

# true = Counter(r)
# fit = Counter(dist.Random(len(r)))
# print(true)
# print(fit)

# dist.Plot(r)

# mortality_data = list(Parser.get_mortality_data().values())
# r1 = []
# for i in range(len(mortality_data)):
#     deaths = mortality_data[i]
#     for _ in range(deaths):
#         r1.append(i)
        
# dist.Fit(r1)
# dist.Plot(r1)

# migrations = [0, 0, 0, 0, 111, 44, 206, 71, 0, 28, 49, 0, 75, 0, 0, 0, 0, 0]
# r = []
# for i in range(len(migrations)):
#     num = migrations[i]
#     for j in range(num):
#         r.append(i)

# print(r)
# dist = Distribution(in_range=False)
# dist.Fit(r)
# dist.Plot(r)