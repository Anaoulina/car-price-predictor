import pandas as pd
from ml_engine.base_model import BaseModel
from ml_engine.regression_model import CarPriceModel
from ml_engine.persistence import ModelPersistence
import time

# ----------------- Decorator for Timing ----------------- #
def time_it(func):
    """Decorator to measure execution time of the ML pipeline."""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        print(f"⏳ Starting [{func.__name__}]...")
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"⏱️ Finished [{func.__name__}] in {round(end_time - start_time, 4)} seconds.\n")
        return result
    return wrapper
# -------------------------------------------------------- #

def get_dummy_data():
    data = {'year': [2010, 2015, 2020], 'mileage': [150000, 80000, 20000], 
            'engine_size': [1.4, 1.6, 2.0], 'price': [50000, 90000, 180000]}
    df = pd.DataFrame(data)
    return df.drop(columns=['price']), df['price']

@time_it
def run_pipeline(model: BaseModel, persistence: ModelPersistence, save_path: str):
    """
    Dependency Inversion: This function depends on Abstractions (BaseModel),
    not concrete classes.
    """
    X, y = get_dummy_data()
    
    print(f"🧠 Training model...")
    best_params = model.tune_and_train(X, y)
    print(f"✨ Best Params: {best_params}")
    
    metrics = model.evaluate(X, y)
    print(f"✅ Metrics: {metrics}")
    
    persistence.save(model.model, save_path) 

if __name__ == "__main__":
    my_model = CarPriceModel()
    my_persistence = ModelPersistence()
    
    run_pipeline(my_model, my_persistence, "models/car_price_model.pkl")