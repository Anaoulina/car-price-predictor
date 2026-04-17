# ml_engine/base_model.py

from abc import ABC, abstractmethod

class BaseModel(ABC):
    """
    Abstract Base Class for all Machine Learning Models in the project.
    Forces all models to have train, predict, save, and load methods.
    """

    @abstractmethod
    def train(self, X, y):
        pass

    @abstractmethod
    def predict(self, X):
        pass

    @abstractmethod
    def save_model(self, file_path):
        pass

    @abstractmethod
    def load_model(self, file_path):
        pass