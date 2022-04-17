from enum import Enum

from termcolor import colored
from classes.item import Item, Map, WeaponMelee, WeaponRanged
from classes.room import Room
from utilities import print

ROOM_NAME_LENGTH = 24

# pylint: disable=unused-argument


def armor(amount: int):
    from main import CHARACTER

    if amount <= CHARACTER.inventory[Items.ARMOR.value]:
        CHARACTER.inventory.remove_item(Items.ARMOR.value, amount=amount)
        CHARACTER.armor += amount
        print(f"You have now {CHARACTER.armor} {Items.ARMOR.value}.")
    else:
        print("You don't have enough Armor in your inventory.")


def arrow(amount: int):
    from main import CHARACTER

    if amount <= CHARACTER.inventory[Items.BULLET_MAGAZINE.value]:
        if CHARACTER.ranged_weapon:
            CHARACTER.inventory.remove_item(
                Items.BULLET_MAGAZINE.value, amount=amount)
            CHARACTER.ranged_weapon.ammunition += amount
            print(
                f"You now have {CHARACTER.ranged_weapon.ammunition} ammunition in your {CHARACTER.ranged_weapon}.")
        else:
            print("You don't have a ranged weapon equipped.")
    else:
        print("You don't have enough Arrows in your inventory.")


def healing_potion(amount: int):
    from main import CHARACTER
    from commands import show_health

    gained_health_per_potion = 25

    CHARACTER.inventory.remove_item(Items.HEALING_POTION.value, amount=amount)
    CHARACTER.add_health(amount*gained_health_per_potion)
    print(f"You regained {amount*gained_health_per_potion} health.")
    show_health()


def key_front_door(amount: int):
    from main import CHARACTER

    from world.rooms import Rooms

    if CHARACTER.room == Rooms.CORRIDOR.value:
        Rooms.FRONT_YARD.value.locked = False
        CHARACTER.inventory.remove_item(Items.KEY_HOME.value)
        print("The front door has been unlocked")
    else:
        print("You need to use this key in the corridor")


def lockpicker(amount: int):
    from main import CHARACTER

    from world.rooms import Rooms

    if CHARACTER.room == Rooms.FRONT_YARD.value:
        Rooms.GARAGE.value.locked = False
        CHARACTER.inventory.remove_item(Items.LOCKPICKER.value)
        print("The garage door has been unlocked")
    else:
        print("The Lockpicker doesn't work in this room")


def _room_string(room: Room) -> str:
    from main import CHARACTER

    from world.items import ROOM_NAME_LENGTH

    if CHARACTER.room == room:
        return colored(room.name.center(ROOM_NAME_LENGTH), "yellow")
    return room.name.center(ROOM_NAME_LENGTH)


def map_home():
    from main import CHARACTER

    from world.rooms import Rooms

    print(f"""
{" "*ROOM_NAME_LENGTH}    {_room_string(Rooms.BEDROOM.value)}
{" "*ROOM_NAME_LENGTH}    {"|".center(ROOM_NAME_LENGTH)}
{" "*ROOM_NAME_LENGTH}    {"|".center(ROOM_NAME_LENGTH)}
{_room_string(Rooms.LIVING_ROOM.value)} -- {_room_string(Rooms.CORRIDOR.value)} -- {_room_string(Rooms.LOUNGE.value)} -- {_room_string(Rooms.KITCHEN.value)}
{" "*ROOM_NAME_LENGTH}    {"|".center(ROOM_NAME_LENGTH)}
{" "*ROOM_NAME_LENGTH}    {"|".center(ROOM_NAME_LENGTH)}
{" "*ROOM_NAME_LENGTH}    {_room_string(Rooms.FRONT_YARD.value)}
""", sleep_time=0.0001)


def map_street():
    from world.rooms import Rooms

    print(f"""
{" "*int(0.6*ROOM_NAME_LENGTH)}  {_room_string(Rooms.NEIGHBOR_JOES_HOUSE.value)}  {_room_string(Rooms.CREEPY_NEIGHBORS_HOUSE.value)}
{" "*int(1.35*ROOM_NAME_LENGTH)}\\ {"".center(int(ROOM_NAME_LENGTH/2))} /
{" "*int(1.35*ROOM_NAME_LENGTH)} \\{"".center(int(ROOM_NAME_LENGTH/2))}/
{_room_string(Rooms.FRONT_YARD.value)} -- {_room_string(Rooms.CANAL_STREET.value)} -- {_room_string(Rooms.MONTANA_AVENUE.value)}
{" "*ROOM_NAME_LENGTH}    {"|".center(ROOM_NAME_LENGTH)}
{" "*ROOM_NAME_LENGTH}    {"|".center(ROOM_NAME_LENGTH)}
{" "*ROOM_NAME_LENGTH}    {_room_string(Rooms.PRINCESS_MAGDALENA_GARDEN.value)}
""", sleep_time=0.0001)


class Items(Enum):
    # General
    COIN: Item = Item(
        name="Coin",
        plural="Coins",
        icon="🪙")
    ARMOR: Item = Item(
        name="Armor",
        plural="Armor",
        icon="🛡",
        use_function=armor,
        use_on_pickup=True)
    BULLET_MAGAZINE: Item = Item(
        name="Bullet cartridge",
        plural="Bullet cartridges",
        use_function=arrow)
    HEALING_POTION: Item = Item(
        name="Healing potion",
        plural="Healing potions",
        use_function=healing_potion)

    # Keys
    KEY_HOME: Item = Item(
        name="Key front door",
        icon="🔑",
        use_function=key_front_door)
    LOCKPICKER: Item = Item(
        name="Lockpicker",
        icon="🔒",
        use_function=lockpicker)

    # Maps
    MAP_HOME: Map = Map(
        name="home map",
        icon="🗺",
        view_function=map_home)

    MAP_STREET: Map = Map(
        name="street map",
        icon="🗺",
        view_function=map_street)

    # Weapons
    REMOTE: WeaponMelee = WeaponMelee(
        name="Remote",
        base_damage=5,
        damage_variation=1)
    KNIFE: WeaponMelee = WeaponMelee(
        name="Knife",
        icon="🔪",
        base_damage=15,
        damage_variation=7)
    AXE: WeaponMelee = WeaponMelee(
        name="Axe",
        icon="🪓",
        base_damage=25,
        damage_variation=10)
    GUN: WeaponRanged = WeaponRanged(
        name="Gun",
        icon="🔫",
        base_damage=12,
        damage_variation=15,
        ammunition=3)

    @ staticmethod
    def get_item_by_name(name: str) -> Item:
        items: 'list[Item]' = [a.value for a in Items]
        for item in items:
            if item.name.lower() == name.lower() or item.plural.lower() == name.lower():
                return item
        return None

    @ staticmethod
    def dict_to_json(items: 'dict[Item]'):
        ret = dict()
        for item, amount in items.items():
            ret[item.name] = amount
        return ret
