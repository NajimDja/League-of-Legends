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

query_champion = """
SELECT 
    c.name as nom, 
    cv.title as titre, 
    cv.lore, 
    cv.tags as categorie, 
    cv.partype as ressource
FROM champion c
LEFT JOIN champion_version cv ON c.id = cv.champ_id
LEFT JOIN patch p ON cv.patch_id = p.id
WHERE p.is_latest = True;
"""

conn = st.connection("postgres", type="sql")
df_champion = conn.query(query_champion, ttl="10m")

st.header("Tableau des champions du jeu")
st.dataframe(df_champion, hide_index=True, key='df_champion')