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
    is_playing: bool = False

    def __init__(self, client: discord.voice_client.VoiceClient) -> None:
        self.client = client

    def add_queue(self, data):
        self.queue.append(data)
    
    def play(self, stream=True):
        # 再生するべきキューが無い場合は中断
        data = self.queue[0]
        if not data:
            return
        
        # 再生を開始
        if not self.client.is_playing():
            player = YTDLSource.make_player(data=data, stream=stream)
            self.client.play(player, after=lambda e: self.on_error(error=e) if e else self.on_finish())
        # 情報を取得
        title = data['title'] or ''
        description = ''
        original_url = data['original_url'] or ''
        channel_name = data['channel'] or ''
        channel_url = data['channel_url'] or ''
        duration = data['duration_string'] or ''
        queue_list = self.queue_to_string()
        history_list = self.history_to_string()
        thumbnail_url = data['thumbnail'] or ''
        queue_count = len(self.queue)
        # レスポンスを作成
        embed: Embed = Embed(title='"{0}"を再生中:notes:'.format(title), description=description, color=0xFF7F7F, timestamp=datetime.datetime.now())
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
    
    def play_next(self):
        self.history.append(self.queue[0])
        self.queue.pop(0)
        if len(self.history) > MAX_HISTORY_COUNT:
            self.history.pop(0)
        self.play()
    
    def on_error(self, error):
        print('Player Error: {0}'.format(error))
        self.play_next()

    def on_finish(self):
        print('Player Finish')
        self.play_next()

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

