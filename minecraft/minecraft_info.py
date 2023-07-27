import os
import boto3
import datetime
from discord.embeds import Embed


class MinecraftInfo:

    STATUS_DICT = {
        'pending' : ':arrows_counterclockwise:起動中',
        'running' : ':green_circle:起動済み',
        'shutting-down' : ':warning:終了中:warning:',
        'terminated' : ':warning:終了済み:warning:',
        'stopping' : ':arrows_counterclockwise:停止中',
        'stopped' : ':red_circle:停止済み'
    }

    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_REGION_NAME = os.environ.get('AWS_REGION_NAME')
    AWS_INSTANCE_ID = os.environ.get('AWS_INSTANCE_ID')
    output_embed: Embed

    instance: any
    status: str

    def __init__(self):
        self.connect()

    def connect(self):
        self.instance = boto3.resource(
            'ec2',
            aws_access_key_id=self.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=self.AWS_SECRET_ACCESS_KEY,
            region_name=self.AWS_REGION_NAME
        ).Instance(self.AWS_INSTANCE_ID)

    def fetch(self) -> Embed:
        self.connect()
        self.status = self.instance.state['Name']
        ipv4 = self.instance.public_ip_address
        embed: Embed = Embed(title='Minecraftサーバー情報', color=0x00b0f4, timestamp=datetime.datetime.utcnow())
        embed.add_field(name='状態', value=self.STATUS_DICT[self.status], inline=True)
        if ipv4:
            embed.add_field(name='IPv4', value=ipv4, inline=True)
            embed.add_field(name='Dynmap', value='[こちら](http://{0}:8123)'.format(ipv4), inline=False)
        embed.set_footer(text='いたずらしないでね;o;')
        return embed
    
    def start(self) -> Embed:
        embed: Embed
        if self.status == 'stopped':
            try:
                self.instance.start()
                embed = self.fetch()
            except:
                embed = self.fetch()
                embed.add_field(name='エラーメッセージ', value='サーバーの起動に失敗したよ。少し時間をおいてからもう一度ためしてね。', inline=False)
        else:
            embed = self.fetch()
            embed.add_field(name='エラーメッセージ', value='サーバーの起動はステータスが停止済みでないと行えません。', inline=False)
        return embed
    
    def stop(self) -> Embed:
        embed: Embed
        if self.status == 'running':
            self.instance.stop()
            embed = self.fetch()
        else:
            embed = self.fetch()
            embed.add_field(name='エラーメッセージ', value='サーバーの停止はステータスが起動済みでないと行えません。', inline=False)
        return embed


