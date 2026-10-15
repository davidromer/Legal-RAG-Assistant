from fastapi import Header, HTTPException, status
from app.core.config import settings

def verificar_api_key(x_api_key: str = Header(...)) -> None:
    if x_api_key != settings.internal_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key inválida",
        )