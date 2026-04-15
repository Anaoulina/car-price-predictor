import joblib

MODEL_PATH = "ml_engine/models/car_price_model.pkl"

model = None


def load_model():
    global model
    if model is None:
        model = joblib.load(MODEL_PATH)
    return model


def predict_price(data):
    model = load_model()

    input_data = [[
        data.brand,
        data.year,
        data.mileage,
        data.fuel
    ]]

    return model.predict(input_data)[0]