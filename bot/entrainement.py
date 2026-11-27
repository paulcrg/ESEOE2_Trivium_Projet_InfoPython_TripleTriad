import discord


# Exercice sur un seul coup. L'ordre des valeurs est haut, droite, bas, gauche.
CARTES = {"Renard": (4, 5, 2, 3), "Golem": (6, 2, 7, 1)}
GARDE = (3, 6, 4, 2)
CASES = ("A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3")
COTES = ("haut", "droite", "bas", "gauche")
# Depuis chacune de ces cases, quel côté de notre carte touche le garde en B2 ?
VERS_GARDE = {"A2": 2, "B1": 1, "B3": 3, "C2": 0}


def consigne():
    return (
        "**Plateau d’entraînement** · Un seul coup à jouer\n"
        "Le Garde rouge est en **B2**, au centre. "
        "Ses valeurs sont **↑ 3 · → 6 · ↓ 4 · ← 2**.\n"
        "Choisis une de tes cartes, puis une case libre pour tenter de le capturer. "
        "Tu joues en bleu."
    )


def resultat(nom, case):
    if case not in VERS_GARDE:
        return False, "Ta carte ne touche pas le Garde par un côté."
    cote = VERS_GARDE[case]
    oppose = (cote + 2) % 4
    attaque, defense = CARTES[nom][cote], GARDE[oppose]
    detail = f"Ton côté {COTES[cote]} vaut **{attaque}**, son côté {COTES[oppose]} vaut **{defense}**."
    if attaque > defense:
        return True, f"{detail} Le Garde passe dans ton camp."
    if attaque == defense:
        return False, f"{detail} Une égalité laisse le Garde dans le camp rouge."
    return False, f"{detail} Le Garde reste dans le camp rouge."


class Case(discord.ui.Button):
    def __init__(self, position, ligne):
        centre = position == "B2"
        super().__init__(
            label=f"{position} · Garde" if centre else position,
            style=discord.ButtonStyle.danger if centre else discord.ButtonStyle.secondary,
            row=ligne,
            disabled=True,
        )
        self.position = position

    async def callback(self, interaction):
        await self.view.poser(interaction, self)


class Entrainement(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)
        self.carte = None
        self.termine = False
        self.cases = {}
        for index, position in enumerate(CASES):
            bouton = Case(position, index // 3)
            self.cases[position] = bouton
            self.add_item(bouton)

    @discord.ui.select(
        placeholder="Choisis ta carte",
        row=3,
        options=[
            discord.SelectOption(
                label=nom,
                description=f"↑ {haut} · → {droite} · ↓ {bas} · ← {gauche}",
            )
            for nom, (haut, droite, bas, gauche) in CARTES.items()
        ],
    )
    async def choisir(self, interaction, selection):
        if self.termine:
            await interaction.response.send_message("Ce coup a déjà été joué.", ephemeral=True)
            return
        self.carte = selection.values[0]
        for position, bouton in self.cases.items():
            bouton.disabled = position == "B2"
        await interaction.response.edit_message(
            content=f"{consigne()}\n\nCarte sélectionnée : **{self.carte}**.", view=self,
        )

    async def poser(self, interaction, bouton):
        if self.termine or self.carte is None or bouton.position == "B2":
            await interaction.response.send_message("Ce coup est indisponible.", ephemeral=True)
            return
        self.termine = True
        capture, bilan = resultat(self.carte, bouton.position)
        bouton.label = f"{bouton.position} · {self.carte}"
        bouton.style = discord.ButtonStyle.primary
        if capture:
            self.cases["B2"].style = discord.ButtonStyle.primary
        for element in self.children:
            element.disabled = True
        await interaction.response.edit_message(
            content=f"**{self.carte} en {bouton.position}**\n{bilan}\nRejoue avec /plateau.",
            view=self,
        )
        self.stop()