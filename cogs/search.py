import discord
from discord import app_commands, Interaction
from discord.ext import commands
from cogs.add import get_database, mylo_token


class Search(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="search",
        description="Busca si un usuario está o no en la Blacklist"
    )
    async def search(self, interaction: Interaction, id: int):
        db = get_database()
        users_collection = db["users"]

        user_exists = users_collection.find_one({"id": id})
        if user_exists:
            self.bot.is_owner
            return await interaction.response.send_message(f'{user_exists["nombre"]} existe en la Blacklist.')
        else:
            return await interaction.response.send_message("No existe en la Blacklist.")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        Search(bot),
        guilds=[discord.Object(id=mylo_token)]
    )
