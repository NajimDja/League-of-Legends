from dotenv import load_dotenv
from sqlalchemy import create_engine, text, Table, MetaData, inspect
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert as pg_insert
import pandas as pd
import os

from db_gestion import DataBaseGestion
from ddragon import pipeline_champion

db = DataBaseGestion()

load_dotenv()
database_url = os.getenv("DATABASE_URL")
engine = create_engine(database_url)
metadata = MetaData()
metadata.reflect(bind=engine)  # Charge toutes les tables depuis la DB

class Pipelines_db:

    def pipeline_insert(self, table_name : str, df_insert : pd.DataFrame):
        with Session(engine) as session:
            nb = db.insert_rows(session, table_name, df_insert)
            session.commit()
            print(f"\t{nb} lignes insérées dans {table_name}")

    def pipeline_update(self, table_name : str, df_maj : pd.DataFrame):
        with Session(engine) as session:
            nb = db.update_rows(session, table_name, df_maj)
            session.commit()
            print(f"\t{nb} lignes mises à jour dans {table_name}")

    def pipeline_delete(self, table_name : str, filters : dict):
        with Session(engine) as session:
            nb = db.delete_rows(session, table_name, filters=filters)
            session.commit()
            print(f"\t{nb} lignes supprimées dans {table_name}")

    def pipeline_drop_table(self, tables_name : list[str], cascade : bool):
        if cascade == False:
            db.drop_tables(engine, tables_name) # Sans CASCADE (échoue s'il y a des FK dépendantes)
        else:
            db.drop_tables(engine, tables_name, cascade=cascade) # Avec CASCADE (supprime aussi les tables liées par FK)

    def pipeline_update_patch(self):
        with Session(engine) as session:
            db.update_patch_latest(session)

def main(version : int = 0):

    pipe = Pipelines_db()

    print("Extraction et transformation des données en cours...")
    table_champion, table_champion_version, table_champ_passive, table_champ_info, table_champ_spells, table_champ_stats, table_champ_stats_up, table_runes, table_patch = pipeline_champion(version=version)
    print("Extraction et transformation terminées")

    print("Chargement des données en base.")
    pipe.pipeline_insert(table_name = "patch", df_insert = table_patch)
    pipe.pipeline_insert(table_name = "champion", df_insert = table_champion)
    pipe.pipeline_insert(table_name = "champion_version", df_insert = table_champion_version)
    pipe.pipeline_insert(table_name = "champion_info", df_insert = table_champ_info)
    pipe.pipeline_insert(table_name = "champion_passive", df_insert = table_champ_passive)
    pipe.pipeline_insert(table_name = "champion_spells", df_insert = table_champ_spells)
    pipe.pipeline_insert(table_name = "champion_stats", df_insert = table_champ_stats)
    pipe.pipeline_insert(table_name = "champion_stats_up", df_insert = table_champ_stats_up)
    print("Chargement des données en base terminé.")


if __name__ == "__main__":
    print("Lancement du processus de récupération, traitement et chargement des données en base.\n")
    print(f"{"*"*20}\nPartie : Champions\n{"*"*20}\n")
    ingestion = str(input("Lancer le pipeline d'ingestion de nouvelles données [Y/N] : "))

    if ingestion == "Y":
        v = int(input("Quelle version est à récupérer [0 -> dernière, 1 -> avant dernière...] : "))
        main(version=v)
    
    update_patch = str(input("Mettre à jour la table patch (is_latest) [Y/N] : "))
    if update_patch == "Y":
        Pipelines_db().pipeline_update_patch()
        print("MAJ terminée.")

    print(f"{"*"*20}\nPartie : Joueur\n{"*"*20}\n")
    
    print("Fin du processus.")
