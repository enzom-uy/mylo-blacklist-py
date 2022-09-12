import os
import discord
from discord.ext import commands
from cogs.add import get_database
from discord.utils import get

discord_token = os.environ.get('DISCORD_BLACKLIST_TOKEN')
mongo_url = os.environ.get('MONGO_BLACKLIST_URL')
mylo_token = 495778166611116042


class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=discord.Intents.all(),
            application_id=1017652191512756256,
            activity=discord.Game(name="!ayuda o /add")
        )
        self.initial_extensions = ["cogs.ayuda", "cogs.add", "cogs.search"]

    async def setup_hook(self):
        for ext in self.initial_extensions:
            await self.load_extension(ext)
        await bot.tree.sync(guild=discord.Object(id=495778166611116042))

    async def on_ready(self):
        print(f"{self.user} has connected to Discord!")


bot = MyBot()


@bot.command(pass_context=True)
async def clear(ctx, number):
    number = int(number)
    await ctx.channel.purge(limit=number)


@bot.command()
async def blacklist(ctx):
    db = get_database()
    users_collection = db["users"]
    users = users_collection.find()
    users_names = []

    for user in users:
        users_names.append(user["nombre"])

    stringified_users_names = " \n".join(users_names)
    await ctx.send(stringified_users_names)

bot.run(f"{discord_token}")
