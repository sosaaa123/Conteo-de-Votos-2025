from typing import Optional
from pydantic import BaseModel

class Stand(BaseModel):
    id_stand: Optional[int]=None
    nombre:str
    descripcion:str
    # "año" 1ro, 2do, etc
    year:int
    division:int
    orientacion:str
    profesor:str
    votos:Optional[int]=None


