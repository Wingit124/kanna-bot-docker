import discord
from discord import message
from discord.ui import view
from anime.anime import Anime


class AnimePagerView(discord.ui.View):

    anime: Anime

    def __init__(self):
        super().__init__()
        self.value = None
    
    @discord.ui.button(label='◀︎◀︎', style=discord.ButtonStyle.blurple)
    async def first(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.anime.get_anime()
        await interaction.message.edit(embed=self.anime.output_embed, view=self)

    @discord.ui.button(label='◀︎', style=discord.ButtonStyle.green)
    async def back(self, button: discord.ui.Button, interaction: discord.Interaction):
        if self.anime.prev_page is not None:
            self.anime.get_anime(self.anime.prev_page)
            await interaction.message.edit(embed=self.anime.output_embed, view=self)

    @discord.ui.button(label='-', style=discord.ButtonStyle.danger)
    async def delete(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.message.delete()

    @discord.ui.button(label='▶︎', style=discord.ButtonStyle.green)
    async def forward(self, button: discord.ui.Button, interaction: discord.Interaction):
        if self.anime.next_page is not None:
            self.anime.get_anime(self.anime.next_page)
            await interaction.message.edit(embed=self.anime.output_embed, view=self)

    @discord.ui.button(label='▶︎▶︎', style=discord.ButtonStyle.blurple)
    async def last(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.anime.get_anime(self.anime.total_count)
        await interaction.message.edit(embed=self.anime.output_embed, view=self)