"""Shop transactions and an optional interactive shop menu.

The Shop checks prices, creates independent item objects, and moves coins and
items. Game scenes only decide when a character visits.
"""

from characters import Character
from items import default_item_factories
from menus import choose_option


class Shop:
    """Sell a catalog of items and buy carried items back from a character."""

    def __init__(self, item_factories=None):
        if item_factories is None:
            factories = default_item_factories()
        else:
            factories = item_factories
        if not factories or not all(callable(factory) for factory in factories):
            raise ValueError("A shop needs one or more item factory functions.")
        self._item_factories = list(factories)

    def catalog_items(self):
        """Return fresh display items for the current catalog."""
        return [factory() for factory in self._item_factories]

    def buy(self, character, index):
        """Buy a catalog item by zero-based index."""
        self._check_character(character)
        if not isinstance(index, int) or isinstance(index, bool):
            return False, "That catalog selection is invalid."
        if not 0 <= index < len(self._item_factories):
            return False, "That catalog selection is invalid."

        item = self._item_factories[index]()
        if not character.wallet.spend(item.price):
            return False, f"You cannot afford {item.name}."

        character.add_item(item)
        return True, f"You bought {item.name} for {item.price} coins."

    def sell(self, character, item):
        """Sell one exact owned item."""
        self._check_character(character)
        if item not in character.inventory.items:
            return False, "That item is not in your inventory."

        character.inventory.remove(item)
        character.wallet.earn(item.sale_price)
        return True, f"You sold {item.name} for {item.sale_price} coins."

    def run(self, character):
        """Run the shop until the player chooses Leave."""
        self._check_character(character)
        print()
        print("You find a survivor trading supplies.")

        while True:
            print()
            print(f"Coins: {character.wallet.balance}")
            action = choose_option("Shop:", ["Buy", "Sell", "Leave"])

            if action == "Leave":
                print("You leave the shop.")
                return
            if action == "Buy":
                self._run_buy_menu(character)
            else:
                self._run_sell_menu(character)

    def _run_buy_menu(self, character):
        catalog_indices = list(range(len(self._item_factories)))
        catalog = self.catalog_items()
        index = choose_option(
            "Items for sale:",
            catalog_indices,
            label=lambda position: catalog[position].description(),
            allow_cancel=True,
        )
        if index is None:
            return
        _, message = self.buy(character, index)
        print(message)

    def _run_sell_menu(self, character):
        items = character.inventory.items
        if not items:
            print("Your inventory is empty.")
            return
        item = choose_option(
            "Choose an item to sell:",
            items,
            label=lambda choice: (
                f"{choice.name} - sells for {choice.sale_price} coins"
            ),
            allow_cancel=True,
        )
        if item is None:
            return
        _, message = self.sell(character, item)
        print(message)

    @staticmethod
    def _check_character(character):
        if not isinstance(character, Character):
            raise ValueError("Shop actions require a Character object.")
