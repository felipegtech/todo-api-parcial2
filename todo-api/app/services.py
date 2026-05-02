# servicios de la app, que contienen la lógica de negocio y validaciones. Se encargan de interactuar con los repositorios para acceder a los datos, y pueden lanzar excepciones HTTP para manejar errores de forma centralizada en las rutas.

from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app import repositories
from app.models import Note
from app.schemas import NoteCreate, NoteUpdate


def list_notes(db: Session) -> List[Note]:
    return repositories.get_all(db)


def get_note(db: Session, note_id: int) -> Note:
    note = repositories.get_by_id(db, note_id)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nota con id={note_id} no encontrada",
        )
    return note


def create_note(db: Session, data: NoteCreate) -> Note:
    # Aquí podrías agregar más reglas: límite de notas por usuario, etc.
    return repositories.create(db, data)


def update_note(db: Session, note_id: int, data: NoteUpdate) -> Note:
    note = get_note(db, note_id)   # reutiliza la validación de existencia
    return repositories.update(db, note, data)


def delete_note(db: Session, note_id: int) -> Note:
    note = get_note(db, note_id)
    return repositories.delete(db, note)
