import os
import pandas as pd
from ml_engine.regression_model import CarPriceModel

# Configuration
MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "car_price_model.pkl")

def create_dummy_data():
    """Creates temporary training data until the Scraping pipeline is ready."""
    data = {
        'year': [2010, 2015, 2018, 2020, 2022],
        'mileage': [150000, 90000, 50000, 20000, 5000],
        'engine_size': [1.4, 1.6, 2.0, 1.5, 2.0],
        'price': [50000, 90000, 140000, 180000, 220000] 
    }
    return pd.DataFrame(data)

def run_training():
    print("🚀 Starting ML Pipeline...")

    # 1. Load Data
    print("📊 Loading data...")
    df = create_dummy_data()
    X = df.drop(columns=['price'])
    y = df['price']

    # 2. Initialize Model
    print("⚙️ Initializing Model...")
    model = CarPriceModel(n_estimators=100, max_depth=10)

    # 3. Train Model
    print("🧠 Training the model...")
    model.train(X, y)

    # 4. Evaluate Model
    metrics = model.evaluate(X, y)
    print(f"✅ Model Evaluation Metrics: {metrics}")

    # 5. Save Model for Backend
    os.makedirs(MODEL_DIR, exist_ok=True)
    model.save_model(MODEL_PATH)
    print(f"💾 Model saved successfully at: {MODEL_PATH}")

if __name__ == "__main__":
    run_training()