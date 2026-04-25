import pandas as pd
import os
import sys
import time
from sklearn.model_selection import train_test_split 

from ml_engine.base_model import BaseModel
from ml_engine.regression_model import CarPriceModel
from ml_engine.persistence import ModelPersistence

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
    data_path = "data_pipeline/scraper/processor/cleaned_cars_test.csv"
    
    try:
        X, y = get_real_data(data_path)
        print(f"📊 Loaded {len(X)} total samples.")
        
        # --- Data Splitting Phase --- #
        # Split the dataset into 80% for training and 20% for testing
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        print(f"🧠 Training model on {len(X_train)} samples...")
        
        # Train and tune the model exclusively on the training set (80%)
        best_params = model.tune_and_train(X_train, y_train)
        print(f"✨ Best Params: {best_params}")
        
        # --- Evaluation Phase --- #
        # 1. Evaluate on the training data to check the learning progress (detects overfitting)
        train_metrics = model.evaluate(X_train, y_train)
        print(f"🎯 Training Metrics: {train_metrics}")
        
        # 2. Evaluate on the unseen test data to measure actual generalization capability
        test_metrics = model.evaluate(X_test, y_test)
        print(f"🚀 Testing Metrics:  {test_metrics}")
        
        # Ensure the directory exists before saving the trained model
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