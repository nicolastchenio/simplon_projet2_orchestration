from pydantic import BaseModel
from typing import List, Optional

class DataInput(BaseModel):
    a: float
    b: float

class DataOutput(BaseModel):
    result: float

class CSVData(BaseModel):
    data: list
    