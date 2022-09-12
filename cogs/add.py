import os
import discord
from discord import app_commands, Interaction
from discord.ext import commands
from cogs.ayuda import mylo_token


mongo_url = os.environ.get('MONGO_BLACKLIST_URL')


def get_database():  # Create database 'blacklist'
    from pymongo import MongoClient
    client = MongoClient(mongo_url)
    return client['blacklist']


class Add(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="add",
        description="Agrega un nuevo usuario a la blacklist."
    )
    async def add(self, interaction: Interaction, nombre: str, id: int, perfil: str, attachment: discord.Attachment) -> None:

        blacklist_db = get_database()
        users_collection = blacklist_db["users"]

        gcName = nombre
        gcId = id
        gcUrl = perfil
        gcImage = None
        if attachment:
            gcImage = attachment.url

        already_exists = users_collection.find_one({"id": gcId})
        if already_exists:
            return await interaction.response.send_message(f'{gcName} ya existe en la **blacklist**.')

        new_document = {
            "id": gcId,
            "nombre": gcName,
            "perfil": gcUrl,
            "imagen": gcImage,
        }

        users_collection.insert_one(new_document)
        embed = discord.Embed(
            title=f"Agregaste a {gcName} la blacklist 💀",
            color=0x32213a,
        )
        embed.add_field(name="Nombre", value=gcName)
        embed.add_field(name="GC Id", value=gcId)
        embed.add_field(name="Perfil de GC", value=gcUrl)
        embed.add_field(name="Captura", value=gcImage)
        embed.set_image(url=gcImage)
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        Add(bot),
        guilds=[discord.Object(id=mylo_token)]
    )
