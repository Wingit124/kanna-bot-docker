from discord.ext import commands
from anime.anime import Anime
from anime.anime_pager_view import AnimePagerView


class AnimeCog(commands.Cog):
    # 初期化処理
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='search_anime', aliases=['sa'])
    async def search_anime(self, context, title):
        anime: Anime = Anime(title)
        if anime.get_anime():
            view: AnimePagerView = AnimePagerView()
            view.anime = anime
            view.message = await context.send(embed=anime.output_embed, view=view)
        else:
            await context.send(embed=anime.output_embed)

def setup(bot):
    return bot.add_cog(AnimeCog(bot))
