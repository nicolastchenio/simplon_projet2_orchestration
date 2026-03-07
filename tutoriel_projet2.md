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

## phase C ##
### Orchestration Docker Compose ###
#### Étape C.1 — Préparer le docker-compose.yml pour le développement ####

- Crée un fichier docker-compose.yml à la racine du projet (si ce n’est pas déjà fait).
- Pour commencer, on va définir trois services : api, front, db
```
services:
  # -------------------- API --------------------
  api:
    build:
      context: ./app_api
    container_name: api_service
    env_file:
      - .env
    ports:
      - "${API_PORT}:8000"
    networks:
      - api-db
      - front-api
    depends_on:
      - db

  # -------------------- Frontend --------------------
  front:
    build:
      context: ./app_front
    container_name: front_service
    env_file:
      - .env
    ports:
      - "${FRONT_PORT}:8501"
    networks:
      - front-api
    depends_on:
      - api

  # -------------------- PostgreSQL --------------------
  db:
    image: postgres:15
    container_name: db_service
    env_file:
      - .env
    ports:
      - "${POSTGRES_PORT}:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
    networks:
      - api-db

# -------------------- Volumes --------------------
volumes:
  pgdata:

# -------------------- Networks --------------------
networks:
  front-api:
  api-db:
```

#### Étape C.2 — adapter le Front et l’API pour utiliser les noms des services Docker comme hôtes, plutôt que 127.0.0.1 ####
- app_front/pages/0_insert.py

```
import streamlit as st
import requests
import os

# URL de l'API dans Docker
API_URL = f"http://api:8000/data"

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
            st.error(f"Erreur API : {response.status_code}")

    except Exception as e:
        st.error(f"Erreur : {e}")
```

app_front/pages/1_read.py
```
import streamlit as st
import requests
import pandas as pd

# URL de l'API dans Docker
API_URL = f"http://api:8000/data"

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
            st.error(f"Erreur API : {response.status_code}")

    except Exception as e:
        st.error(f"Erreur : {e}")
```
#### Étape C.3 — creer les Dockerfile ###
- Dockerfile pour l’API (app_api/Dockerfile)
```
# Base image Python
FROM python:3.11-slim

# Copier uv depuis l’image officielle
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances
COPY pyproject.toml uv.lock /app/

# Installer les dépendances avec uv pip dans l’environnement système
RUN uv pip install --system --no-cache -r pyproject.toml

# Copier tout le code de l'API
COPY . /app

# Commande pour lancer l'API
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

- Dockerfile pour le Frontend (app_front/Dockerfile)
```
# Base image Python
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier uv depuis l'image officielle
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copier les fichiers de dépendances
COPY pyproject.toml uv.lock /app/

# Installer les dépendances avec uv pip
RUN uv pip install --system --no-cache -r pyproject.toml

# Copier tout le code du front
COPY . /app

# Exposer le port
EXPOSE 8501

# Commande pour lancer Streamlit
# --server.headless=true à Streamlit pour éviter les alertes de sécurité et permettre le fonctionnement dans un conteneur
CMD ["uv", "streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
```

#### Étape C.4 — tester le docker-compose en local ###
pour vérifier que :
- Le front voit l’API
- L’API peut accéder à PostgreSQL
- Les données persistent via le volume pgdata

Penser a demarrer docker sur son ordinateur en local.

1. Nettoyer l’existant
- Arrête tous les conteneurs en cours (si tu en as) :
```
docker-compose down
```

- Supprime les volumes temporaires pour être sûr de repartir propre :
```
docker volume ls 
docker volume rm simplon_projet2_orchestration_pgdata
```

PENSER AUSSI A Supprimer les .venv de app_front et app_api car pas besoin avec docker

2. Lancer Docker Compose
Dans le dossier de ton projet (où est ton docker-compose.yml) :
```
docker-compose up --build
```

Docker va builder l’API et le front
Docker va créer le conteneur PostgreSQL et le volume pour persister les données
Les réseaux front-api et api-db seront créés

À ce stade, regarde les logs pour t’assurer que :

L’API démarre (Uvicorn running on http://0.0.0.0:8000)
PostgreSQL démarre sans erreur (database system is ready to accept connections)
Streamlit démarre (You can now view your Streamlit app in your browser)

3. Tester la communication Front → API
- Ouvre ton navigateur :
http://localhost:8501


- Teste la page d’insertion (0_insert) : ajoute une valeur, clique sur Envoyer.
-Teste la page de lecture (1_read) : récupère les données et vérifie que ton CSV / POST fonctionne via l’API.

note : il y avait des bug j ai donc du modifier le code notamment pour passer avec la base de donnee et non plus avec le document csv  :

app_api > main.py :
```
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
```

app_front > 0_insert.py :
```
import streamlit as st
import requests
import os

# URL de l'API dans Docker
API_URL = f"http://api:8000/data"

st.title("Insertion de données")
st.write("Ajouter des données via l'API.")

# L'utilisateur ne fournit que la valeur
value = st.number_input("Valeur", min_value=0)

if st.button("Envoyer"):
    try:
        # On envoie seulement la valeur, l'id sera géré côté backend
        payload = {"value": value}
        response = requests.post(API_URL, json=payload)

        if response.status_code == 200:
            data = response.json()
            st.success(data["message"])
        else:
            st.error(f"Erreur API ({response.status_code})")

    except Exception as e:
        st.error(f"Erreur : {e}")
```

app_front > 1_read.py :
```
import streamlit as st
import requests
import pandas as pd

# URL de l'API dans Docker
API_URL = "http://api:8000/data"

st.title("Lecture des données")
st.write("Récupération des données depuis l'API.")

# bouton de rafraîchissement
if st.button("Actualiser les données"):
    st.experimental_rerun()

try:
    response = requests.get(API_URL)

    if response.status_code == 200:
        data = response.json()

        df = pd.DataFrame(data.get("data", []))

        st.success(data.get("message", "Données récupérées"))

        if not df.empty:
            st.dataframe(df)
        else:
            st.warning("Aucune donnée disponible")

    else:
        st.error(f"Erreur API : {response.status_code}")
        st.text(response.text)

except requests.exceptions.RequestException as e:
    st.error(f"Erreur de connexion à l'API : {e}")
```

modules > crud.py :

```
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
```

app_api > pyproject.toml :

```
[project]
name = "app_api"
version = "0.1.0"
requires-python = ">=3.11"

dependencies = [
    "fastapi>=0.135.1",
    "uvicorn>=0.41.0",
    "sqlalchemy>=2.0.48",
    "pydantic>=2.12.5",
    "pandas>=3.0.1",
    "pytest>=9.0.2",
    "pytest-asyncio>=1.3.0",
    "httpx>=0.28.1",
    "psycopg2-binary>=2.9.7"
]

[tool.pytest.ini_options]
pythonpath = ["."]
testpaths = ["tests"]
```

.env :

```
# Database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=mydb
POSTGRES_PORT=5432

# API & Front
API_PORT=8000
FRONT_PORT=8501
API_HOST=api

# SQLAlchemy connection string
DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/mydb

```

4. Tester la persistance des données
- Ajoute quelques données via le front.
- Arrête les conteneurs :
```
docker-compose down
```

- Relance les conteneurs :
```
docker-compose up
```

Vérifie dans le front que les données ajoutées sont toujours là.
Si oui, le volume pgdata fonctionne correctement et PostgreSQL conserve les données.

