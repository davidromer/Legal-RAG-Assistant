from fastapi.testclient import TestClient
from app.main import app

cliente = TestClient(app)

def test_chat_sin_documentos_no_alucina():
    respuesta = cliente.post("/chat", json={"question": "¿Qué dice una cláusula que no existe?"})
    assert respuesta.status_code == 200
    cuerpo = respuesta.json()
    assert "No encontré información suficiente" in cuerpo["answer"]
    assert cuerpo["sources"] == []