# Survival Horror: Python Learning Project

This project teaches Python by building a small turn-based survival horror
game. You can play the current demonstration, inspect one concept at a time,
and extend the same classes into a longer game.

## Run the demo

Use Python 3.9 or newer:

```bash
python3 main.py
```

The demo creates a survivor, gives you three starter items, opens a shop, and
runs one encounter. It does not save progress yet.

## Module map

| Module | What it teaches | What it hides |
| --- | --- | --- |
| `items.py` | Classes and inheritance | Item statistics and weapon resources |
| `inventory.py` | Lists and object composition | Adding, removing, filtering, and reloading |
| `characters.py` | Classes working together | Trait and role bonus calculations |
| `enemies.py` | Small subclasses | Enemy statistics and health limits |
| `currency.py` | Encapsulation | Safe coin spending and earning |
| `shop.py` | Methods and business rules | Prices, purchases, and sales |
| `menus.py` | Loops and input validation | Number parsing and repeated prompts |
| `combat.py` | State and turn-based decisions | Damage, rewards, and encounter results |
| `main.py` | Importing and composition | The details owned by every other module |

Start with `main.py` to see the full flow. Then open the module for the concept
you want to study. A scene should call public methods such as
`inventory.add(item)`, `shop.buy(character, index)`, or `battle.attack(weapon)`
instead of changing internal attributes such as `inventory._items`.

## Small building-block examples

### Create and carry items

```python
from inventory import Inventory
from items import create_bandages, create_pistol

backpack = Inventory()
backpack.add(create_pistol())
backpack.add(create_bandages())

for line in backpack.summary_lines():
    print(line)
```

Factory functions return a new object each time. Two calls to
`create_pistol()` make two independent pistols with their own ammunition and
durability.

### Create a character

```python
from characters import Brave, Character, Medic
from currency import Wallet

survivor = Character(
    name="Alex",
    trait=Brave(),
    role=Medic(),
    origin="Mexico",
    wallet=Wallet(100),
)
```

Traits and roles are objects inside the character. `Character.attack_damage()`
and `Character.heal()` apply their bonuses, so battle scenes do not need large
`if` statements for every possible combination.

### Buy an item

```python
from shop import Shop

shop = Shop()
success, message = shop.buy(survivor, 6)  # The shovel is catalog index 6.
print(message)
```

The shop checks the wallet, spends coins, creates the item, and adds it to the
inventory. The caller only handles the result.

### Build a battle one action at a time

```python
from combat import Battle
from enemies import Zombie
from items import create_knife

knife = create_knife()
survivor.add_item(knife)
battle = Battle(survivor, Zombie())

turn_used, message = battle.attack(knife)
print(message)

if turn_used and battle.result() is None:
    print(battle.enemy_turn())
```

For a complete menu-driven fight, use `battle.run()`. For a custom lesson or
scene, call the action methods yourself.

## Suggested exercises

1. Add an enemy subclass to `enemies.py` and include it in
   `default_enemies()`.
2. Add a recovery item factory to `items.py` and the default shop catalog.
3. Add a trait by overriding one neutral method from `Trait`.
4. Add a role that changes starting health, healing, damage, or ammunition.
5. Write a campaign loop that checks `BattleResult` and creates another enemy
   after a victory.
6. Add a story choice between the shop and the next encounter.

Keep each new rule in the module that owns the affected concept. This lets
`main.py` remain a readable map of the game rather than becoming the entire
game.
