from discord.embeds import Embed
from youtube.utils import YTDLSource
import datetime
import discord

MAX_HISTORY_COUNT: int = 5

class Youtube:
    client: discord.voice_client.VoiceClient
    # キュー
    queue: list[dict] = []
    history: list[dict] = []
    now_playing: dict = None
    is_user_action: bool = True

    def __init__(self, client: discord.voice_client.VoiceClient) -> None:
        self.client = client

    def add_queue(self, data):
        self.queue.append(data)
        if not self.client.is_playing():
            self.play()
    
    # 再生開始
    def play(self, stream=True):
        # 再生するべきキューが無い場合は中断
        self.now_playing = self.queue[0]
        if not self.now_playing:
            return
        
        # 再生を開始
        if not self.client.is_playing():
            player = YTDLSource.make_player(data=self.now_playing, stream=stream)
            self.client.play(player, after=lambda e: self.on_error(error=e) if e else self.on_finish())
    
    # 曲送り
    def next(self, is_user_action: bool = True):
        if len(self.queue) > 0:
            self.history.append(self.queue.pop(0))
        if len(self.history) > MAX_HISTORY_COUNT:
            self.history.pop(0)
        self.is_user_action = is_user_action
        self.client.stop()
        self.play()

    # 曲戻し
    def previous(self, is_user_action: bool = True):
        if len(self.history) > 0:
            self.queue.insert(0, self.history.pop())
        self.is_user_action = is_user_action
        self.client.stop()
        self.play()

    def make_embed(self):
        data: dict = {}
        if self.now_playing:
            data = self.now_playing
        # 情報を取得
        title = data.get('title', '')
        original_url = data.get('original_url', '')
        channel_name = data.get('channel', '')
        channel_url = data.get('channel_url', '')
        duration = data.get('duration_string', '')
        thumbnail_url = data.get('thumbnail', '')
        queue_list = self.queue_to_string()
        history_list = self.history_to_string()
        queue_count = len(self.queue)
        # レスポンスを作成
        embed: Embed
        if title:
            embed = Embed(title='"{0}"を再生中:notes:'.format(title), description='', color=0xFF7F7F, timestamp=datetime.datetime.now())
        else:
            embed = Embed(title='再生待機中:zzz:'.format(title), description='再生待機中だよ`/youtube`を使用して好きな動画をキューに追加してね', color=0xFF7F7F, timestamp=datetime.datetime.now())
        if original_url:
            embed.add_field(name='ビデオ', value='[こちら]({0})'.format(original_url), inline=True)
        if channel_name and channel_url:
            embed.add_field(name='チャンネル', value='[{0}]({1})'.format(channel_name, channel_url), inline=True)
        if duration:
            embed.add_field(name='再生時間', value=duration, inline=True)
        if history_list:
            embed.add_field(name='再生履歴'.format(MAX_HISTORY_COUNT), value=history_list, inline=False)
        if queue_list:
            embed.add_field(name='キュー', value=queue_list, inline=False)
        if thumbnail_url:
            embed.set_thumbnail(url=thumbnail_url)
        if queue_count:
            embed.set_footer(text='Playing 1 of {0}'.format(queue_count))
        return embed
    
    def on_error(self, error):
        print('Player Error: {0}'.format(error))
        self.next(is_user_action=False)

    def on_finish(self):
        print('Player Finish')
        if self.is_user_action:
            self.is_user_action = False
        else:
            self.next(is_user_action=False)

    def queue_to_string(self):
        output: str = ''
        display_index: int = 0
        for data in self.queue:
            # 再生中の曲はキューに表示したくない
            if display_index == 0:
                display_index += 1
                continue
            output += '{0}. {1}({2})\n'.format(display_index, data['title'], data['duration_string'])
            display_index += 1
        return output
    
    def history_to_string(self):
        output: str = ''
        for data in self.history:
            output += '- {0}({1})\n'.format(data['title'], data['duration_string'])
        return output

