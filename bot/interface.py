import discord


def creer_embed_accueil():
    return discord.Embed(
        title="Trivium • Triple Triad",
        description=(
            "Bienvenue sur Trivium !\n"
            "Découvre les règles du Triple Triad avant ta première partie."
        ),
    )


class MenuAccueil(discord.ui.View):
    @discord.ui.button(
        label="Règles du jeu",
        style=discord.ButtonStyle.secondary,
    )
    async def afficher_regles(
        self,
        interaction: discord.Interaction,
        bouton: discord.ui.Button,
    ):
        regles = (
            "**Les règles du Triple Triad**\n\n"
            "1. Chaque joueur commence avec **5 cartes**. À tour de rôle, "
            "posez une carte sur une case libre du plateau **3 × 3**.\n"
            "2. Chaque carte a une valeur sur chacun de ses quatre côtés. "
            "Si ta carte touche une carte adverse, compare les deux côtés "
            "en contact. Si ta valeur est **strictement supérieure**, "
            "tu captures la carte adverse. En cas d’égalité, elle reste à son propriétaire.\n"
            "3. Quand le plateau est plein, le joueur qui contrôle le plus "
            "de cartes gagne. La carte encore en main compte dans le score."
        )
        await interaction.response.send_message(regles, ephemeral=True)