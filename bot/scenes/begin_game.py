from discord import TextChannel, Member
from discord.ext.commands import Bot

from utils import Text as T
from utils import Emoji as E

from bot.embeds.game_embed import GameEmbed
from bot.embeds.embed_option import EmbedOption
from bot.embeds.embed_option_delegate import EmbedOptionDelegate

class BeginGameScene(EmbedOptionDelegate):

    async def show(self, channel: TextChannel, from_bot: Bot):
        embed = GameEmbed(
            T.bold("Let's play craps!"),
            "please!",
            option_delegate=self
        )
        options = self.create_options()
        embed.add_options(options)
        await embed.send_to(channel, from_bot)

    def create_options(self):
        option = EmbedOption(
            "Signup",
            "sign up to play the game",
            E.THUMBS_UP)
        return [option]

    async def handle_option_selected(
        self,
        option,
        selected_by: Member,
        in_channel: TextChannel,
        with_bot: Bot
    ):
        print("delegate method called")
        await in_channel.send(f"selected {option.emoji}")
