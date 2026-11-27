import asyncio
import logging
import sqlite3

import discord

from bot.preparations import enregistrer_duel


class Invitation(discord.ui.View):
    def __init__(self, serveur, auteur, adversaire):
        super().__init__(timeout=120)
        self.serveur = serveur
        self.auteur = auteur
        self.adversaire = adversaire
        self.message = None
        self.fermee = False
        self.verrou = asyncio.Lock()

    async def interaction_check(self, interaction):
        if interaction.user.id == self.adversaire.id:
            return True
        await interaction.response.send_message(
            "Seul le joueur défié peut répondre à cette invitation.", ephemeral=True,
        )
        return False

    async def repondre(self, interaction, accepte):
        await interaction.response.defer()
        async with self.verrou:
            if self.fermee:
                await interaction.followup.send("Cette invitation est terminée.", ephemeral=True)
                return
            if accepte:
                try:
                    enregistrer_duel(self.serveur, self.auteur.id, self.adversaire.id)
                except sqlite3.Error:
                    logging.exception("Échec de l’enregistrement du duel")
                    await interaction.followup.send(
                        "Enregistrement impossible. Tu peux réessayer.", ephemeral=True,
                    )
                    return
                texte = (
                    f"Duel accepté entre {self.auteur.mention} et {self.adversaire.mention}.\n"
                    "Votre duel est préparé. Chacun peut le retrouver avec /reprendre."
                )
            else:
                texte = f"{self.adversaire.mention} a refusé le défi de {self.auteur.mention}."
            self.fermee = True
            self.stop()
            await interaction.edit_original_response(
                content=texte, view=None, allowed_mentions=discord.AllowedMentions.none(),
            )

    @discord.ui.button(label="Accepter", style=discord.ButtonStyle.success)
    async def accepter(self, interaction, bouton):
        await self.repondre(interaction, True)

    @discord.ui.button(label="Refuser", style=discord.ButtonStyle.danger)
    async def refuser(self, interaction, bouton):
        await self.repondre(interaction, False)

    async def on_timeout(self):
        async with self.verrou:
            if self.fermee or self.message is None:
                return
            self.fermee = True
            try:
                await self.message.edit(content="Le délai de réponse au défi est écoulé.", view=None)
            except discord.HTTPException:
                logging.info("Impossible de modifier le message du défi expiré", exc_info=True)


class ChoixAdversaire(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=180)
        self.envoi_en_cours = False

    @discord.ui.select(cls=discord.ui.UserSelect, placeholder="Choisis ton adversaire")
    async def selectionner(self, interaction, selection):
        adversaire = selection.values[0]
        if adversaire.id == interaction.user.id or adversaire.bot:
            await interaction.response.send_message(
                "Choisis un autre joueur du serveur, avec un compte humain.", ephemeral=True,
            )
            return
        if self.envoi_en_cours:
            await interaction.response.send_message("Défi déjà demandé.", ephemeral=True)
            return

        self.envoi_en_cours = True
        await interaction.response.defer()
        invitation = Invitation(interaction.guild_id, interaction.user, adversaire)
        try:
            invitation.message = await interaction.channel.send(
                f"{adversaire.mention}, {interaction.user.mention} te défie à Triple Triad !\n"
                "Tu as deux minutes pour répondre.",
                view=invitation,
                allowed_mentions=discord.AllowedMentions(users=[adversaire]),
            )
        except discord.HTTPException:
            self.envoi_en_cours = False
            invitation.stop()
            await interaction.followup.send(
                "Impossible de publier le défi dans ce salon. "
                "Vérifie que le bot peut y envoyer des messages, puis réessaie.",
                ephemeral=True,
            )
            return
        self.stop()
        await interaction.edit_original_response(
            content=f"Invitation publiée pour {adversaire.mention}.", view=None,
        )