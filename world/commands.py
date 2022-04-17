from enum import Enum
import json
import sys

from classes.command import Command
from classes.item import Item, Map, Weapon, WeaponMelee, WeaponRanged
from classes.npc import NPC
from classes.person import Person
from classes.room import Room
from utilities import print, trailing_s

from world.rooms import Rooms, room_connections

# pylint: disable=unused-argument


def help_menu(args: 'list[str]'):
    from main import CHARACTER

    sleep_time = 0.0001
    print("----- Help -----", sleep_time=sleep_time)
    print(
        f"{'Command':20}{'Arguments':19}{'Description':70}{'Aliases':20}", sleep_time=sleep_time)
    for command in Commands:
        if not bool(CHARACTER.room.npc) or command.value.available_in_fight:
            print(
                f"{command.value.keyword:20}{' '.join([f'<{arg}>' for arg in command.value.args]):19}{command.value.description:70}{', '.join(command.value.aliases):20}", sleep_time=sleep_time)
    print("-----", sleep_time=sleep_time)


def show_statistics(args: 'list[str]'):
    from main import CHARACTER

    sleep_time = 0.001
    print(f"----- {trailing_s(CHARACTER)} Statistics -----",
          sleep_time=sleep_time)
    print(CHARACTER.fighting_stats(), sleep_time=sleep_time)
    print("-----", sleep_time=sleep_time)


def show_inventory(args: 'list[str]'):
    from main import CHARACTER

    sleep_time = 0.001
    print(f"----- {trailing_s(CHARACTER)} Inventory -----",
          sleep_time=sleep_time)
    print(f"Melee weapon: {CHARACTER.melee_weapon}", sleep_time=sleep_time)
    if CHARACTER.ranged_weapon:
        print(f"Ranged weapon: {CHARACTER.ranged_weapon}",
              sleep_time=sleep_time)
    for item, amount in CHARACTER.inventory.items():
        print(f"{item.__str__(amount=amount)}", sleep_time=sleep_time)
    print("-----")


def buy(args: 'list[str]'):
    from main import CHARACTER

    from world.items import Items

    try:
        int(args[-1])
        amount = int(args.pop())
    except ValueError:
        amount = 1
    item = Items.get_item_by_name(" ".join(args))
    if item in CHARACTER.room.items_to_buy:
        cost = CHARACTER.room.items_to_buy[item]
        if Items.COIN.value in CHARACTER.inventory.keys() and CHARACTER.inventory[Items.COIN.value] >= amount*cost:
            CHARACTER.inventory.remove_item(Items.COIN.value, amount*cost)
            CHARACTER.inventory.add_item(item, amount)
        else:
            print("You don't have enough coins in your inventory.")
    else:
        print("This item can't be bought.")


def take(args: 'list[str]'):
    from main import CHARACTER

    from world.items import Items

    item_name = " ".join(args)
    item = Items.get_item_by_name(item_name)
    if item in CHARACTER.room.loot.keys():
        amount = CHARACTER.room.loot[item]
        if CHARACTER.inventory.add_item(item, amount):
            CHARACTER.room.loot.remove_item(item, amount)
        else:
            CHARACTER.room.loot.remove_item(item, amount)
    else:
        print("This item doesn't exist in this room.")


def drop(args: 'list[str]'):
    from main import CHARACTER

    from world.items import Items

    item_name = " ".join(args)
    item = Items.get_item_by_name(item_name)
    if item in CHARACTER.inventory:
        amount = CHARACTER.inventory[item]
    elif item.name in (CHARACTER.melee_weapon.name,  CHARACTER.ranged_weapon.name):
        amount = 1
    else:
        print("You can't drop an item you don't have in your inventory")
        return
    if CHARACTER.inventory.remove_item(item, amount):
        CHARACTER.room.loot.add_item(item, amount)
    print(f"Dropped {item.__str__(amount=amount)} in {CHARACTER.room}")


def search_room(args: 'list[str]'):
    from main import CHARACTER

    loot: 'dict[Item]' = CHARACTER.room.loot
    for loot_item, amount in loot.items():
        print(loot_item.__str__(amount=amount))
    if not loot:
        print("This room is empty.")


def use(args: 'list[str]'):
    from main import CHARACTER

    from world.items import Items

    try:
        int(args[-1])
        amount = int(args.pop())
    except ValueError:
        amount = 1
    item_name = " ".join(args)
    item = Items.get_item_by_name(item_name)
    if item in CHARACTER.inventory:
        item.use(amount=amount)
    else:
        print("You don't have this item in your inventory")


