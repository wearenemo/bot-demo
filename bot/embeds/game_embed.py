import asyncio
from datetime import datetime as dt

from discord import Embed, Colour, Member
from discord.abc import Messageable
from discord.ext.commands import Bot

from bot.embeds.embed_option import EmbedOption
from bot.embeds.embed_option_delegate import EmbedOptionDelegate
from bot.embeds.option_response import EmbedOptionResponse


class GameEmbed(Embed):

    default_colour = Colour.dark_red()
    default_footer_text = "make your choice by reacting"
    default_timeout = 15.0

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

        super().__init__(title=title, description=description, **kwargs)

        self._options = []
        self._option_delegate = option_delegate

        if not timeout:
            self.timeout = self.default_timeout

        if options:
            self.add_options(options)

    def add_option(self, option: EmbedOption):
        if self.option_delegate:
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

    async def send_to(self,
                      channel: Messageable,
                      from_bot: Bot,
                      multiple_responses=False):
        sent_msg = await channel.send(embed=self)
        listen_emojis = {}
        for opt in self.options:
            listen_emojis[opt.emoji] = opt
            await sent_msg.add_reaction(opt.emoji)

        # this is a common pattern in bot world.
        # look into bot.wait_for documentation for info
        def check(rxn, user):
            if user.id == from_bot.user.id:
                return False
            if not isinstance(user, Member):
                return False
            if rxn.message != sent_msg:
                return False
            return str(rxn.emoji) in listen_emojis

        responses = []
        start = dt.utcnow()
        try:
            # main loop to collect responses until timeout
            # or we get response (if multiple_responses==False)
            while True:

                # Just being safe
                elapsed = (dt.utcnow() - start).total_seconds()
                if elapsed > self.timeout:
                    raise asyncio.TimeoutError()

                # Wait for next response
                timeout = self.timeout - elapsed
                rxn, member = await from_bot.wait_for(
                    'reaction_add',
                    check=check,
                    timeout=timeout)

                # get corresponding option for response
                option = listen_emojis.get(str(rxn.emoji))
                if not option:
                    raise ValueError("weird")

                # call response handler
                await option.on_selected(member, channel, from_bot)

                # create response object
                response = EmbedOptionResponse(option, member)
                if multiple_responses:
                    responses.append(response)
                else:
                    return response

        except asyncio.TimeoutError:
            if multiple_responses:
                return responses
            else:
                return None

    @property
    def options(self):
        return self._options

    @property
    def option_delegate(self):
        return self._option_delegate
