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