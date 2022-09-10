import os
from typing import List
import discord
from discord.ext import commands

discord_token = os.environ.get('DISCORD_BLACKLIST_TOKEN')
mongo_url = os.environ.get('MONGO_BLACKLIST_URL')

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


def get_database():  # Create database 'blacklist'
    from pymongo import MongoClient

    print(mongo_url)
    client = MongoClient(mongo_url)
    return client['blacklist']


if __name__ == "__main__":
    blacklist_db = get_database()
    users_collection = blacklist_db["users"]


@bot.event
async def on_ready():
    print("Bot is online")


class AddUserFlags(commands.FlagConverter):  # Flags for the !add command
    nombre: str
    id: str
    perfil: str


@bot.command()
async def ayuda(ctx):
    embed = discord.Embed(
        title="Cómo usar el bot y no parecer un Mateo Cornetta",
        description="El formato para agregar a alguien nuevo a la blacklist es:\n\n!add nombre: [NOMBRE] id: [ID] perfil: [LINK DE GC]\n**Obligatorio adjuntar una captura del perfil**\n\n Ejemplo:",
        color=0x32213a,
    )
    embed.set_image(url="https://i.imgur.com/fgpUIQf.png")
    await ctx.send(embed=embed)


@bot.command()  # Add new user to blacklist command
async def add(ctx, attachment: discord.Attachment, *, flags: AddUserFlags,):
    gcName = flags.nombre
    gcId = flags.id
    gcUrl = flags.perfil
    gcImage = None
    if attachment:
        gcImage = attachment.url

    already_exists = users_collection.find_one({"id": gcId})
    if already_exists:
        return await ctx.send(f'{gcName} ya existe en la **blacklist**.')

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
    await ctx.send(embed=embed)

bot.run(f"{discord_token}")
