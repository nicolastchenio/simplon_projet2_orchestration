# tutoriel projet2 orchestration #

ATTENTION : suite a des probleme de version avec python 3.13 j ai du passer en cours de developpement en python 3.11

## phase A ##
### Étape 1 — Vérifier la structure du projet ###
#### Créer la structure suivante dans app_api : ####
```
app_api
│
├── main.py
├── pyproject.toml
├── uv.lock
│
├── models
│   ├── __init__.py
│   └── models.py
│
├── modules
│   ├── __init__.py
│   ├── connect.py
│   └── crud.py
│
├── maths
│   ├── __init__.py
│   └── mon_module.py
│
└── data
    └── moncsv.csv
```

Créer aussi :

```
tests
 ├── test_api.py
 └── test_math_csv.py

 ```

Actions fait :
1. renommer dossier app en app_api
2. Crée manuellement pyproject.toml dans app_api avec un contenu minimal pour l’API (comme demandé dans ton sujet) :
```
[project]
name = "app_api"
version = "0.1.0"

dependencies = [
    "fastapi>=0.135.1",
    "uvicorn>=0.41.0",
    "sqlalchemy>=2.0.48",
    "pydantic>=2.12.5",
    "pandas>=3.0.1",
    "pytest>=9.0.2",
]

[tool.pytest.ini_options]
pythonpath = ["."]
testpaths = ["tests"]
```
Ensuite, dans app_api, faire : ```uv sync```
Cela créera uv.lock et, si .venv local n’existe pas, un .venv local pour l’API => le supprimer car on en a pas besoin

3. Renommer ton ancien dossier modules en maths
4. Créer un nouveau dossier modules
5. Créer un nouveau dossier data pour y mettre le fichier moncsv.csv
6. Créer un nouveau dossier models
7. creation ou modification des fichiers :

- models/models.py
```
from pydantic import BaseModel
from typing import List, Optional

class DataInput(BaseModel):
    a: float
    b: float

class DataOutput(BaseModel):
    result: float

class CSVData(BaseModel):
    data: list
```

- modules/connect.py
```
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
```

- modules/crud.py
```
import pandas as pd

def save_csv_to_db(csv_path: str) -> pd.DataFrame:
    """Simule une sauvegarde dans la BDD avec pandas (Phase A)."""
    df = pd.read_csv(csv_path)
    return df

def read_csv_from_db(csv_path: str) -> pd.DataFrame:
    """Simule la récupération depuis la BDD avec pandas."""
    df = pd.read_csv(csv_path)
    return df
```

Pour Phase A, on reste sur CSV. Plus tard, on remplacera par des opérations SQL réelles.

- main.py (app_api/main.py)
```
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
```

Ne pas oublier de créer les fichiers __init.py respectifs


Explications

models.py → pour futurs modèles Pydantic, actuellement simple.
connect.py → prépare SQLite (Phase A on l’utilise pas encore, juste simulation).
crud.py → simule les opérations avec CSV.
main.py → routes FastAPI :
- POST /data → sauvegarde CSV
- GET /data → récupère CSV
-  GET /math → teste les fonctions de mon_module.py et compte les lignes du CSV

#### creation de la structure : ####

```
tests
 ├── test_api.py
 └── test_math_csv.py
```

la structure existe deja il faut juste un second fichier de tests, test_api.py, pour vérifier le fonctionnement de ton API FastAPI (routes /data et /math).

```
from fastapi.testclient import TestClient
from app_api.main import app

client = TestClient(app)

CSV_PATH = "app_api/data/moncsv.csv"

def test_get_data():
    """Test GET /data route."""
    response = client.get("/data")
    assert response.status_code == 200
    json_data = response.json()
    assert "data" in json_data
    assert isinstance(json_data["data"], list)

def test_post_data():
    """Test POST /data route."""
    response = client.post("/data")
    assert response.status_code == 200
    json_data = response.json()
    assert "data" in json_data
    assert "lignes sauvegardées" in json_data["message"]

def test_math_route():
    """Test GET /math route."""
    response = client.get("/math")
    assert response.status_code == 200
    json_data = response.json()
    # Vérifie les clés
    for key in ["add", "sub", "square", "rows_in_csv"]:
        assert key in json_data
```

Explications :
- TestClient FastAPI → permet de tester l’API sans la lancer dans un serveur réel.
- test_get_data → récupère les données du CSV via la route /data.
- test_post_data → simule la sauvegarde des données via /data.
- test_math_route → vérifie que les fonctions du module métier et print_data fonctionnent via /math.

### Étape 2  — Frontend Streamlit ###
#### creation de la structure : ####
```
app_front/
├── main.py           # point d’entrée Streamlit
├── pyproject.toml    # dépendances front (streamlit, pandas)
├── uv.lock           # créé après uv sync
├── pages/
│   ├── 0_insert.py   # page pour saisir les données
│   └── 1_read.py     # page pour afficher les données
```
1. creation des dossiers
2. creation des fichiers du dossiers "pages" :
- 0_insert.py

```
import streamlit as st
import requests
import os
import pandas as pd

# Récupération de l'hôte de l'API
API_HOST = os.getenv("API_HOST", "127.0.0.1")
API_URL = f"http://{API_HOST}:8000/data"

st.title("Insertion de données")

st.write("Ajouter des données via l'API.")

name = st.text_input("Nom")
value = st.number_input("Valeur", min_value=0)

if st.button("Envoyer"):
    try:
        payload = {"name": name, "value": value}
        response = requests.post(API_URL, json=payload)

        if response.status_code == 200:
            data = response.json()
            st.success(data["message"])
        else:
            st.error("Erreur API")

    except Exception as e:
        st.error(f"Erreur : {e}")
```

