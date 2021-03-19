from discord import Member, TextChannel
from discord.ext.commands import Bot


class EmbedOptionDelegate:
    """
    Abstract class. Anyone who presents an
    embed option should implement.
    """
    async def handle_option_selected(
        self,
        option,
        selected_by: Member,
        in_channel: TextChannel,
        with_bot: Bot
    ):
        raise NotImplementedError("Must be subclassed")
