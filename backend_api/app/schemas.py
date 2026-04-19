from pydantic import BaseModel

class CarInput(BaseModel):
    brand: str     
    year: int
    mileage: int
    fuel: str      