- 1_read.py

```
import streamlit as st
import requests
import pandas as pd
import os

# Récupération de l'hôte de l'API
API_HOST = os.getenv("API_HOST", "127.0.0.1")
API_URL = f"http://{API_HOST}:8000/data"

st.title("Lecture des données")
st.write("Récupération des données depuis l'API.")

if st.button("Afficher les données"):
    try:
        response = requests.get(API_URL)

        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data.get("data", []))
            st.success(data.get("message", "Données récupérées"))
            st.dataframe(df)
        else:
            st.error("Erreur API")

    except Exception as e:
        st.error(f"Erreur : {e}")
```
3. creation du fichier main.py

```
import streamlit as st

st.title("Frontend Streamlit")

st.write("Application de démonstration pour l'API FastAPI.")

st.write("Utilisez le menu de gauche pour :")
st.write("- Insérer des données")
st.write("- Lire les données")
```

4. creation du fichier pyproject.toml
```
cd app_front
uv init
uv add streamlit requests pandas
uv sync
```

note uv sync ne creer pas le fichier uv.lock dans le dossier aap_front => car il utilise celui quin est a la racine du projet

### Étape 3  — Verification ###

ayant fait des test j ai eu des probleme j ai donc :
supprimer pyproject.toml /  uv.lock / .venv a la racine du projet
Puis travailler service par service.
#### Vérifier que l’API fonctionne ####

Pour l’API:
```
cd app_api
uv sync
uv run uvicorn main:app --reload
```

- Ouvrir dans le navigateur :
http://127.0.0.1:8000/docs
test ok 

- Si main.py contient un endpoint /, tester :
http://127.0.0.1:8000
j ai => {"detail":"Not Found"}
signifie simplement que tu n’as pas défini de route / dans ton API FastAPI.
FastAPI fonctionne uniquement avec les routes que tu déclares explicitement.
=> dans app_api > main.py j ai rajouter :
```
@app.get("/")
def root():
    return {"message": "API opérationnelle"}
```

- Routes à tester :
GET /data => http://127.0.0.1:8000/data
POST /data => http://127.0.0.1:8000/data
GET /math => http://127.0.0.1:8000/math

j avais ce message => {"message":"API opérationnelle"}
donc j ai du :

dans app_api > main.py
j avais
CSV_PATH = "app_api/data/moncsv.csv
j ai remplacé par
CSV_PATH = "data/moncsv.csv"

Pour tester le POST /data, tu as plusieurs options :
- Via Swagger / OpenAPI Docs
Va sur http://127.0.0.1:8000/docs
Trouve POST /data
Clique sur Try it out
Clique sur Execute
La réponse apparaîtra en bas, avec le JSON renvoyé par ton endpoint (message + data)

-Via curl dans le terminal
curl -X POST http://127.0.0.1:8000/data
Tu recevras le JSON directement dans la console.

#### Vérifier que streamlit fonctionne ####

Pour le front :
```
cd app_front
uv sync
uv run streamlit run main.py
```

j ai eu un probleme j ai du Depuis app_front :
```
uv add "altair>=4.2.0,<5"
uv sync
```
et j ai du changer de version de python => passer de 3.13 a 3.11.2
puis 
1. Supprimer l'ancien .venv si nécessaire
rmdir /s /q .venv

2. Créer un nouveau venv avec Python 3.11
py -3.11 -m venv .venv

3. Activer le venv
.venv\Scripts\activate

4. Vérifier la version
python --version

Après ça, python --version doit afficher Python 3.11.x. Ensuite tu pourras faire :

```
uv sync
uv run streamlit run main.py
```

note personnelle:
j ai du faire la meme chose pour le dossier app_api apres

teste stremalit fait
- http://localhost:8501
- read
- insert

#### Vérifier que Vérifier les tests API fonctionne ####
j ai du :

```
cd app_api
.venv\Scripts\activate
uv add pytest
uv add pytest-asyncio  # si tu veux gérer des tests asynchrones avec FastAPI
uv sync
```
Depuis la racine du projet ou depuis app_api (en fonction du PYTHONPATH) :

```
set PYTHONPATH=.
pytest tests/ -v
```
j ai une erreur et j ai du 

```
cd app_api
.venv\Scripts\activate
uv add httpx
uv sync

```

pour tester executer la commande :
Aller a à la racine :
```
cd C:\Users\Apprenant\Desktop\SIMPLON METROPOLE\simplon_projet2_orchestration
```

Active l’environnement Python de l’API :
```
app_api\.venv\Scripts\activate
```

Lance pytest sur le dossier tests :
```
set PYTHONPATH=app_api
python -m pytest tests/ -v
```

## phase B ##
### Variables d’environnement et hygiène ###
1. Créer un fichier .env dans la racine du projet (ou dans app_api) pour stocker les paramètres sensibles, par exemple :
```
# .env
API_HOST=127.0.0.1
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=mydb
POSTGRES_PORT=5432
```

2. Créer .env.example (version template à partager sur GitHub) :
```
# .env.example
API_HOST=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=
POSTGRES_PORT=
```
3. Mettre à jour ton code pour utiliser ces variables :
- Dans app_api/modules/connect.py :
```
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = (
    f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:"
    f"{os.getenv('POSTGRES_PASSWORD')}@db:{os.getenv('POSTGRES_PORT', 5432)}/"
    f"{os.getenv('POSTGRES_DB')}"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```
- Pour le front (app_front/0_insert.py et 1_read.py) :
```
API_HOST = os.getenv("API_HOST", "127.0.0.1")
API_URL = f"http://{API_HOST}:8000/data"
```

- Mettre .env et .venv dans .gitignore et .dockignore pour éviter de versionner les secrets ou les environnements locaux.

