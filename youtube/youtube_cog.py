import discord
from discord import app_commands
from discord.ext import tasks
from discord.ext import commands
from youtube.youtube import Youtube
from youtube.youtube_control_view import YoutubeControlView

class YoutubeCog(commands.Cog):

    youtubes: dict[Youtube] = {}

    def __init__(self, bot):
        self.bot: commands.Bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Successfully loaded: YoutubeCog')
        self.check_update.start()
        await self.bot.tree.sync()

    @app_commands.command(name='youtube', description='Youtubeの動画を再生するよ')
    async def youtube(self, context: discord.Interaction):

        await context.response.defer(thinking=True)

        if context.user.voice is None:
            await context.followup.send('ボイスチャンネルに参加してね', ephemeral=True)
            return

        if context.guild.voice_client is None:
            await context.user.voice.channel.connect()

        if not context.guild.id in self.youtubes:
            self.youtubes[context.guild.id] = Youtube(client=context.guild.voice_client)

        # ViewとEmbedを生成
        youtube: Youtube = self.youtubes.get(context.guild.id)
        embed = youtube.make_embed()
        view = YoutubeControlView(youtube=youtube)
        # すでにセッションに紐づいたメッセージがある場合は先に消しておく
        await self.delete_message(youtube=youtube)
        # メッセージを送信
        message = await context.followup.send(embed=embed, view=view)
        youtube.message = message

    @app_commands.command(name='bye', description='ボイスチャンネルから抜けるよ')
    async def disconnect(self, context: discord.Interaction):
        # セッションをリセット
        youtube: Youtube = self.youtubes.pop(context.guild.id)
        await self.delete_message(youtube=youtube)

        # ボイスチャンネルに接続してるか
        if context.guild.voice_client is None:
            await context.response.send_message('ボイスチャンネルに参加してないよ', ephemeral=True)
        else:
            await context.response.send_message('またね', ephemeral=True)
            await context.guild.voice_client.disconnect()

    @tasks.loop(seconds=3)
    async def check_update(self):
        for youtube in self.youtubes.values():
            try:
                message: discord.Message = youtube.message
                if message:
                    channel = await self.bot.fetch_channel(message.channel.id)
                    if channel:
                        message = await channel.fetch_message(message.id)
                        if message:
                            await message.edit(embed=youtube.make_embed())
            except:
                pass
                    
    async def delete_message(self, youtube: Youtube):
        try:
            message: discord.Message = youtube.message
            if message:
                channel = await self.bot.fetch_channel(message.channel.id)
                if channel:
                    message = await channel.fetch_message(message.id)
                    if message:
                        await message.delete()
        except:
            pass


def setup(bot):
    return bot.add_cog(YoutubeCog(bot))
