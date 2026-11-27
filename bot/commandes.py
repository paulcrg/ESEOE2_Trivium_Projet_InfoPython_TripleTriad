import discord
from discord import app_commands
from discord.ext import commands

from bot.entrainement import Entrainement, consigne
from bot.interface import ChoixMode, MenuAccueil, REGLES, afficher_preparation, creer_embed_accueil


class Commandes(commands.Cog):
    @app_commands.command(name="ping", description="Vérifier que Trivium est en ligne")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message("Pong ! Trivium est en ligne.")

    @app_commands.command(name="aide", description="Afficher les commandes de Trivium")
    async def aide(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "**Commandes de Trivium**\n"
            "/menu — Ouvrir le menu\n"
            "/jouer — Préparer un duel ou choisir une IA\n"
            "/regles — Lire les règles de base\n"
            "/plateau — Essayer une capture en un coup\n"
            "/reprendre — Retrouver ta dernière préparation sur ce serveur\n"
            "/ping — Vérifier que le bot répond\n"
            "/aide — Afficher cette liste",
            ephemeral=True,
        )

    @app_commands.command(name="menu", description="Ouvrir le menu de Trivium")
    async def menu(self, interaction: discord.Interaction):
        await interaction.response.send_message(embed=creer_embed_accueil(), view=MenuAccueil())

    @app_commands.command(name="jouer", description="Défier un membre ou choisir une IA")
    async def jouer(self, interaction: discord.Interaction):
        await interaction.response.send_message("Contre qui veux-tu jouer ?", view=ChoixMode(), ephemeral=True)

    @app_commands.command(name="regles", description="Lire les règles de Triple Triad")
    async def regles(self, interaction: discord.Interaction):
        await interaction.response.send_message(REGLES, ephemeral=True)

    @app_commands.command(name="plateau", description="T’entraîner à capturer une carte en un coup")
    async def plateau(self, interaction: discord.Interaction):
        await interaction.response.send_message(consigne(), view=Entrainement(), ephemeral=True)

    @app_commands.command(name="reprendre", description="Retrouver ta dernière préparation de partie")
    async def reprendre(self, interaction: discord.Interaction):
        await afficher_preparation(interaction)