from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# SQLite en local pour Phase A
DATABASE_URL = "sqlite:///./app_api/data/data.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()