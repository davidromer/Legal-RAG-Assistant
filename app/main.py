import logging
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi import FastAPI
from app.db.connection import Base, engine, habilitar_pgvector
from app.db.models import Document, Chunk
from app.api import documents, chat
from app.core.logging import configurar_logging

logger = logging.getLogger("legal_rag")

configurar_logging()
habilitar_pgvector()
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Legal RAG Assistant")

app.include_router(documents.router)
app.include_router(chat.router)

@app.exception_handler(Exception)
async def manejador_global(request: Request, exc: Exception):
    logger.error(f"Error no controlado en {request.url.path}: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Ocurrió un error interno procesando la solicitud"},
    )