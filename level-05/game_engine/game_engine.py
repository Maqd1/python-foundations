from __future__ import annotations

from abc import ABC, abstractmethod
from contextlib import contextmanager
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Iterator
from enum import Enum
import json
import math


# ============================================================
# DATA CLASSES
# ============================================================

@dataclass
class Position:
    x: float
    y: float

    def distance_to(self, other: "Position") -> float:
        return math.sqrt(
            (self.x - other.x) ** 2
            + (self.y - other.y) ** 2
        )

    def __str__(self) -> str:
        return f"({self.x:g}, {self.y:g})"


@dataclass
class Item:
    name: str
    weight: float
    value: int
    quantity: int = 1
    attack: int = 0

    def __str__(self) -> str:
        if self.quantity > 1:
            return f"{self.name} x{self.quantity}"
        return self.name


# ============================================================
# MAGIC METHODS FOR DAMAGE AND HEALING
# ============================================================

@dataclass
class Damage:
    amount: int

    def __add__(self, other: "Damage") -> "Damage":
        return Damage(self.amount + other.amount)

    def __sub__(self, other: "Damage") -> "Damage":
        return Damage(max(0, self.amount - other.amount))

    def __mul__(self, multiplier: int) -> "Damage":
        return Damage(self.amount * multiplier)

    def __str__(self) -> str:
        return f"{self.amount} damage"


@dataclass
class Healing:
    amount: int

    def __add__(self, other: "Healing") -> "Healing":
        return Healing(self.amount + other.amount)

    def __mul__(self, multiplier: int) -> "Healing":
        return Healing(self.amount * multiplier)

    def __str__(self) -> str:
        return f"{self.amount} healing"


# ============================================================
# ENUMS
# ============================================================

class Direction(Enum):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"


class EventType(Enum):
    MOVE = "MOVE"
    ATTACK = "ATTACK"
    DAMAGE = "DAMAGE"
    HEAL = "HEAL"
    DEFEAT = "DEFEAT"
    TRADE = "TRADE"
    SYSTEM = "SYSTEM"


# ============================================================
# COMPONENT INTERFACE
# ============================================================

class Component(ABC):

    @abstractmethod
    def update(self, entity: "Entity", engine: "GameEngine") -> None:
        pass


# ============================================================
# COMPONENTS
# ============================================================

@dataclass
class MovementComponent(Component):
    speed: float = 1.0
    direction: Direction = Direction.UP

    def update(
        self,
        entity: "Entity",
        engine: "GameEngine"
    ) -> None:

        if not entity.active:
            return

        if self.direction == Direction.UP:
            entity.position.y += self.speed

        elif self.direction == Direction.DOWN:
            entity.position.y -= self.speed

        elif self.direction == Direction.LEFT:
            entity.position.x -= self.speed

        elif self.direction == Direction.RIGHT:
            entity.position.x += self.speed


@dataclass
class HealthComponent(Component):
    hp: int
    max_hp: int
    armor: int = 0

    def __post_init__(self) -> None:
        if self.max_hp <= 0:
            raise ValueError("max_hp must be greater than 0.")

        if self.hp < 0:
            raise ValueError("hp cannot be negative.")

        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def update(
        self,
        entity: "Entity",
        engine: "GameEngine"
    ) -> None:
        pass

    def take_damage(self, damage: Damage) -> int:
        actual_damage = max(
            0,
            damage.amount - self.armor
        )

        self.hp = max(
            0,
            self.hp - actual_damage
        )

        return actual_damage

    def heal(self, healing: Healing) -> int:
        old_hp = self.hp

        self.hp = min(
            self.max_hp,
            self.hp + healing.amount
        )

        return self.hp - old_hp

    @property
    def is_alive(self) -> bool:
        return self.hp > 0


@dataclass
class CombatComponent(Component):
    attack: int
    defense: int

    def update(
        self,
        entity: "Entity",
        engine: "GameEngine"
    ) -> None:
        pass

    def calculate_damage(self) -> Damage:
        return Damage(self.attack)


@dataclass
class RenderComponent(Component):
    sprite: str
    color: str

    def update(
        self,
        entity: "Entity",
        engine: "GameEngine"
    ) -> None:
        pass

    def render(self, entity: "Entity") -> None:
        print(
            f"   {self.sprite} "
            f"{entity.name} at {entity.position}"
        )


# ============================================================
# ABSTRACT ENTITY
# ============================================================

