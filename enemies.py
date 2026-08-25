"""Enemy classes for the first survival horror encounters.

Each subclass changes only its statistics. Students can add an enemy by
following the same small constructor pattern.
"""

from characters import Character


class Enemy:
    """Base class for something a character can fight."""

    def __init__(self, name, health, damage, coin_reward):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("An enemy needs a name.")
        self._require_positive(health, "Health")
        self._require_positive(damage, "Damage")
        self._require_non_negative(coin_reward, "Coin reward")

        self.name = name
        self.maximum_health = health
        self.health = health
        self.damage = damage
        self.coin_reward = coin_reward

    @property
    def is_alive(self):
        return self.health > 0

    def take_damage(self, amount):
        self._require_non_negative(amount, "Damage")
        old_health = self.health
        self.health = max(0, self.health - amount)
        return old_health - self.health

    def attack(self, character):
        if not isinstance(character, Character):
            raise ValueError("An enemy can only attack a Character object.")
        return character.take_damage(self.damage)

    @staticmethod
    def _require_non_negative(value, field_name):
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise ValueError(f"{field_name} must be a non-negative whole number.")

    @classmethod
    def _require_positive(cls, value, field_name):
        cls._require_non_negative(value, field_name)
        if value == 0:
            raise ValueError(f"{field_name} must be greater than zero.")


class Zombie(Enemy):
    def __init__(self):
        super().__init__("Zombie", health=45, damage=8, coin_reward=20)


class Runner(Enemy):
    def __init__(self):
        super().__init__("Runner", health=30, damage=10, coin_reward=25)


class Brute(Enemy):
    def __init__(self):
        super().__init__("Brute", health=80, damage=14, coin_reward=50)


def default_enemies():
    return [Zombie(), Runner(), Brute()]

