# Survival Horror Foundations Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an English, beginner-readable, turn-based survival horror demo
from focused class-based modules.

**Architecture:** Domain modules own items, inventory, characters, enemies,
currency, shopping, and battle rules. A small menu module owns input validation,
and `main.py` composes the public interfaces into a playable example without
leaking module bookkeeping.

**Tech Stack:** Python 3 standard library only

**Spec:** `docs/superpowers/specs/2026-08-24-survival-horror-foundations-design.md`

## Global Constraints

- Use only the Python standard library.
- Do not add test files or a testing framework.
- Keep all source identifiers, comments, docstrings, prompts, labels, and
  messages in English.
- Use explicit constructors and ordinary class methods suitable for beginning
  Python students.
- Importing a module must not start the game or prompt for input.
- Verify work with compilation, imports, inline smoke scenarios, and scripted
  gameplay.

---

### Task 1: Item and Currency Models

**Files:**
- Create: `items.py`
- Create: `currency.py`

**Interfaces:**
- Produces: `Wallet(starting_coins: int = 0)`, `balance`, `earn(amount: int)`,
  `can_afford(price: int)`, and `spend(amount: int)`.
- Produces: `Item`, `Weapon`, `Firearm`, `MeleeWeapon`, `RecoveryItem`, and
  `Ammo` classes.
- Produces: `create_pistol()`, `create_medkit()`, `create_light_ammo()`,
  `create_bandages()`, `create_rifle()`, `create_knife()`, `create_shovel()`,
  `create_shotgun()`, `create_heavy_ammo()`, and `default_item_factories()`.

- [ ] **Step 1: Implement the wallet contract**

  Add explicit validation and this public behavior:

  ```python
  wallet = Wallet(100)
  wallet.can_afford(30)  # True
  wallet.spend(30)       # True; balance becomes 70
  wallet.spend(100)      # False; balance stays 70
  wallet.earn(10)        # balance becomes 80
  ```

- [ ] **Step 2: Implement the item hierarchy**

  Use these constructor shapes:

  ```python
  Item(name, price, sale_price)
  Weapon(name, damage, price, sale_price, durability=100)
  Firearm(name, damage, bullets, capacity, ammo_type, price, sale_price,
          durability=100)
  MeleeWeapon(name, damage, price, sale_price, durability=100)
  RecoveryItem(name, healing, price, sale_price)
  Ammo(name, amount, ammo_type, price, sale_price)
  ```

  `Weapon.use()` consumes one durability. `Weapon.repair(amount)` caps at 100.
  `Firearm.can_fire(rounds)` and `Firearm.fire(rounds)` own bullet validation.
  `Firearm.reload(ammo)` moves only the needed compatible rounds and leaves the
  remainder in the ammunition object.

- [ ] **Step 3: Add fresh-item factory functions**

  Encode all values from the spec and return the nine factories from
  `default_item_factories()` in the planned display order.

- [ ] **Step 4: Run focused inline smoke verification**

  Run:

  ```bash
  python3 -c "from currency import Wallet; from items import create_pistol, create_light_ammo; w=Wallet(100); assert w.spend(30) and w.balance == 70; p=create_pistol(); a=create_light_ammo(); p.fire(1); p.reload(a); assert p.bullets == 20 and a.amount == 29"
  ```

  Expected: exit code 0 with no output.

### Task 2: Inventory and Character Models

**Files:**
- Replace: `inventory.py`
- Create: `characters.py`

**Interfaces:**
- Consumes: all item classes from Task 1 and `Wallet`.
- Produces: `Inventory(items=None)`, read-only-copy property `items`, `add()`,
  `remove()`, `weapons()`, `recovery_items()`, `ammo_for(ammo_type)`,
  `reload(firearm)`, and `summary_lines()`.
- Produces: `Trait`, `Brave`, `Stealthy`, `Intelligent`, `Aggressive`, `Role`,
  `Medic`, `Soldier`, `Firefighter`, `Mechanic`, and `Character`.
