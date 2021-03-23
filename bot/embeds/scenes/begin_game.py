from utils import Text as T
from utils import Emoji as E

from bot.embeds.game_embed import GameEmbed
from bot.embeds.embed_option import EmbedOption
from bot.embeds.embed_option_delegate import EmbedOptionDelegate


class BeginGameEmbed(GameEmbed):
    def __init__(self, option_delegate: EmbedOptionDelegate):
        super().__init__(
            T.bold("What's the haps?!"),
            "We're playing craps!",
            option_delegate=option_delegate)
        options = self.create_options()
        self.add_options(options)

    def create_options(self):
        option1 = EmbedOption(
            "Haps?",
            "Let's play Craps! 💰",
            E.THUMBS_UP)

        option2 = EmbedOption(
            "FOMO",
            "Oh no... 😭",
            E.THUMBS_DOWN)
        return [option1, option2]
