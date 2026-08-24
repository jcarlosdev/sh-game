# Survival Horror Foundations Design

## Purpose

Turn the existing Spanish prototype into a small English turn-based survival
horror project that serves two purposes:

1. Students can inspect focused modules to learn Python classes, inheritance,
   composition, loops, conditionals, and method calls.
2. Students can run `main.py` to see those modules assembled into a short
   playable demonstration.

The implementation uses only the Python standard library and does not add a
test suite. Public methods stay small and descriptive, while modules hide list
management, price checks, bonus calculations, and input validation.

## Existing Features to Preserve

The English version preserves the prototype's choices and RPG data:

- Traits: Brave, Stealthy, Intelligent, and Aggressive.
- Roles: Medic, Soldier, Firefighter, and Mechanic.
- Origins: Mexico, Canada, Spain, and Russia.
- Starting currency: 100 coins.
- Three freely selected starter items.
- Items: pistol, medkit, light ammunition, bandages, rifle, knife, shovel,
  shotgun, and heavy ammunition.
- Existing weapon damage, ammunition capacity, purchase price, and sale value
  are retained where those values already exist.

All identifiers, comments, docstrings, prompts, menu labels, status messages,
item names, and character descriptions will be English.

## Module Structure

### `items.py`

Defines the inventory item hierarchy:

- `Item` owns the shared `name`, `price`, and `sale_price` attributes.
- `Weapon` adds `damage`, `durability`, and repair behavior.
- `Firearm` adds ammunition type, loaded ammunition, capacity, reloading, and
  ammunition consumption.
- `MeleeWeapon` represents weapons that do not require ammunition.
- `RecoveryItem` has healing power and can be consumed.
- `Ammo` has an ammunition type and quantity and can be consumed during a
  reload.

Weapons lose one durability per successful attack and cannot attack at zero
durability. Factory functions create fresh instances of every planned item so
shops and starter selections never share mutable item objects.

Item values:

| Item | Important values | Buy | Sell |
| --- | --- | ---: | ---: |
| Pistol | 20 light rounds, 15 damage | 100 | 40 |
| Medkit | 10 healing | 50 | 20 |
| Light ammunition | 30 rounds | 30 | 15 |
| Bandages | 5 healing | 20 | 10 |
| Rifle | 10 heavy rounds, 25 damage | 200 | 80 |
| Knife | 10 damage | 50 | 20 |
| Shovel | 8 damage | 30 | 10 |
| Shotgun | 5 heavy rounds, 35 damage | 300 | 120 |
| Heavy ammunition | 15 rounds | 50 | 25 |

Pistol capacity is 20, rifle capacity is 10, and shotgun capacity is 5. All
weapons start with 100 durability.

### `inventory.py`

`Inventory` owns a private list of items. Its public methods add, remove, find,
list, and count items. It also provides focused operations for returning
weapons and recovery items, consuming a recovery item, and reloading a firearm
from a compatible ammunition pack. Callers do not edit the internal list.

The same class supports starter items, shop purchases, and combat actions.
Duplicate consumables and weapons are allowed because each purchase is a
separate object.

### `characters.py`

`Character` is composed from a name, a trait object, a role object, an origin,
an `Inventory`, and a `Wallet`. It owns `health`, `maximum_health`, and methods
for damage, healing, attack calculations, rewards, escaping, ammunition pickup,
and repairs.

Trait classes implement these bonuses:

- `Brave`: adds 10 damage to every weapon attack.
- `Stealthy`: enemies do not counterattack after this character's first action
  in a battle, and escape chance is 75% instead of the normal 40%.
- `Intelligent`: coin rewards are increased by 25%, rounded up.
- `Aggressive`: weapon damage is increased by 25%, rounded up. Firearms consume
  two rounds per attack; the firearm must have both rounds available.

Role classes implement these bonuses:

- `Medic`: recovery items heal 50% more, rounded up.
- `Soldier`: firearm damage is increased by 20%, rounded up.
- `Firefighter`: maximum and starting health are 130 instead of 100, and
  incoming damage is reduced by 20%, rounded down with a minimum of one.
- `Mechanic`: ammunition packs provide 50% more rounds, rounded up, and the
  character can restore 25 durability to one chosen weapon after a victorious
  battle. Other roles cannot perform this repair action.

Damage modifiers are applied in this order: weapon base damage, role modifier,
then trait modifier. A character cannot heal beyond maximum health or have
health below zero.

### `enemies.py`

`Enemy` owns `name`, `maximum_health`, `health`, `damage`, and `coin_reward`.
It exposes methods to attack, take damage, and report whether it is alive.

