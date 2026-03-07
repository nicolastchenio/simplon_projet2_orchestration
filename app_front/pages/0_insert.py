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