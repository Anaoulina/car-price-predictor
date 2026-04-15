import joblib
import numpy as np

MODEL_PATH = "ml_engine/models/car_price_model.pkl"

model = joblib.load(MODEL_PATH)


def predict_price(data):
    try:
        input_data = np.array([[
            data.brand,
            data.year,
            data.mileage,
            data.fuel
        ]])

        prediction = model.predict(input_data)
        return float(prediction[0])

    except Exception as e:
        print("ERROR:", e)
        return str(e)