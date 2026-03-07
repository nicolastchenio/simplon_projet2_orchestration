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