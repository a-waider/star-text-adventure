import random

from termcolor import colored

from classes.item import Item


class NPC:
    def __init__(self,
                 name: str,
                 health: int = 100,
                 base_damage: int = 10,
                 krit_damage: int = 0,
                 krit_chance: float = 0,
                 armor: int = 0,
                 loot: 'dict[Item]' = None):
        self.name = name
        self.health = health
        self.base_damage = base_damage
        self.krit_damage = krit_damage
        self.krit_chance = krit_chance
        self.armor = armor
        self.loot = loot if loot is not None else dict()

    def __str__(self):
        return colored(self.name, color="red")

    def to_json(self):
        from world.items import Items
        return {
            "name": self.name,
            "health": self.health,
            "base_damage": self.base_damage,
            "krit_damage": self.krit_damage,
            "krit_chance": self.krit_chance,
            "armor": self.armor,
            "loot": Items.dict_to_json(self.loot)
        }

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

    def show_npc_stats(self):
        print(f"""
            Health:  {colored(round(self.health), 'blue')}
            Damage:  {self.base_damage}
            Armor:   {self.armor}
            Coin(s): {colored(self, 'yellow')}
            """)

    def fighting_stats(self) -> str:
        if self.health < 30:
            health_color = "yellow"
        elif self.health < 10:
            health_color = "red"
        else:
            health_color = "green"
        ret = f"Health: {colored(self.health, health_color)}\nArmor: {colored(self.armor, 'blue')}"
        return ret
