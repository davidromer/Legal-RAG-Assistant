import re
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.core.config import settings

def limpiar_texto(texto: str) -> str:
    texto = re.sub(r"-\n", "", texto)      # une palabras cortadas al final de línea
    texto = re.sub(r"\s+", " ", texto)      # colapsa espacios/saltos redundantes
    return texto.strip()

def dividir_en_chunks(paginas: list[tuple[int, str]]) -> list[dict]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        separators=["\n\n", "\n", ". ", " "],
    )
    chunks = []
    for numero_pagina, texto in paginas:
        texto_limpio = limpiar_texto(texto)
        for fragmento in splitter.split_text(texto_limpio):
            chunks.append({"content": fragmento, "page": numero_pagina})
    return chunks