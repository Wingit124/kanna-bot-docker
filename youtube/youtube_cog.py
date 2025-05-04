import discord
from discord import app_commands
from discord.ext import tasks
from discord.ext import commands
from asyncio import create_task
from youtube.youtube import Youtube
from youtube.youtube_control_view import YoutubeControlView

class YoutubeCog(commands.Cog):

    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.youtubes: dict[int, Youtube] = {}
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('[INFO] Successfully loaded: YoutubeCog')
        self.update_message.start()
        self.refresh_message_token.start()
        self.check_task.start()
        await self.bot.tree.sync()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        # ボイスチャンネルにBot以外がいなくなったら切断する
        voice_client = member.guild.voice_client
        if voice_client and len([member for member in voice_client.channel.members if not member.bot]) == 0:
            # 切断
            await voice_client.disconnect()
            # メッセージを削除
            youtube: Youtube = self.youtubes.pop(member.guild.id)
            await self.delete_message(youtube=youtube)

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
    async def update_message(self):
        try:
            for youtube in self.youtubes.values():
                # 編集中かどうか
                if youtube.is_editing:
                    print(f"[NOTICE] YoutubeCog.edit_message: edit message skipped")
                    continue
                # メッセージがあるか
                message: discord.Message = youtube.message
                if not message:
                    continue
                # メッセージを編集
                youtube.is_editing = True
                youtube.message = await message.edit(embed=youtube.make_embed())
                youtube.is_editing = False
        except Exception as e:
            print(f"[ERROR] YoutubeCog.update_message: {e}")

    @tasks.loop(seconds=300)
    async def refresh_message_token(self):
        try:
            for youtube in self.youtubes.values():
                message: discord.Message = youtube.message
                if not message:
                    return
                channel = await self.bot.fetch_channel(message.channel.id)
                if not channel:
                    return
                fetched_message = await channel.fetch_message(message.id)
                if not fetched_message:
                    return
                youtube.message = fetched_message
        except Exception as e:
            print(f"[ERROR] YoutubeCog.refresh_message_token{e}")
    
    @tasks.loop(seconds=10)
    async def check_task(self):
        if not self.update_message.is_running:
            self.update_message.restart()
        if not self.refresh_message_token.is_running:
            self.refresh_message_token.restart()
                    
    async def delete_message(self, youtube: Youtube):
        try:
            message: discord.Message = youtube.message
            if not message:
                return
            channel = await self.bot.fetch_channel(message.channel.id)
            if not channel:
                return
            message = await channel.fetch_message(message.id)
            if not message:
                return
            await message.delete()
        except Exception as e:
            print(f"[ERROR] YoutubeCog.delete_message{e}")


def setup(bot):
    return bot.add_cog(YoutubeCog(bot))
