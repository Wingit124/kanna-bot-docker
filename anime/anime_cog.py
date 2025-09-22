import discord
from discord import app_commands
from discord.ext import commands
from anime.anime import Anime
from anime.anime_pager_view import AnimePagerView


class AnimeCog(commands.Cog):

    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @app_commands.command(name='anime', description='タイトルからアニメの情報を調べるよ')
    async def search_anime(self, context: discord.Interaction, title: str):
        anime: Anime = Anime(title)
        if anime.get_anime():
            view: AnimePagerView = AnimePagerView(anime)
            await context.response.send_message(embed=anime.output_embed, view=view) 
        else:
            await context.response.send_message(anime.error, ephemeral=True)

    async def cog_load(self):
        print('[INFO] Successfully loaded: AnimeCog')

def setup(bot):
    return bot.add_cog(AnimeCog(bot))
