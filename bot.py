from discord.ext.commands import Bot
from youtube import youtube
from othello import othello
from anime import anime


TOKEN = 'ODczNDQyODg1NjI0NzkxMDgx.YQ4fEw.niRIHtJN2FD_Q9mN2ge-NRuLB0Y'

bot = Bot(command_prefix=['d:','D:'])
bot.load_extension('youtube.youtube_cog')
bot.load_extension('othello.othello_cog')
bot.load_extension('anime.anime_cog')


@bot.event
async def on_ready():
    print('Logged in as {0}!'.format(bot.user.name))

bot.run(TOKEN)
