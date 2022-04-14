from enum import Enum

from classes.item import Item, WeaponMelee, WeaponRanged


def book():
    pass


def key_front_door():
    from main import CHARACTER

    from world.rooms import Rooms

    if CHARACTER.room == Rooms.CORRIDOR.value:
        Rooms.GARDEN.value.locked = False
        print("The front door has been unlocked")
    else:
        print("You need to use this key in the corridor")


class Items(Enum):
    # World 1: Creapy House
    COIN: Item = Item(
        name="Coin",
        plural="Coins")
    KEY_HOME: Item = Item(
        name="Key front door",
        use_function=key_front_door)

    # Weapons
    FIST: WeaponMelee = WeaponMelee(
        name="Fist",
        base_damage=5,
        damage_variation=1)
    KNIFE: WeaponMelee = WeaponMelee(
        name="Knife",
        base_damage=20,
        damage_variation=10)
    BOW: WeaponRanged = WeaponRanged(
        name="Bow",
        base_damage=15,
        damage_variation=15)

    @staticmethod
    def get_item_by_name(name: str) -> Item:
        items: 'list[Item]' = [a.value for a in Items]
        for item in items:
            if item.name.lower() == name.lower() or item.plural.lower() == name.lower():
                return item
        return None

    @staticmethod
    def dict_to_json(items: 'dict[Item]'):
        ret = dict()  # pylint: disable=duplicate-code
        for item, amount in items.items():
            ret[str(item)] = amount
        return ret
