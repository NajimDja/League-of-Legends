import streamlit as st

# Config de la page
st.set_page_config(
    page_title="Application League of Legends",
    page_icon="images\League-of-Legends-Embleme-650x366.webp",
    layout="wide",  # ou "centered"
    initial_sidebar_state="expanded"
)

home_page = st.Page("pages/home_page.py", default=True, title="Home page", icon="🏠")
champions_page = st.Page("pages/champions.py", title="Champions", icon="🛡️")
joueur_page = st.Page("pages/joueur.py", title="Joueur", icon="👤")
# live_page = st.Page("pages/live.py", title="Streaming", icon="📹")

pg = st.navigation([home_page, champions_page, joueur_page], position='top')
pg.run()