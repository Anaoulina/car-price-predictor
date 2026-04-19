import pandas as pd
from ml_engine.persistence import ModelPersistence

MODEL_PATH = "ml_engine/models/car_price_model.pkl"

try:
    model = ModelPersistence.load(MODEL_PATH)
    print("✅ Model loaded successfully in Predictor")
except Exception as e:
    print(f"❌ Failed to load model: {e}")
    model = None

def predict_price(data):
    try:
        input_dict = {
            'Brand': data.brand,
            'Year': data.year,
            'Mileage': data.mileage,
            'Fuel': data.fuel,
            'Gearbox': 'Manuelle'
        }
        
        input_df = pd.DataFrame([input_dict])
        
        prediction = model.predict(input_df)
        return float(prediction[0])
    except Exception as e:
        return {"error": str(e)}