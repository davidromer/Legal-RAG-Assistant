from pypdf import PdfReader
from docx import Document as DocxDocument

def extraer_texto_pdf(ruta: str) -> list[tuple[int, str]]:
    lector = PdfReader(ruta)
    paginas = []
    for numero, pagina in enumerate(lector.pages, start=1):
        texto = pagina.extract_text() or ""
        if texto.strip():
            paginas.append((numero, texto))
    return paginas

def extraer_texto_docx(ruta: str) -> list[tuple[int, str]]:
    doc = DocxDocument(ruta)
    texto_completo = "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    # DOCX no trae paginación nativa: se trata como una sola "página lógica"
    return [(1, texto_completo)]

def extraer_texto(ruta: str, extension: str) -> list[tuple[int, str]]:
    if extension == ".pdf":
        return extraer_texto_pdf(ruta)
    if extension == ".docx":
        return extraer_texto_docx(ruta)
    raise ValueError(f"Formato no soportado: {extension}")