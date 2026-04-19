import pandas as pd
import os
import sys
from ml_engine.base_model import BaseModel
from ml_engine.regression_model import CarPriceModel
from ml_engine.persistence import ModelPersistence
import time

# Ensure imports work regardless of execution location
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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

# ----------------- Real Data Loading ----------------- #
def get_real_data(file_path):
    """Load cleaned data from the scraper output."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ Cleaned data file not found at: {file_path}")
    
    df = pd.read_csv(file_path)
    
    # Selecting the features that match our Scraper/Cleaner output
    # Make sure these column names match exactly what's in your CSV
    features = ['Brand', 'Year', 'Mileage', 'Fuel', 'Gearbox']
    target = 'Price'
    
    X = df[features]
    y = df[target]
    
    return X, y

@time_it
def run_pipeline(model: BaseModel, persistence: ModelPersistence, save_path: str):
    """
    Dependency Inversion: Uses the cleaned CSV data instead of dummy data.
    """
    # Adjust this path based on where you are running the script from
    data_path = "data_pipeline/scraper/processor/cleaned_cars_test.csv"
    
    try:
        X, y = get_real_data(data_path)
        print(f"📊 Loaded {len(X)} samples for training.")
        
        print(f"🧠 Training model...")
        best_params = model.tune_and_train(X, y)
        print(f"✨ Best Params: {best_params}")
        
        metrics = model.evaluate(X, y)
        print(f"✅ Training Metrics: {metrics}")
        
        # Ensure the directory exists before saving
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        persistence.save(model.model, save_path)
        
    except Exception as e:
        print(f"❌ Pipeline failed: {e}")

if __name__ == "__main__":
    # Initialize components
    my_model = CarPriceModel()
    my_persistence = ModelPersistence()
    
    # Run pipeline and save the model in the models folder
    run_pipeline(my_model, my_persistence, "models/car_price_model.pkl")