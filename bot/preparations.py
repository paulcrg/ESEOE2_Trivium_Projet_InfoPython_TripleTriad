import sqlite3
from contextlib import closing
from pathlib import Path


BASE = Path(__file__).resolve().parents[1] / "trivium.sqlite3"


def initialiser():
    with closing(sqlite3.connect(BASE)) as db, db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS preparations (
                serveur INTEGER NOT NULL,
                joueur INTEGER NOT NULL,
                adversaire INTEGER,
                ia TEXT,
                PRIMARY KEY (serveur, joueur),
                CHECK ((adversaire IS NULL) != (ia IS NULL))
            )
        """)


def _enregistrer(lignes):
    with closing(sqlite3.connect(BASE)) as db, db:
        db.executemany("""
            INSERT INTO preparations (serveur, joueur, adversaire, ia)
            VALUES (?, ?, ?, ?)
            ON CONFLICT (serveur, joueur) DO UPDATE SET
                adversaire = excluded.adversaire, ia = excluded.ia
        """, lignes)


def enregistrer_duel(serveur, joueur, adversaire):
    # Les deux joueurs retrouvent le duel même si le bot redémarre.
    _enregistrer([
        (serveur, joueur, adversaire, None),
        (serveur, adversaire, joueur, None),
    ])


def enregistrer_ia(serveur, joueur, niveau):
    _enregistrer([(serveur, joueur, None, niveau)])


def retrouver(serveur, joueur):
    with closing(sqlite3.connect(BASE)) as db:
        return db.execute(
            "SELECT adversaire, ia FROM preparations WHERE serveur = ? AND joueur = ?",
            (serveur, joueur),
        ).fetchone()