import discord
from discord.ext import commands


mylo_token = 495778166611116042


class Ayuda(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    async def ayuda(self, ctx):
        embed = discord.Embed(
            title="Cómo usar el bot y no parecer un Mateo Cornetta",
            description="El formato para agregar a alguien nuevo a la blacklist es:\n\n!add nombre: [NOMBRE] id: [ID] perfil: [LINK DE GC]\n**Obligatorio adjuntar una captura del perfil**\n\n Ejemplo:",
            color=0x32213a,
        )
        embed.set_image(url="https://i.imgur.com/fgpUIQf.png")
        await ctx.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        Ayuda(bot),
        guilds=[discord.Object(id=mylo_token)]
    )
