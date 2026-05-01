import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app

# Base de datos en memoria solo para tests
TEST_DB_URL = "sqlite:///./test.db"
engine_test = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)


def override_get_db():
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine_test)
    yield
    Base.metadata.drop_all(bind=engine_test)


client = TestClient(app)


# ── Tests CRUD ──────────────────────────────────────────────────────────────

def test_create_note():
    res = client.post("/api/notes", json={"title": "Estudiar FastAPI"})
    assert res.status_code == 201
    data = res.json()
    assert data["title"] == "Estudiar FastAPI"
    assert data["completed"] is False
    assert "id" in data
    assert "created_at" in data


def test_get_all_notes():
    client.post("/api/notes", json={"title": "Nota 1"})
    client.post("/api/notes", json={"title": "Nota 2"})
    res = client.get("/api/notes")
    assert res.status_code == 200
    assert len(res.json()) == 2


def test_get_note_by_id():
    created = client.post("/api/notes", json={"title": "Específica"}).json()
    res = client.get(f"/api/notes/{created['id']}")
    assert res.status_code == 200
    assert res.json()["title"] == "Específica"


def test_get_note_not_found():
    res = client.get("/api/notes/9999")
    assert res.status_code == 404


def test_update_note():
    created = client.post("/api/notes", json={"title": "Original"}).json()
    res = client.put(f"/api/notes/{created['id']}", json={"completed": True})
    assert res.status_code == 200
    assert res.json()["completed"] is True


def test_delete_note():
    created = client.post("/api/notes", json={"title": "Borrar"}).json()
    res = client.delete(f"/api/notes/{created['id']}")
    assert res.status_code == 200
    # Verificar que ya no existe
    res2 = client.get(f"/api/notes/{created['id']}")
    assert res2.status_code == 404


# ── Tests validaciones ──────────────────────────────────────────────────────

def test_create_note_empty_title():
    res = client.post("/api/notes", json={"title": ""})
    assert res.status_code == 422   # Unprocessable Entity


def test_create_note_content_too_long():
    res = client.post("/api/notes", json={"title": "ok", "content": "x" * 1001})
    assert res.status_code == 422
