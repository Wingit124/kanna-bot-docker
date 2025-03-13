import discord
from discord import app_commands
from discord.ext import commands
from minecraft.minecraft_info import MinecraftInfo
from minecraft.minecraft_info_view import MinecraftInfoView

class MinecraftCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('[INFO] Successfully loaded: MinecraftCog')
        await self.bot.tree.sync()

    @app_commands.command(name='minecraft', description='マインクラフトサーバーのインスタンス情報を表示するよ')
    @app_commands.checks.has_any_role(556435235999449106)
    async def fetch_minecraft_info(self, context: discord.Interaction):
        info: MinecraftInfo = MinecraftInfo()
        view: MinecraftInfoView = MinecraftInfoView(info)
        await context.response.send_message(embed=info.fetch(), view=view) 

def setup(bot):
    return bot.add_cog(MinecraftCog(bot))
