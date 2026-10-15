import json
from app.db.connection import SessionLocal
from app.services import retrieval, generation

def evaluar(ruta_dataset: str = "tests/eval_dataset.json") -> dict:
    preguntas = json.load(open(ruta_dataset, encoding="utf-8"))
    db = SessionLocal()
    aciertos_retrieval = 0
    respuestas_fundamentadas = 0

    for caso in preguntas:
        chunks = retrieval.buscar_chunks_relevantes(db, caso["question"])
        documentos_recuperados = {c.document_id for c in chunks}

        if caso["expected_document_id"] in documentos_recuperados:
            aciertos_retrieval += 1

        resultado = generation.generar_respuesta(caso["question"], chunks)
        if caso["expected_answer_contains"].lower() in resultado["answer"].lower():
            respuestas_fundamentadas += 1

    total = len(preguntas)
    return {
        "retrieval_hit_rate": round(aciertos_retrieval / total, 3),
        "answer_faithfulness": round(respuestas_fundamentadas / total, 3),
        "total_preguntas": total,
    }

if __name__ == "__main__":
    print(evaluar())