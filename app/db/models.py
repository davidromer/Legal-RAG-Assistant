import datetime
from sqlalchemy import Column, String, Integer, Text, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from app.db.connection import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(String, primary_key=True)
    filename = Column(String, nullable=False)
    document_type = Column(String, nullable=True)   # "contrato", "sentencia"...
    jurisdiction = Column(String, nullable=True)     # "Colombia"
    uploaded_at = Column(DateTime, default=datetime.datetime.utcnow)

    chunks = relationship("Chunk", back_populates="document", cascade="all, delete-orphan")

class Chunk(Base):
    __tablename__ = "chunks"

    id = Column(String, primary_key=True)
    document_id = Column(String, ForeignKey("documents.id"), nullable=False)
    content = Column(Text, nullable=False)
    page = Column(Integer, nullable=True)
    section = Column(String, nullable=True)          # "Cláusula Quinta"
    embedding = Column(Vector(1536))
    metadata_json = Column(JSON, default=dict)

    document = relationship("Document", back_populates="chunks")