from enum import Enum

from classes.item import Item, Map, Weapon, WeaponMelee, WeaponRanged
from classes.room import Room
from termcolor import colored
from utilities import print

# pylint: disable=unused-argument


def armor(amount: int):
    from main import CHARACTER

    if amount <= CHARACTER.inventory[Items.ARMOR.value]:
        CHARACTER.inventory.remove_item(Items.ARMOR.value, amount=amount)
        CHARACTER.armor += amount
        print(f"You have now {CHARACTER.armor} {Items.ARMOR.value}.")
    else:
        print("You don't have enough Armor in your inventory.")


def bullet_cartridge(amount: int):
    from main import CHARACTER

    if amount <= CHARACTER.inventory[Items.BULLET_CARTRIDGE.value]:
        if CHARACTER.ranged_weapon:
            if CHARACTER.ranged_weapon.name in (Items.PISTOL.value.name, Items.AK_47.value.name):
                CHARACTER.inventory.remove_item(
                    Items.BULLET_CARTRIDGE.value, amount=amount)
                CHARACTER.ranged_weapon.ammunition += amount
                print(
                    f"You now have {CHARACTER.ranged_weapon.ammunition} ammunition in your {CHARACTER.ranged_weapon}.")
            else:
                print(
                    f"You can't equip {Items.BULLET_CARTRIDGE.value} on your {CHARACTER.ranged_weapon}.")
        else:
            print("You don't have a ranged weapon equipped.")
    else:
        print(
            f"You don't have enough {Items.BULLET_CARTRIDGE.value} in your inventory.")


def healing_potion(amount: int):
    from main import CHARACTER

    from world.commands import show_statistics

    gained_health_per_potion = 25

    CHARACTER.inventory.remove_item(Items.HEALING_POTION.value, amount=amount)
    CHARACTER.add_health(amount*gained_health_per_potion)
    print(f"You regained {amount*gained_health_per_potion} health.")
    show_statistics()


def apple(amount: int):
    from main import CHARACTER

    from world.commands import show_statistics

    gained_health_per_apple = 2*amount

    CHARACTER.inventory.remove_item(Items.APPLE.value, amount=amount)
    CHARACTER.add_health(amount*gained_health_per_apple)
    print(f"You regained {amount*gained_health_per_apple} health.")
    show_statistics()


def banana(amount: int):
    from main import CHARACTER

    from world.commands import show_statistics

    gained_health_per_banana = 4*amount

    CHARACTER.inventory.remove_item(Items.BANANA.value, amount=amount)
    CHARACTER.add_health(amount*gained_health_per_banana)
    print(f"You regained {amount*gained_health_per_banana} health.")
    show_statistics()


def eggplant(amount: int):
    from main import CHARACTER

    print(f"The {Items.EGGPLANT.value} can't boost your health. \
Instead your sex appeal increases enormously.")
    CHARACTER.inventory.remove_item(Items.EGGPLANT.value)


def pretzel(amount: int):
    from main import CHARACTER

    from world.commands import show_statistics

    gained_health_per_pretzel = 3*amount

    CHARACTER.inventory.remove_item(Items.PRETZEL.value, amount=amount)
    CHARACTER.add_health(amount*gained_health_per_pretzel)
    print(f"You regained {amount*gained_health_per_pretzel} health.")
    show_statistics()


def antidote(amount: int):
    from main import CHARACTER

    from world.rooms import Rooms

    if CHARACTER.inventory[Items.ANTIDOTE.value] > 1:
        CHARACTER.inventory[Items.ANTIDOTE.value] = 1
        print("Don't try to trick the game ;)")
        return
    if CHARACTER.room.npc:
        if CHARACTER.room == Rooms.BOSSFIGHT_ARENA.value:
            print("The Antidote doesn't work against The zombie boss.")
        else:
            print(
                f"You healed {CHARACTER.room.npc}. {CHARACTER.room.npc} is no longer a thread.")
            CHARACTER.inventory.remove_item(Items.ANTIDOTE.value)
            CHARACTER.cures += 1
            CHARACTER.room.npc = None


