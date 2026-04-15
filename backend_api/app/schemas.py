from pydantic import BaseModel

class CarInput(BaseModel):
    brand: int
    year: int
    mileage: int
    fuel: int