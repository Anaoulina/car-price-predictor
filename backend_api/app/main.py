from fastapi import FastAPI
from backend_api.app.schemas import CarInput
from backend_api.services.predictor import predict_price
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Car Price Prediction API")

@app.get("/")
def home():
    return {"message": "API is running"}

@app.post("/predict")
def predict(data: CarInput):
    price = predict_price(data)
    return {"predicted_price": price}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)