class Entity(ABC):

    def __init__(
        self,
        entity_id: int,
        name: str,
        position: Position
    ):
        self.id = entity_id
        self.name = name
        self.position = position
        self.active = True
        self.components: list[Component] = []

    @abstractmethod
    def entity_type(self) -> str:
        pass

    def add_component(self, component: Component) -> None:
        self.components.append(component)

    def get_component(self, component_type: type):
        for component in self.components:
            if isinstance(component, component_type):
                return component

        return None

    def update(
        self,
        engine: "GameEngine"
    ) -> None:

        if not self.active:
            return

        for component in self.components:
            component.update(self, engine)

    def render(self) -> None:
        render_component = self.get_component(
            RenderComponent
        )

        if render_component:
            render_component.render(self)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Entity):
            return NotImplemented

        return self.id == other.id

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(id={self.id}, name={self.name!r})"
        )


# ============================================================
# PLAYER
# ============================================================

class Player(Entity):

    def __init__(
        self,
        entity_id: int,
        name: str,
        position: Position,
        health: int = 100
    ):
        super().__init__(
            entity_id,
            name,
            position
        )

        self.score = 0
        self.gold = 150
        self.inventory: list[Item] = []
        self.equipped_item: Item | None = None

        self.add_component(
            MovementComponent(
                speed=5,
                direction=Direction.UP
            )
        )

        self.add_component(
            HealthComponent(
                hp=health,
                max_hp=100,
                armor=8
            )
        )

        self.add_component(
            CombatComponent(
                attack=15,
                defense=8
            )
        )

        self.add_component(
            RenderComponent(
                sprite="👤",
                color="blue"
            )
        )

    def entity_type(self) -> str:
        return "PLAYER"

    @property
    def health_component(self) -> HealthComponent:
        return self.get_component(HealthComponent)

    @property
    def combat_component(self) -> CombatComponent:
        return self.get_component(CombatComponent)

    def add_item(self, item: Item) -> None:
        for existing in self.inventory:
            if existing.name == item.name:
                existing.quantity += item.quantity
                return

        self.inventory.append(item)

    def remove_item(
        self,
        item_name: str,
        quantity: int = 1
    ) -> bool:

        for item in self.inventory:
            if item.name == item_name:
                if item.quantity < quantity:
                    return False

                item.quantity -= quantity

                if item.quantity == 0:
                    self.inventory.remove(item)

                return True

        return False

    def equip(self, item_name: str) -> bool:
        for item in self.inventory:
            if item.name == item_name:
                self.equipped_item = item

                if item.attack > 0:
                    self.combat_component.attack = (
                        15 + item.attack
                    )

                return True

        return False

    def unequip(self) -> None:
        self.equipped_item = None
        self.combat_component.attack = 15

    def inventory_weight(self) -> float:
        return sum(
            item.weight * item.quantity
            for item in self.inventory
        )

    def inventory_count(self) -> int:
        return sum(
            item.quantity
            for item in self.inventory
        )


# ============================================================
# ENEMY
# ============================================================

class Enemy(Entity):

    def __init__(
        self,
        entity_id: int,
        name: str,
        position: Position,
        enemy_type: str,
        damage: int,
        drop_items: list[Item],
        hp: int
    ):
        super().__init__(
            entity_id,
            name,
            position
        )

        self.type = enemy_type
        self.damage = damage
        self.drop_items = drop_items

        self.add_component(
            HealthComponent(
                hp=hp,
                max_hp=hp,
                armor=0
            )
        )

        self.add_component(
            CombatComponent(
                attack=damage,
                defense=5
            )
        )

        self.add_component(
            RenderComponent(
                sprite="👹",
                color="red"
            )
        )

    def entity_type(self) -> str:
        return "ENEMY"

    @property
    def health_component(self) -> HealthComponent:
        return self.get_component(HealthComponent)

    @property
    def combat_component(self) -> CombatComponent:
        return self.get_component(CombatComponent)

    def attack_target(
        self,
        target: Entity,
        engine: "GameEngine"
    ) -> None:

        health = target.get_component(
            HealthComponent
        )

        if health is None:
            return

        damage = Damage(self.damage)

        actual_damage = health.take_damage(
            damage
        )

        engine.emit_event(
            EventType.ATTACK,
            f"{self.name} attacked "
            f"{target.name} (-{actual_damage} HP)"
        )

        if not health.is_alive:
            target.active = False

            engine.emit_event(
                EventType.DEFEAT,
                f"{target.name} defeated!"
            )


