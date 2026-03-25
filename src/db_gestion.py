from sqlalchemy import create_engine, text, Table, MetaData, inspect, select, func
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert as pg_insert
import pandas as pd
import os
from dotenv import load_dotenv
import re
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch

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
    

    def visualize_database(self, engine, output_path: str = "db_schema.png", figsize: tuple = (18, 12), dpi: int = 150) -> str:
        """
        Génère une image du schéma de la base de données (tables, colonnes, clés, relations).

        Args:
            output_path : chemin de sauvegarde de l'image (.png)
            figsize     : taille de la figure matplotlib
            dpi         : résolution de l'image

        Returns:
            Le chemin de l'image générée.
        """
        inspector = inspect(engine)

        # ── 1. Collecte des métadonnées ───────────────────────────────────────

        tables    = {}
        relations = []

        for table_name in inspector.get_table_names():
            columns  = inspector.get_columns(table_name)
            pk_cols  = set(inspector.get_pk_constraint(table_name).get("constrained_columns", []))  # ✅ corrigé
            fk_cols  = {}

            for fk in inspector.get_foreign_keys(table_name):
                for col in fk["constrained_columns"]:
                    fk_cols[col] = fk["referred_table"]
                relations.append({
                    "from_table": table_name,
                    "to_table":   fk["referred_table"],
                    "from_col":   fk["constrained_columns"][0],
                    "to_col":     fk["referred_columns"][0],
                })

            tables[table_name] = {
                "columns": [
                    {
                        "name":   col["name"],
                        "type":   str(col["type"]),
                        "is_pk":  col["name"] in pk_cols,
                        "is_fk":  col["name"] in fk_cols,
                        "fk_ref": fk_cols.get(col["name"]),
                    }
                    for col in columns
                ]
            }

        # ── 2. Calcul de la disposition (grille automatique) ──────────────────

        n_tables   = len(tables)
        n_cols     = max(1, min(4, n_tables))
        n_rows     = (n_tables + n_cols - 1) // n_cols
        ROW_HEIGHT = 0.32
        HEADER_H   = 0.55
        PADDING    = 0.4
        COL_W      = 3.8

        positions = {}
        for i, table_name in enumerate(tables):
            col_idx = i % n_cols
            row_idx = i // n_cols
            max_rows_in_row = max(
                len(tables[t]["columns"])
                for j, t in enumerate(tables)
                if j // n_cols == row_idx
            )
            table_h = HEADER_H + len(tables[table_name]["columns"]) * ROW_HEIGHT
            x = col_idx * (COL_W + PADDING)
            y = -row_idx * (HEADER_H + max_rows_in_row * ROW_HEIGHT + PADDING)
            positions[table_name] = (x, y, COL_W, table_h)

        # ── 3. Dessin ─────────────────────────────────────────────────────────

        COLORS = {
            "header_bg":  "#2C3E50", "header_txt": "#FFFFFF",
            "pk_bg":      "#F39C12", "pk_txt":     "#FFFFFF",
            "fk_bg":      "#2980B9", "fk_txt":     "#FFFFFF",
            "col_bg":     "#ECF0F1", "col_txt":    "#2C3E50",
            "col_alt_bg": "#FDFEFE", "border":     "#BDC3C7",
            "relation":   "#E74C3C", "bg":         "#F8F9FA",
        }

        total_w = n_cols * (COL_W + PADDING)
        total_h = n_rows * (HEADER_H + 10 * ROW_HEIGHT + PADDING)

        fig, ax = plt.subplots(figsize=figsize)
        fig.patch.set_facecolor(COLORS["bg"])
        ax.set_facecolor(COLORS["bg"])
        ax.set_xlim(-0.3, total_w)
        ax.set_ylim(-total_h, HEADER_H + 0.5)
        ax.axis("off")

        ax.text(total_w / 2, HEADER_H + 0.1, "Schéma de la base de données",
                ha="center", va="bottom", fontsize=14, fontweight="bold",
                color=COLORS["header_bg"])

        for table_name, (x, y, w, h) in positions.items():
            cols    = tables[table_name]["columns"]
            table_h = HEADER_H + len(cols) * ROW_HEIGHT

            ax.add_patch(FancyBboxPatch(
                (x + 0.04, y - table_h - 0.04), w, table_h,
                boxstyle="round,pad=0.05", linewidth=0,
                facecolor="#BDC3C7", zorder=1))

            ax.add_patch(FancyBboxPatch(
                (x, y - table_h), w, table_h,
                boxstyle="round,pad=0.05", linewidth=1.2,
                edgecolor=COLORS["border"], facecolor="white", zorder=2))

            ax.add_patch(FancyBboxPatch(
                (x, y - HEADER_H), w, HEADER_H,
                boxstyle="round,pad=0.05", linewidth=0,
                facecolor=COLORS["header_bg"], zorder=3))

            ax.text(x + w / 2, y - HEADER_H / 2, table_name.upper(),
                    ha="center", va="center", fontsize=9, fontweight="bold",
                    color=COLORS["header_txt"], zorder=4)

            for k, col in enumerate(cols):
                cy = y - HEADER_H - k * ROW_HEIGHT

                if col["is_pk"]:
                    bg, txt, icon = COLORS["pk_bg"], COLORS["pk_txt"], "🔑 "
                elif col["is_fk"]:
                    bg, txt, icon = COLORS["fk_bg"], COLORS["fk_txt"], "🔗 "
                else:
                    bg   = COLORS["col_bg"] if k % 2 == 0 else COLORS["col_alt_bg"]
                    txt  = COLORS["col_txt"]
                    icon = ""

                ax.add_patch(FancyBboxPatch(
                    (x + 0.05, cy - ROW_HEIGHT + 0.03), w - 0.1, ROW_HEIGHT - 0.04,
                    boxstyle="round,pad=0.02", linewidth=0.5,
                    edgecolor=COLORS["border"], facecolor=bg, zorder=3))

                ax.text(x + 0.18, cy - ROW_HEIGHT / 2, f"{icon}{col['name']}",
                        ha="left", va="center", fontsize=7, color=txt, zorder=4)
                ax.text(x + w - 0.12, cy - ROW_HEIGHT / 2,
                        col["type"].split("(")[0],
                        ha="right", va="center", fontsize=6.5,
                        color=txt, style="italic", zorder=4, alpha=0.85)

        for rel in relations:
            if rel["from_table"] not in positions or rel["to_table"] not in positions:
                continue

            fx, fy, fw, _ = positions[rel["from_table"]]
            tx, ty, tw, _ = positions[rel["to_table"]]

            from_col_idx = next((i for i, c in enumerate(tables[rel["from_table"]]["columns"])
                                 if c["name"] == rel["from_col"]), 0)
            to_col_idx   = next((i for i, c in enumerate(tables[rel["to_table"]]["columns"])
                                 if c["name"] == rel["to_col"]), 0)

            y_from = fy - HEADER_H - (from_col_idx + 0.5) * ROW_HEIGHT
            y_to   = ty - HEADER_H - (to_col_idx   + 0.5) * ROW_HEIGHT
            x_from, x_to = (fx + fw, tx) if fx < tx else (fx, tx + tw)

            ax.annotate("",
                xy=(x_to, y_to), xytext=(x_from, y_from),
                arrowprops=dict(arrowstyle="-|>", color=COLORS["relation"],
                                lw=1.2, connectionstyle="arc3,rad=0.15"),
                zorder=5)

        ax.legend(
            handles=[
                mpatches.Patch(facecolor=COLORS["pk_bg"],   label="Clé primaire (PK)"),
                mpatches.Patch(facecolor=COLORS["fk_bg"],   label="Clé étrangère (FK)"),
                mpatches.Patch(facecolor=COLORS["col_bg"],  label="Colonne standard"),
                mpatches.Patch(facecolor=COLORS["relation"],label="Relation FK"),
            ],
            loc="lower right", fontsize=8, framealpha=0.9,
            title="Légende", title_fontsize=8
        )

        plt.tight_layout()
        plt.savefig(output_path, dpi=dpi, bbox_inches="tight", facecolor=COLORS["bg"])
        plt.close()

        print(f"Schéma sauvegardé → {output_path}")
        return output_path


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

if __name__ == "__main__":
    dbg = DataBaseGestion()
    dbg.visualize_database(engine=engine)