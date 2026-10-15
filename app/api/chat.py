from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.connection import get_db
from app.schemas.requests import PreguntaRequest, RespuestaChat
from app.services import retrieval, generation

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("", response_model=RespuestaChat)
def preguntar(datos: PreguntaRequest, db: Session = Depends(get_db)):
    chunks = retrieval.buscar_chunks_relevantes(db, datos.question, datos.document_id)
    return generation.generar_respuesta(datos.question, chunks)