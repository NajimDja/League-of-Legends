from sqlalchemy import create_engine, text, Table, MetaData, inspect
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert as pg_insert
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
database_url = os.getenv("DATABASE_URL")
engine = create_engine(database_url)
metadata = MetaData()
metadata.reflect(bind=engine)  # Charge toutes les tables depuis la DB

class DataBaseGestion:

    def get_tables_columns(self, engine) -> dict[str, list[str]]:
        """
        Retourne un dictionnaire {nom_table: [col1, col2, ...]} 
        pour toutes les tables du schéma.
        """
        inspector = inspect(engine)
        tables = {
            table_name: [col["name"] for col in inspector.get_columns(table_name)]
            for table_name in inspector.get_table_names()
        }
        for k in tables:
            print(f"Table {k} avec les colonnes suivante : {tables[k]}\n")

    def insert_rows(self, session: Session, table_name: str, df: pd.DataFrame) -> int:
        """
        Insère les lignes du DataFrame dans la table.
        Ignore les conflits sur la clé primaire (DO NOTHING).
        Retourne le nombre de lignes insérées.
        """
        if df.empty:
            return 0

        table = metadata.tables[table_name]
        stmt = pg_insert(table).values(df.to_dict(orient="records"))
        stmt = stmt.on_conflict_do_nothing()
        result = session.execute(stmt)
        return result.rowcount

    def update_rows(self, session: Session, table_name: str, df: pd.DataFrame) -> int:
        """
        Met à jour les lignes existantes via un upsert sur la clé primaire.
        Les lignes absentes de la table sont ignorées (DO NOTHING sur insert).
        Retourne le nombre de lignes affectées.
        """
        if df.empty:
            return 0

        table = metadata.tables[table_name]
        pk_cols = {col.name for col in table.primary_key.columns}
        update_cols = {
            col.name: stmt.excluded[col.name]  # type: ignore
            for col in table.columns
            if col.name not in pk_cols
        }

        stmt = pg_insert(table).values(df.to_dict(orient="records"))
        stmt = stmt.on_conflict_do_update(
            index_elements=list(pk_cols),
            set_=update_cols
        )
        result = session.execute(stmt)
        return result.rowcount
    
    def delete_rows(self, session: Session, table_name: str, filters: dict) -> int:
        """
        Supprime les lignes correspondant aux filtres.

        Args:
            filters: {nom_colonne: valeur} — ex: {"patch_id": 3, "champ_id": 42}

        Retourne le nombre de lignes supprimées.
        """
        if not filters:
            raise ValueError("Aucun filtre fourni — utilisez drop_table() pour vider une table entière.")

        table = metadata.tables[table_name]
        conditions = [table.c[col] == val for col, val in filters.items()]

        stmt = table.delete().where(*conditions)
        result = session.execute(stmt)
        return result.rowcount
    
    def drop_tables(self, engine, table_names: list[str], cascade: bool = False):
        """
        Supprime définitivement les tables listées.

        Args:
            table_names : liste des tables à supprimer
            cascade     : si True, supprime aussi les tables dépendantes via FK
        """
        tables_to_drop = [
            metadata.tables[name]
            for name in table_names
            if name in metadata.tables
        ]

        missing = [name for name in table_names if name not in metadata.tables]
        if missing:
            raise ValueError(f"Tables introuvables dans le schéma : {missing}")

        with engine.begin() as conn:
            if cascade:
                for name in table_names:
                    conn.execute(text(f'DROP TABLE IF EXISTS "{name}" CASCADE'))
            else:
                metadata.drop_all(bind=conn, tables=tables_to_drop)

        # Mettre à jour le metadata local
        for table in tables_to_drop:
            metadata.remove(table)

        print(f"Tables supprimées : {table_names}")