- Produces: `default_traits()`, `default_roles()`, and `default_origins()`.

- [ ] **Step 1: Replace the single Pistol class with Inventory**

  Store items in `_items`, return a copy from `items`, and centralize compatible
  ammunition lookup and firearm reloading. Remove ammunition packs when their
  amount reaches zero.

- [ ] **Step 2: Implement traits and roles as bonus objects**

  Give base classes neutral modifier methods, then override only the relevant
  behavior in each subclass. Their public names and descriptions must match the
  spec. Use `math.ceil()` for upward rounding.

- [ ] **Step 3: Implement Character as the bonus boundary**

  Use:

  ```python
  Character(name, trait, role, origin, inventory=None, wallet=None)
  character.attack_damage(weapon)
  character.ammo_cost(weapon)
  character.take_damage(amount)
  character.heal(recovery_item)
  character.receive_ammo(ammo)
  character.earn_reward(base_coins)
  character.repair_weapon(weapon)
  ```

  The character applies role and trait modifiers in the documented order,
  clamps health, and exposes `is_alive` as a property.

- [ ] **Step 4: Run bonus and inventory smoke verification**

  Run one `python3 -c` scenario that asserts Brave adds 10 damage, Soldier adds
  20% firearm damage, Firefighter starts at 130 health and reduces damage,
  Medic improves healing, Intelligent improves rewards, Aggressive costs two
  rounds, Stealthy has 75% escape chance, and Mechanic improves ammunition and
  repairs 25 durability.

  Expected: exit code 0 with no output.

### Task 3: Enemies and Combat Building Blocks

**Files:**
- Create: `enemies.py`
- Create: `combat.py`

**Interfaces:**
- Consumes: `Character`, `Inventory`, `Weapon`, `Firearm`, `RecoveryItem`, and
  menu selection helpers.
- Produces: `Enemy`, `Zombie`, `Runner`, `Brute`, and `default_enemies()`.
- Produces: `BattleResult.VICTORY`, `BattleResult.DEFEAT`,
  `BattleResult.ESCAPED`, and `Battle(character, enemy, random_source=None)`.
- Produces battle actions `attack(weapon)`, `reload(firearm)`,
  `use_recovery_item(item)`, `try_escape()`, `enemy_turn()`, and `run()`.

- [ ] **Step 1: Implement the enemy hierarchy**

  `Enemy.take_damage()` clamps health to zero, `Enemy.attack(character)` routes
  damage through the character's role resistance, and subclass constructors
  set the exact health, damage, and reward values from the spec.

- [ ] **Step 2: Implement non-interactive battle actions**

  Each action returns a readable message or result and owns all resource
  changes. An attack consumes weapon durability, plus ammunition for firearms.
  Victory rewards coins once. Failed escape and successful item/reload actions
  allow the enemy turn.

- [ ] **Step 3: Implement the interactive battle loop**

  Present Attack, Reload, Use recovery item, and Escape. Filter item submenus so
  unavailable actions explain the problem and return safely. Suppress the first
  enemy counterattack for Stealthy characters and offer the Mechanic repair
  after victory.

- [ ] **Step 4: Verify deterministic battle actions inline**

  Run scenarios with a tiny local random stub to prove victory, defeat, escape,
  firearm ammunition use, melee use, healing, reload, rewards, and the Stealthy
  opening suppression without creating a test file.

  Expected: exit code 0 with no assertion failures.

### Task 4: Menus and Shop

**Files:**
- Create: `menus.py`
- Create: `shop.py`

**Interfaces:**
- Consumes: item factories, `Character`, `Inventory`, and `Wallet` behavior.
- Produces: `choose_option(title, options, label=None, allow_cancel=False,
  input_function=input)` and `choose_multiple(title, options, count,
  label=None, input_function=input)`.
- Produces: `Shop(item_factories=None)`, `catalog_items()`, `buy(character,
  index)`, `sell(character, item)`, and `run(character)`.

