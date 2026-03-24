from sqlalchemy import create_engine, text, Table, MetaData, inspect, select, func
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
    

    def upsert_rows(self, session: Session, table_name: str, df: pd.DataFrame) -> int:
        """
        Insère les lignes du DataFrame dans la table.
        Si un conflit sur la clé primaire est détecté, met à jour les colonnes non-PK.
        Retourne le nombre de lignes affectées.
        """
        if df.empty:
            return 0

        table = metadata.tables[table_name]
        pk_cols = {col.name for col in table.primary_key.columns}

        stmt = pg_insert(table).values(df.to_dict(orient="records"))

        update_cols = {
            col.name: stmt.excluded[col.name]
            for col in table.columns
            if col.name not in pk_cols
        }

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

    def update_patch_latest(self, session: Session) -> None:
        """
        Met is_latest=True sur le patch avec l'id le plus élevé,
        et is_latest=False sur tous les autres.
        """
        table = metadata.tables["patch"]

        # Récupère l'id le plus élevé
        result = session.execute(select(func.max(table.c.id)))
        max_id = result.scalar()

        if max_id is None:
            print("La table patch est vide.")
            return

        # Met tout à False
        session.execute(
            table.update().values(is_latest=False)
        )

        # Met le plus récent à True
        session.execute(
            table.update()
            .where(table.c.id == max_id)
            .values(is_latest=True)
        )

        session.commit()
        print(f"Patch {max_id} défini comme latest.")
    
    def get_latest_patch(self, session: Session) -> dict | None:
        """
        Retourne le patch avec l'id le plus élevé sous forme de dictionnaire.
        Retourne None si la table est vide.
        """
        table = metadata.tables["patch"]

        result = session.execute(
            select(table).order_by(table.c.id.desc()).limit(1)
        )
        row = result.mappings().first()

        if row is None:
            print("La table patch est vide.")
            return None

        return dict(row)


class Pipelines_db:

    def __init__(self):
        
        self.db = DataBaseGestion()

    def pipeline_insert(self, table_name : str, df_insert : pd.DataFrame):
        with Session(engine) as session:
            nb = self.db.insert_rows(session, table_name, df_insert)
            session.commit()
            print(f"\t{nb} lignes insérées dans {table_name}")

    def pipeline_update(self, table_name : str, df_maj : pd.DataFrame):
        with Session(engine) as session:
            nb = self.db.update_rows(session, table_name, df_maj)
            session.commit()
            print(f"\t{nb} lignes mises à jour dans {table_name}")
    
    def pipeline_upsert(self, table_name : str, df_upsert : pd.DataFrame):
        with Session(engine) as session:
            nb = self.db.upsert_rows(session, table_name, df_upsert)
            session.commit()
            print(f"\t{nb} lignes insérées ou mises à jour dans {table_name}")

    def pipeline_delete(self, table_name : str, filters : dict):
        with Session(engine) as session:
            nb = self.db.delete_rows(session, table_name, filters=filters)
            session.commit()
            print(f"\t{nb} lignes supprimées dans {table_name}")

    def pipeline_drop_table(self, tables_name : list[str], cascade : bool):
        if cascade == False:
            self.db.drop_tables(engine, tables_name) # Sans CASCADE (échoue s'il y a des FK dépendantes)
        else:
            self.db.drop_tables(engine, tables_name, cascade=cascade) # Avec CASCADE (supprime aussi les tables liées par FK)

    def pipeline_update_patch(self):
        with Session(engine) as session:
            self.db.update_patch_latest(session)