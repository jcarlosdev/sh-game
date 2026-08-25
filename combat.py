"""Turn-based battle actions and an optional interactive battle loop.

The action methods make combat useful as building blocks. ``run()`` adds menus
to those same methods to produce a complete initial encounter.
"""

import random

from characters import Character
from enemies import Enemy
from items import Firearm, RecoveryItem, Weapon


class BattleResult:
    """Readable result values for connecting battles to future game scenes."""

    VICTORY = "victory"
    DEFEAT = "defeat"
    ESCAPED = "escaped"


class Battle:
    """Coordinate one character and one enemy until their encounter ends."""

    def __init__(self, character, enemy, random_source=None):
        if not isinstance(character, Character):
            raise ValueError("A battle needs a Character object.")
        if not isinstance(enemy, Enemy):
            raise ValueError("A battle needs an Enemy object.")

        self.character = character
        self.enemy = enemy
        self.random_source = random_source or random
        self.escaped = False
        self._first_player_action = True
        self._reward_given = False

    def attack(self, weapon):
        """Attempt one weapon attack and return (turn_used, message)."""
        if self._battle_is_over():
            return False, "The battle is already over."
        if weapon not in self.character.inventory.weapons():
            return False, "That weapon is not in your inventory."
        if not weapon.is_usable:
            return False, f"{weapon.name} is broken."

        if isinstance(weapon, Firearm):
            ammunition_cost = self.character.ammo_cost(weapon)
            if not weapon.can_fire(ammunition_cost):
                return False, (
                    f"{weapon.name} needs {ammunition_cost} loaded "
                    f"round(s) for this attack."
                )
            weapon.fire(ammunition_cost)
        else:
            weapon.use()

        damage = self.character.attack_damage(weapon)
        damage_dealt = self.enemy.take_damage(damage)
        message = (
            f"{self.character.name} attacks with {weapon.name} and deals "
            f"{damage_dealt} damage."
        )

        if not self.enemy.is_alive:
            reward = self._award_victory()
            message += f" {self.enemy.name} is defeated! You earn {reward} coins."

        return True, message

    def reload(self, firearm):
        """Attempt to reload and return (turn_used, message)."""
        if self._battle_is_over():
            return False, "The battle is already over."
        if firearm not in self.character.inventory.firearms():
            return False, "That firearm is not in your inventory."
        if firearm.bullets == firearm.capacity:
            return False, f"{firearm.name} is already fully loaded."

        rounds_moved = self.character.inventory.reload(firearm)
        if rounds_moved == 0:
            return False, f"You have no compatible ammunition for {firearm.name}."
        return True, f"You load {rounds_moved} round(s) into {firearm.name}."

    def use_recovery_item(self, item):
        """Attempt healing and return (turn_used, message)."""
        if self._battle_is_over():
            return False, "The battle is already over."
        if item not in self.character.inventory.recovery_items():
            return False, "That recovery item is not in your inventory."
        if not isinstance(item, RecoveryItem):
            return False, "That item cannot restore health."

        health_restored = self.character.heal(item)
        if health_restored == 0:
            return False, "Your health is already full."

        self.character.inventory.remove(item)
        return True, f"You use {item.name} and restore {health_restored} health."

    def try_escape(self):
        """Attempt escape and return (escaped, message). The attempt uses a turn."""
        if self._battle_is_over():
            return False, "The battle is already over."
        if self.random_source.random() < self.character.escape_chance:
            self.escaped = True
            return True, "You escape from the encounter."
        return False, "You fail to escape."

    def enemy_turn(self):
        """Perform the enemy attack and return a readable message."""
        if not self.enemy.is_alive or not self.character.is_alive or self.escaped:
            return "The enemy cannot attack."
        damage_taken = self.enemy.attack(self.character)
        return f"{self.enemy.name} attacks and deals {damage_taken} damage."

    def result(self):
        """Return the current terminal result, or None while battle continues."""
        if not self.enemy.is_alive:
            self._award_victory()
            return BattleResult.VICTORY
        if not self.character.is_alive:
            return BattleResult.DEFEAT
        if self.escaped:
            return BattleResult.ESCAPED
        return None

    def run(self):
        """Run a menu-driven encounter and return a BattleResult value."""
        from menus import choose_option

        print()
        print(f"A {self.enemy.name} blocks your path!")

        while self.result() is None:
            self._print_status()
            action = choose_option(
                "Choose your action:",
                ["Attack", "Reload", "Use recovery item", "Escape"],
            )

            turn_used = False
            escaped = False

            if action == "Attack":
                turn_used = self._run_attack_menu(choose_option)
            elif action == "Reload":
                turn_used = self._run_reload_menu(choose_option)
            elif action == "Use recovery item":
                turn_used = self._run_recovery_menu(choose_option)
            else:
                escaped, message = self.try_escape()
                turn_used = True
                print(message)

            if escaped or not self.enemy.is_alive:
                continue
            if turn_used:
                self._run_counterattack()

        battle_result = self.result()
        if battle_result == BattleResult.VICTORY:
            self._offer_mechanic_repair(choose_option)
        return battle_result

    def _run_attack_menu(self, choose_option):
        weapons = self.character.inventory.weapons()
        if not weapons:
            print("You have no weapons. Try to escape!")
            return False
        weapon = choose_option(
            "Choose a weapon:",
            weapons,
            label=lambda choice: choice.description(),
            allow_cancel=True,
        )
        if weapon is None:
            return False
        turn_used, message = self.attack(weapon)
        print(message)
        return turn_used

    def _run_reload_menu(self, choose_option):
        firearms = self.character.inventory.firearms()
        if not firearms:
            print("You have no firearms to reload.")
            return False
        firearm = choose_option(
            "Choose a firearm:",
            firearms,
            label=lambda choice: choice.description(),
            allow_cancel=True,
        )
        if firearm is None:
            return False
        turn_used, message = self.reload(firearm)
        print(message)
        return turn_used

    def _run_recovery_menu(self, choose_option):
        recovery_items = self.character.inventory.recovery_items()
        if not recovery_items:
            print("You have no recovery items.")
            return False
        item = choose_option(
            "Choose a recovery item:",
            recovery_items,
            label=lambda choice: choice.description(),
            allow_cancel=True,
        )
        if item is None:
            return False
        turn_used, message = self.use_recovery_item(item)
        print(message)
        return turn_used

    def _run_counterattack(self):
        if (
            self._first_player_action
            and self.character.trait.skips_first_counterattack
        ):
            print("Your stealth keeps the enemy from reacting in time.")
        else:
            print(self.enemy_turn())
        self._first_player_action = False

    def _battle_is_over(self):
        return (
            not self.enemy.is_alive
            or not self.character.is_alive
            or self.escaped
        )

    def _award_victory(self):
        if self._reward_given:
            return 0
        reward = self.character.earn_reward(self.enemy.coin_reward)
        self._reward_given = True
        return reward

    def _offer_mechanic_repair(self, choose_option):
        if not self.character.role.can_repair_weapons:
            return
        damaged_weapons = [
            weapon
            for weapon in self.character.inventory.weapons()
            if weapon.durability < weapon.MAXIMUM_DURABILITY
        ]
        if not damaged_weapons:
            return

        weapon = choose_option(
            "Mechanic bonus: choose a weapon to repair:",
            damaged_weapons,
            label=lambda choice: choice.description(),
            allow_cancel=True,
        )
        if weapon is not None:
            repaired = self.character.repair_weapon(weapon)
            print(f"You restore {repaired} durability to {weapon.name}.")

    def _print_status(self):
        print()
        print(
            f"{self.character.name}: "
            f"{self.character.health}/{self.character.maximum_health} health"
        )
        print(
            f"{self.enemy.name}: "
            f"{self.enemy.health}/{self.enemy.maximum_health} health"
        )
