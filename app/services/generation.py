from openai import OpenAI
from app.core.config import settings

cliente = OpenAI(api_key=settings.openai_api_key)

PROMPT_SISTEMA = """Eres un asistente legal que responde EXCLUSIVAMENTE con base en los
fragmentos de documentos proporcionados. Si la evidencia es insuficiente, responde
exactamente: "No encontré información suficiente en los documentos proporcionados."
Cada afirmación debe citar su fuente entre corchetes, ej: [contrato.pdf, pág. 12]."""

def construir_contexto(chunks) -> str:
    partes = [f"[{c.document.filename}, pág. {c.page}]\n{c.content}" for c in chunks]
    return "\n\n---\n\n".join(partes)

def generar_respuesta(pregunta: str, chunks) -> dict:
    if not chunks:
        return {
            "answer": "No encontré información suficiente en los documentos proporcionados.",
            "sources": [],
        }

    contexto = construir_contexto(chunks)
    respuesta = cliente.chat.completions.create(
        model=settings.llm_model,
        messages=[
            {"role": "system", "content": PROMPT_SISTEMA},
            {"role": "user", "content": f"Contexto:\n{contexto}\n\nPregunta: {pregunta}"},
        ],
        temperature=0,
    )
    texto = respuesta.choices[0].message.content
    fuentes = [
        {"document": c.document.filename, "page": c.page, "section": c.section}
        for c in chunks
    ]
    return {"answer": texto, "sources": fuentes}