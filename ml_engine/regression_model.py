from sklearn.ensemble import RandomForestRegressor
from base_model import BaseModel

class CarPriceModel(BaseModel):

    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100)

    def train(self, X, y):
        self.model.fit(X, y)

    def predict(self, X):
        return self.model.predict(X)