from dataclasses import dataclass

from discord import Member

from bot.embeds.embed_option import EmbedOption


@dataclass
class EmbedOptionResponse:
    option: EmbedOption
    member: Member
