from os import name
import discord
from discord import app_commands
from discord.embeds import Embed
from discord.ext import commands
from youtube.utils import YTDLSource
from youtube.youtube import Youtube

class YoutubeCog(commands.Cog):

    youtubes: dict[Youtube] = {}

    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Successfully loaded: YoutubeCog')
        await self.bot.tree.sync()

    @app_commands.command(name='youtube', description='Youtubeの動画を再生するよ')
    async def youtube_play(self, context: discord.Interaction, title_or_url: str):

        await context.response.defer(thinking=True)

        if context.user.voice is None:
            await context.response.send_message('ボイスチャンネルに参加してね', ephemeral=True)
            return

        if context.guild.voice_client is None:
            await context.user.voice.channel.connect()

        if not context.guild.id in self.youtubes:
            self.youtubes[context.guild.id] = Youtube(client=context.guild.voice_client)

        youtube: Youtube = self.youtubes[context.guild_id]

        data = await YTDLSource.data_from_url(url=title_or_url)
        youtube.add_queue(data=data)
        embed = youtube.play()
        await context.followup.send(embed=embed)

    @app_commands.command(name='bye', description='ボイスチャンネルから抜けるよ')
    async def disconnect(self, context: discord.Interaction):
        if context.guild.voice_client is None:
            await context.response.send_message('ボイスチャンネルに参加してないよ', ephemeral=True)
            return
        await context.response.send_message('またね', ephemeral=True)
        await context.guild.voice_client.disconnect()

def setup(bot):
    return bot.add_cog(YoutubeCog(bot))
