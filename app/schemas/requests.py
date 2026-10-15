from pydantic import BaseModel

class PreguntaRequest(BaseModel):
    question: str
    document_id: str | None = None

class FuenteRespuesta(BaseModel):
    document: str
    page: int | None
    section: str | None

class RespuestaChat(BaseModel):
    answer: str
    sources: list[FuenteRespuesta]