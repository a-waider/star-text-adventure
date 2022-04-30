import random
from typing import Tuple

from termcolor import colored
from utilities import colored_health

from classes.inventory import Inventory
from classes.item import Item, Weapon

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

    def __bool__(self):
        """Returns True if the npc is alive else False."""
        return self.health > 0

    def to_json(self):
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

    def attack(self) -> 'Tuple[int, bool]':
        if random.random() > (1-self.krit_chance):
            return int(self.krit_damage), True
        return int(self.base_damage), False

    def defend(self, damage: int):
        from main import CHARACTER

        if self.armor == 0:
            self.health = max(self.health-damage, 0)
        else:
            self.health = max(self.health-int(damage / self.armor * 10), 0)
        self.armor = round(max(self.armor - damage*0.25, 0), 1)
        if self.health <= 0:
            CHARACTER.kills += 1
            print(f"You defeated {self}.")
            for item, amount in self.loot.items():
                CHARACTER.room.loot.add_item(item, amount)
            CHARACTER.room.npc = None

    def fighting_stats(self, prev_health: int = None, prev_armor: int = None, weapon: Weapon = None) -> str:
        heart_icon, health_color = colored_health(self.health, self.max_health)
        health_lost_string: str = f"{prev_health} - {prev_health-self.health}  ({weapon}) = " if prev_health else ""
        armor_damage_string: str = f"{prev_armor} - {prev_armor-self.armor} = " if prev_armor else ""
        return f"""{'Health: ':15}{heart_icon} {health_lost_string}\
{colored(f'{self.health} / {self.max_health}', health_color)}
{'Armor: ':15}🛡  {armor_damage_string}{colored(self.armor, 'blue')}"""
