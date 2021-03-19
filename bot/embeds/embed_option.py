from discord import Member, TextChannel, Emoji
from discord.ext.commands import Bot

from bot.embeds.embed_option_delegate import EmbedOptionDelegate

from utils import Text as T


class EmbedOption:
    """
    A selectable option to include in a GameEmbed

    Each EmbedOption will be added as a "field" on that embed
    """

    def __init__(self,
                 name: str,
                 value: str,
                 emoji: str,
                 inline: bool = True,
                 delegate: EmbedOptionDelegate = None):
        """
        @params
            name      required for creating a "field" in an Embed
            value     also required
            emoji     used as the "button" representation of this option
            inline    optional for creating field
            delegate  handles selection events
        """
        self._name = name
        self._value = value
        self._emoji = emoji
        self.inline = inline
        self._delegate = delegate

    @property
    def emoji(self):
        return self._emoji

    @property
    def name(self):
        return self._name

    @property
    def delegate(self):
        return self._delegate

    @property
    def field_name(self):
        return f'{self.emoji} {T.bold(self.name)}'

    @property
    def field_value(self):
        return self._value

    def set_delegate(self, delegate: EmbedOptionDelegate):
        if self.delegate:
            raise ValueError("option delegate already set")
        self._delegate = delegate

    async def on_selected(
        self,
        by: Member,
        in_channel: TextChannel,
        with_bot: Bot
    ):
        if self.delegate:
            return await self.delegate.handle_option_selected(
                self, by, in_channel, with_bot)
        else:
            raise NotImplementedError(
                "No delegate set and EmbedOption not subclassed")
