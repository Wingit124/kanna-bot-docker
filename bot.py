from discord.ext.commands import Bot
from othello import othello


TOKEN = 'ODczNDQyODg1NjI0NzkxMDgx.YQ4fEw.niRIHtJN2FD_Q9mN2ge-NRuLB0Y'

bot = Bot(command_prefix=['d:','D:'])
bot.load_extension('othello.othello_cog')


@bot.event
async def on_ready():
    print('Logged in as {0}!'.format(bot.user.name))

bot.run(TOKEN)
