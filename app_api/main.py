from fastapi import FastAPI
import pandas as pd
from maths.mon_module import add, sub, square, print_data
from modules import crud
import os

app = FastAPI(title="API Phase A")

BASE_DIR = os.path.dirname(__file__)
CSV_PATH = os.path.join(BASE_DIR, "data", "moncsv.csv")
# CSV_PATH = "data/moncsv.csv"

@app.get("/")
def root():
    return {"message": "API opérationnelle"}

@app.post("/data")
def save_data():
    df = crud.save_csv_to_db(CSV_PATH)
    return {"message": f"{len(df)} lignes sauvegardées", "data": df.to_dict(orient="records")}

@app.get("/data")
def get_data():
    df = crud.read_csv_from_db(CSV_PATH)
    return {"message": f"{len(df)} lignes récupérées", "data": df.to_dict(orient="records")}

@app.get("/math")
def test_math():
    results = {
        "add": add(2,3),
        "sub": sub(5,2),
        "square": square(4)
    }
    df = pd.read_csv(CSV_PATH)
    n_rows = print_data(df)
    results["rows_in_csv"] = n_rows
    return results