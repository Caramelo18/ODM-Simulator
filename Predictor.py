from sklearn.model_selection import KFold, cross_val_score, cross_val_predict, cross_validate
from sklearn import linear_model
from sklearn.metrics import r2_score
from sklearn import preprocessing
import Parser
import numpy as np

class Predictor:
    def __init__(self):
        self.mortality_predictor = linear_model.ARDRegression()
        
        self.natality_predictor = linear_model.Lars()

        self.migration_predictor = linear_model.LinearRegression()

        self.mortality_offset = 1000000
    
    def init_mortality_predictor(self, custom_mortality):
        mortality_data = custom_mortality

        if mortality_data is None:
            mortality_data = Parser.get_mortality_data_2011_2018()
            mortality_data.pop(2018, None)
        population_data = Parser.get_population_data()

        mortality_data = list(mortality_data.values())
        population_data = list(population_data.values())

        for i in range(len(mortality_data)):
            perc = mortality_data[i] / sum(population_data[i].values())
            mortality_data[i] = perc * self.mortality_offset

        pop_data = []
        for val in population_data:
            rng = list(val.values())
            pop_data.append(rng)

        mortality_data = np.array(mortality_data)
        population_data = np.array(pop_data).astype(float)

        population_data = preprocessing.scale(population_data)

        k_fold = KFold(n_splits=7)

        for train_index, _ in k_fold.split(mortality_data):
        #     print("train indices:", train_index)
        #     print("train data:", population_data[train_index])
        #     print("test indices:", test_index)
        #     print("test data:", population_data[test_index])
            self.mortality_predictor.fit(population_data[train_index], mortality_data[train_index])   
        
        self.evaluate_mortality(population_data, mortality_data)

    def init_natality_predictor_ages(self):
        natality_data = Parser.get_natality_data_2011_2018()
        natality_data.pop(2018, None)

        population_data = Parser.get_population_data()

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

        for train_index, _ in k_fold.split(natality_data):
            # print("train indices:", train_index)
            # print("train data:", population_data[train_index])
            # print("test indices:", test_index)
            # print("test data:", population_data[test_index])
            self.natality_predictor.fit(population_data[train_index], natality_data[train_index])

        
        self.evaluate_natality(population_data, natality_data)

    def init_natality_predictor(self, custom_natality):
        population_data = Parser.get_population_data()
        total_population = []
        for year in population_data:
            total_population.append(sum(population_data[year].values()))
        total_population.reverse()

        natality_data = custom_natality
        
        if natality_data is None:
            natality_data = Parser.get_natality_data_2011_2018()
            natality_data.pop(2018, None)
        
        x = np.arange(len(natality_data.keys()))
        x = x[:, np.newaxis]
        y = list(natality_data.values())
        y.reverse()

        for i in range(len(y)):
            births = y[i]
            pop = total_population[i]
            y[i] = births / pop 

        self.natality_predictor.fit(x, y)

        self.natality_tick = len(x)
        self.evaluate_natality(x, y)

    def init_migration_predictor(self, custom_migrations):
        balances = custom_migrations
        
        if balances is None:
            balances = {'2011': -109, '2012': -91, '2013': -82, '2014': -99, '2015': 161, '2016': -217, '2017': -250}

        population_data = Parser.get_population_data()
        total_population = []
        for year in population_data:
            total_population.append(sum(population_data[year].values()))
        total_population.reverse()
        
        x = np.arange(len(balances.keys()))
        x = x[:, np.newaxis]
        y = list(balances.values())

        for i in range(len(y)):
            migr = y[i]
            pop = total_population[i]
            y[i] = migr / pop 
                
        self.migration_predictor.fit(x, y)
        
        self.migration_tick = len(x) 
        self.evaluate_migrations(x, y)
    
    def predict_mortality(self, age_distribution):
        data = preprocessing.scale(age_distribution)
        total = sum(age_distribution)
        pred = self.mortality_predictor.predict([data])[0] / self.mortality_offset
        pred = int(pred * total)
        # print("Predicted Mortality: ", pred)
        return pred

    def predict_natality(self, population_number):
        x = np.asarray([self.natality_tick])
        x = x[:, np.newaxis]

        result = self.natality_predictor.predict(x)
        self.natality_tick += 1
        
        result = int(round(result[0] * population_number, 0))
        
        return result


    def predict_migrations(self, population_number):
        x = np.asarray([self.migration_tick])
        x = x[:, np.newaxis]
        
        result = self.migration_predictor.predict(x)
        self.migration_tick += 1
        
        result = int(round(result[0] * population_number, 0))
        return result

    def evaluate_mortality(self, population_data, mortality_data):
        pred = cross_val_predict(self.mortality_predictor, population_data, mortality_data, cv=7)
        score = r2_score(mortality_data, pred)

        print("Mortality R2 Score:", score)
        
    def evaluate_natality_ages(self, population_data, natality_data):
        pred = cross_val_predict(self.natality_predictor, population_data, natality_data, cv=7)
        score = r2_score(natality_data, pred)
        
        print("Natality R2 Score:", score)
    
    def evaluate_natality(self, x, y):
        score = self.natality_predictor.score(x, y)
        print("Natality R2 Score", score)

    def evaluate_migrations(self, x, y):
        score = self.migration_predictor.score(x, y)
        print("Migration R2 Score:", score)

# p = Predictor()
# p.init_mortality_predictor()
# p.init_natality_predictor()
# p.init_migration_predictor()
