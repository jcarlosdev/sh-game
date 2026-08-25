"""Coin handling for the game.

Most game code only needs to ask a wallet whether it can afford something,
spend coins, or earn coins. The wallet keeps balance validation in one place.
"""


class Wallet:
    """Store a character's coins without allowing a negative balance."""

    def __init__(self, starting_coins=0):
        self._check_amount(starting_coins)
        self._balance = starting_coins

    @property
    def balance(self):
        """Return the number of coins currently available."""
        return self._balance

    def can_afford(self, price):
        """Return True when the wallet contains at least ``price`` coins."""
        self._check_amount(price)
        return self._balance >= price

    def spend(self, amount):
        """Spend coins and return True, or return False when funds are low."""
        self._check_amount(amount)

        if not self.can_afford(amount):
            return False

        self._balance -= amount
        return True

    def earn(self, amount):
        """Add coins to the wallet."""
        self._check_amount(amount)
        self._balance += amount

    @staticmethod
    def _check_amount(amount):
        if not isinstance(amount, int) or isinstance(amount, bool):
            raise ValueError("Coin amounts must be whole numbers.")
        if amount < 0:
            raise ValueError("Coin amounts cannot be negative.")
