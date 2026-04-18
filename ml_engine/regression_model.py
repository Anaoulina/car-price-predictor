from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV
from ml_engine.base_model import BaseModel

class CarPriceModel(BaseModel):
    def __init__(self, random_state=42):
        self.model = RandomForestRegressor(random_state=random_state)
        self.random_state = random_state

    def train(self, X, y):
        self.model.fit(X, y)

    def tune_and_train(self, X, y):
        param_grid = {'n_estimators': [50, 100], 'max_depth': [5, None]}
        grid_search = GridSearchCV(
            estimator=RandomForestRegressor(random_state=self.random_state),
            param_grid=param_grid, cv=2 # Using 2 for dummy data, change to 5 for real data
            , n_jobs=-1
        )
        grid_search.fit(X, y)
        self.model = grid_search.best_estimator_
        return grid_search.best_params_

    def predict(self, X):
        return self.model.predict(X)

    def evaluate(self, X, y):
        preds = self.predict(X)
        return {"MSE": round(mean_squared_error(y, preds), 2), "R2": round(r2_score(y, preds), 4)}