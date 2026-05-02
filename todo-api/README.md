# Todo API - Felipe Gomez Daza

## 1. Descripción del proyecto
API RESTful para gestión de notas (To-Do List) desarrollada con FastAPI y PostgreSQL.
Implementa arquitectura en capas (Layered Architecture) con los principios SOLID.

**Stack tecnológico:**
- FastAPI — framework web
- PostgreSQL — base de datos
- SQLAlchemy — ORM
- Docker + Docker Compose — contenedores
- httpx — cliente HTTP para API externa

**Arquitectura:**
- `routes.py` — recibe peticiones HTTP (Controlador)
- `services.py` — lógica de negocio
- `repositories.py` — acceso a datos
- `models.py` — modelos de base de datos
- `schemas.py` — validación de datos

## 2. Requisitos del sistema
- Python 3.11+
- Docker y Docker Compose
- Git

## 3. Instalación y ejecución

### Con Docker
```bash
cp .env.example .env
docker-compose up --build
```

### Local
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 5000

## 6. Ejemplos de uso

### Crear nota
```bash
curl -X POST http://localhost:5000/api/notes \
  -H "Content-Type: application/json" \
  -d '{"title": "Estudiar FastAPI", "content": "Repasar SQLAlchemy"}'
```
**Response 201:**
```json
{
  "id": 1,
  "title": "Estudiar FastAPI",
  "content": "Repasar SQLAlchemy",
  "completed": false,
  "created_at": "2026-05-01T04:09:48Z",
  "updated_at": "2026-05-01T04:09:48Z"
}
```

### Error 404
```json
{"detail": "Nota con id=99 no encontrada"}
```

### Error 422 (validación)
```json
{"detail": [{"type": "missing", "loc": ["body", "title"], "msg": "Field required"}]}
```

## 7. Documentación interactiva
Swagger UI: http://localhost:5000/docs
