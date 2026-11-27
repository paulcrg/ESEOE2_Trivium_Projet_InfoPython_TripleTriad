import json
import random
from pathlib import Path


class Carte:
    """
    Représente une carte Triple Triad.
    Les valeurs des 4 côtés vont de 1 à 10.
    """

    def __init__(
        self,
        nom: str,
        haut: int,
        droite: int,
        bas: int,
        gauche: int,
        niveau: int = 1,
        proprietaire: str | None = None,
    ):
        for cote, val in (("haut", haut),("droite", droite),("bas", bas),("gauche", gauche)):
            if not (1 <= val <= 10):
                raise ValueError(f"La valeur '{cote}' de {nom} doit être entre 1 et 10 (reçu: {val}).")

        self.nom = nom
        self.haut = haut
        self.droite = droite
        self.bas = bas
        self.gauche = gauche
        self.niveau = niveau
        self.proprietaire: str | None = proprietaire  # "Joueur1", "Joueur2" ou "IA"

    @staticmethod
    def formaterValeur(val: int) -> str:
        """Convertit la valeur numérique en affichage Triple Triad (10 -> 'A')"""
        return "A" if val == 10 else str(val)

    def copier(self, proprietaire: str | None = None):
        """Retourne une copie indépendante de la carte pour éviter de modifier le catalogue"""
        return Carte(
            nom=self.nom,
            haut=self.haut,
            droite=self.droite,
            bas=self.bas,
            gauche=self.gauche,
            niveau=self.niveau,
            proprietaire=proprietaire if proprietaire is not None else self.proprietaire,
        )

    def affichage_compact(self):
        """Affichage sur une ligne"""
        h = self.formaterValeur(self.haut)
        d = self.formaterValeur(self.droite)
        b = self.formaterValeur(self.bas)
        g = self.formaterValeur(self.gauche)
        return f"**{self.nom}** (Niv.{self.niveau}) — 'H:{h} D:{d} B:{b} G:{g}'"

    def __str__(self):
        h = self.formaterValeur(self.haut)
        d = self.formaterValeur(self.droite)
        b = self.formaterValeur(self.bas)
        g = self.formaterValeur(self.gauche)
        return (
            f"{self.nom} (Niv.{self.niveau})\n"
            f"   {h}\n"
            f" {g}   {d}\n"
            f"   {b}"
        )

    def __repr__(self):
        return (
            f"Carte(nom={self.nom!r}, H={self.haut}, D={self.droite}, "
            f"B={self.bas}, G={self.gauche}, proprietaire={self.proprietaire!r})"
        )


FICHIER_CARTES = Path(__file__).with_name("cartes.json")


def charger_catalogue(chemin: Path = FICHIER_CARTES):
    """Lit le fichier JSON et crée un objet Carte pour chaque entrée."""
    with open(chemin, encoding="utf-8") as fichier:
        donnees = json.load(fichier)
    return [Carte(**infos) for infos in donnees]


CATALOGUE_CARTES: list[Carte] = charger_catalogue()


class Deck:
    """Distribution des mains de 5 cartes"""

    @staticmethod
    def generer_main_aleatoire(proprietaire: str, taille: int = 5):
        """Tire un nombre 'taille' de cartes au hasard dans le catalogue"""
        selection = random.sample(CATALOGUE_CARTES, k=taille)
        return [carte.copier(proprietaire=proprietaire) for carte in selection]

    @staticmethod
    def generer_main_equilibree(proprietaire: str):
        """
        Tire une main équilibrée de 5 cartes :
        1 carte de chaque niveau (1, 2, 3, 4 et 5).
        """
        main: list[Carte] = []
        for niveau in range(1, 6):
            cartes_niveau = [c for c in CATALOGUE_CARTES if c.niveau == niveau]
            carte_choisie = random.choice(cartes_niveau)
            main.append(carte_choisie.copier(proprietaire=proprietaire))
        random.shuffle(main)
        return main