def view(args: 'list[str]'):
    from main import CHARACTER

    map_name = " ".join(args)
    map_object = Map.get_map_by_name(map_name)
    if map_object in CHARACTER.inventory.keys():
        map_object.view()
    else:
        print("You don't have this map in your inventory")


def where_am_i(args: 'list[str]'):
    from main import CHARACTER

    print(f"You are in {CHARACTER.room}.")


def where_can_i_go(args: 'list[str]'):
    from main import CHARACTER

    print(", ".join(str(room)
          for room in CHARACTER.room.get_connected_rooms()))


def go(args: 'list[str]'):
    # pylint: disable=invalid-name
    from main import CHARACTER

    current_room: Room = CHARACTER.room
    next_room: Room = Rooms.get_room_by_name(" ".join(args))
    for room_connection in room_connections:
        if current_room in room_connection and next_room in room_connection:
            if next_room.locked:
                print(next_room.lock_message)
            else:
                CHARACTER.room = next_room
                CHARACTER.room.enter_room()
            return
    print("You can't go in this room.")


def equip(args: 'list[str]'):
    from main import CHARACTER

    weapon = Weapon.get_weapon_by_name(" ".join(args))
    if weapon in CHARACTER.inventory.keys():
        if CHARACTER.inventory[weapon] > 1:
            raise Exception("Should never enter this branch")
        if isinstance(weapon, WeaponMelee):  # Melee Weapon
            if CHARACTER.melee_weapon:
                CHARACTER.inventory.add_item(CHARACTER.melee_weapon)
            CHARACTER.melee_weapon = weapon
        elif isinstance(weapon, WeaponRanged):  # Ranged Weapon
            if CHARACTER.ranged_weapon:
                CHARACTER.inventory.add_item(CHARACTER.ranged_weapon)
            CHARACTER.ranged_weapon = weapon
        CHARACTER.inventory.remove_item(weapon)
        print(
            f"You have now {weapon} equipped. Your previous equipped weapon is in your inventory.")
    else:
        print(f"You can't equip {' '.join(args)}")


def inspect(args: 'list[str]'):
    from main import CHARACTER

    weapon = Weapon.get_weapon_by_name(" ".join(args))
    weapons = []
    if CHARACTER.melee_weapon:
        weapons.append(CHARACTER.melee_weapon.name)
    if CHARACTER.ranged_weapon:
        weapons.append(CHARACTER.ranged_weapon.name)
    for item in CHARACTER.inventory:
        if isinstance(item, Weapon):
            weapons.append(item.name)

    if weapon and weapon.name in weapons:
        print(f"----- {weapon} -----")
        print(f"Base damage: {weapon.base_damage}")
        # TODO: Maybe rename to krit damage
        print(f"Damage variation: {weapon.damage_variation}")
        if isinstance(weapon, WeaponRanged):
            print(f"Ammunition: {CHARACTER.ranged_weapon.ammunition}")
        print("-----")
    else:
        print("You don't have this weapon equipped or in your inventory")


def attack(args: 'list[str]'):
    from main import CHARACTER

    from world.commands import create_savepoint

    npc: NPC = CHARACTER.room.npc
    if npc:
        character_attack_damage: int = 0
        if args[0] == "melee":
            if CHARACTER.melee_weapon:
                character_attack_damage = CHARACTER.attack_melee()
            else:
                print("You don't have a melee weapon")
                return
        elif args[0] == "ranged":
            if CHARACTER.ranged_weapon:
                character_attack_damage = CHARACTER.attack_ranged()
            else:
                print("You don't have a ranged weapon")
                return
        else:
            print(
                "You must define which weapon type you want to use. Valid types are \"melee\" and \"ranged\".")
            return
        npc_attack_damage = npc.attack()
        npc.defend(character_attack_damage)
        CHARACTER.defend(npc_attack_damage)
        if npc.health <= 0:
            CHARACTER.kills += 1
            print(f"----- {CHARACTER} ----")
            print(CHARACTER.fighting_stats())
            print("-----")
            print(f"You defeated {npc}.")
            new_items_string = ""
            for item, amount in npc.loot.items():
                if item == list(npc.loot.keys())[0]:
                    new_items_string += item.__str__(amount=amount)
                elif item == list(npc.loot.keys())[-1]:
                    new_items_string += f" and {item.__str__(amount=amount)}"
                else:
                    new_items_string += f", {item.__str__(amount=amount)}"
                if not CHARACTER.inventory.add_item(item, amount):
                    CHARACTER.room.loot.add_item(item, amount)
            CHARACTER.room.npc = None
            CHARACTER.room.enter_room()
        elif CHARACTER.health <= 0:
            CHARACTER.deaths += 1
            CHARACTER.health = 100
            CHARACTER.room = CHARACTER.respawn_point
            print(
                f"You have been killed by {npc} and respawn in {CHARACTER.room}")
            create_savepoint()
        else:
            print(f"----- {npc} -----")
            print(npc.fighting_stats())
            print(f"----- {CHARACTER} ----")
            print(CHARACTER.fighting_stats())
            print("-----")
    else:
        print("There are no npc's to fight.")


