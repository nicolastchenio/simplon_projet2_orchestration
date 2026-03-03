# La version de python
FROM python:3.12-slim
# On récupère uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
# on crée un dossier pour l'application
WORKDIR /app
# On copie uniquement les fichiers de dépendances
COPY pyproject.toml uv.lock ./
# On installe les paquets (uv sync -> .venv)
RUN uv pip install --system -r pyproject.toml
# On copie le reste
COPY . .
# On exécute le code
CMD ["python", "app/main.py"]