def holy_scepter(amount: int):
    from main import CHARACTER

    armor_gained_by_holy_scepter = 40

    CHARACTER.inventory.remove_item(
        Items.HOLY_SCEPTER.value, CHARACTER.inventory[Items.HOLY_SCEPTER.value])
    CHARACTER.armor += armor_gained_by_holy_scepter
    print(f"You have now {CHARACTER.armor} {Items.ARMOR.value}.")


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
        print(f"The door to {Rooms.GARAGE.value} has been unlocked.")
    elif CHARACTER.room in (Rooms.MONTANA_AVENUE.value, Rooms.NEWMAN_ROW.value):
        Rooms.HAIRY_BARBER.value.locked = False
        print(f"The door to {Rooms.HAIRY_BARBER.value} has been unlocked")
    else:
        print("The Lockpicker doesn't work in this room.")


def key_motel_one(amount: int):
    from main import CHARACTER

    from world.rooms import KILLS_TO_OPEN_MOTEL_ONE, Rooms
    if CHARACTER.room == Rooms.NEWMAN_ROW.value:
        Rooms.MOTEL_ONE.value.locked = False
        print(f"You have shown yourself worthy to enter {Rooms.MOTEL_ONE.value} \
by killing {KILLS_TO_OPEN_MOTEL_ONE} zombies.")
    else:
        print(f"You can't go to {Rooms.MOTEL_ONE.value} from here.")


def _room_string(room: Room, blurred: bool = False) -> str:
    from main import CHARACTER

    from world.rooms import Rooms

    room_name_length = max([len(room.name) for room in Rooms])

    if blurred:
        room_name = ("*"*len(room.name)).center(room_name_length)
    else:
        room_name = room.name.center(room_name_length)
    if CHARACTER.room == room:
        return colored(room_name, "yellow")
    return room_name


def map_home():
    from world.rooms import Rooms

    room_name_length = max([len(room.name) for room in Rooms])

    print(f"""
{" "*room_name_length}    {_room_string(Rooms.BEDROOM.value)}
{" "*room_name_length}    {"|".center(room_name_length)}
{" "*room_name_length}    {"|".center(room_name_length)}
{_room_string(Rooms.LIVING_ROOM.value)}----{_room_string(Rooms.CORRIDOR.value)}----{_room_string(Rooms.LOUNGE.value)}----{_room_string(Rooms.KITCHEN.value)}
{" "*room_name_length}    {"|".center(room_name_length)}
{" "*room_name_length}    {"|".center(room_name_length)}
{_room_string(Rooms.GRAVESTONE.value)}----{_room_string(Rooms.FRONT_YARD.value)}----{_room_string(Rooms.GARAGE.value)}
""", sleep_time=0.0001)


def map_street_blurred(blurred: bool = True):
    from world.rooms import Rooms

    def _blurred(room: Room) -> str:
        return "*"*len(room.name)

    room_name_length = max([len(room.name) for room in Rooms])

    tmp = "\\"
    print(f"""
{" "*int(0.6*room_name_length)}  {_room_string(Rooms.NEIGHBOR_JOES_HOUSE.value)}  {_room_string(Rooms.CREEPY_NEIGHBORS_HOUSE.value)}{_room_string(Rooms.REWE_TO_GO.value, blurred=blurred)}{_room_string(Rooms.SACRISTY.value, blurred=blurred)}
{" "*int(1.35*room_name_length)}\\ {"".center(int(room_name_length/2))} /{" "*room_name_length} /{" "*room_name_length} /
{" "*int(1.35*room_name_length)} \\{"".center(int(room_name_length/2))}/ {" "*room_name_length}/ {" "*room_name_length}/
{_room_string(Rooms.FRONT_YARD.value)}----{_room_string(Rooms.CANAL_STREET.value)}----{_room_string(Rooms.MONTANA_AVENUE.value)}----{_room_string(Rooms.CATHETRAL.value)}----{_room_string(Rooms.CATACOMB.value, blurred=blurred)}
{" "*room_name_length}    {"|".center(room_name_length)}    {"|".center(room_name_length)}
{" "*room_name_length}   {"/".center(room_name_length)}      {tmp.center(room_name_length)}
{_room_string(Rooms.PRINCESS_MAGDALENA_GARDEN.value, blurred=blurred)} {"--<".center(room_name_length)}          {">--".center(room_name_length)} {_room_string(Rooms.HAIRY_BARBER.value)}----{_room_string(Rooms.BATHROOM.value)}
{" "*room_name_length if blurred else "|".center(room_name_length)}   {tmp.center(room_name_length)}      {"/".center(room_name_length)}
{" "*room_name_length if blurred else "|".center(room_name_length)}    {"|".center(room_name_length)}    {"|".center(room_name_length)}
{" "*room_name_length if blurred else _room_string(Rooms.BOSSFIGHT_ARENA.value)}    {_room_string(Rooms.WILSON_GROVE.value, blurred=blurred)}----{_room_string(Rooms.NEWMAN_ROW.value)}----{_room_string(Rooms.MOTEL_ONE.value, blurred=blurred)}
""", sleep_time=0.0001)


