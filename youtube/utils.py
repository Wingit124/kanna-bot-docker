from discord.embeds import Embed
import asyncio
import os
import yt_dlp
import discord

yt_dlp.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': True,
    'logtostderr': False,
    'quiet': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0', 
    'reconnect': True,
    'reconnect_streamed': True,
    'reconnect_delay_max': 5,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'config_location': os.path.join(os.getcwd(), 'yt-dlp.conf')
}

ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn -sn'
}

ytdl = yt_dlp.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.1):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def data_from_url(cls, url, loop=None, stream=True):
        try:
            loop = loop or asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

            if 'entries' in data:
                # take first item from a playlist
                data = data['entries'][0]
            
            return data
        except Exception as e:
            print(f"[ERROR] Error in YTDLSource.data_from_url {e}")
            return None
    
    @classmethod
    def make_player(cls, data, stream=True):
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)