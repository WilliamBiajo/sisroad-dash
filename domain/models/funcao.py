from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class Funcao(BaseModel):
    id: Optional[int] = None
    descricao: str = Field(..., min_length=1)
    salario: Optional[float] = None
    inicio: Optional[date] = None
    fim: Optional[date] = None
    extras: dict = {}
