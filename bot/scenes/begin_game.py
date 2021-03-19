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
        responses = await embed.send_to(
            channel, from_bot, multiple_responses=True)

        # just a demo
        for r in responses:
            await channel.send(f'{r.member.mention} wants to play!')

    def create_options(self):
        option = EmbedOption(
            "Signup",
            "sign up to play the game",
            E.THUMBS_UP)
        return [option]

    ##############################
    # EmbedOptionDelegate methods
    async def handle_option_selected(
        self,
        option,
        selected_by: Member,
        in_channel: TextChannel,
        with_bot: Bot
    ):
        await in_channel.send(f"{selected_by.name} selected {option.emoji}")
