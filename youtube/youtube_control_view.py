import discord
from discord.message import Message
from youtube.youtube import Youtube
from youtube.youtube_search_modal import YoutubeSearchModal


class YoutubeControlView(discord.ui.View):

    youtube: Youtube

    def __init__(self, youtube: Youtube):
        self.youtube = youtube
        super().__init__(timeout=None)

    async def on_timeout(self) -> None:
        # await self.message.edit(embed=self.youtube.make_embed().set_footer(text='Time out.'), view=None)
        self.clear_items()
        self.anime = None
        return await super().on_timeout()

    @discord.ui.button(label='◀︎◀︎', style=discord.ButtonStyle.blurple)
    async def previous(self, interaction: discord.Interaction, button: discord.ui.button):
        self.youtube.previous()
        await interaction.response.edit_message(embed=self.youtube.make_embed(), view=self)

    @discord.ui.button(label='追加', style=discord.ButtonStyle.green)
    async def search(self, interaction: discord.Interaction, button: discord.ui.button):
        modal = YoutubeSearchModal(youtube=self.youtube)
        await interaction.response.send_modal(modal)

    @discord.ui.button(label='▶︎▶︎', style=discord.ButtonStyle.blurple)
    async def next(self, interaction: discord.Interaction, button: discord.ui.button):
        self.youtube.next()
        await interaction.response.edit_message(embed=self.youtube.make_embed(), view=self)