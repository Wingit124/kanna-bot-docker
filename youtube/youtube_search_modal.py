import discord
import discord.ui.modal
from youtube.utils import YTDLSource
from youtube.youtube import Youtube


class YoutubeSearchModal(discord.ui.Modal, title='動画をキューに追加'):

    youtube: Youtube

    def __init__(self, youtube: Youtube):
        self.youtube = youtube
        super().__init__(timeout=None)

    url = discord.ui.TextInput(
        label='Youtubeのリンクかキーワードを入力してね',
        placeholder='https://www.youtube.com/watch?v=..., 青空のラプソディ...',
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer(thinking=True)
        data = await YTDLSource.data_from_url(url=self.url.value)
        self.youtube.add_queue(data=data)
        await interaction.followup.edit_message(message_id=self.youtube.message.id, embed=self.youtube.make_embed())
        await interaction.delete_original_response()