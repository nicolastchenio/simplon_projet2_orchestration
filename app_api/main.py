import os
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, Float, MetaData, Table, select
from sqlalchemy.orm import sessionmaker

from maths.mon_module import add, sub, square, print_data

# -------------------------
# Configuration FastAPI
# -------------------------
app = FastAPI(title="API avec PostgreSQL")

# -------------------------
# Base de données
# -------------------------
DATABASE_URL = os.getenv("DATABASE_URL")  # pris depuis le .env

engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Définition de la table "data"
data_table = Table(
    "data",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("value", Float, nullable=False)
)

# Création de la table si elle n'existe pas
metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

# -------------------------
# Modèle Pydantic
# -------------------------
class DataInput(BaseModel):
    value: float

# -------------------------
# Routes
# -------------------------
@app.get("/")
def root():
    return {"message": "API opérationnelle"}


@app.post("/data")
def save_data(data: DataInput):
    """Ajoute une nouvelle ligne dans PostgreSQL"""
    session = SessionLocal()
    try:
        insert_stmt = data_table.insert().values(value=data.value)
        session.execute(insert_stmt)
        session.commit()
        return {"message": "1 ligne ajoutée"}
    finally:
        session.close()


@app.get("/data")
def get_data():
    """Récupère toutes les lignes de PostgreSQL"""
    session = SessionLocal()
    try:
        select_stmt = select(data_table)
        result = session.execute(select_stmt)
        rows = [{"id": r.id, "value": r.value} for r in result]
        return jsonable_encoder({
            "message": f"{len(rows)} lignes récupérées",
            "data": rows
        })
    finally:
        session.close()


@app.get("/math")
def test_math():
    results = {
        "add": add(2,3),
        "sub": sub(5,2),
        "square": square(4)
    }

    # Compter le nombre de lignes en BDD
    session = SessionLocal()
    try:
        count = session.execute(select(data_table)).rowcount
        results["rows_in_db"] = count
    finally:
        session.close()

    return results