# ============================================================
# NPC
# ============================================================

class NPC(Entity):

    def __init__(
        self,
        entity_id: int,
        name: str,
        position: Position,
        dialogue: str,
        quests: list[str]
    ):
        super().__init__(
            entity_id,
            name,
            position
        )

        self.dialogue = dialogue
        self.quests = quests

        self.add_component(
            RenderComponent(
                sprite="🧙",
                color="yellow"
            )
        )

    def entity_type(self) -> str:
        return "NPC"

    def talk(self) -> None:
        print(f'\n💬 {self.name}: "{self.dialogue}"')

        if self.quests:
            print("Quests:")

            for quest in self.quests:
                print(f"  - {quest}")


# ============================================================
# MULTIPLE INHERITANCE
# ============================================================

class EntityComponent(Entity, Component):
    """
    Demonstrates multiple inheritance.

    This class is both an Entity and a Component.
    """

    def __init__(
        self,
        entity_id: int,
        name: str,
        position: Position
    ):
        Entity.__init__(
            self,
            entity_id,
            name,
            position
        )

    def entity_type(self) -> str:
        return "ENTITY_COMPONENT"

    def update(
        self,
        entity: Entity,
        engine: "GameEngine"
    ) -> None:
        print(
            f"EntityComponent updated "
            f"for {entity.name}"
        )


# ============================================================
# EVENT SYSTEM
# ============================================================

@dataclass
class GameEvent:
    frame: int
    event_type: EventType
    message: str

    def __str__(self) -> str:
        return (
            f"{self.frame}: {self.message}"
        )


class EventSystem:

    def __init__(self):
        self.events: list[GameEvent] = []

    def emit(
        self,
        frame: int,
        event_type: EventType,
        message: str
    ) -> None:

        event = GameEvent(
            frame=frame,
            event_type=event_type,
            message=message
        )

        self.events.append(event)

        print(
            f"⚡ {event}"
        )

    def clear(self) -> None:
        self.events.clear()


# ============================================================
# INVENTORY TRADING
# ============================================================

class InventorySystem:

    @staticmethod
    def trade(
        seller: Player,
        buyer: Player,
        item_name: str,
        quantity: int,
        price: int,
        engine: "GameEngine"
    ) -> bool:

        if quantity <= 0:
            return False

        if seller.gold < price:
            return False

        if not seller.remove_item(
            item_name,
            quantity
        ):
            return False

        item = Item(
            name=item_name,
            weight=0.5,
            value=price,
            quantity=quantity
        )

        buyer.add_item(item)

        seller.gold -= price
        buyer.gold += price

        engine.emit_event(
            EventType.TRADE,
            f"{buyer.name} bought "
            f"{quantity} {item_name} "
            f"from {seller.name} for {price}g"
        )

        return True


# ============================================================
# COLLISION SYSTEM
# ============================================================

class CollisionSystem:

    @staticmethod
    def check_collision(
        first: Entity,
        second: Entity,
        distance: float = 1.0
    ) -> bool:

        return (
            first.position.distance_to(
                second.position
            ) <= distance
        )

    @staticmethod
    def detect_collisions(
        entities: list[Entity]
    ) -> list[tuple[Entity, Entity]]:

        collisions = []

        for index, first in enumerate(entities):
            for second in entities[index + 1:]:

                if not first.active or not second.active:
                    continue

                if CollisionSystem.check_collision(
                    first,
                    second
                ):
                    collisions.append(
                        (first, second)
                    )

        return collisions


# ============================================================
# FILE CONTEXT MANAGER
# ============================================================

@contextmanager
def open_game_file(
    filename: str,
    mode: str
) -> Iterator:

    file = open(
        filename,
        mode,
        encoding="utf-8"
    )

    try:
        yield file
    finally:
        file.close()


# ============================================================
# GAME ENGINE
# ============================================================

