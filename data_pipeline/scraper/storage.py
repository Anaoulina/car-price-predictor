import pandas as pd
from abc import ABC, abstractmethod
from threading import Lock

class DataStorage(ABC):
    @abstractmethod
    def save(self, data: list[dict], filename: str):
        pass

class CSVStorage(DataStorage):
    _instance = None
    _lock = Lock() # To make it Thread-Safe

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance
# data_pipeline/scraper/storage.py

def save(self, data, filename):
    import pandas as pd
    df = pd.DataFrame(data)
    # Using utf-8-sig makes CSV files Excel-friendly in Windows
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"💾 Data saved successfully to {filename}")