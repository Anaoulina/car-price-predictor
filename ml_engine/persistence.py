import joblib
import os

class ModelPersistence:
    @staticmethod
    def save(model, file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        joblib.dump(model, file_path)
        print(f"💾 Model saved successfully at: {file_path}")

    @staticmethod
    def load(file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"No model found at {file_path}")
        return joblib.load(file_path)