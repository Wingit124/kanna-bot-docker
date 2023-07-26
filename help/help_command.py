from discord.ext import commands

class CustomHelpCommand(commands.DefaultHelpCommand):
    def __init__(self):
        super().__init__()
        self.commands_heading = "コマンド:"
        self.no_category = "カテゴリなし"
        self.command_attrs["help"] = "このメッセージを表示"

    def get_ending_note(self):
        return ("すべてスラッシュコマンドに移行したよ")