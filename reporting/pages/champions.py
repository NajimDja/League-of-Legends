import streamlit as st

# Config de la page
st.set_page_config(
    page_title="Dashboard Champions",
    page_icon="images\League-of-Legends-Embleme-650x366.webp",
    layout="wide",  # ou "centered"
    initial_sidebar_state="expanded"
)

st.title("Dashboard des champions", text_alignment='center')

st.markdown(
    "On retrouve sur ce dashboard les données des champions, c'est à dire leurs statistiques de base, leurs spells, leur passif" \
    " et l'augmentation de chacune de leur statistique par niveau gagné. On retrouvera également certains KPI générals sur chaque champion" \
    " comme leur Winrate global, leur pourcentage de ban ou encore sur quelle lane où ils sont le plus joués."
)