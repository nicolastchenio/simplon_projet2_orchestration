import streamlit as st
import requests
import os

# Récupération de l'hôte de l'API
API_HOST = os.getenv("API_HOST", "127.0.0.1")
API_URL = f"http://{API_HOST}:8000/data"

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