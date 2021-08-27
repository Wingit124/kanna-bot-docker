import asyncio
from os import name
import discord
import youtube_dl
from discord.embeds import Embed
from discord.ext import commands
from discord.ext.commands.context import Context

youtube_dl.utils.bug_reports_message = lambda: ''

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

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


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

    @commands.command(name='youtube_play', aliases=['yp'])
    async def youtube_play(self, context: Context, url):

        if not context.message.author.voice:
            await context.send(embed=Embed(title='ボイスチャンネルに参加してね', color=0xff0000))
            return

        if context.voice_client is None:
            await context.message.author.voice.channel.connect()

        player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
        context.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else print('finished'))
        embed: Embed = Embed(title='さいせいちゅう', color=0x00ff00)
        embed.add_field(name='タイトル', value=player.title, inline=True)
        embed.add_field(name='ダウンロード', value='[こちら]({0})'.format(player.url))
        await context.send(embed=embed, color=0x00ff00)

    @commands.command(name='disconnect', aliases=['dc'])
    async def disconnect(self, context: Context):
        await context.send(embed=Embed(title='またね', color=0x0000ff))
        await context.voice_client.disconnect()

def setup(bot):
    return bot.add_cog(YoutubeCog(bot))
