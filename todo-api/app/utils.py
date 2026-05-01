from datetime import datetime, timezone


def utc_now() -> datetime:
    """Retorna datetime actual en UTC. Útil para tests y seeders."""
    return datetime.now(timezone.utc)


def format_error(detail: str, code: str = "ERROR") -> dict:
    """Formato estándar de error para respuestas consistentes."""
    return {"error": {"code": code, "detail": detail}}