"""Inventory storage and item-specific lookup operations.

Game code asks this class for weapons, recovery items, or ammunition instead of
editing a list directly. That keeps inventory bookkeeping out of game scenes.
"""

from items import Ammo, Firearm, Item, RecoveryItem, Weapon


class Inventory:
    """Own the items carried by one character."""

    def __init__(self, items=None):
        self._items = []
        for item in items or []:
            self.add(item)

    @property
    def items(self):
        """Return a copy so callers cannot accidentally change storage."""
        return list(self._items)

    def add(self, item):
        if not isinstance(item, Item):
            raise ValueError("Only Item objects can be added to an inventory.")
        self._items.append(item)

    def remove(self, item):
        """Remove an owned item and report whether it was found."""
        if item not in self._items:
            return False
        self._items.remove(item)
        return True

    def find(self, name):
        """Return the first item with a matching name, or None."""
        for item in self._items:
            if item.name.lower() == name.lower():
                return item
        return None

    def count(self, item_type=None):
        if item_type is None:
            return len(self._items)
        return len([item for item in self._items if isinstance(item, item_type)])

    def weapons(self):
        return [item for item in self._items if isinstance(item, Weapon)]

    def firearms(self):
        return [item for item in self._items if isinstance(item, Firearm)]

    def recovery_items(self):
        return [item for item in self._items if isinstance(item, RecoveryItem)]

    def ammo_for(self, ammo_type):
        return [
            item
            for item in self._items
            if isinstance(item, Ammo) and item.ammo_type == ammo_type
        ]

    def reload(self, firearm):
        """Reload a firearm from compatible packs and return rounds moved."""
        if not isinstance(firearm, Firearm):
            return 0

        rounds_moved = 0
        for ammo in self.ammo_for(firearm.ammo_type):
            rounds_moved += firearm.reload(ammo)
            if ammo.amount == 0:
                self.remove(ammo)
            if firearm.bullets == firearm.capacity:
                break
        return rounds_moved

    def summary_lines(self):
        """Return readable inventory lines without printing them."""
        if not self._items:
            return ["Inventory is empty."]

        lines = []
        for number, item in enumerate(self._items, start=1):
            lines.append(f"{number}. {item.description()}")
        return lines
