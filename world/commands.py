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
        f"{'Command':20}{'Arguments':19}: {'Description':70}{'Aliases':20}", sleep_time=sleep_time)
    for command in commands:
        if not bool(CHARACTER.room.npc) or command.available_in_fight:
            print(
                f"{command.keyword:20}{' '.join(command.args):19}: {command.description:70}{', '.join(command.aliases):20}", sleep_time=sleep_time)
    print("-----", sleep_time=sleep_time)


def show_statistics(args: 'list[str]'):
    from main import CHARACTER

    print(f"----- {trailing_s(CHARACTER)} Statistics -----")
    print(f"Kills: {CHARACTER.kills}")
    print(f"Deaths: {CHARACTER.deaths}")
    print("-----")


def show_inventory(args: 'list[str]'):
    from main import CHARACTER

    print(f"----- {trailing_s(CHARACTER)} Inventory -----")
    print(f"Melee weapon: {CHARACTER.melee_weapon}")
    if CHARACTER.ranged_weapon:
        print(f"Ranged weapon: {CHARACTER.ranged_weapon}")
    for item, amount in CHARACTER.inventory.items():
        print(f"{item.__str__(amount=amount)}")
    print("-----")


def show_health(args: 'list[str]'):
    from main import CHARACTER

    print(f"----- {trailing_s(CHARACTER)} Health -----")
    print(CHARACTER.fighting_stats())
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
            if amount == 1:
                print(f"{item} has been added to your inventory.")
            else:
                print(
                    f"{amount} {item.__str__(plural=True)} have been added to your inventory.")
        else:
            print("You don't have enough coins in your inventory")
    else:
        print("This item can't be bought")


def take(args: 'list[str]'):
    from main import CHARACTER

    from world.items import Items

    item_name = " ".join(args)
    item = Items.get_item_by_name(item_name)
    if item in CHARACTER.room.loot.keys():
        amount = CHARACTER.room.loot[item]
        CHARACTER.room.loot.pop(item, None)
        CHARACTER.inventory.add_item(item, amount)
    else:
        print("This item does not exist")


def search_room(args: 'list[str]'):
    from main import CHARACTER

    loot: 'dict[Item]' = CHARACTER.room.loot
    for loot_item, amount in loot.items():
        print(loot_item.__str__(amount=amount))


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

    from world.items import Items

    map_name = " ".join(args)
    map_object = Map.get_map_by_name(map_name)
    if map_object in CHARACTER.inventory.keys():
        map_object.view()
    else:
        print("You don't have this map in your inventory")


def where_am_i(args: 'list[str]'):
    from main import CHARACTER

    print(f"You are in {CHARACTER.room}")


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
    print("You can't go in this room")


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
        print(f"Damage variation: {weapon.damage_variation}")
        if isinstance(weapon, WeaponRanged):
            print(f"Ammunition: {weapon.ammunition}")
        print("-----")
    else:
        print("You don't have this weapon equipped or in your inventory")


def attack(args: 'list[str]'):
    from main import CHARACTER

    from world.commands import create_savepoint
    from world.rooms import respawn_rooms

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
            print("You must define which weapon you want to use.")
            return
        npc_attack_damage = npc.attack()
        npc.defend(character_attack_damage)
        CHARACTER.defend(npc_attack_damage)
        if npc.health <= 0:
            print(f"You defeated {npc}")
            print(f"----- {CHARACTER} ----")
            print(CHARACTER.fighting_stats())
            print("-----")
            new_items_string = ""
            for item, amount in npc.loot.items():
                if item == list(npc.loot.keys())[0]:
                    new_items_string += item.__str__(amount=amount)
                elif item == list(npc.loot.keys())[-1]:
                    new_items_string += f" and {item.__str__(amount=amount)}"
                else:
                    new_items_string += f", {item.__str__(amount=amount)}"
                if not CHARACTER.inventory.add_item(item, amount, force=True):
                    CHARACTER.room.loot.add_item(item, amount)
            if npc.loot:
                if len(list(npc.loot.keys())) > 1 or npc.loot[list(npc.loot.keys())[0]] > 1:
                    print(f"{new_items_string} have been added your inventory")
                else:
                    print(f"{new_items_string} has been added your inventory")
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

    from world.items import Items

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
        f"Successfully importet savepoint from \"{filename}\". Welcome back, {CHARACTER.name}. You are now in {CHARACTER.room}.")
    CHARACTER.room.enter_room()


def exit_game(args: 'list[str]' = None):
    create_savepoint()
    print("Exiting game...")
    sys.exit(0)


commands: 'list[Command]' = [
    Command("help",
            description="Shows this help message",
            available_in_fight=True,
            command=help_menu),
    Command("show statistics",
            aliases=["show stats"],
            description="Shows the statistics to your character",
            available_in_fight=True,
            command=show_statistics),
    Command("show inventory",
            aliases=["show inv"],
            description="Shows the inventory of your character",
            available_in_fight=True,
            command=show_inventory),
    Command("show health",
            description="Shows the health of your character",
            available_in_fight=True,
            command=show_health),
    Command("where am i",
            description="Shows your current room",
            available_in_fight=True,
            command=where_am_i),
    Command("where can i go",
            description="Shows the rooms you can enter from your current position",
            command=where_can_i_go),
    Command("go",
            args=["room"],
            description="Move your character to another room",
            command=go),
    Command("search room",
            aliases=["search", "look"],
            description="Searches the room for loot",
            command=search_room),
    Command("buy",
            args=["item", "amount"],
            description="Buys an item",
            valid_rooms=[
                Rooms.GARAGE.value,
            ],
            command=buy),
    Command("take",
            args=["item"],
            description="Takes all items of a kind into the inventory",
            command=take),
    Command("use",
            args=["item", "amount"],
            description="Uses an item from your inventory",
            command=use),
    Command("view",
            args=["map name"],
            description="Displays the map",
            command=view),
    Command("equip",
            args=["weapon name"],
            description="Equips a weapon",
            available_in_fight=True,
            command=equip),
    Command("inspect",
            args=["weapon name"],
            description="Shows the specs of a equipped weapon or a weapon in your inventory",
            available_in_fight=True,
            command=inspect),
    Command("attack",
            args=["weapon type"],
            description="Attacks an enemy. Valid types are \"melee\" or \"ranged\"",
            available_in_fight=True,
            command=attack),
    Command("create savepoint",
            args=["filename"],
            aliases=["save"],
            description="Creates a savepoint",
            available_in_fight=True,
            command=create_savepoint),
    Command("import savepoint",
            args=["filename"],
            description="Imports a savepoint",
            available_in_fight=True,
            command=import_savepoint),
    Command("exit",
            description="Exits the game",
            available_in_fight=True,
            command=exit_game)
]
