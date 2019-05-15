from sklearn.model_selection import KFold, cross_val_score, cross_val_predict, cross_validate
from sklearn import linear_model
from sklearn.metrics import r2_score
from sklearn import preprocessing
import Parser
import numpy as np

class Predictor:
    def __init__(self):
        self.mortality_predictor = linear_model.ARDRegression()
        #Lasso - 0.76
        #ADR   - 0.85
        self.natality_predictor = linear_model.BayesianRidge(n_iter=20000)

        self.mortality_offset = 1000000
        #BBayesianRidge - 0.2

    
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
            mortality_data[i] = perc * self.mortality_offset

        pop_data = []
        for val in population_data:
            rng = list(val.values())
            # rng = [x / sum(rng) for x in rng]
            pop_data.append(rng)

            
        mortality_data = np.array(mortality_data)
        population_data = np.array(pop_data).astype(float)

        population_data = preprocessing.scale(population_data)

        k_fold = KFold(n_splits=7)

        for train_index, test_index in k_fold.split(mortality_data):
        #     print("train indices:", train_index)
        #     print("train data:", population_data[train_index])
        #     print("test indices:", test_index)
        #     print("test data:", population_data[test_index])
            self.mortality_predictor.fit(population_data[train_index], mortality_data[train_index])   
        
        self.evaluate_mortality(population_data, mortality_data)

    def init_natality_predictor(self):
        natality_data = Parser.get_natality_data_2011_2018()
        natality_data.pop(2018, None)
        population_data = Parser.get_population_data()

        years = list(population_data.keys())

        natality_data = list(natality_data.values())
        population_data = list(population_data.values())
        
        for i in range(len(natality_data)):
            perc = natality_data[i] / sum(population_data[i].values())
            natality_data[i] = perc 


        pop_data = []
        for val in population_data:
            rng = list(val.values())
            # rng = [x / sum(rng) for x in rng]
            pop_data.append(rng)

        natality_data = np.array(natality_data)
        population_data = np.array(pop_data).astype(float)

        population_data = preprocessing.scale(population_data)

        k_fold = KFold(n_splits=7)

        for train_index, test_index in k_fold.split(natality_data):
            # print("train indices:", train_index)
            # print("train data:", population_data[train_index])
            # print("test indices:", test_index)
            # print("test data:", population_data[test_index])
            self.natality_predictor.fit(population_data[train_index], natality_data[train_index])

        
        self.evaluate_natality(population_data, natality_data)

    
    def predict_mortality(self, age_distribution):
        data = preprocessing.scale(age_distribution)
        total = sum(age_distribution)
        pred = self.mortality_predictor.predict([data])[0] / self.mortality_offset
        pred = int(pred * total)
        print("Predicted Mortality: ", pred)

    def evaluate_mortality(self, population_data, mortality_data):
        pred = cross_val_predict(self.mortality_predictor, population_data, mortality_data, cv=7)
        score = r2_score(mortality_data, pred)

        print("Mortality R2 Score:", score)
        
    def evaluate_natality(self, population_data, natality_data):
        pred = cross_val_predict(self.natality_predictor, population_data, natality_data, cv=7)
        score = r2_score(natality_data, pred)
        
        print("Natality R2 Score:", score)

p = Predictor()
p.init_mortality_predictor()
p.init_natality_predictor()
