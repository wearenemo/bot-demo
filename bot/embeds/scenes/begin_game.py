from utils import Text as T
from utils import Emoji as E

from bot.embeds.game_embed import GameEmbed
from bot.embeds.embed_option import EmbedOption
from bot.embeds.embed_option_delegate import EmbedOptionDelegate


class BeginGameEmbed(GameEmbed):
    def __init__(self, option_delegate: EmbedOptionDelegate):
        super().__init__(
            T.bold("Let's play craps!"),
            "please!",
            option_delegate=option_delegate)
        options = self.create_options()
        self.add_options(options)

    def create_options(self):
        option = EmbedOption(
            "Signup",
            "sign up to play the game",
            E.THUMBS_UP)
        return [option]
