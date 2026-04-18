from abc import ABC, abstractmethod

class Trainable(ABC):
    @abstractmethod
    def train(self, X, y): pass
    
    @abstractmethod
    def tune_and_train(self, X, y): pass

class Predictable(ABC):
    @abstractmethod
    def predict(self, X): pass
    
    @abstractmethod
    def evaluate(self, X, y): pass

class BaseModel(Trainable, Predictable, ABC):
    pass