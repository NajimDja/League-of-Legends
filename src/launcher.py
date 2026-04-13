from dotenv import load_dotenv
from sqlalchemy import create_engine, text, Table, MetaData, inspect
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert as pg_insert
import pandas as pd
import os

from db_gestion import Pipelines_db
from ddragon import pipeline_ddragon
from player import pipeline_new_player

load_dotenv()
database_url = os.getenv("DATABASE_URL")
engine = create_engine(database_url)
metadata = MetaData()
metadata.reflect(bind=engine)  # Charge toutes les tables depuis la DB


def main_ddragon(version : int = 0):

    pipe = Pipelines_db()

    print("Extraction et transformation des données en cours...")
    table_champion, table_champion_version, table_champ_passive, table_champ_info, table_champ_spells, table_champ_stats, table_champ_stats_up, table_runes, table_patch, table_item, table_summoner_spells = pipeline_ddragon(version=version)
    print("Extraction et transformation terminées")

    print("Chargement des données en base.")
    pipe.pipeline_upsert(table_name = "patch", df_upsert= table_patch)
    pipe.pipeline_upsert(table_name = "champion", df_upsert = table_champion)
    pipe.pipeline_upsert(table_name = "champion_version", df_upsert = table_champion_version)
    pipe.pipeline_upsert(table_name = "champion_info", df_upsert = table_champ_info)
    pipe.pipeline_upsert(table_name = "champion_passive", df_upsert = table_champ_passive)
    pipe.pipeline_upsert(table_name = "champion_spells", df_upsert = table_champ_spells)
    pipe.pipeline_upsert(table_name = "champion_stats", df_upsert = table_champ_stats)
    pipe.pipeline_upsert(table_name = "champion_stats_up", df_upsert = table_champ_stats_up)
    pipe.pipeline_upsert(table_name = "runes", df_upsert = table_runes)
    pipe.pipeline_upsert(table_name = "items", df_upsert = table_item)
    pipe.pipeline_upsert(table_name = "summoner_spells", df_upsert = table_summoner_spells)
    print("Chargement des données en base terminé.")


def main_player(gameName : str, tagLine : str):

    pipe = Pipelines_db()

    print("Extraction et transformation des données en cours...")
    df_account, games_data, df_summoner, df_challenges, df_champion_mastery, df_queue = pipeline_new_player(gameName=gameName, tagLine=tagLine)
    print("Extractions et transformations terminées")

    print("Chargement des données en base")
    pipe.pipeline_upsert(table_name = "account", df_upsert = df_account)
    pipe.pipeline_upsert(table_name = "summoner", df_upsert = df_summoner)
    pipe.pipeline_upsert(table_name = "champion_mastery", df_upsert = df_champion_mastery)
    pipe.pipeline_upsert(table_name = "queue", df_upsert = df_queue)

    for name in games_data:
        df = games_data[name]
        pipe.pipeline_upsert(table_name=name, df_upsert=df)
    
    pipe.pipeline_upsert(table_name = "challenges", df_upsert = df_challenges)

    print("Chargement des données en base terminé.")
    print("Processus d'intégration des données d'un joueur terminé.")


if __name__ == "__main__":
    
    print("Lancement du processus de récupération, traitement et chargement des données en base.\n")

    print(f"{'*'*20}\nPartie : Champions\n{'*'*20}\n")

    ingestion = str(input("Lancer le pipeline d'ingestion de nouvelles données [Y/N] : "))

    if ingestion == "Y":
        v = int(input("Quelle version est à récupérer [0 -> dernière, 1 -> avant dernière...] : "))
        main_ddragon(version=v)
    
    update_patch = str(input("Mettre à jour la table patch (is_latest) [Y/N] : "))
    if update_patch == "Y":
        Pipelines_db().pipeline_update_patch()
        print("MAJ terminée.")


    print(f"\n{'*'*20}\nPartie : Joueur\n{'*'*20}\n")

    player_integration = str(input("Souhaitez vous intégrer les données d'un joueur [Y/N] : "))

    if player_integration == "Y":
        game_name = str(input("Entrez le nom de jeu : "))
        tag_line = str(input("Entrez le tagline (#...) : "))
        main_player(gameName=game_name, tagLine=tag_line)
    
    
    print("Fin du processus.")
