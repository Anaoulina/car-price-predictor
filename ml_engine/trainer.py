import joblib
from ml_engine.regression_model import CarPriceModel
from data_pipeline.scraper.processor import load_data, preprocess

# Load dataset
df = load_data("data_pipeline/data/cars.csv")

# Preprocess
X, y = preprocess(df)

# Train model
model = CarPriceModel()
model.train(X, y)

# Save model
joblib.dump(model, "ml_engine/models/car_price_model.pkl")

print("Model trained and saved successfully!")