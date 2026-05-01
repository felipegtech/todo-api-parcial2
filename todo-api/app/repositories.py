from typing import List, Optional

from sqlalchemy.orm import Session

from app.models import Note
from app.schemas import NoteCreate, NoteUpdate


def get_all(db: Session) -> List[Note]:
    return db.query(Note).order_by(Note.created_at.desc()).all()


def get_by_id(db: Session, note_id: int) -> Optional[Note]:
    return db.query(Note).filter(Note.id == note_id).first()


def create(db: Session, data: NoteCreate) -> Note:
    note = Note(
        title=data.title,
        content=data.content,
        completed=data.completed,
    )
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


def update(db: Session, note: Note, data: NoteUpdate) -> Note:
    if data.title is not None:
        note.title = data.title
    if data.content is not None:
        note.content = data.content
    if data.completed is not None:
        note.completed = data.completed
    db.commit()
    db.refresh(note)
    return note


def delete(db: Session, note: Note) -> Note:
    db.delete(note)
    db.commit()
    return note
