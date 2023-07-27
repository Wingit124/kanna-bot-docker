import os
from dotenv import load_dotenv
import asyncio
import discord
from discord.ext import commands
from help.help_command import CustomHelpCommand

load_dotenv()

TOKEN = os.environ.get('DISCORD_BOT_TOKEN')

EXTENSIONS = [
    'anime.anime_cog',
    'minecraft.minecraft_cog'
]

intents = discord.Intents.default()
intents.members = False
intents.message_content = True

bot = commands.Bot(command_prefix='d:', case_insensitive=False, intents=intents, help_command=CustomHelpCommand())

@bot.event
async def on_ready():
    print('Logged in as {0}!'.format(bot.user.name))

async def load_extensions():
    for cog in EXTENSIONS:
        await bot.load_extension(cog)

async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

asyncio.run(main())