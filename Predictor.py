from sklearn.model_selection import KFold, cross_val_score, cross_val_predict
from sklearn import linear_model
from sklearn.metrics import r2_score
from sklearn import preprocessing
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

        for i in range(len(mortality_data)):
            perc = mortality_data[i] / sum(population_data[i].values())
            mortality_data[i] = perc * 1000000

        pop_data = []
        for val in population_data:
            rng = list(val.values())
            # rng = [x / sum(rng) for x in rng]
            pop_data.append(rng)

            
        mortality_data = np.array(mortality_data)
        population_data = np.array(pop_data).astype(float)

        population_data = preprocessing.scale(population_data)
        

        k_fold = KFold(n_splits=7)

        for train_index, test_index in k_fold.split(population_data):
        #     print("train indices:", train_index)
        #     print("train data:", population_data[train_index])
        #     print("test indices:", test_index)
        #     print("test data:", population_data[test_index])
            self.mortality_predictor.fit(population_data[train_index], mortality_data[train_index])

        # pred = cross_val_predict(self.mortality_predictor, population_data, mortality_data, cv=7)
        # print("pred", pred)
        # return
        
        # predictions = []

        # for i in range(len(population_data)):
        #     data = population_data[i]
        #     pred = self.mortality_predictor.predict([data])
        #     predictions.append(pred)
        #     print(pred, mortality_data[i])
        # print(predictions)
        # score = r2_score(mortality_data, predictions)
        # print(score)
    
    def predict_mortality(self, age_distribution):
        data = preprocessing.scale(age_distribution)
        total = sum(age_distribution)
        pred = self.mortality_predictor.predict([data])[0] / 1000000
        pred = pred * total
        print("Predicted Mortality: ", pred)



# p = Predictor()
# p.init_mortality_predictor()