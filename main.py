import os
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


@bot.command()  # Add new user to blacklist command
async def add(ctx, attachment: discord.Attachment | None, *, flags: AddUserFlags,):
    gcName = flags.nombre
    gcId = flags.id
    gcUrl = flags.perfil
    gcImage = None
    if attachment:
        gcImage = attachment.url
    else:
        gcImage = ""

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
    await ctx.send(f'Se agregó al pete de {gcName}, con GC ID: {gcId} a la blacklist. {gcImage}')

bot.run(f"{discord_token}")
