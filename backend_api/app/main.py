from fastapi import FastAPI
from backend_api.app.schemas import CarInput
from backend_api.services.predictor import predict_price

app = FastAPI(title="Car Price Prediction API")

@app.get("/")
def home():
    return {"message": "API is running"}

@app.post("/predict")
def predict(data: CarInput):
    price = predict_price(data)
    return {"predicted_price": price}