- [ ] **Step 1: Implement reusable validated menu selection**

  Keep parsing, range checks, duplicate prevention, and cancel handling inside
  `menus.py`. Return selected objects, not raw numeric strings.

- [ ] **Step 2: Implement shop transactions**

  Buy creates a fresh catalog item, checks and spends coins, and adds it to the
  inventory. Sell removes the exact owned item and earns its sale value. Both
  return `(success, message)`.

- [ ] **Step 3: Implement the interactive shop loop**

  Repeatedly show balance and Buy, Sell, Leave actions. The shop owns catalog
  display and transaction messages while delegating selection validation to
  `menus.py`.

- [ ] **Step 4: Run menu and shop smoke verification**

  Use a small iterator-backed input function to assert invalid menu input is
  retried. Buy and sell a shovel and assert wallet and inventory values.

  Expected: exit code 0 with no assertion failures.

### Task 5: Playable Demo and Student Guide

**Files:**
- Replace: `main.py`
- Create: `README.md`

**Interfaces:**
- Consumes: all public module interfaces from Tasks 1-4.
- Produces: `create_character()`, `choose_starter_items(character)`, `main()`,
  and a guarded runnable entry point.

- [ ] **Step 1: Compose character creation and starter selection**

  Use the shared menus for trait, role, origin, and three distinct factory
  choices. Add new item instances to the character and print a concise
  character summary.

- [ ] **Step 2: Compose the short playable flow**

  Create the 100-coin character, run the shop, choose one random enemy type,
  run one battle, and show the result plus final health, coins, and inventory.

- [ ] **Step 3: Add the student README**

  Document Python version requirements, `python3 main.py`, the module map,
  minimal construction examples, and extension exercises for a new item,
  enemy, trait, role, and multi-battle campaign loop.

- [ ] **Step 4: Compile and import every module**

  Run:

  ```bash
  PYTHONPYCACHEPREFIX=/tmp/sh-game-pycache python3 -m compileall -q .
  PYTHONPYCACHEPREFIX=/tmp/sh-game-pycache python3 -c "import items, inventory, currency, characters, enemies, menus, shop, combat, main"
  ```

  Expected: both commands exit 0 and importing produces no output or prompts.

### Task 6: Full No-Test Verification and Review

**Files:**
- Modify only source or documentation files where verification reveals a defect.

**Interfaces:**
- Consumes: completed runnable project.
- Produces: verified source with no Spanish player-facing terms and no test
  files.

- [ ] **Step 1: Run the full inline domain smoke scenario**

  Exercise every item factory, inventory actions, every trait, every role, all
  enemy types, wallet boundaries, shop buy/sell, and deterministic battle
  results in one temporary or stdin-fed script. Do not save it as a test file.

- [ ] **Step 2: Run scripted end-to-end gameplay**

  Pipe deterministic choices into `python3 main.py`, covering character setup,
  three starter items, leaving the shop, and combat actions through a terminal
  result. Check the process exits normally.

- [ ] **Step 3: Search for untranslated source text and forbidden test files**

  Run:

  ```bash
  rg -n "Pistola|Botiquín|Munición|Vendas|Cuchillo|Pala|Escopeta|Monedas|Escoge|Elige|Médico|Bombero|Mecánico|Valiente|Sigiloso|Inteligente|Agresivo|México|Canadá|España|Rusia" --glob '*.py' --glob '*.md' .
  rg --files | rg '(^|/)(test_|tests?/|.*_test\\.py$)'
  ```

  Expected: no matches, except that country proper nouns are represented by
  their standard English spellings (`Mexico`, `Canada`, `Spain`, `Russia`).

- [ ] **Step 4: Review the diff against every requirement**

  Compare the final file list and diff with the design specification. Confirm
  that the public interfaces hide bookkeeping, the demo is runnable, no test
  files exist, and unrelated changes are absent.

- [ ] **Step 5: Run final fresh verification**

  Re-run compilation, import, inline domain smoke, end-to-end gameplay, and
  translation searches immediately before the completion report.