class GameEngine:

    def __init__(self):
        self.entities: list[Entity] = []
        self.frame = 0
        self.event_system = EventSystem()

        self.time_played_hours = 2.3
        self.enemies_defeated = 45
        self.gold_collected = 2350
        self.level = 12
        self.experience = 4500
        self.experience_required = 5000

    # --------------------------------------------------------
    # ENTITY MANAGEMENT
    # --------------------------------------------------------

    def add_entity(self, entity: Entity) -> None:
        self.entities.append(entity)

    def remove_entity(
        self,
        entity_id: int
    ) -> None:

        self.entities = [
            entity
            for entity in self.entities
            if entity.id != entity_id
        ]

    def get_entity(
        self,
        entity_id: int
    ) -> Entity | None:

        for entity in self.entities:
            if entity.id == entity_id:
                return entity

        return None

    # --------------------------------------------------------
    # EVENT SYSTEM
    # --------------------------------------------------------

    def emit_event(
        self,
        event_type: EventType,
        message: str
    ) -> None:

        self.event_system.emit(
            self.frame,
            event_type,
            message
        )

    # --------------------------------------------------------
    # GAME LOOP
    # --------------------------------------------------------

    def update(self) -> None:

        self.frame += 1

        for entity in self.entities:
            entity.update(self)

    def render(self) -> None:

        for entity in self.entities:
            if entity.active:
                entity.render()

    def run(self, frames: int = 1) -> None:

        for _ in range(frames):
            self.update()
            self.render()

    # --------------------------------------------------------
    # COLLISION
    # --------------------------------------------------------

    def check_collisions(self) -> None:

        collisions = CollisionSystem.detect_collisions(
            self.entities
        )

        for first, second in collisions:
            self.emit_event(
                EventType.SYSTEM,
                f"Collision: "
                f"{first.name} and {second.name}"
            )

    # --------------------------------------------------------
    # SAVE GAME
    # --------------------------------------------------------

    def save_game(
        self,
        filename: str
    ) -> None:

        data = {
            "frame": self.frame,
            "statistics": {
                "time_played_hours":
                    self.time_played_hours,
                "enemies_defeated":
                    self.enemies_defeated,
                "gold_collected":
                    self.gold_collected,
                "level":
                    self.level,
                "experience":
                    self.experience,
                "experience_required":
                    self.experience_required
            },
            "entities": []
        }

        for entity in self.entities:

            entity_data = {
                "id": entity.id,
                "name": entity.name,
                "type": entity.entity_type(),
                "position": asdict(entity.position),
                "active": entity.active
            }

            if isinstance(entity, Player):

                entity_data["score"] = entity.score
                entity_data["gold"] = entity.gold
                entity_data["inventory"] = [
                    asdict(item)
                    for item in entity.inventory
                ]

            elif isinstance(entity, Enemy):

                entity_data["enemy_type"] = entity.type
                entity_data["damage"] = entity.damage

            elif isinstance(entity, NPC):

                entity_data["dialogue"] = entity.dialogue
                entity_data["quests"] = entity.quests

            data["entities"].append(entity_data)

        with open_game_file(
            filename,
            "w"
        ) as file:

            json.dump(
                data,
                file,
                indent=4
            )

    # --------------------------------------------------------
    # LOAD GAME
    # --------------------------------------------------------

    def load_game(
        self,
        filename: str
    ) -> None:

        with open_game_file(
            filename,
            "r"
        ) as file:

            data = json.load(file)

        self.frame = data["frame"]

        statistics = data["statistics"]

        self.time_played_hours = (
            statistics["time_played_hours"]
        )

        self.enemies_defeated = (
            statistics["enemies_defeated"]
        )

        self.gold_collected = (
            statistics["gold_collected"]
        )

        self.level = statistics["level"]
        self.experience = statistics["experience"]
        self.experience_required = (
            statistics["experience_required"]
        )

        self.entities.clear()

        for entity_data in data["entities"]:

            position = Position(
                **entity_data["position"]
            )

            entity_type = entity_data["type"]

            if entity_type == "PLAYER":

                player = Player(
                    entity_id=entity_data["id"],
                    name=entity_data["name"],
                    position=position
                )

                player.score = entity_data["score"]
                player.gold = entity_data["gold"]
                player.active = entity_data["active"]

                for item_data in entity_data["inventory"]:
                    player.add_item(
                        Item(**item_data)
                    )

                self.add_entity(player)

            elif entity_type == "ENEMY":

                enemy = Enemy(
                    entity_id=entity_data["id"],
                    name=entity_data["name"],
                    position=position,
                    enemy_type=entity_data[
                        "enemy_type"
                    ],
                    damage=entity_data["damage"],
                    drop_items=[],
                    hp=30
                )

                enemy.active = entity_data["active"]

                self.add_entity(enemy)

            elif entity_type == "NPC":

                npc = NPC(
                    entity_id=entity_data["id"],
                    name=entity_data["name"],
                    position=position,
                    dialogue=entity_data["dialogue"],
                    quests=entity_data["quests"]
                )

                npc.active = entity_data["active"]

                self.add_entity(npc)

    # --------------------------------------------------------
    # PLAYER ATTACK
    # --------------------------------------------------------

    def player_attack(
        self,
        player: Player,
        enemy: Enemy
    ) -> None:

        damage = Damage(
            player.combat_component.attack
        )

        actual_damage = (
            enemy.health_component.take_damage(
                damage
            )
        )

        self.emit_event(
            EventType.ATTACK,
            f"{player.name} attacked "
            f"{enemy.name} "
            f"(-{actual_damage} HP)"
        )

        if not enemy.health_component.is_alive:

            enemy.active = False

            self.enemies_defeated += 1

            self.emit_event(
                EventType.DEFEAT,
                f"{enemy.name} defeated!"
            )

            for item in enemy.drop_items:

                if isinstance(
                    player,
                    Player
                ):
                    player.add_item(item)

                    self.emit_event(
                        EventType.TRADE,
                        f"{enemy.name} dropped "
                        f"{item}"
                    )

    # --------------------------------------------------------
    # DISPLAY GAME STATE
    # --------------------------------------------------------

    def display_state(self) -> None:

        print("\n" + "=" * 65)
        print("🎮 GAME ENGINE v1.0 🎮")
        print("=" * 65)

        print("\n🛡️ GAME STATE")
        print(f"Frame: {self.frame}")
        print(
            f"Entities: "
            f"{len(self.entities)}"
        )

        players = [
            entity
            for entity in self.entities
            if isinstance(entity, Player)
        ]

        enemies = [
            entity
            for entity in self.entities
            if isinstance(entity, Enemy)
            and entity.active
        ]

        if players:

            player = players[0]

            health = player.health_component

            print("\n👤 PLAYER")
            print(f"Name: {player.name}")
            print(
                f"Health: "
                f"{health.hp}/{health.max_hp}"
            )
            print(
                f"Position: "
                f"{player.position}"
            )
            print(
                f"Inventory: "
                f"{player.inventory_count()} items"
            )

            for item in player.inventory:
                print(f"  - {item}")

            print(f"Gold: {player.gold}g")

            print("\n🔧 COMPONENTS")
            print("Player:")

            movement = player.get_component(
                MovementComponent
            )

            combat = player.combat_component

            print(
                f"  - Movement: "
                f"Speed {movement.speed}, "
                f"Direction: "
                f"{movement.direction.value}"
            )

            print(
                f"  - Health: "
                f"{health.hp}/{health.max_hp}"
            )

            print(
                f"  - Combat: "
                f"Attack {combat.attack}, "
                f"Defense {combat.defense}"
            )

        print(
            f"\n⚔️ ENEMIES "
            f"({len(enemies)} active):"
        )

        for index, enemy in enumerate(
            enemies,
            start=1
        ):

            health = enemy.health_component

            print(
                f"{index}. {enemy.name} "
                f"(HP: {health.hp})"
            )

            print(
                f"   Position: "
                f"{enemy.position}"
            )

            print(
                f"   Damage: "
                f"{enemy.damage}"
            )

            drops = ", ".join(
                str(item)
                for item in enemy.drop_items
            )

            print(
                f"   Drops: "
                f"{drops or 'None'}"
            )

    # --------------------------------------------------------
    # STATISTICS
    # --------------------------------------------------------

    def display_statistics(self) -> None:

        print("\n📊 STATISTICS")

        print(
            f"Time played: "
            f"{self.time_played_hours} hours"
        )

        print(
            f"Enemies defeated: "
            f"{self.enemies_defeated}"
        )

        print(
            f"Gold collected: "
            f"{self.gold_collected}g"
        )

        print(
            f"Level: {self.level}"
        )

        print(
            f"Experience: "
            f"{self.experience}/"
            f"{self.experience_required}"
        )


