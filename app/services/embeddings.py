from openai import OpenAI
from app.core.config import settings

cliente = OpenAI(api_key=settings.openai_api_key)

def generar_embedding(texto: str) -> list[float]:
    respuesta = cliente.embeddings.create(model=settings.embedding_model, input=texto)
    return respuesta.data[0].embedding

def generar_embeddings_lote(textos: list[str]) -> list[list[float]]:
    respuesta = cliente.embeddings.create(model=settings.embedding_model, input=textos)
    return [item.embedding for item in respuesta.data]