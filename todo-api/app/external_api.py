# Cliente para Api Externa jSONPlaceholder que se usarA para obtener usuarios y posts de la api.
import httpx 
from fastapi import HTTPException, status


BASE_URL = "https://jsonplaceholder.typicode.com"
TIMEOUT = 10.0

client = httpx.Client(base_url=BASE_URL, timeout=TIMEOUT)

def _get(path: str):
    """Realiza una solicitud GET a la api Jsonplaceholder."""
    try:
        with httpx.Client(timeout=TIMEOUT) as client:
            response = client.get(f"{BASE_URL}{path}")
            response.raise_for_status()  
            return response.json()
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Tiempo de espera agotado al contactar JSONPlaceholder",
        )
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=f"Error desde API externa: {exc.response.text}",
        )
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Fue imposible conectar con JSONPlaceholder: {str(exc)}",
        )


def get_users():
    return _get("/users")


def get_posts():
    return _get("/posts")


def get_post(post_id: int):
    return _get(f"/posts/{post_id}")
