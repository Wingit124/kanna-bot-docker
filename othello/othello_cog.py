from discord.ext import commands
from othello.othello import Othello
import re

class OthelloCog(commands.Cog):

    othellos = {}

    # 初期化処理
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='othello_start', aliases=['os'])
    async def start(self, context):
        # ctx.channelはTextChannel型
        if not context.channel.id in self.othellos:
            self.othellos[context.channel.id] = Othello()

        if self.othellos[context.channel.id].is_playing:
            await context.send('すでに開始されているゲームがあるよ')
        else:
            self.othellos[context.channel.id].start()
            await context.send(self.othellos[context.channel.id].output)

    @commands.command(name='othello_finish', aliases=['of'])
    async def finish(self, context):
        if self.check_start_othello(context):
            self.othellos[context.channel.id].finish()
            await context.send(self.othellos[context.channel.id].output)
        else:
            await context.send('ゲームが開始されてないよ')

    @commands.command(name='othello_toggle_hint', aliases=['oh'])
    async def toggle_hint(self, context):
        if self.check_start_othello(context):
            self.othellos[context.channel.id].toggle_hint()
            await context.send(self.othellos[context.channel.id].output)
        else:
            await context.send('ゲームが開始されてないよ')

    @commands.command(name='othello_put', aliases=['op'])
    async def put(self, context, position):
        if self.check_start_othello(context):
            if re.compile('^[a-h][0-7]$').search(position):
                y = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'].index(position[0])
                x = ['0','1','2','3','4','5','6','7'].index(position[1])
                print('x={0}, y={1}'.format(x, y))
                self.othellos[context.channel.id].put(x, y)
                await context.send(self.othellos[context.channel.id].output)
            else:
                await context.send('「a～h」「0～7」の範囲内で「a0」のように指定してね')
        else:
            await context.send('ゲームが開始されてないよ')

    def check_start_othello(self, context):
        return context.channel.id in self.othellos and self.othellos[context.channel.id]

def setup(bot):
    return bot.add_cog(OthelloCog(bot))
