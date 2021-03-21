import asyncio

from discord import TextChannel, Member
from discord.ext.commands import Bot

from bot.embeds.embed_option_delegate import EmbedOptionDelegate
from bot.embeds.scenes.begin_game import BeginGameEmbed

from utils import Text as T


class BeginGameScene(EmbedOptionDelegate):

    async def show(self, channel: TextChannel, from_bot: Bot):
        embed = BeginGameEmbed(self)
        responses = await embed.send_to(
            channel, from_bot, multiple_responses=True)

        bet_str = 'Place a bet during a betting round to sit at an empty seat'
        lets_play = "LET'S PLAY CRAPS!"
        await channel.send(
            f'{T.bold(lets_play)}\n'
            f'{T.block_quote(bet_str)}'
        )
        return responses

    ##############################
    # EmbedOptionDelegate methods

    async def handle_option_selected(
        self,
        option,
        selected_by: Member,
        in_channel: TextChannel,
        with_bot: Bot
    ):
        print(f"{selected_by.name} selected {option.emoji}")
