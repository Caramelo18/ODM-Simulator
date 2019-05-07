from sklearn.model_selection import KFold, cross_val_score, cross_val_predict
from sklearn import linear_model
from sklearn.metrics import accuracy_score
import Parser
import numpy as np


mortality_data = Parser.get_mortality_data_2011_2018()
mortality_data.pop(2018, None)
population_data = Parser.get_population_data()

years = list(population_data.keys())

print(years)
mortality_data = list(mortality_data.values())
population_data = list(population_data.values())

pop_data = []
for val in population_data:
    rng = list(val.values())
    pop_data.append(rng)
    
mortality_data = np.array(mortality_data)
population_data = np.array(pop_data)
# print(pop_data)

k_fold = KFold(n_splits=4)

lasso = linear_model.Lasso(max_iter=10000)
y_pred = cross_val_predict(lasso, X = population_data, y = mortality_data, cv = 7)
print(mortality_data)
print(y_pred)

accuracy = accuracy_score(y_pred.astype(int), mortality_data.astype(int))
print(accuracy)

# x = lasso.predict(mortality_data[2])
# print(x)