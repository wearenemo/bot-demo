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
