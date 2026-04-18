import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from ml_engine.base_model import BaseModel

class CarPriceModel(BaseModel):
    def __init__(self, n_estimators=100, max_depth=None, random_state=42):
        # Initialize the scikit-learn model
        self.model = RandomForestRegressor(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=random_state
        )

    def train(self, X, y):
        self.model.fit(X, y)

    def predict(self, X):
        return self.model.predict(X)

    def evaluate(self, X, y):
        # Calculate how accurate the model is
        predictions = self.predict(X)
        mse = mean_squared_error(y, predictions)
        r2 = r2_score(y, predictions)
        return {"MSE": round(mse, 2), "R2_Score": round(r2, 4)}

    def save_model(self, file_path):
        # Export the model as a .pkl file for the Backend
        joblib.dump(self.model, file_path)

    def load_model(self, file_path):
        # Load the model (used by the Backend)
        self.model = joblib.load(file_path)