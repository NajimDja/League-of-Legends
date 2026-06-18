import streamlit as st

# Config de la page
st.set_page_config(
    page_title="Application League of Legends",
    page_icon="images\League-of-Legends-Embleme-650x366.webp",
    layout="wide",  # ou "centered"
    initial_sidebar_state="expanded"
)

# Titre home page
st.title("Dashboard League of Legends", text_alignment='center')

# Description du dashboard
st.markdown(
    "Ce Dashboard Streamlit permet de visualiser des données de la base de données League of Legends" \
" construite à partir de l'extraction et de la transformation des données récupérées à partir d'appels de l'API de RIOT Games." \
" Le but est de permettre aux joueurs dont leur compte est enregistré en base, de pouvoir visualiser l'historique de leurs parties jouées." \
" Ils pourront observer des métriques multiples permettant l'analyse stratégique et orienté data de leurs parties. Par exemple :" \
"\n- **KDA (Kill / Death / Assist)** : ratio de kills, morts et assistances effectuées *(= (K+A)/D )*." \
"\n- **Gold/minute moyen** : nombre de gold gagnés en moyenne par minute lors d'une game." \
"\n- **Win rate** : ratio de partie gagnées." \
"\n- **CS par minute moyen** : nombre de sbires/monstres tués en moyenne par minute.", 
text_alignment='justify')

st.header("Joueurs disponibles")

# Connexion automatique via secrets.toml
conn = st.connection("postgres", type="sql")

# Requête en lecture (retourne un DataFrame)
df = conn.query("SELECT * FROM account;", ttl="10m")
st.dataframe(df)