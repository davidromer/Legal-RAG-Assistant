from sqlalchemy.orm import Session
from app.db.models import Chunk, Document
from app.services.embeddings import generar_embedding
from app.core.config import settings
from sqlalchemy import func, text

def buscar_chunks_relevantes(
    db: Session, pregunta: str, document_id: str | None = None, k: int | None = None,
) -> list[Chunk]:
    vector_pregunta = generar_embedding(pregunta)
    consulta = db.query(Chunk).order_by(Chunk.embedding.cosine_distance(vector_pregunta))
    if document_id:
        consulta = consulta.filter(Chunk.document_id == document_id)
    return consulta.limit(k or settings.top_k).all()

def busqueda_hibrida(
    db: Session, pregunta: str, document_type: str | None = None,
    jurisdiction: str | None = None, k: int = 5,
) -> list[Chunk]:
    vector_pregunta = generar_embedding(pregunta)

    # distancia vectorial normalizada + ranking de texto completo, combinados con peso
    consulta = db.query(Chunk).join(Document).filter(
        func.to_tsvector("spanish", Chunk.content).op("@@")(func.plainto_tsquery("spanish", pregunta))
        | text("1=1")   # deja pasar también los que solo matchean por vector
    ).order_by(Chunk.embedding.cosine_distance(vector_pregunta))

    if document_type:
        consulta = consulta.filter(Document.document_type == document_type)
    if jurisdiction:
        consulta = consulta.filter(Document.jurisdiction == jurisdiction)

    return consulta.limit(k).all()