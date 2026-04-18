import pandas as pd
from ml_engine.persistence import ModelPersistence

MODEL_PATH = "ml_engine/models/car_price_model.pkl"
try:
    model = ModelPersistence.load(MODEL_PATH)
except Exception as e:
    print(f"❌ Failed to load model: {e}")
    model = None

def predict_price(data):
    try:
    
        input_df = pd.DataFrame([data.dict()])

        prediction = model.predict(input_df)
        
        return float(prediction[0])

    except Exception as e:
        print("ERROR during prediction:", e)
        return {"error": str(e)}