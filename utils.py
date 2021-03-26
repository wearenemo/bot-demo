class Text:

    @staticmethod
    def bold(s: str):
        return f"**{s}**"

    @staticmethod
    def mono(s: str):
        """
        monospaced string / code
        """
        return f"```\n{s}\n```"

    @staticmethod
    def inline_mono(s):
        return f'`{s}`'

    @staticmethod
    def block_quote(s: str):
        """
        blockquote string

        WARNING: causes remainder of discord
        message to be formatted as quote
        """
        return f">>> {s}"

    @staticmethod
    def quote_lines(s: str):
        """
        alternative to bq

        avoids formatting entire remainder of message as
        block quote.
        """
        line_quote = "> "
        s = line_quote + s
        return line_quote.join(s.splitlines())

    @staticmethod
    def underline(s):
        return f"\_\_{s}\_\_"


class Emoji:

    CHECKMARK    = '✅'
    RED_X        = '❌'
    STOP_SIGN    = '🛑'
    HOURGLASS    = '⌛'
    THUMBS_UP    = '👍'
    THUMBS_DOWN  = '👎'
    QUIET_MONKEY = '🙊'
    ENVELOPE     = '✉️'
    PLAY         = '▶️'
    DIE          = '🎲'
    SLOT_MACHINE = '🎰'
    MONEY_BAG    = '💰'
    MONEY_WINGS  = '💸'
    SAD          = '😭'
    SEVEN        = '7️⃣'
    TEN          = '🔟'
    REFRESH      = '🔄'
    CLOCK        = '🕙'

