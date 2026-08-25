"""Run a short playable survival horror demonstration.

This file intentionally contains very little game logic. It shows students how
the focused modules can be assembled into character creation, shopping, and a
first battle.
"""

import random

from characters import Character, default_origins, default_roles, default_traits
from combat import Battle
from currency import Wallet
from enemies import default_enemies
from items import default_item_factories
from menus import choose_multiple, choose_option
from shop import Shop


def ask_for_name(input_function=input):
    """Ask until the player enters a non-empty character name."""
    while True:
        name = input_function("Enter your character's name: ").strip()
        if name:
            return name
        print("Please enter at least one character for the name.")


def create_character(input_function=input):
    """Create a character from the planned trait, role, and origin choices."""
    name = ask_for_name(input_function)

    trait = choose_option(
        "Choose your trait:",
        default_traits(),
        label=lambda choice: f"{choice.name} - {choice.description}",
        input_function=input_function,
    )
    role = choose_option(
        "Choose your role:",
        default_roles(),
        label=lambda choice: f"{choice.name} - {choice.description}",
        input_function=input_function,
    )
    origin = choose_option(
        "Choose your origin:",
        default_origins(),
        input_function=input_function,
    )

    return Character(
        name,
        trait,
        role,
        origin,
        wallet=Wallet(100),
    )


def choose_starter_items(character, input_function=input):
    """Let the player choose three different free item types."""
    factories = default_item_factories()
    selected_factories = choose_multiple(
        "Choose three free starter items:",
        factories,
        count=3,
        label=lambda factory: factory().description(),
        input_function=input_function,
    )

    for factory in selected_factories:
        character.add_item(factory())


def print_character(character):
    print()
    print("Character")
    print("---------")
    for line in character.summary_lines():
        print(line)


def print_inventory(character):
    print()
    print("Inventory")
    print("---------")
    for line in character.inventory.summary_lines():
        print(line)


def main():
    """Run character creation, a shop visit, and one initial battle."""
    print("SURVIVAL HORROR")
    print("Create a survivor and face your first encounter.")
    print()

    character = create_character()
    print_character(character)

    choose_starter_items(character)
    print_inventory(character)

    shop = Shop()
    shop.run(character)

    enemy = random.choice(default_enemies())
    battle = Battle(character, enemy)
    result = battle.run()

    print()
    print(f"Battle result: {result.title()}")
    print(f"Final health: {character.health}/{character.maximum_health}")
    print(f"Final coins: {character.wallet.balance}")
    print_inventory(character)


if __name__ == "__main__":
    main()
