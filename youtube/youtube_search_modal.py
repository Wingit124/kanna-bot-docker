import discord
import weakref
from typing import Callable, Optional
import discord.ui.modal
from youtube.utils import YTDLSource
from youtube.youtube import Youtube


class YoutubeSearchModal(discord.ui.Modal, title='動画をキューに追加'):

    def __init__(self, youtube: Youtube):
        self.youtube: Callable[[], Optional[Youtube]] = weakref.ref(youtube)
        super().__init__(timeout=None)

    url = discord.ui.TextInput(
        label='Youtubeのリンクかキーワードを入力してね',
        placeholder='https://www.youtube.com/watch?v=..., 青空のラプソディ...',
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        print(f"[INFO] Queue added '{self.url.value}' by {interaction.user.name}")
        await interaction.response.defer(thinking=True, ephemeral=True)
        data = await YTDLSource.data_from_url(url=self.url.value)
        if not data:
            return
        youtube = self.youtube()
        if youtube:
            youtube.add_queue(data=data)
            await interaction.followup.edit_message(message_id=youtube.message.id, embed=youtube.make_embed())
            await interaction.delete_original_response()
        else:
            await interaction.followup.send("動画が見つからなかったよ", ephemeral=True)
        