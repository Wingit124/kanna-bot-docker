from discord.embeds import Embed
from youtube.utils import YTDLSource
import datetime
import discord
import time

class Youtube:

    MAX_HISTORY_COUNT: int = 5
    PROGRESS_BAR: str = "▬"
    PROGRESS_THUMB: str = '🔘'
    PROGRESS_SIZE: int = 30

    def __init__(self, client: discord.voice_client.VoiceClient) -> None:
        self.message: discord.Message = None
        self.client: discord.voice_client.VoiceClient = client
        # キュー
        self.queue: list[dict] = []
        self.history: list[dict] = []
        self.now_playing: dict = {}
        self.is_user_action: bool = False
        self.play_start_time: time = time.time()

    def add_queue(self, data):
        self.queue.append(data)
        if not self.client.is_playing():
            self.play()
    
    # 再生開始
    def play(self, stream=True):
        # 再生するべきキューが無い場合は中断
        if not self.queue:
            self.now_playing = {}
            return
        # 再生を開始
        if not self.client.is_playing():
            self.now_playing = self.queue[0]
            player = YTDLSource.make_player(data=self.now_playing, stream=stream)
            self.client.play(player, after=lambda e: self.on_error(error=e) if e else self.on_finish())
            self.play_start_time = time.time()
    
    # 曲送り
    def next(self, is_user_action: bool = True):
        if len(self.queue) > 0:
            self.history.append(self.queue.pop(0))
        if len(self.history) > self.MAX_HISTORY_COUNT:
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

    def make_embed(self) -> Embed:
        data: dict = self.now_playing
        # 情報を取得
        title = data.get('title', '')
        original_url = data.get('original_url', '')
        channel_name = data.get('channel', '')
        channel_url = data.get('channel_url', '')
        duration = data.get('duration', 0)
        thumbnail_url = data.get('thumbnail', '')
        progress_bar = self.progress_string()
        queue_list = self.queue_to_string()
        history_list = self.history_to_string()
        queue_count = len(self.queue)
        now = datetime.datetime.now().replace(second=0, microsecond=0)
        # レスポンスを作成
        embed: Embed
        if title:
            embed = Embed(title='"{0}"を再生中:notes:'.format(title), description='', color=0xFF7F7F, timestamp=now)
        else:
            embed = Embed(title='再生待機中:zzz:'.format(title), description='再生待機中だよ`追加`ボタンをクリックして好きな動画をキューに追加してね', color=0xFF7F7F, timestamp=now)
            embed.set_image(url='https://zunda-sleep.win9y.com/kanna_sleep.jpg')
        if progress_bar:
            embed.description = '`{0}`'.format(progress_bar)
        if original_url:
            embed.add_field(name='ビデオ', value='[こちら]({0})'.format(original_url), inline=True)
        if channel_name and channel_url:
            embed.add_field(name='チャンネル', value='[{0}]({1})'.format(channel_name, channel_url), inline=True)
        if duration:
            embed.add_field(name='再生時間', value=self.format_seconds(seconds=duration), inline=True)
        if history_list and not title:
            embed.add_field(name='再生履歴'.format(self.MAX_HISTORY_COUNT), value=history_list, inline=False)
        if queue_list:
            embed.add_field(name='キュー', value=queue_list, inline=False)
        if thumbnail_url:
            embed.set_thumbnail(url=thumbnail_url)
        if queue_count:
            embed.set_footer(text='Playing 1 of {0}'.format(queue_count))
        return embed
    
    def on_error(self, error):
        print('[ERROR] Player error occurred: {0}'.format(error))
        self.next(is_user_action=False)

    def on_finish(self):
        print('[INFO] Player finished')
        if self.is_user_action:
            self.is_user_action = False
        else:
            self.next(is_user_action=False)

    def queue_to_string(self) -> str:
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
    
    def history_to_string(self) -> str:
        output: str = ''
        for data in self.history:
            output += '- {0}({1})\n'.format(data['title'], data['duration_string'])
        return output
    
    def progress_string(self) -> str:
        total_time = self.now_playing.get('duration', 0)
        elapsed_time = time.time() - self.play_start_time
        # 再生時間が0の場合は早期リターン
        if total_time < 1:
            return ''
        # プログレスバーを生成
        elapsed_ratio = elapsed_time / total_time
        index = int(elapsed_ratio * self.PROGRESS_SIZE)
        progress_bar = list(self.PROGRESS_BAR * (self.PROGRESS_SIZE - 1))
        progress_bar.insert(index, self.PROGRESS_THUMB)
        progress_bar = "".join(progress_bar)
        # 時間をフォーマット
        total_time = self.format_seconds(seconds=int(total_time))
        elapsed_time = self.format_seconds(seconds=int(elapsed_time), reference_format=total_time)
        return '{0} [{1}] {2}'.format(elapsed_time, progress_bar, total_time)


    def format_seconds(self, seconds: int, reference_format: str = None):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        # 参考にするフォーマットがある場合は参考にする
        digits_count = 0
        if reference_format:
            digits_count = reference_format.count(':')
        # フォーマットをそろえて出力する
        list = []
        if hours or digits_count > 1:
            list.append(f"{int(hours):02}")
        list.append(f"{int(minutes):02}")
        list.append(f"{int(seconds):02}")
        return ':'.join(list)
        