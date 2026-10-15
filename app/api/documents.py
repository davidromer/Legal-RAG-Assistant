import os, shutil, uuid
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.connection import get_db
from app.db.models import Document, Chunk
from app.services import ingestion, chunking, embeddings

router = APIRouter(prefix="/documents", tags=["Documents"])
EXTENSIONES_VALIDAS = {".pdf", ".docx"}

@router.post("")
def subir_documento(archivo: UploadFile = File(...), db: Session = Depends(get_db)):
    extension = os.path.splitext(archivo.filename)[1].lower()
    if extension not in EXTENSIONES_VALIDAS:
        raise HTTPException(status_code=400, detail="Solo se aceptan PDF o DOCX")

    document_id = str(uuid.uuid4())
    os.makedirs("data", exist_ok=True)
    ruta_temporal = f"data/{document_id}{extension}"
    with open(ruta_temporal, "wb") as buffer:
        shutil.copyfileobj(archivo.file, buffer)

    paginas = ingestion.extraer_texto(ruta_temporal, extension)
    fragmentos = chunking.dividir_en_chunks(paginas)

    db.add(Document(id=document_id, filename=archivo.filename))

    vectores = embeddings.generar_embeddings_lote([f["content"] for f in fragmentos])
    for fragmento, vector in zip(fragmentos, vectores):
        db.add(Chunk(
            id=str(uuid.uuid4()), document_id=document_id,
            content=fragmento["content"], page=fragmento["page"], embedding=vector,
        ))

    db.commit()
    return {"document_id": document_id, "filename": archivo.filename, "chunks_creados": len(fragmentos)}