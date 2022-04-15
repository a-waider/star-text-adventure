from enum import Enum

from classes.item import Item, Map, WeaponMelee, WeaponRanged


ROOM_NAME_LENGTH = 15


def book():
    pass


def key_front_door():
    from main import CHARACTER

    from world.rooms import Rooms

    if CHARACTER.room == Rooms.CORRIDOR.value:
        Rooms.FRONT_YARD.value.locked = False
        print("The front door has been unlocked")
    else:
        print("You need to use this key in the corridor")


def lockpicker():
    from main import CHARACTER

    from world.rooms import Rooms

    if CHARACTER.room == Rooms.FRONT_YARD.value:
        Rooms.GARAGE.value.locked = False
        print("The front door has been unlocked")
    else:
        print("The Lockpicker doesn't work in this room")


def map_home():
    from world.rooms import Rooms

    print(f"""
{"".center(ROOM_NAME_LENGTH)}    {Rooms.BEDROOM.value.name.center(ROOM_NAME_LENGTH)}    {"".center(ROOM_NAME_LENGTH)}    {"".center(ROOM_NAME_LENGTH)}
{"".center(ROOM_NAME_LENGTH)}    {"|".center(ROOM_NAME_LENGTH)}    {"".center(ROOM_NAME_LENGTH)}    {"".center(ROOM_NAME_LENGTH)}
{"".center(ROOM_NAME_LENGTH)}    {"|".center(ROOM_NAME_LENGTH)}    {"".center(ROOM_NAME_LENGTH)}    {"".center(ROOM_NAME_LENGTH)}
{Rooms.LIVING_ROOM.value.name.center(ROOM_NAME_LENGTH)} -- {Rooms.CORRIDOR.value.name.center(ROOM_NAME_LENGTH)} -- \
    {Rooms.LOUNGE.value.name.center(ROOM_NAME_LENGTH)} -- {Rooms.KITCHEN.value.name.center(ROOM_NAME_LENGTH)}
{"".center(ROOM_NAME_LENGTH)}    {"|".center(ROOM_NAME_LENGTH)}    {"".center(ROOM_NAME_LENGTH)}    {"".center(ROOM_NAME_LENGTH)}
{"".center(ROOM_NAME_LENGTH)}    {"|".center(ROOM_NAME_LENGTH)}    {"".center(ROOM_NAME_LENGTH)}    {"".center(ROOM_NAME_LENGTH)}
{"".center(ROOM_NAME_LENGTH)}    {Rooms.FRONT_YARD.value.name.center(ROOM_NAME_LENGTH)}    {"".center(ROOM_NAME_LENGTH)}    {"".center(ROOM_NAME_LENGTH)}
""")


def map_street():
    from world.rooms import Rooms


class Items(Enum):
    # World 1: Creapy House
    COIN: Item = Item(
        name="Coin",
        plural="Coins",
        icon="🪙")

    # Keys
    KEY_HOME: Item = Item(
        name="Key front door",
        icon="🔑🗝",
        use_function=key_front_door)
    LOCKPICKER: Item = Item(
        name="Lockpicker",
        use_function=lockpicker)

    # Maps
    MAP_HOME: Map = Map(
        name="home map",
        view_function=map_home)

    MAP_STREET: Map = Map(
        name="street map",
        view_function=map_street)

    # Weapons
    FIST: WeaponMelee = WeaponMelee(
        name="Fist",
        icon="👊",
        base_damage=5,
        damage_variation=1)
    KNIFE: WeaponMelee = WeaponMelee(
        name="Knife",
        icon="🔪",
        base_damage=20,
        damage_variation=10)
    BOW: WeaponRanged = WeaponRanged(
        name="Bow",
        icon="🏹",
        base_damage=15,
        damage_variation=15)

    @ staticmethod
    def get_item_by_name(name: str) -> Item:
        items: 'list[Item]' = [a.value for a in Items]
        for item in items:
            if item.name.lower() == name.lower() or item.plural.lower() == name.lower():
                return item
        return None

    @ staticmethod
    def dict_to_json(items: 'dict[Item]'):
        ret = dict()  # pylint: disable=duplicate-code
        for item, amount in items.items():
            ret[str(item)] = amount
        return ret
