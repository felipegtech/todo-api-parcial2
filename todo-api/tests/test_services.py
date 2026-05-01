"""
tests/test_services.py — Pruebas de lógica de negocio (unit tests).
"""
import pytest
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app import services
from app.schemas import NoteCreate, NoteUpdate

engine_test = create_engine("sqlite:///./test_services.db", connect_args={"check_same_thread": False})
TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)


@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine_test)
    session = TestingSession()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine_test)


def test_create_and_get(db):
    note = services.create_note(db, NoteCreate(title="Test"))
    assert note.id is not None
    fetched = services.get_note(db, note.id)
    assert fetched.title == "Test"


def test_get_nonexistent_raises_404(db):
    with pytest.raises(HTTPException) as exc:
        services.get_note(db, 9999)
    assert exc.value.status_code == 404


def test_update_note(db):
    note = services.create_note(db, NoteCreate(title="Antes"))
    updated = services.update_note(db, note.id, NoteUpdate(title="Después", completed=True))
    assert updated.title == "Después"
    assert updated.completed is True


def test_delete_note(db):
    note = services.create_note(db, NoteCreate(title="Eliminar"))
    services.delete_note(db, note.id)
    with pytest.raises(HTTPException):
        services.get_note(db, note.id)
