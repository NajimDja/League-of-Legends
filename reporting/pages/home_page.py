import streamlit as st
import pandas as pd

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

st.markdown(
    "Plusieurs pages sont disponible sur l'application :" \
    "\n- **Champions** : cette page concerne les informations sur les champions du jeu, comme leurs statistiques et capacités." \
    "\n- **Joueur** : informations sur les joueurs dont leur compte est enregistré en base, comme par exemple leur maîtise des champions", 
    text_alignment='justify'
    )


nom_table = [
    "account",
    "challenges",
    "champion",
    "champion_info",
    "champion_mastery",
    "champion_passive",
    "champion_spells",
    "champion_stats",
    "champion_stats_up",
    "champion_version",
    "game_capacites",
    "game_communication",
    "game_damage",
    "game_economie",
    "game_farming",
    "game_fight",
    "game_info",
    "game_objectives",
    "game_performance",
    "game_player",
    "game_player_info",
    "game_runes",
    "items",
    "patch",
    "player_id_map",
    "queue",
    "runes",
    "summoner",
    "summoner_spells"
]

description_table = [
    "Référence les comptes des joueurs enregistrés en base",
    "Avancement d'un joueur dans les challenges du jeu",
    "Répertorie tout les champions du jeu",
    "Aperçu général d'un champion",
    "Niveau de maîtrise de chaque champion pour un joueur enregistré en base",
    "Informations concernant le passif d'un champion",
    "Informations concernant les spells d'un champion",
    "Informations sur les statistiques de base d'un champion",
    "Informations sur les statistiques de monter de niveau d'un champion",
    "Référence les différentes version d'un champion dans jeu en fonction des patch",
    "Capacités utilisées en game (nombre par spell, summoners...)",
    "Information sur la communication et la vision en jeu (pings, wards...)",
    "Information sur les dégâts fait/tanker dans la game (physique, magique...)",
    "Information sur les golds et items pris dans une game",
    "Information sur le farming in game (CS tués, avantage sur la lane...)",
    "Information sur les combats in game (kill, mort, assit, aces...)",
    "Contient les informations générales d'un game (id, timestamp, durée...)",
    "Information sur les objectifs globaux in game (drakes, baron, tourelles...)",
    "Performance in game (win, temps de jeu réel, tourelle perdue, ff...)",
    "Table de relation entre les id des joueurs et une game",
    "Informations générales sur un joueur dans une game (champion, level, lane...)",
    "Information sur les runes sélectionnées in game",
    "Référence tout les items du jeu associé à une version de patch",
    "Référence les différents patchs",
    "Table de mapping d'un identifiant de compte d'un joueur",
    "Table de rank d'un joueur",
    "Référence les runes dans le jeu associé à une version de patch",
    "Information sur le profil d'un joeur",
    "Référence les summoners spells associé à une version de patch"
]

df = pd.DataFrame({
    "Nom de table": nom_table,
    "Description": description_table
})

st.header("Table disponibles en base de données")
st.markdown("Table disponibles dans la base de données, associées à leur description respective.")
st.dataframe(df, hide_index=True, key='df_bdd')