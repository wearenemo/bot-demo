import asyncio

from discord import Embed, Colour, Member
from discord.abc import Messageable
from discord.ext.commands import Bot

from bot.embeds.embed_option import EmbedOption
from bot.embeds.embed_option_delegate import EmbedOptionDelegate

from utils import Emoji as E


class GameEmbed(Embed):

    default_colour = Colour.dark_red()
    default_footer_text = "make your choice by reacting"
    default_timeout = 120.0  # 2 mins

    def __init__(
        self,
        title: str,
        description: str,
        option_delegate: EmbedOptionDelegate = None,
        options: [EmbedOption] = None,
        timeout: float = None,
        **kwargs
    ):

        if "colour" not in kwargs and "color" not in kwargs:
            kwargs['colour'] = self.default_colour

        # del kwargs['title']
        # del kwargs['description']
        super().__init__(title=title, description=description, **kwargs)

        self._options = []
        self._option_delegate = option_delegate

        if not timeout:
            self.timeout = self.default_timeout

        if options:
            self.add_options(options)

    def add_option(self, option: EmbedOption):
        if self.option_delegate:
            print("SETTING OPTION DELGATE")
            option.set_delegate(self.option_delegate)
        self._options.append(option)
        self.add_field(
            name=option.field_name,
            value=option.field_value,
            inline=option.inline)

        # set the footer if its not set
        if not self.footer or self.footer == Embed.Empty:
            self.set_footer(text=self.default_footer_text)

    def add_options(self, options: [EmbedOption]):
        for opt in options:
            self.add_option(opt)

    async def send_to(self, channel: Messageable, from_bot: Bot):
        sent_msg = await channel.send(embed=self)
        listen_emojis = {}
        for opt in self.options:
            listen_emojis[opt.emoji] = opt
            await sent_msg.add_reaction(opt.emoji)

        def check(rxn, user):
            if user.id == from_bot.user.id:
                return False
            if not isinstance(user, Member):
                return False
            if rxn.message != sent_msg:
                return False
            return str(rxn.emoji) in listen_emojis

        try:
            rxn, member = await from_bot.wait_for(
                'reaction_add',
                check=check,
                timeout=self.timeout)

            option = listen_emojis.get(str(rxn.emoji))
            if not option:
                raise ValueError("weird")

            return await option.on_selected(member, channel, from_bot)

        except asyncio.TimeoutError:
            await sent_msg.clear_reactions()
            await sent_msg.add_reaction(E.HOURGLASS)

    @property
    def options(self):
        return self._options

    @property
    def option_delegate(self):
        return self._option_delegate
