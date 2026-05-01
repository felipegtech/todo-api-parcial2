from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

# Entradas 
class NoteCreate(BaseModel):
    title:     str            = Field(..., min_length=1, max_length=200,  description="Título requerido")
    content:   Optional[str]  = Field(None, max_length=1000,             description="Contenido opcional")
    completed: bool           = Field(False,                             description="Estado de completado")


class NoteUpdate(BaseModel):
    title:     Optional[str]  = Field(None, min_length=1, max_length=200)
    content:   Optional[str]  = Field(None, max_length=1000)
    completed: Optional[bool] = None


# Salidas

class NoteResponse(BaseModel):
    id:         int
    title:      str
    content:    Optional[str]
    completed:  bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}   # Pydantic v2 — lee atributos ORM
