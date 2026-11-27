import logging
import sqlite3

import discord

from bot.duels import ChoixAdversaire
from bot.entrainement import Entrainement, consigne
from bot.preparations import enregistrer_ia, retrouver


REGLES = (
    "**Triple Triad — règles de base**\n"
    "Chaque joueur reçoit **5 cartes**. Posez à tour de rôle une carte sur une case "
    "libre du plateau **3 × 3**.\n\n"
    "Chaque carte a quatre valeurs : **haut, droite, bas, gauche**. "
    "Le **A** vaut **10**. Si ta carte touche une carte adverse par un côté, "
    "compare les deux valeurs en contact. Si la tienne est strictement supérieure, "
    "tu captures cette carte. Une égalité ne change rien.\n\n"
    "Après neuf poses, compte les cartes de chaque camp, y compris la carte encore "
    "en main. Le meilleur score gagne. À 5–5, il y a égalité."
)


def creer_embed_accueil():
    return discord.Embed(
        title="Trivium • Triple Triad",
        description=(
            "**Jouer** pour défier un membre ou préparer une partie contre l’IA.\n"
            "**Entraînement** pour essayer une capture sur le plateau."
        ),
    )


async def afficher_preparation(interaction):
    preparation = retrouver(interaction.guild_id, interaction.user.id)
    if preparation is None:
        texte = "Tu n’as encore aucune préparation sur ce serveur. Commence avec /jouer."
    else:
        adversaire, ia = preparation
        mode = f"Duel avec <@{adversaire}>" if adversaire is not None else f"IA · {ia}"
        texte = (
            f"**Ta dernière préparation**\n{mode}\n"
            "Le moteur de partie sera raccordé dans une prochaine version."
        )
    await interaction.response.send_message(texte, ephemeral=True)


class ChoixIA(discord.ui.View):
    @discord.ui.select(
        placeholder="Choisis la difficulté",
        options=[
            discord.SelectOption(label="Facile", value="Facile (aléatoire)",
                                 description="IA prévue : coups aléatoires"),
            discord.SelectOption(label="Stratégique", value="Stratégique (Minimax)",
                                 description="IA prévue : recherche Minimax"),
        ],
    )
    async def choisir(self, interaction, selection):
        niveau = selection.values[0]
        try:
            enregistrer_ia(interaction.guild_id, interaction.user.id, niveau)
        except sqlite3.Error:
            logging.exception("Échec de l’enregistrement du choix de l’IA")
            await interaction.response.send_message(
                "Enregistrement impossible. Tu peux réessayer.", ephemeral=True,
            )
            return
        await interaction.response.edit_message(
            content=f"Préparation enregistrée : **IA · {niveau}**.\n"
                    "Retrouve ce choix avec /reprendre. Le moteur IA sera raccordé ensuite.",
            view=None,
        )
        self.stop()


class ChoixMode(discord.ui.View):
    @discord.ui.button(label="Défier un joueur", style=discord.ButtonStyle.primary)
    async def choisir_duel(self, interaction, bouton):
        await interaction.response.edit_message(content="Qui veux-tu défier ?", view=ChoixAdversaire())

    @discord.ui.button(label="Affronter l’IA", style=discord.ButtonStyle.primary)
    async def choisir_ia(self, interaction, bouton):
        await interaction.response.edit_message(content="Quelle IA veux-tu affronter ?", view=ChoixIA())


class MenuAccueil(discord.ui.View):
    # Des identifiants stables permettent aux menus publics de survivre au redémarrage.
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Jouer", style=discord.ButtonStyle.success, custom_id="trivium:jouer")
    async def jouer(self, interaction, bouton):
        await interaction.response.send_message("Contre qui veux-tu jouer ?", view=ChoixMode(), ephemeral=True)

    @discord.ui.button(label="Règles du jeu", style=discord.ButtonStyle.secondary, custom_id="trivium:regles")
    async def regles(self, interaction, bouton):
        await interaction.response.send_message(REGLES, ephemeral=True)

    @discord.ui.button(label="Entraînement", style=discord.ButtonStyle.primary, custom_id="trivium:plateau")
    async def plateau(self, interaction, bouton):
        await interaction.response.send_message(consigne(), view=Entrainement(), ephemeral=True)

    @discord.ui.button(label="Reprendre", style=discord.ButtonStyle.secondary, custom_id="trivium:reprendre")
    async def reprendre(self, interaction, bouton):
        await afficher_preparation(interaction)