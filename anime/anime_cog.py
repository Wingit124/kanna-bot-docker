from discord import embeds
from discord.ext import commands
from anime.anime import Anime
import requests


class AnimeCog(commands.Cog):

    # 初期化処理
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='search_anime', aliases=['sa'])
    async def search_anime(self, context, title):
        await context.send(embed=Anime().get_anime_by_title(title))

def setup(bot):
    return bot.add_cog(AnimeCog(bot))
