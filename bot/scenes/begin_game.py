from discord import TextChannel, Member
from discord.ext.commands import Bot

from bot.embeds.embed_option_delegate import EmbedOptionDelegate
from bot.embeds.scenes.begin_game import BeginGameEmbed


class BeginGameScene(EmbedOptionDelegate):

    async def show(self, channel: TextChannel, from_bot: Bot):
        embed = BeginGameEmbed(self)
        responses = await embed.send_to(
            channel, from_bot, multiple_responses=True)

        # just a demo
        for r in responses:
            await channel.send(f'{r.member.mention} wants to play!')
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
        await in_channel.send(f"{selected_by.name} selected {option.emoji}")