Three initial enemy types provide different parameters:

| Enemy | Health | Damage | Coin reward |
| --- | ---: | ---: | ---: |
| Zombie | 45 | 8 | 20 |
| Runner | 30 | 10 | 25 |
| Brute | 80 | 14 | 50 |

Subclass constructors contain these values, making it straightforward for a
student to add another enemy type.

### `currency.py`

`Wallet` stores a non-negative integer coin balance. `earn()` increases the
balance. `can_afford()` checks a price. `spend()` refuses invalid or
unaffordable purchases without allowing a negative balance.

### `shop.py`

`Shop` owns a catalog of item factory functions. It creates a fresh item for
each purchase, checks the character's wallet, charges coins, and adds the item
to the character's inventory. Selling removes the exact item and pays its sale
value. Public purchase and sale methods return a success flag and a readable
message so the menu layer does not duplicate business rules.

The default shop sells every planned item. Its user interface allows repeated
purchases and sales until the player chooses to leave.

### `menus.py`

Reusable functions print numbered choices and repeatedly request input until a
valid selection is entered. The module provides single-choice and
multiple-choice functions and supports an optional cancel choice. Callers pass
objects and a small label function, then receive selected objects rather than
parsing strings themselves.

### `combat.py`

`Battle` coordinates one `Character`, one `Enemy`, and a random-number source.
Its focused public actions are:

- Attack with a selected usable weapon.
- Reload a selected firearm from compatible inventory ammunition.
- Use a selected recovery item.
- Attempt escape.
- Perform the enemy turn.
- Run an interactive battle menu until victory, defeat, or escape.

An attack checks durability and ammunition, calculates character bonuses,
damages the enemy, and consumes the required durability and ammunition. Using
an item, reloading, and a failed escape all consume the player's turn. The
enemy attacks afterward unless it died, the character escaped, or the
Stealthy opening bonus suppresses that first counterattack.

Victory awards the enemy's coins through the character reward method, allowing
the Intelligent bonus to apply. A victorious Mechanic is offered one weapon
repair. Defeat ends the playable demonstration without resetting character
state. Escaping awards no coins.

`BattleResult` exposes readable `VICTORY`, `DEFEAT`, and `ESCAPED` values so a
later lesson can connect several encounters without depending on printed text.

### `main.py`

The runnable demonstration follows this sequence:

1. Ask for the character name.
2. Select a trait, role, and origin with the reusable menu.
3. Create the character and show the applied health and bonuses.
4. Select three different free starter item types from the default catalog.
5. Show the 100-coin balance and inventory.
6. Offer the default shop, including buying, selling, or leaving.
7. Start an initial fight against a randomly chosen Zombie, Runner, or Brute.
8. Show the result, final health, coin balance, and inventory.

The executable flow is under a `main()` function and a
`if __name__ == "__main__":` guard. Importing modules never starts prompts or
prints demonstration output.

### `README.md`

Explains how to run the game, maps each module to beginner programming
concepts, and includes short examples for constructing an item, inventory,
character, enemy, shop, and battle. It also suggests safe extension exercises
such as adding an enemy, item, or role.

## Error Handling and Teaching Style

- Menu functions recover from empty, non-numeric, and out-of-range input.
- Empty action menus explain why an action is unavailable and return to the
  battle menu.
- Domain methods reject negative prices, healing, damage, ammunition, and coin
  values with clear `ValueError` messages.
- Expected gameplay failures, such as insufficient coins or incompatible
  ammunition, return readable results rather than producing tracebacks.
- Classes use explicit constructors and ordinary methods instead of advanced
  metaprogramming or third-party frameworks.
- Each module begins with a short docstring explaining what it hides and what
  students normally call.

## Verification

No test files or testing framework will be added. Completion is verified by:

1. Compiling every Python module with `python3 -m compileall`.
2. Importing every module to confirm imports have no interactive side effects.
3. Running small inline smoke scenarios for item creation, purchase, sale,
   healing, reloading, every trait and role bonus, enemy damage, victory reward,
   and each battle result building block.
4. Running `main.py` with scripted menu input to exercise character creation,
   starter selection, the shop, and an initial fight.
5. Searching the project source for the original Spanish player-facing terms.

## Out of Scope

- Saved games, maps, story progression, armor, status effects, leveling,
  graphical interfaces, sound, networking, and third-party packages.
- A campaign loop containing multiple required battles. The modules and
  `BattleResult` intentionally provide the building blocks for students to add
  that loop in a later lesson.
- Automated test files, as explicitly requested.