def create_savepoint(args: 'list[str]' = None, background: bool = False):
    from main import CHARACTER, DEFAULT_SAVEPOINT_FILENAME

    filename = " ".join(args) if args else DEFAULT_SAVEPOINT_FILENAME
    json_output = {
        "character": CHARACTER.to_json(),
        "rooms": Rooms.to_json()
    }
    with open(filename, "w") as file:
        file.write(json.dumps(json_output, indent=4, ensure_ascii=True))
    if not background:
        print(f"Successfully created savepoint at \"{filename}\"")


def import_savepoint(args: 'list[str]' = None):
    from main import CHARACTER, DEFAULT_SAVEPOINT_FILENAME

    filename = " ".join(args) if isinstance(
        args, list) else DEFAULT_SAVEPOINT_FILENAME
    try:
        with open(filename) as file:
            json_import = json.loads(file.read())

            # Character
            Person.from_json(json_import["character"])

            # Rooms
            json_rooms = json_import["rooms"]
            for json_room in json_rooms:
                Room.from_json(json_room)
    except FileNotFoundError:
        print(f"\"{filename}\" does not exist")

    print(
        f"Successfully importet savepoint from \"{filename}\". Welcome back, {CHARACTER.name}.")
    CHARACTER.room.enter_room()


def exit_game(args: 'list[str]' = None):
    create_savepoint()
    print("Exiting game...")
    sys.exit(0)


class Commands(Enum):
    HELP: Command = Command(
        "help",
        description="Shows this help message",
        available_in_fight=True,
        command=help_menu)
    SHOW_STATISTICS: Command = Command(
        "show statistics",
        aliases=["show stats"],
        description="Shows the statistics to your character",
        available_in_fight=True,
        command=show_statistics)
    SHOW_INVENTORY: Command = Command(
        "show inventory",
        aliases=["show inv"],
        description="Shows the inventory of your character",
        available_in_fight=True,
        command=show_inventory)
    WHERE_AM_I: Command = Command(
        "where am i",
        description="Shows your current room",
        available_in_fight=True,
        command=where_am_i)
    WHERE_CAN_I_GO: Command = Command(
        "where can i go",
        description="Shows the rooms you can enter from your current position",
        command=where_can_i_go)
    GO: Command = Command(
        "go",
        args=["room"],
        description="Move your character to another room",
        command=go)
    SEARCH_ROOM: Command = Command(
        "search room",
        aliases=["search", "look"],
        description="Searches the room for loot",
        command=search_room)
    BUY: Command = Command(
        "buy",
        args=["item", "amount"],
        description="Buys an item",
        valid_rooms=[
            Rooms.GARAGE.value,
        ],
        command=buy)
    TAKE: Command = Command(
        "take",
        args=["item"],
        description="Takes all items of a kind into the inventory",
        command=take)
    DROP: Command = Command(
        "drop",
        args=["item"],
        description="Drops the item in the current room",
        command=drop)
    USE: Command = Command(
        "use",
        args=["item", "amount"],
        description="Uses an item from your inventory",
        available_in_fight=True,
        command=use)
    VIEW: Command = Command(
        "view",
        args=["map name"],
        description="Displays the map",
        command=view)
    EQUIP: Command = Command(
        "equip",
        args=["weapon name"],
        description="Equips a weapon",
        available_in_fight=True,
        command=equip)
    INSPECT: Command = Command(
        "inspect",
        args=["weapon name"],
        description="Shows the specs of a equipped weapon or a weapon in your inventory",
        available_in_fight=True,
        command=inspect)
    ATTACK: Command = Command(
        "attack",
        args=["weapon type"],
        description="Attacks an enemy. Valid types are \"melee\" or \"ranged\"",
        available_in_fight=True,
        command=attack)
    CREATE_SAVEPOINT: Command = Command(
        "create savepoint",
        args=["filename"],
        aliases=["save"],
        description="Creates a savepoint",
        available_in_fight=True,
        command=create_savepoint)
    IMPORT_SAVEPOINT: Command = Command(
        "import savepoint",
        args=["filename"],
        description="Imports a savepoint",
        available_in_fight=True,
        command=import_savepoint)
    EXIT: Command = Command(
        "exit",
        description="Exits the game",
        available_in_fight=True,
        command=exit_game)
