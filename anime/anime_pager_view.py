import discord
from anime.anime import Anime


class AnimePagerView(discord.ui.View):

    def __init__(self, anime: Anime):
        self.anime: Anime = anime
        super().__init__()

    async def on_timeout(self) -> None:
        #await self.message.edit(embed=self.anime.output_embed.set_footer(text='Time out.'), view=None)
        self.clear_items()
        self.anime = None
        return await super().on_timeout()
    
    @discord.ui.button(label='◀︎◀︎', style=discord.ButtonStyle.blurple)
    async def first(self, interaction: discord.Interaction, button: discord.ui.button):
        self.anime.get_anime()
        await interaction.response.edit_message(embed=self.anime.output_embed, view=self)

    @discord.ui.button(label='◀︎', style=discord.ButtonStyle.green)
    async def back(self, interaction: discord.Interaction, button: discord.ui.button):
        if self.anime.prev_page is not None:
            self.anime.get_anime(self.anime.prev_page)
            await interaction.response.edit_message(embed=self.anime.output_embed, view=self)

    @discord.ui.button(label='✖︎', style=discord.ButtonStyle.danger)
    async def delete(self, interaction: discord.Interaction, button: discord.ui.button):
        await interaction.response.edit_message(delete_after=1)

    @discord.ui.button(label='▶︎', style=discord.ButtonStyle.green)
    async def forward(self, interaction: discord.Interaction, button: discord.ui.button):
        if self.anime.next_page is not None:
            self.anime.get_anime(self.anime.next_page)
            await interaction.response.edit_message(embed=self.anime.output_embed, view=self)

    @discord.ui.button(label='▶︎▶︎', style=discord.ButtonStyle.blurple)
    async def last(self, interaction: discord.Interaction, button: discord.ui.button):
        self.anime.get_anime(self.anime.total_count)
        await interaction.response.edit_message(embed=self.anime.output_embed, view=self)