def map_street_full():
    from world.rooms import Rooms

    Rooms.REWE_TO_GO.value.locked = False
    Rooms.SACRISTY.value.locked = False
    Rooms.CATACOMB.value.locked = False
    Rooms.PRINCESS_MAGDALENA_GARDEN.value.locked = False
    Rooms.WILSON_GROVE.value.locked = False
    map_street_blurred(blurred=False)


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
    BULLET_CARTRIDGE: Item = Item(
        name="Bullet cartridge",
        plural="Bullet cartridges",
        use_function=bullet_cartridge)
    HEALING_POTION: Item = Item(
        name="Healing potion",
        plural="Healing potions",
        use_function=healing_potion)
    APPLE: Item = Item(
        name="Apple",
        plural="Apples",
        icon="🍎",
        use_function=apple)
    BANANA: Item = Item(
        name="Banana",
        plural="Bananas",
        icon="🍌",
        use_function=banana)
    EGGPLANT: Item = Item(
        name="Eggplant",
        plural="Eggplants",
        icon="🍆",
        use_function=eggplant)
    PRETZEL: Item = Item(
        name="Pretzel",
        plural="Pretzels",
        icon="🥨",
        use_function=pretzel)
    ANTIDOTE: Item = Item(
        name="Antidote",
        plural="Antidotes",
        icon="💉",
        use_function=antidote,
        use_on_pickup=True)
    HOLY_SCEPTER: Item = Item(
        name="Scepter",
        plural="Scepters",
        icon="👑",
        use_function=holy_scepter,
        use_on_pickup=True)

    # Keys
    KEY_HOME: Item = Item(
        name="Key front door",
        icon="🔑",
        use_function=key_front_door)
    LOCKPICKER: Item = Item(
        name="Lockpicker",
        icon="🔒",
        use_function=lockpicker)
    KEY_MOTEL_ONE: Item = Item(
        name="Key motel ONE",
        icon="🔑",
        use_function=key_motel_one)

    # Maps
    MAP_HOME: Map = Map(
        name="home map",
        icon="🗺",
        view_function=map_home)
    MAP_STREET_BLURRED: Map = Map(
        name="damaged street map",
        icon="🗺",
        view_function=map_street_blurred)
    MAP_STREET_FULL: Map = Map(
        name="street map",
        icon="🗺",
        view_function=map_street_full)

    # Weapons
    REMOTE: WeaponMelee = WeaponMelee(
        name="Remote",
        base_damage=5,
        max_extra_damage=1)
    KNIFE: WeaponMelee = WeaponMelee(
        name="Knife",
        icon="🔪",
        base_damage=15,
        max_extra_damage=7)
    AXE: WeaponMelee = WeaponMelee(
        name="Axe",
        icon="🪓",
        base_damage=25,
        max_extra_damage=10)
    PISTOL: WeaponRanged = WeaponRanged(
        name="Pistol",
        icon="🔫",
        base_damage=12,
        max_extra_damage=15,
        ammunition=3)
    AK_47: WeaponRanged = WeaponRanged(
        name="AK-47",
        icon="",
        base_damage=22,
        max_extra_damage=8,
        ammunition=6)
    SCISSORS: WeaponMelee = WeaponMelee(
        name="Scissors",
        icon="",
        base_damage=8,
        max_extra_damage=2)

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
