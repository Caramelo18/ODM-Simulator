from sklearn.model_selection import KFold, cross_val_score, cross_val_predict
from sklearn import linear_model
from sklearn.metrics import r2_score
import Parser
import numpy as np

class Predictor:
    def __init__(self):
        self.mortality_predictor = linear_model.Lasso(max_iter=20000)
        self.natality_predictor = linear_model.Lasso(max_iter=20000)
    
    def init_mortality_predictor(self):
        mortality_data = Parser.get_mortality_data_2011_2018()
        mortality_data.pop(2018, None)
        population_data = Parser.get_population_data()

        years = list(population_data.keys())

        # print(years)
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

        for train_index, test_index in k_fold.split(population_data):
        #     print("train indices:", train_index)
        #     print("train data:", population_data[train_index])
        #     print("test indices:", test_index)
        #     print("test data:", population_data[test_index])
            self.mortality_predictor.fit(population_data[train_index], mortality_data[train_index])

        # pred = cross_val_predict(lasso, population_data, mortality_data, cv=7)
        # accuracy = accuracy_score(pred.astype(int), mortality_data.astype(int))
        # print(accuracy)

        predictions = []

        for i in range(len(population_data)):
            data = population_data[i]
            pred = int(self.mortality_predictor.predict([data]))
            predictions.append(pred)
            print(pred, mortality_data[i])

        score = r2_score(mortality_data, predictions)
        print(score)



# p = Predictor()
# p.init_mortality_predictor()