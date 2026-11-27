import os
from pathlib import Path

import discord
from discord.ext import commands
from dotenv import load_dotenv

from bot.commandes import Commandes
from bot.interface import MenuAccueil
from bot.preparations import initialiser


class TriviumBot(commands.Bot):
    def __init__(self, serveur_id: int):
        super().__init__(command_prefix="!", intents=discord.Intents.default())
        self.serveur = discord.Object(id=serveur_id)

    async def setup_hook(self):
        initialiser()
        await self.add_cog(Commandes())
        self.add_view(MenuAccueil())
        self.tree.copy_global_to(guild=self.serveur)
        commandes = await self.tree.sync(guild=self.serveur)
        print(f"{len(commandes)} commandes synchronisées sur le serveur.")

    async def on_ready(self):
        print(f"{self.user} est en ligne !")


if __name__ == "__main__":
    load_dotenv(Path(__file__).with_name(".env"))
    token = os.getenv("DISCORD_TOKEN")
    serveur_id = os.getenv("DISCORD_GUILD_ID", "")
    if not token or not serveur_id.isdecimal():
        raise ValueError("Vérifie DISCORD_TOKEN et DISCORD_GUILD_ID dans ton .env.")
    TriviumBot(int(serveur_id)).run(token)