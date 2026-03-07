# modules/crud.py
from sqlalchemy import create_engine, text
import pandas as pd
import os

DATABASE_URL = os.getenv("DATABASE_URL")  # à définir dans .env

engine = create_engine(DATABASE_URL, echo=False)


def save_value_to_db(value: float):
    """Insère une ligne dans la table data."""
    with engine.begin() as conn:
        conn.execute(
            text("INSERT INTO data(value) VALUES (:value)"),
            {"value": value}
        )


def read_data_from_db() -> pd.DataFrame:
    """Lit toutes les données depuis la table data."""
    with engine.connect() as conn:
        df = pd.read_sql("SELECT * FROM data", conn)
    return df


def init_db():
    """Créer la table si elle n'existe pas."""
    with engine.begin() as conn:
        conn.execute(
            text("""
                CREATE TABLE IF NOT EXISTS data (
                    id SERIAL PRIMARY KEY,
                    value FLOAT NOT NULL
                )
            """)
        )