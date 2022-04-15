import random

from termcolor import colored

from classes.inventory import Inventory
from classes.item import Item

DEFAULT_MAX_HEALTH = 100
DEFAULT_HEALTH = None
DEFAULT_BASE_DAMAGE = 10
DEFAULT_KRIT_DAMAGE = 0
DEFAULT_KRIT_CHANCE = 0
DEFAULT_ARMOR = 0
DEFAULT_LOOT = None


class NPC:
    def __init__(self,
                 name: str,
                 max_health: int = DEFAULT_MAX_HEALTH,
                 health: int = DEFAULT_HEALTH,
                 base_damage: int = DEFAULT_BASE_DAMAGE,
                 krit_damage: int = DEFAULT_KRIT_DAMAGE,
                 krit_chance: float = DEFAULT_KRIT_CHANCE,
                 armor: int = DEFAULT_ARMOR,
                 loot: 'dict[Item]' = DEFAULT_LOOT):
        self.name: str = name
        self.max_health: int = max_health
        self.health: int = health if health else max_health
        self.base_damage: int = base_damage
        self.krit_damage: int = krit_damage
        self.krit_chance: float = krit_chance
        self.armor: int = armor
        self.loot: 'Inventory[Item,int]' = loot if loot is not None else Inventory(
        )

    def __str__(self):
        return colored(self.name, color="red")

    def to_json(self):
        from world.items import Items
        return {
            "name": self.name,
            "max_health": self.max_health,
            "health": self.health,
            "base_damage": self.base_damage,
            "krit_damage": self.krit_damage,
            "krit_chance": self.krit_chance,
            "armor": self.armor,
            "loot": self.loot.to_json()
        }

    @staticmethod
    def from_json(json_object: 'dict') -> 'NPC':
        from world.items import Items

        return NPC(
            name=json_object["name"],
            max_health=json_object["max_health"] if json_object["max_health"] else DEFAULT_MAX_HEALTH,
            health=json_object["health"] if json_object["health"] else DEFAULT_HEALTH,
            base_damage=json_object["base_damage"] if json_object["base_damage"] else DEFAULT_BASE_DAMAGE,
            krit_damage=json_object["krit_damage"] if json_object["krit_damage"] else DEFAULT_KRIT_DAMAGE,
            krit_chance=json_object["krit_chance"] if json_object["krit_chance"] else DEFAULT_KRIT_CHANCE,
            armor=json_object["armor"] if json_object["armor"] else DEFAULT_ARMOR,
            loot=Inventory.from_json(json_object["loot"])
        ) if json_object else None

    def attack(self) -> int:
        rand = random.random()
        # TODO: probably logical error
        if self.krit_chance < rand:
            return int(self.base_damage)
        return int(self.krit_damage)

    def defend(self, damage: int):
        self.armor = max(self.armor - damage*0.25, 0)
        if self.armor == 0:
            self.health = max(self.health-damage, 0)
        else:
            self.health = max(self.health-int(damage / self.armor * 10), 0)

    def fighting_stats(self) -> str:
        if self.health/self.max_health < 0.3:
            health_color = "yellow"
            heart_icon = "💛"
        elif self.health/self.max_health < 0.1:
            health_color = "red"
            heart_icon = "❤"
        else:
            health_color = "green"
            heart_icon = "💚"
        return f"{'Health: ':15}{heart_icon} {colored(self.health, health_color)}\n{'Armor: ':15}🛡  {colored(self.armor, 'blue')}"
