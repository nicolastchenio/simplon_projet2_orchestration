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