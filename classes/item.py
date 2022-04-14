import random

from exceptions import UseFunctionNotDefined


class Item:
    def __init__(self, name: str, plural: str = "", use_function=lambda: None):
        self.name: str = name
        self.plural: str = plural
        self.use_function = use_function

    def __str__(self):
        return self.name

    def use(self):
        from main import CHARACTER

        if self.use_function:
            self.use_function()
            CHARACTER.inventory.pop(self, None)
        else:
            raise UseFunctionNotDefined


class Weapon(Item):
    def __init__(
            self,
            name: str,
            plural: str = "",
            base_damage: int = 0,
            damage_variation: float = 0):
        super().__init__(name, plural)
        self.base_damage: int = base_damage
        self.damage_variation: float = damage_variation

    def to_json(self) -> dict:
        return {
            "name": self.name,
            "plural": self.plural,
            "base_damage": self.base_damage,
            "damage_variation": self.damage_variation
        }

    def attack(self) -> int:
        attack_damage = self.base_damage + \
            random.randint(0, self.damage_variation)
        return attack_damage

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
    pass


class WeaponRanged(Weapon):
    def __init__(self,
                 name: str,
                 plural: str = "",
                 base_damage: int = 0,
                 damage_variation: float = 0,
                 ammunition: int = 0):
        super().__init__(name, plural, base_damage, damage_variation)
        self.ammunition: int = ammunition

    def to_json(self) -> dict:
        ret = super().to_json()
        ret["ammunition"] = self.ammunition
        return ret

    def attack(self) -> int:
        if self.ammunition > 0:
            super().attack()
        else:
            print("You have no more ammunition")
