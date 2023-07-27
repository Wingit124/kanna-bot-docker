import discord
from discord.message import Message
from minecraft.minecraft_info import MinecraftInfo


class MinecraftInfoView(discord.ui.View):

    START_BUTTON_STATUS_DICT = {
        'pending' : False,
        'running' : False,
        'shutting-down' : False,
        'terminated' : False,
        'stopping' : False,
        'stopped' : True
    }

    STOP_BUTTON_STATUS_DICT = {
        'pending' : False,
        'running' : True,
        'shutting-down' : False,
        'terminated' : False,
        'stopping' : False,
        'stopped' : False
    }

    minecraft_info: MinecraftInfo

    def __init__(self, minecraft_info: MinecraftInfo):
        self.minecraft_info = minecraft_info
        super().__init__()

    async def on_timeout(self) -> None:
        #await self.message.edit(embed=self.anime.output_embed.set_footer(text='Time out.'), view=None)
        self.clear_items()
        self.minecraft_info = None
        return await super().on_timeout()
    
    @discord.ui.button(label='起動', style=discord.ButtonStyle.green, custom_id='start')
    async def start(self, interaction: discord.Interaction, button: discord.ui.button):
        button.disabled = True
        embed = self.minecraft_info.start()
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label='停止', style=discord.ButtonStyle.danger, custom_id='stop')
    async def stop(self, interaction: discord.Interaction, button: discord.ui.button):
        button.disabled = True
        embed = self.minecraft_info.stop()
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label='更新', style=discord.ButtonStyle.grey, custom_id='refresh')
    async def refresh(self, interaction: discord.Interaction, button: discord.ui.button):
        embed = self.minecraft_info.fetch()
        self.sync_button_status()
        await interaction.response.edit_message(embed=embed, view=self)

    def sync_button_status(self):
        for button in self.children:
            if button.custom_id == 'start':
                button.disabled = not self.START_BUTTON_STATUS_DICT[self.minecraft_info.status]
            elif button.custom_id == 'stop':
                button.disabled = not self.STOP_BUTTON_STATUS_DICT[self.minecraft_info.status]