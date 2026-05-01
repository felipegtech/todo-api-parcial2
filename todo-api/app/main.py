from fastapi import FastAPI
from app.database import Base, engine
from app.routes import router

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Todo API - Parcial 2 - Felipe Gomez Daza",
    description="API para gestionar tareas usando el framework FastAPI y base de datos PostgreSQL.)",
    version="1.0.0",
)


app.include_router(router)


@app.get("/", tags = ["Health"])
def health_check():
    return {
        "status": "ok",
        "message": "Todo el sistema API esta funcionando como se debe",
        "docs": "/docs"
    }