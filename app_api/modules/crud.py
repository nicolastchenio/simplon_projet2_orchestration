import pandas as pd

def save_csv_to_db(csv_path: str) -> pd.DataFrame:
    """Simule une sauvegarde dans la BDD avec pandas (Phase A)."""
    df = pd.read_csv(csv_path)
    return df

def read_csv_from_db(csv_path: str) -> pd.DataFrame:
    """Simule la récupération depuis la BDD avec pandas."""
    df = pd.read_csv(csv_path)
    return df