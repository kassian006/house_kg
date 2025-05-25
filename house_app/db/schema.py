from pydantic import BaseModel
from typing import Optional

class HouseSchema(BaseModel):
    area: int
    year: int
    garage: int
    total_basement: int
    bath: int
    overall_quality: int
    neighborhood: Optional[int] = None
    price: Optional[int] = None

    class Config:
        from_attributes = True