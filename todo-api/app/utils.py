from datetime import datetime, timezone

def utc_now() -> datetime:
    """Retorna datetime actual en UTC. Útil para los tests."""
    return datetime.now(timezone.utc)


def format_error(detail: str, code: str = "ERROR") -> dict:
    """formatea ese error para que sea coherente con la respuesta de error de FastAPI."""
    return {"error": {"code": code, "detail": detail}}