"""Character, trait, and role classes.

The Character class is the public boundary for RPG calculations. Combat code
does not need to know which trait adds damage or which role improves healing.
"""

import math

from currency import Wallet
from inventory import Inventory
from items import Ammo, Firearm, RecoveryItem, Weapon


class Trait:
    """Base character personality with neutral bonus behavior."""

    name = "No trait"
    description = "No trait bonus."
    escape_chance = 0.40
    skips_first_counterattack = False

    def modify_damage(self, damage, weapon):
        return damage

    def ammunition_cost(self, weapon):
        return 1

    def modify_reward(self, coins):
        return coins


class Brave(Trait):
    name = "Brave"
    description = "Adds 10 damage to every weapon attack."

    def modify_damage(self, damage, weapon):
        return damage + 10


class Stealthy(Trait):
    name = "Stealthy"
    description = "Avoids the first counterattack and escapes more easily."
    escape_chance = 0.75
    skips_first_counterattack = True


class Intelligent(Trait):
    name = "Intelligent"
    description = "Earns 25% more coins from encounters."

    def modify_reward(self, coins):
        return math.ceil(coins * 1.25)


class Aggressive(Trait):
    name = "Aggressive"
    description = "Deals 25% more damage but firearms use two rounds."

    def modify_damage(self, damage, weapon):
        return math.ceil(damage * 1.25)

    def ammunition_cost(self, weapon):
        if isinstance(weapon, Firearm):
            return 2
        return 1


class Role:
    """Base profession with neutral bonus behavior."""

    name = "No role"
    description = "No role bonus."
    starting_health = 100
    can_repair_weapons = False

    def modify_damage(self, damage, weapon):
        return damage

    def modify_healing(self, healing):
        return healing

    def modify_incoming_damage(self, damage):
        return damage

    def modify_ammunition(self, amount):
        return amount


class Medic(Role):
    name = "Medic"
    description = "Recovery items heal 50% more health."

    def modify_healing(self, healing):
        return math.ceil(healing * 1.50)


class Soldier(Role):
    name = "Soldier"
    description = "Firearms deal 20% more damage."

    def modify_damage(self, damage, weapon):
        if isinstance(weapon, Firearm):
            return math.ceil(damage * 1.20)
        return damage


class Firefighter(Role):
    name = "Firefighter"
    description = "Starts with 130 health and takes 20% less damage."
    starting_health = 130

    def modify_incoming_damage(self, damage):
        if damage == 0:
            return 0
        return max(1, math.floor(damage * 0.80))


class Mechanic(Role):
    name = "Mechanic"
    description = "Finds 50% more ammunition and can repair weapons."
    can_repair_weapons = True

    def modify_ammunition(self, amount):
        return math.ceil(amount * 1.50)


class Character:
    """A playable survivor composed from a trait, role, inventory, and wallet."""

    def __init__(
        self,
        name,
        trait,
        role,
        origin,
        inventory=None,
        wallet=None,
    ):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("A character needs a name.")
        if not isinstance(trait, Trait):
            raise ValueError("A character needs a Trait object.")
        if not isinstance(role, Role):
            raise ValueError("A character needs a Role object.")
        if origin not in default_origins():
            raise ValueError("Choose one of the available origins.")

        self.name = name.strip()
        self.trait = trait
        self.role = role
        self.origin = origin
        self.inventory = inventory if inventory is not None else Inventory()
        self.wallet = wallet if wallet is not None else Wallet()
        self.maximum_health = role.starting_health
        self.health = self.maximum_health

    @property
    def is_alive(self):
        return self.health > 0

    @property
    def escape_chance(self):
        return self.trait.escape_chance

    def attack_damage(self, weapon):
        """Calculate a weapon attack using role, then trait bonuses."""
        if not isinstance(weapon, Weapon):
            raise ValueError("Attacks require a Weapon object.")
        damage = self.role.modify_damage(weapon.damage, weapon)
        return self.trait.modify_damage(damage, weapon)

    def ammo_cost(self, weapon):
        if not isinstance(weapon, Weapon):
            raise ValueError("Ammunition cost requires a Weapon object.")
        return self.trait.ammunition_cost(weapon)

    def take_damage(self, amount):
        if not isinstance(amount, int) or isinstance(amount, bool) or amount < 0:
            raise ValueError("Damage must be a non-negative whole number.")
        damage_taken = self.role.modify_incoming_damage(amount)
        self.health = max(0, self.health - damage_taken)
        return damage_taken

    def heal(self, recovery_item):
        if not isinstance(recovery_item, RecoveryItem):
            raise ValueError("Healing requires a RecoveryItem object.")
        healing = self.role.modify_healing(recovery_item.healing)
        old_health = self.health
        self.health = min(self.maximum_health, self.health + healing)
        return self.health - old_health

    def add_item(self, item):
        """Add an item, applying the role's ammunition pickup bonus."""
        if isinstance(item, Ammo):
            return self.receive_ammo(item)
        self.inventory.add(item)
        return item

    def receive_ammo(self, ammo):
        if not isinstance(ammo, Ammo):
            raise ValueError("Ammunition pickup requires an Ammo object.")
        ammo.amount = self.role.modify_ammunition(ammo.amount)
        self.inventory.add(ammo)
        return ammo

    def earn_reward(self, base_coins):
        if (
            not isinstance(base_coins, int)
            or isinstance(base_coins, bool)
            or base_coins < 0
        ):
            raise ValueError("Rewards must be non-negative whole numbers.")
        reward = self.trait.modify_reward(base_coins)
        self.wallet.earn(reward)
        return reward

    def repair_weapon(self, weapon):
        if not self.role.can_repair_weapons:
            return 0
        if not isinstance(weapon, Weapon):
            raise ValueError("Repairs require a Weapon object.")
        return weapon.repair(25)

    def summary_lines(self):
        return [
            f"Name: {self.name}",
            f"Trait: {self.trait.name} - {self.trait.description}",
            f"Role: {self.role.name} - {self.role.description}",
            f"Origin: {self.origin}",
            f"Health: {self.health}/{self.maximum_health}",
            f"Coins: {self.wallet.balance}",
        ]


def default_traits():
    return [Brave(), Stealthy(), Intelligent(), Aggressive()]


def default_roles():
    return [Medic(), Soldier(), Firefighter(), Mechanic()]


def default_origins():
    return ["Mexico", "Canada", "Spain", "Russia"]
