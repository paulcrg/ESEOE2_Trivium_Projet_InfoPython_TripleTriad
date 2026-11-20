import os

import discord
from discord.ext import commands
from dotenv import load_dotenv


# Chargement de la configuration
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("DISCORD_GUILD_ID")


# Classe principale du bot
class TriviumBot(commands.Bot):

    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(
            command_prefix="!",
            intents=intents
        )

    async def setup_hook(self):
        # Synchronisation des commandes sur le serveur
        guild = discord.Object(id=int(GUILD_ID))
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)

    async def on_ready(self):
        print(f"{self.user} est en ligne !")


bot = TriviumBot()


# Commande /ping
@bot.tree.command(
    name="ping",
    description="Vérifier que le bot fonctionne"
)
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(
        "Pong ! Trivium est en ligne."
    )


# Commande /aide
@bot.tree.command(
    name="aide",
    description="Afficher les commandes disponibles"
)
async def aide(interaction: discord.Interaction):
    message = (
        "**Commandes de Trivium**\n"
        "/ping - Vérifier le bot\n"
        "/aide - Afficher les commandes"
    )
    await interaction.response.send_message(message)


# Lancement du bot
if __name__ == "__main__":
    if not TOKEN or not GUILD_ID:
        raise ValueError("Vérifie ton fichier .env")

    bot.run(TOKEN)
