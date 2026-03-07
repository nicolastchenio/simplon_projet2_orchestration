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
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]