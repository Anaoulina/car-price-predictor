from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from ml_engine.base_model import BaseModel

class CarPriceModel(BaseModel):
    def __init__(self, random_state=42):
        self.random_state = random_state
        self.model = None # Will be initialized as a Pipeline in train/tune

    def _get_preprocessor(self):
        """Creates a transformer to handle categorical text data."""
        categorical_features = ['Brand', 'Fuel', 'Gearbox']
        
        # OneHotEncoder converts text like 'Mercedes' into numbers (0, 1)
        categorical_transformer = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
        
        preprocessor = ColumnTransformer(
            transformers=[
                ('cat', categorical_transformer, categorical_features)
            ],
            remainder='passthrough' # Keep numerical columns (Year, Mileage) as they are
        )
        return preprocessor

    def train(self, X, y):
        # Create a pipeline: Preprocess data then run Regressor
        self.model = Pipeline(steps=[
            ('preprocessor', self._get_preprocessor()),
            ('regressor', RandomForestRegressor(random_state=self.random_state))
        ])
        self.model.fit(X, y)

    def tune_and_train(self, X, y):
        # Define the base pipeline
        base_pipeline = Pipeline(steps=[
            ('preprocessor', self._get_preprocessor()),
            ('regressor', RandomForestRegressor(random_state=self.random_state))
        ])

        # Hyperparameters (Note the 'regressor__' prefix)
        param_grid = {
            'regressor__n_estimators': [50, 100],
            'regressor__max_depth': [5, None]
        }

        grid_search = GridSearchCV(
            estimator=base_pipeline,
            param_grid=param_grid, 
            cv=2, 
            n_jobs=-1
        )
        
        grid_search.fit(X, y)
        self.model = grid_search.best_estimator_
        return grid_search.best_params_

    def predict(self, X):
        if self.model is None:
            raise ValueError("Model is not trained yet!")
        return self.model.predict(X)

    def evaluate(self, X, y):
        preds = self.predict(X)
        return {
            "MSE": round(mean_squared_error(y, preds), 2), 
            "R2": round(r2_score(y, preds), 4)
        }