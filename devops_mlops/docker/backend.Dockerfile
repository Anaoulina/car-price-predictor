FROM python:3.11

WORKDIR /app

COPY backend_api/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY backend_api/ backend_api/
COPY ml_engine/ ml_engine/
COPY data_pipeline/ data_pipeline/

ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["uvicorn", "backend_api.app.main:app", "--host", "0.0.0.0", "--port", "8000"]