# ============================================================
# SAMPLE GAME
# ============================================================

def create_game() -> GameEngine:

    engine = GameEngine()

    player = Player(
        entity_id=1,
        name="Damilola",
        position=Position(34, 56)
    )

    player.add_item(
        Item(
            name="Sword",
            weight=3.0,
            value=100,
            attack=10
        )
    )

    player.add_item(
        Item(
            name="Health Potion",
            weight=0.5,
            value=25,
            quantity=3
        )
    )

    player.add_item(
        Item(
            name="Gold Coin",
            weight=0.01,
            value=1,
            quantity=150
        )
    )

    player.equip("Sword")

    goblin = Enemy(
        entity_id=2,
        name="Goblin",
        position=Position(45, 52),
        enemy_type="Goblin",
        damage=5,
        drop_items=[
            Item(
                name="Gold Coin",
                weight=0.01,
                value=10,
                quantity=10
            ),
            Item(
                name="Leather",
                weight=1.0,
                value=15
            )
        ],
        hp=30
    )

    skeleton = Enemy(
        entity_id=3,
        name="Skeleton",
        position=Position(32, 60),
        enemy_type="Skeleton",
        damage=8,
        drop_items=[
            Item(
                name="Bone",
                weight=0.5,
                value=10
            ),
            Item(
                name="Gold Coin",
                weight=0.01,
                value=15,
                quantity=15
            )
        ],
        hp=50
    )

    boss = Enemy(
        entity_id=4,
        name="Boss",
        position=Position(50, 50),
        enemy_type="Boss",
        damage=20,
        drop_items=[
            Item(
                name="Epic Sword",
                weight=4.0,
                value=500,
                attack=25
            ),
            Item(
                name="Gold Coin",
                weight=0.01,
                value=100,
                quantity=100
            )
        ],
        hp=200
    )

    npc = NPC(
        entity_id=5,
        name="Village Elder",
        position=Position(30, 50),
        dialogue="The village needs your help!",
        quests=[
            "Defeat the Goblin",
            "Find the lost sword"
        ]
    )

    engine.add_entity(player)
    engine.add_entity(goblin)
    engine.add_entity(skeleton)
    engine.add_entity(boss)
    engine.add_entity(npc)

    return engine


