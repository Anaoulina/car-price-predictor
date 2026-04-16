# 🚗 Car Price Prediction – MLOps Project

## 📌 Overview

This project is a full end-to-end Machine Learning system for predicting car prices.

It includes:
- 🧠 Machine Learning model (scikit-learn)
- ⚙️ Data pipeline for preprocessing
- 🚀 Backend API using FastAPI
- 🌐 Frontend application using Vite + React
- 🐳 Full containerization with Docker & Docker Compose

The goal is to demonstrate a complete MLOps workflow from data processing to deployment.

---

## 🏗️ Architecture

Frontend (React + Vite)
        ↓
Backend API (FastAPI)
        ↓
ML Engine (scikit-learn model)
        ↓
Data Pipeline (preprocessing)

All services are orchestrated using Docker Compose.

---

## 📁 Project Structure

car-price-predictor/
│
├── backend_api/ # FastAPI backend
├── frontend/ # React frontend (Vite)
├── ml_engine/ # ML model training & prediction
├── data_pipeline/ # Data preprocessing
│
├── devops_mlops/
│ └── docker/
│ ├── backend.Dockerfile
│ ├── frontend.Dockerfile
│ └── docker-compose.yml
│
├── README.md


---
## ⚙️ Tech Stack

### Backend
- Python 3.11
- FastAPI
- Uvicorn
- scikit-learn
- pandas
- numpy

### Frontend
- React (Vite)
- JavaScript
- HTML/CSS

### DevOps
- Docker
- Docker Compose

---

## 🚀 Run the Project with Docker (Recommended)

### ⚠️ Prerequisites
- Docker
- Docker Compose

---

## 🐳 Run with Docker (Recommended)

### 1️⃣ Clone the repository

```bash
git clone https://github.com/Anaoulina/car-price-predictor.git
cd car-price-predictor
```

### 2️⃣ Build and start all services
```bash
docker compose -f devops_mlops/docker/docker-compose.yml up --build
```

### 3️⃣ Access the application

Once everything is running:

- 🌐 Frontend: http://localhost:5173
- ⚙️ Backend API: http://localhost:8000
- 📘 API Documentation (Swagger): http://localhost:8000/docs

## 🧪 Run Without Docker (Development Mode)
### Backend
```bach
cd backend_api
pip install -r requirements.txt
cd ..
PYTHONPATH=. uvicorn backend_api.app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## 🧠 Machine Learning Pipeline

The ML system includes:

- Data cleaning & preprocessing
- Feature engineering
- Model training (scikit-learn)
- Model serialization (pickle/joblib)
- Real-time prediction via API
  
## 🔌 API Endpoints

| Method | Endpoint | Description       |
| ------ | -------- | ----------------- |
| POST   | /predict | Predict car price |
| GET    | /health  | Check API status  |

## 🐳 Docker Services

| Service  | Port |
| -------- | ---- |
| frontend | 5173 |
| backend  | 8000 |

## 📌 Notes

- First build may take time (downloads dependencies)
- Ensure Docker Desktop is running
- Backend automatically loads ML model on startup
- Frontend connects to backend API automatically

## 🧪 Example Workflow

1. User enters car features in frontend
2. Frontend sends request to backend API
3. Backend processes input using ML model
4. Prediction is returned to frontend
5. Result is displayed to user
