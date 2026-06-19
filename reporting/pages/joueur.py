import streamlit as st

# Config de la page
st.set_page_config(
    page_title="Dashboard Joueur",
    page_icon="images\League-of-Legends-Embleme-650x366.webp",
    layout="wide",  # ou "centered"
    initial_sidebar_state="expanded"
)

st.title("Dashboard des joueurs", text_alignment='center')

st.markdown(
    "Dashboard des joueurs permettant de consulter leur statistiques et avancement général dans le jeu.",
    text_alignment='justify')

query_joueur = """
SELECT *
FROM account;
"""

conn = st.connection("postgres", type="sql")
df_joueur = conn.query(query_joueur, ttl="10m")
st.dataframe(df_joueur, hide_index=True, key='df_joueur')