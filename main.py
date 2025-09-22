import os
from dotenv import load_dotenv
import ctypes.util
import asyncio
import discord
from discord.ext import commands
from help.help_command import CustomHelpCommand

load_dotenv()

TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
OPUS_PATH = os.environ.get('OPUS_PATH')

EXTENSIONS = [
    'anime.anime_cog',
    'youtube.youtube_cog'
]

intents = discord.Intents.default()
intents.members = False
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix='d:', case_insensitive=False, intents=intents, help_command=CustomHelpCommand())

@bot.event
async def on_ready():
    print('[INFO] Logged in as {0}!'.format(bot.user.name))
    # OPUS読み込み
    if not discord.opus.is_loaded():
        opus_path = ctypes.util.find_library("opus") or OPUS_PATH
        print(f"[INFO] Loading opus from: {opus_path}")
        discord.opus.load_opus(opus_path)
        print(f"[INFO] Opus loaded: {discord.opus.is_loaded()}")
    # スラッシュコマンド同期
    synced = await bot.tree.sync()
    print(f"[INFO] Synced {len(synced)} slash commands.")

async def load_extensions():
    for cog in EXTENSIONS:
        await bot.load_extension(cog)

async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

asyncio.run(main())