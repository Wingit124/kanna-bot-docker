from discord.ext import commands
import requests


class AnimeCog(commands.Cog):

    # 初期化処理
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['test'])
    async def test(self, context):
        await context.send('つかれたー')

def setup(bot):
    return bot.add_cog(AnimeCog(bot))
