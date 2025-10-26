from typing import Optional
from pydantic import BaseModel

class Stand(BaseModel):
    id_stand: Optional[int]=None
    nombre:str
    descripcion:str
    curso:str
    orientacion:str
    profesor:str
    votos:Optional[int]=None


