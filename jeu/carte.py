import random


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
        self.bas bas
        self.gauche = gauche
        self.niveau = niveau
        self.proprietaire: str | None = proprietaire  # "Joueur1", "Joueur2" ou "IA"

    @staticmethod
    def formaterValeur(val: int) -> str:
        """Convertit la valeur numérique en affichage Triple Triad (10 -> 'A')"""
        return "A" if val == 10 else str(val)

    def copier(self, proprietaire | None = None):
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
        return f"{self.emoji} **{self.nom}** (Niv.{self.niveau}) — 'H:{h} D:{d} B:{b} G:{g}'"

    def __str__(self):
        h = self.formaterValeur(self.haut)
        d = self.formaterValeur(self.droite)
        b = self.formaterValeur(self.bas)
        g = self.formaterValeur(self.gauche)
        return (
            f"{self.emoji} {self.nom} (Niv.{self.niveau})\n"
            f"   {h}\n"
            f" {g}   {d}\n"
            f"   {b}"
        )

    def __repr__(self):
        return (
            f"Carte(nom={self.nom!r}, H={self.haut}, D={self.droite}, "
            f"B={self.bas}, G={self.gauche}, proprietaire={self.proprietaire!r})"
        )


#50 cartes
CATALOGUE_CARTES: list[Carte] = [
    # Commune
    Carte("Baguette",       haut=4, droite=3, bas=2, gauche=3, niveau=1),
    Carte("Croissant",      haut=3, droite=5, bas=2, gauche=4, niveau=1),
    Carte("Frites",         haut=2, droite=4, bas=5, gauche=3, niveau=1),
    Carte("Salade César",   haut=5, droite=2, bas=3, gauche=4, niveau=1),

    # Peu commune
    Carte("Crêpe",  haut=5, droite=4, bas=5, gauche=4, niveau=2),
    Carte("Hot-Dog",        haut=6, droite=3, bas=4, gauche=5, niveau=2),
    Carte("Tiramisu",       haut=4, droite=6, bas=5, gauche=4, niveau=2),
    Carte("Sushi Saumon",   haut=6, droite=5, bas=3, gauche=6, niveau=2),

    # Rare
    Carte("Pizza 4 fromages", haut=6, droite=6, bas=5, gauche=6, niveau=3),
    Carte("Burger",     haut=7, droite=5, bas=6, gauche=5, niveau=3),
    Carte("Tacos 3 viandes",  haut=5, droite=7, bas=7, gauche=5, niveau=3),
    Carte("pâtes Carbonara",        haut=7, droite=6, bas=4, gauche=7, niveau=3),

    # Très rare
    Carte("Crousty",   haut=8, droite=6, bas=7, gauche=7, niveau=4),
    Carte("Couscous",   haut=7, droite=8, bas=7, gauche=6, niveau=4),
    Carte("Tartiflette",      haut=8, droite=7, bas=6, gauche=8, niveau=4),
    Carte("Kebab",       haut=6, droite=9, bas=7, gauche=7, niveau=4),

    # Légendaires
    Carte("Bœuf Bourguignon",   haut=10, droite=8,  bas=7,  gauche=8, niveau=5),
    Carte("Vol au vent",    haut=9,  droite=9,  bas=8,  gauche=8, niveau=5),
    Carte("Fondue Savoyarde",   haut=8,  droite=10, bas=8,  gauche=7, niveau=5),
    Carte("Poulet Gaston-Gérard", haut=7,  droite=8,  bas=10, gauche=9, niveau=5),
]


class Deck:
    """Distribution des mains de 5 cartes"""

    @staticmethod
    def generer_main_aleatoire(proprietaire: str, taille: int = 5) -> list[Carte]:
        """Tire `taille` cartes totalement au hasard dans le catalogue."""
        selection = random.sample(CATALOGUE_CARTES, k=taille)
        return [carte.copier(proprietaire=proprietaire) for carte in selection]

    @staticmethod
    def generer_main_equilibree(proprietaire: str) -> list[Carte]:
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


# Test
if __name__ == "__main__":
    main_test = Deck.generer_main_equilibree("Joueur1")
    print("=== Main équilibrée générée ===")
    for c in main_test:
        print(c.affichage_compact())
    print("\nExemple d'affichage détaillé :")
    print(main_test[0])