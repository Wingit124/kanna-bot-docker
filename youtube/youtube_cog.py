import asyncio
from os import name
import discord
import yt_dlp
from discord import app_commands
from discord.embeds import Embed
from discord.ext import commands
from discord.ext.commands.context import Context

yt_dlp.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = yt_dlp.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.1):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class YoutubeCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Successfully loaded: YoutubeCog')
        await self.bot.tree.sync()

    @app_commands.command(name='youtube', description='指定したYoutubeの動画を再生するよ')
    async def youtube_play(self, context: discord.Interaction, url: str):

        await context.response.defer(thinking=True)

        if context.user.voice is None:
            await context.response.send_message('ボイスチャンネルに参加してね', ephemeral=True)
            return

        if context.guild.voice_client is None:
            await context.user.voice.channel.connect()

        player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
        context.guild.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else print('finished'))
        embed: Embed = Embed(title='再生中:notes:', color=0x00ff00)
        embed.add_field(name='タイトル', value=player.title, inline=False)
        embed.add_field(name='ダウンロード', value='[こちら]({0})'.format(player.url))
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
