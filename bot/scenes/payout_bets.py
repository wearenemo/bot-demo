class PayoutBetsScene:
    async def show(
        self,
        bot,
        payouts,
        table,
        dice,
        outcome,
        channel
    ):
        await channel.send(
            f'Outcome was {outcome} from {dice}.')
