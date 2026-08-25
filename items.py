"""Item classes and ready-to-use item factory functions.

Other modules create items through functions such as ``create_pistol()``.
This keeps all item statistics in one file and guarantees a fresh object each
time an item is awarded or purchased.
"""


LIGHT_AMMO = "light"
HEAVY_AMMO = "heavy"


def _require_non_negative(value, field_name):
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueError(f"{field_name} must be a whole number.")
    if value < 0:
        raise ValueError(f"{field_name} cannot be negative.")


def _require_positive(value, field_name):
    _require_non_negative(value, field_name)
    if value == 0:
        raise ValueError(f"{field_name} must be greater than zero.")


class Item:
    """Base class for everything a character can carry."""

    def __init__(self, name, price, sale_price):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("An item needs a name.")
        _require_non_negative(price, "Price")
        _require_non_negative(sale_price, "Sale price")

        self.name = name
        self.price = price
        self.sale_price = sale_price

    def description(self):
        """Return a short line suitable for inventory and shop menus."""
        return f"{self.name} - {self.price} coins"

    def __str__(self):
        return self.name


class Weapon(Item):
    """Base class for weapons that wear down when used."""

    MAXIMUM_DURABILITY = 100

    def __init__(self, name, damage, price, sale_price, durability=100):
        super().__init__(name, price, sale_price)
        _require_positive(damage, "Damage")
        _require_non_negative(durability, "Durability")

        self.damage = damage
        self.durability = min(durability, self.MAXIMUM_DURABILITY)

    @property
    def is_usable(self):
        return self.durability > 0

    def use(self):
        """Consume one durability point and report whether use was possible."""
        if not self.is_usable:
            return False

        self.durability -= 1
        return True

    def repair(self, amount):
        """Restore durability without exceeding the weapon maximum."""
        _require_non_negative(amount, "Repair amount")
        old_durability = self.durability
        self.durability = min(
            self.MAXIMUM_DURABILITY,
            self.durability + amount,
        )
        return self.durability - old_durability

    def description(self):
        return (
            f"{self.name} - {self.damage} damage, "
            f"{self.durability}/{self.MAXIMUM_DURABILITY} durability, "
            f"{self.price} coins"
        )


class Firearm(Weapon):
    """A weapon with a limited magazine and one ammunition type."""

    def __init__(
        self,
        name,
        damage,
        bullets,
        capacity,
        ammo_type,
        price,
        sale_price,
        durability=100,
    ):
        super().__init__(name, damage, price, sale_price, durability)
        _require_positive(capacity, "Ammunition capacity")
        _require_non_negative(bullets, "Loaded ammunition")
        if bullets > capacity:
            raise ValueError("Loaded ammunition cannot exceed capacity.")
        if not isinstance(ammo_type, str) or not ammo_type.strip():
            raise ValueError("A firearm needs an ammunition type.")

        self.bullets = bullets
        self.capacity = capacity
        self.ammo_type = ammo_type

    def can_fire(self, rounds=1):
        _require_positive(rounds, "Rounds")
        return self.is_usable and self.bullets >= rounds

    def fire(self, rounds=1):
        """Consume ammunition and durability when the shot is possible."""
        if not self.can_fire(rounds):
            return False

        self.bullets -= rounds
        self.use()
        return True

    def reload(self, ammo):
        """Move compatible rounds from an Ammo object into this firearm."""
        if not isinstance(ammo, Ammo) or ammo.ammo_type != self.ammo_type:
            return 0

        empty_spaces = self.capacity - self.bullets
        rounds_moved = min(empty_spaces, ammo.amount)
        self.bullets += rounds_moved
        ammo.amount -= rounds_moved
        return rounds_moved

    def description(self):
        return (
            f"{self.name} - {self.damage} damage, "
            f"{self.bullets}/{self.capacity} rounds, "
            f"{self.durability}/{self.MAXIMUM_DURABILITY} durability, "
            f"{self.price} coins"
        )


class MeleeWeapon(Weapon):
    """A weapon that uses durability but no ammunition."""


class RecoveryItem(Item):
    """A consumable item that restores health."""

    def __init__(self, name, healing, price, sale_price):
        super().__init__(name, price, sale_price)
        _require_positive(healing, "Healing")
        self.healing = healing

    def description(self):
        return f"{self.name} - heals {self.healing}, {self.price} coins"


class Ammo(Item):
    """A consumable pack of ammunition for one firearm type."""

    def __init__(self, name, amount, ammo_type, price, sale_price):
        super().__init__(name, price, sale_price)
        _require_positive(amount, "Ammunition amount")
        if not isinstance(ammo_type, str) or not ammo_type.strip():
            raise ValueError("Ammunition needs a type.")

        self.amount = amount
        self.ammo_type = ammo_type

    def description(self):
        return f"{self.name} - {self.amount} rounds, {self.price} coins"


def create_pistol():
    return Firearm("Pistol", 15, 20, 20, LIGHT_AMMO, 100, 40)


def create_medkit():
    return RecoveryItem("Medkit", 10, 50, 20)


def create_light_ammo():
    return Ammo("Light ammunition", 30, LIGHT_AMMO, 30, 15)


def create_bandages():
    return RecoveryItem("Bandages", 5, 20, 10)


def create_rifle():
    return Firearm("Rifle", 25, 10, 10, HEAVY_AMMO, 200, 80)


def create_knife():
    return MeleeWeapon("Knife", 10, 50, 20)


def create_shovel():
    return MeleeWeapon("Shovel", 8, 30, 10)


def create_shotgun():
    return Firearm("Shotgun", 35, 5, 5, HEAVY_AMMO, 300, 120)


def create_heavy_ammo():
    return Ammo("Heavy ammunition", 15, HEAVY_AMMO, 50, 25)


def default_item_factories():
    """Return the planned item factories in their display order."""
    return [
        create_pistol,
        create_medkit,
        create_light_ammo,
        create_bandages,
        create_rifle,
        create_knife,
        create_shovel,
        create_shotgun,
        create_heavy_ammo,
    ]
