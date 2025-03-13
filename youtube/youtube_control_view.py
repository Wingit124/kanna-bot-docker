import discord
import weakref
from typing import Callable, Optional
from youtube.youtube import Youtube
from youtube.youtube_search_modal import YoutubeSearchModal


class YoutubeControlView(discord.ui.View):

    def __init__(self, youtube: Youtube):
        self.youtube: Callable[[], Optional[Youtube]] = weakref.ref(youtube)
        super().__init__(timeout=None)

    async def on_timeout(self) -> None:
        # await self.message.edit(embed=self.youtube.make_embed().set_footer(text='Time out.'), view=None)
        self.clear_items()
        self.anime = None
        return await super().on_timeout()

    @discord.ui.button(label='◀︎◀︎', style=discord.ButtonStyle.blurple)
    async def previous(self, interaction: discord.Interaction, button: discord.ui.button):
        youtube = self.youtube()
        if not youtube:
            return
        youtube.previous()
        await interaction.response.edit_message(embed=youtube.make_embed(), view=self)

    @discord.ui.button(label='追加', style=discord.ButtonStyle.green)
    async def search(self, interaction: discord.Interaction, button: discord.ui.button):
        youtube = self.youtube()
        if not youtube:
            return
        modal = YoutubeSearchModal(youtube=youtube)
        await interaction.response.send_modal(modal)

    @discord.ui.button(label='▶︎▶︎', style=discord.ButtonStyle.blurple)
    async def next(self, interaction: discord.Interaction, button: discord.ui.button):
        youtube = self.youtube()
        if not youtube:
            return
        youtube.next()
        await interaction.response.edit_message(embed=youtube.make_embed(), view=self)