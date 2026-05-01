from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app import services
from app.database import get_db
from app.external_api import get_post, get_posts, get_users
from app.schemas import NoteCreate, NoteResponse, NoteUpdate


router = APIRouter(prefix="/api")


# ── Notas ──────────────────────────────────────────────────────────────────

@router.get(
    "/notes",
    response_model=List[NoteResponse],
    summary="Obtener todas las notas",
    tags=["Notes"],
)
def list_notes(db: Session = Depends(get_db)):
    return services.list_notes(db)


@router.get(
    "/notes/{note_id}",
    response_model=NoteResponse,
    summary="Obtener una nota por ID",
    tags=["Notes"],
)
def get_note(note_id: int, db: Session = Depends(get_db)):
    return services.get_note(db, note_id)


@router.post(
    "/notes",
    response_model=NoteResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una nueva nota",
    tags=["Notes"],
)
def create_note(data: NoteCreate, db: Session = Depends(get_db)):
    return services.create_note(db, data)


@router.put(
    "/notes/{note_id}",
    response_model=NoteResponse,
    summary="Actualizar una nota",
    tags=["Notes"],
)
def update_note(note_id: int, data: NoteUpdate, db: Session = Depends(get_db)):
    return services.update_note(db, note_id, data)


@router.delete(
    "/notes/{note_id}",
    response_model=NoteResponse,
    summary="Eliminar una nota",
    tags=["Notes"],
)
def delete_note(note_id: int, db: Session = Depends(get_db)):
    return services.delete_note(db, note_id)


# ── API Externa JSONPlaceholder ────────────────────────────────────────────

@router.get(
    "/external/users",
    summary="Usuarios desde JSONPlaceholder",
    tags=["External"],
)
def external_users():
    return get_users()


@router.get(
    "/external/posts",
    summary="Posts desde JSONPlaceholder",
    tags=["External"],
)
def external_posts():
    return get_posts()


@router.get(
    "/external/posts/{post_id}",
    summary="Post específico desde JSONPlaceholder",
    tags=["External"],
)
def external_post(post_id: int):
    return get_post(post_id)