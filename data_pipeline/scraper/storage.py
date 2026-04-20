import pandas as pd
from abc import ABC, abstractmethod
from threading import Lock
import os

class DataStorage(ABC):
    @abstractmethod
    def save(self, data: list[dict], filename: str):
        pass

class CSVStorage(DataStorage):
    _instance = None
    _lock = Lock()  # To make it Thread-Safe

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance

    def save(self, data, filename):
        if not data:
            print("⚠️ No data to save.")
            return
            
        df = pd.DataFrame(data)
        
        file_exists = os.path.isfile(filename)
        
        df.to_csv(filename, mode='a', index=False, encoding='utf-8-sig', header=not file_exists)
        print(f"💾 Data saved successfully to {filename} ({len(data)} cars added)")