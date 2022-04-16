import random

from exceptions import UseFunctionNotDefined
from termcolor import colored


class Item:
    def __init__(self, name: str, plural: str = "", icon: str = "", use_function=lambda: None):
        self.name: str = name
        self.plural: str = plural
        self.icon: str = icon
        self.use_function = use_function

    def __str__(self, plural: bool = False):
        ret = ""
        if self.icon:
            ret += f"{self.icon}  "
        if plural:
            ret += colored(self.plural, "yellow")
        else:
            ret += colored(self.name, "yellow")
        return ret

    def use(self, amount: int = 1):
        from main import CHARACTER

        if self.use_function:
            self.use_function(amount=amount)
        else:
            raise UseFunctionNotDefined


class Map(Item):
    def __init__(
            self,
            name: str,
            plural: str = "",
            icon: str = "",
            view_function=lambda: None):
        super().__init__(name, plural, icon)
        self.view_function = view_function

    def view(self):
        self.view_function()

    @staticmethod
    def get_map_by_name(name: str):
        from world.items import Items

        maps: 'list[Map]' = [
            item.value for item in Items if isinstance(item.value, Map)]
        for requested_map in maps:
            if requested_map.name.lower() == name.lower():
                return requested_map
        return None


class Weapon(Item):
    def __init__(
            self,
            name: str,
            plural: str = "",
            icon: str = "",
            base_damage: int = 0,
            damage_variation: float = 0):
        super().__init__(name, plural, icon)
        self.base_damage: int = base_damage
        self.damage_variation: float = damage_variation

    def to_json(self) -> dict:
        return {
            "name": self.name,
            "plural": self.plural,
            "icon": self.icon,
            "base_damage": self.base_damage,
            "damage_variation": self.damage_variation
        }

    @staticmethod
    def from_json(json_object: 'dict') -> 'Weapon':
        if json_object:
            return Weapon(
                name=json_object["name"],
                plural=json_object["plural"],
                icon=json_object["icon"],
                base_damage=json_object["base_damage"],
                damage_variation=json_object["damage_variation"],
            )
        return None

    def attack(self) -> int:
        return self.base_damage + random.randint(0, self.damage_variation)

    @staticmethod
    def get_weapon_by_name(name: str) -> 'Weapon':
        from world.items import Items

        weapons: 'list[Weapon]' = [
            item.value for item in Items if isinstance(item.value, Weapon)]
        for weapon in weapons:
            if weapon.name.lower() == name.lower():
                return weapon
        return None


class WeaponMelee(Weapon):
    @staticmethod
    def from_json(json_object: 'dict') -> 'WeaponMelee':
        if json_object:
            weapon: Weapon = Weapon.from_json(json_object)
            return WeaponMelee(
                name=weapon.name,
                plural=weapon.plural,
                icon=weapon.icon,
                base_damage=weapon.base_damage)
        return None


class WeaponRanged(Weapon):
    def __init__(self,
                 name: str,
                 plural: str = "",
                 icon: str = "",
                 base_damage: int = 0,
                 damage_variation: float = 0,
                 ammunition: int = 0):
        super().__init__(name, plural, icon, base_damage, damage_variation)
        self.ammunition: int = ammunition

    def to_json(self) -> dict:
        ret = super().to_json()
        ret["ammunition"] = self.ammunition
        return ret

    @ staticmethod
    def from_json(json_object: 'dict') -> 'WeaponRanged':
        if json_object:
            weapon: Weapon = Weapon.from_json(json_object)
            return WeaponRanged(
                name=weapon.name,
                plural=weapon.plural,
                icon=weapon.icon,
                base_damage=weapon.base_damage,
                ammunition=json_object["ammunition"])
        return None

    def attack(self) -> int:
        if self.ammunition > 0:
            return super().attack()
        else:
            print("You have no more ammunition")
