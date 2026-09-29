# Game Engine with Inheritance

A small Python game engine demonstrating advanced object-oriented programming concepts.

The project contains an entity system, component system, game loop, event system, collision detection, inventory management, trading, combat, and JSON game-state persistence.

## Features

### Entity System

The engine contains an abstract `Entity` base class.

Concrete entities include:

- `Player`
- `Enemy`
- `NPC`

Each entity has:

- ID
- Name
- Position
- Active state
- Components

### Player

The player supports:

- Health
- Score
- Gold
- Inventory
- Equip/unequip
- Combat
- Movement

### Enemy

Enemies contain:

- Enemy type
- Damage
- Health
- Combat statistics
- Dropped items

### NPC

NPCs contain:

- Dialogue
- Quests

---

## Component System

The engine uses composition through components.

Available components:

### MovementComponent

Stores:

- Speed
- Direction

### HealthComponent

Stores:

- Current HP
- Maximum HP
- Armor

It also provides:

```python
take_damage()
heal()