from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def habilitar_pgvector() -> None:
    with engine.connect() as conexion:
        conexion.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        conexion.commit()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()