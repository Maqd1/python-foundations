'''

Q7: The Game Engine with Inheritance (Very Hard)

Create a small game engine with entities, components, and game loop.

Requirements:

    Entity System:

        Entity: id, position, active

        Player (inherits Entity): health, score, inventory

        Enemy (inherits Entity): type, damage, drop_items

        NPC (inherits Entity): dialogue, quests

    Component System:

        MovementComponent: speed, direction

        HealthComponent: hp, max_hp, armor

        CombatComponent: attack, defense

        RenderComponent: sprite, color

    Game Engine:

        Game loop (update, render)

        Event system

        Collision detection

        Save/Load game state

    Inventory System:

        Items with weight, value

        Equip/unequip

        Trading between entities

    Advanced OOP:

        Abstract classes for game entities

        Multiple inheritance (Entity + Component)

        Magic methods for arithmetic (damage, healing)

        Dataclasses for game data

Sample Output:
text

🎮 GAME ENGINE v1.0 🎮

🛡️ GAME STATE
Frame: 1234
Entities: 15

👤 PLAYER
Name: Damilola
Health: 100/100
Position: (34, 56)
Inventory: 5/10 items
  - Sword (Attack: 10)
  - Health Potion x3
  - Gold: 150g

⚔️ ENEMIES (3 active):
1. Goblin (HP: 30)
   Position: (45, 52)
   Damage: 5
   Drops: Gold (10g), Leather

2. Skeleton (HP: 50)
   Position: (32, 60)
   Damage: 8
   Drops: Bone, Gold (15g)

3. Boss (HP: 200)
   Position: (50, 50)
   Damage: 20
   Drops: Epic Sword, 100g

🔧 COMPONENTS:
Player:
  - Movement: Speed 5, Direction: UP
  - Health: 100/100
  - Combat: Attack 15, Defense 8

⚡ EVENT LOG:
1234: Player moved to (34, 56)
1235: Player attacked Goblin (-15 HP)
1236: Goblin attacked Player (-5 HP)
1237: Goblin defeated! (Dropped 10g)

💾 Saving game... ✅

📊 STATISTICS:
Time played: 2.3 hours
Enemies defeated: 45
Gold collected: 2,350g
Level: 12
Experience: 4,500/5,000

Concepts: Advanced inheritance, composition, game loop, event system, abstract classes, multiple inheritance, magic methods, dataclasses
'''