# ============================================================
# DEMO
# ============================================================

def main() -> None:

    engine = create_game()

    engine.frame = 1234

    engine.display_state()

    # --------------------------------------------------------
    # EVENT: PLAYER MOVEMENT
    # --------------------------------------------------------

    player = engine.get_entity(1)

    if isinstance(player, Player):

        movement = player.get_component(
            MovementComponent
        )

        movement.direction = Direction.UP

        old_position = str(player.position)

        engine.update()

        engine.emit_event(
            EventType.MOVE,
            f"Player moved from "
            f"{old_position} to "
            f"{player.position}"
        )

    # --------------------------------------------------------
    # PLAYER ATTACKS GOBLIN
    # --------------------------------------------------------

    goblin = engine.get_entity(2)

    if (
        isinstance(player, Player)
        and isinstance(goblin, Enemy)
    ):

        engine.frame = 1235

        engine.player_attack(
            player,
            goblin
        )

    # --------------------------------------------------------
    # GOBLIN ATTACKS PLAYER
    # --------------------------------------------------------

    if (
        isinstance(player, Player)
        and isinstance(goblin, Enemy)
        and goblin.active
    ):

        engine.frame = 1236

        goblin.attack_target(
            player,
            engine
        )

    # --------------------------------------------------------
    # SECOND ATTACK TO DEFEAT GOBLIN
    # --------------------------------------------------------

    if (
        isinstance(player, Player)
        and isinstance(goblin, Enemy)
        and goblin.active
    ):

        engine.frame = 1237

        engine.player_attack(
            player,
            goblin
        )

    # --------------------------------------------------------
    # NPC
    # --------------------------------------------------------

    npc = engine.get_entity(5)

    if isinstance(npc, NPC):
        npc.talk()

    # --------------------------------------------------------
    # COLLISION
    # --------------------------------------------------------

    engine.check_collisions()

    # --------------------------------------------------------
    # SAVE
    # --------------------------------------------------------

    print("\n💾 Saving game...", end=" ")

    save_file = "game_state.json"

    engine.save_game(save_file)

    print("✅")

    # --------------------------------------------------------
    # LOAD TEST
    # --------------------------------------------------------

    loaded_engine = GameEngine()

    loaded_engine.load_game(
        save_file
    )

    print(
        f"Loaded game at frame "
        f"{loaded_engine.frame}"
    )

    # --------------------------------------------------------
    # STATISTICS
    # --------------------------------------------------------

    engine.display_statistics()


if __name__ == "__main__":
    main()