from classes.inventory import Inventory
from classes.npc import NPC
from main import CHARACTER, main
from world.items import Items
from world.rooms import Rooms


def setup_function():
    CHARACTER.inventory.clear()
    CHARACTER.inventory.max_items = 5


def execute_commands(commands: 'list[str]'):
    main(test_mode=True, user_commands=commands)


def test_unlock_front_door():
    Rooms.FRONT_YARD.value.locked = True
    CHARACTER.room = Rooms.CORRIDOR.value
    CHARACTER.inventory.add_item(Items.KEY_HOME.value)
    execute_commands(commands=[
        f"use {Items.KEY_HOME.value.name}"
    ])
    assert Rooms.FRONT_YARD.value.locked is False
    assert Items.KEY_HOME.value not in CHARACTER.inventory
    execute_commands(commands=[
        f"go {Rooms.FRONT_YARD.value.name}"
    ])
    assert CHARACTER.room == Rooms.FRONT_YARD.value
    Rooms.FRONT_YARD.value.locked = True


def test_cant_go_to_locked_room():
    CHARACTER.room = Rooms.CORRIDOR.value
    execute_commands(commands=[
        f"go {Rooms.FRONT_YARD.value.name}"
    ])
    assert CHARACTER.room == Rooms.CORRIDOR.value
    assert Rooms.FRONT_YARD.value.locked is True


def test_take_item(items_to_take: int = 3):
    Rooms.CORRIDOR.value.loot = Inventory({
        Items.COIN.value: items_to_take
    })
    CHARACTER.room = Rooms.CORRIDOR.value
    execute_commands(commands=[
        f"take {Items.COIN.value.name}"
    ])
    assert Items.COIN.value in CHARACTER.inventory
    assert CHARACTER.inventory[Items.COIN.value] == items_to_take


def test_drop_item(items_to_drop: int = 2):
    CHARACTER.inventory.add_item(Items.COIN.value, items_to_drop)
    execute_commands(commands=[
        f"drop {Items.COIN.value.name}"
    ])
    assert Items.COIN.value not in CHARACTER.inventory
    assert Items.COIN.value in CHARACTER.room.loot
    assert CHARACTER.room.loot[Items.COIN.value] == items_to_drop


def test_equip_melee_weapon():
    CHARACTER.melee_weapon = Items.REMOTE.value
    CHARACTER.inventory.add_item(Items.KNIFE.value)
    execute_commands(commands=[
        f"equip {Items.KNIFE.value.name}"
    ])
    assert CHARACTER.melee_weapon == Items.KNIFE.value
    assert Items.KNIFE.value not in CHARACTER.inventory
    assert Items.REMOTE.value in CHARACTER.inventory


def test_equip_ranged_weapon():
    CHARACTER.ranged_weapon = None
    CHARACTER.inventory.add_item(Items.GUN.value)
    execute_commands(commands=[
        f"equip {Items.GUN.value.name}"
    ])
    assert CHARACTER.ranged_weapon == Items.GUN.value
    assert len(CHARACTER.inventory) == 0


def test_max_inventory():
    CHARACTER.inventory.max_items = 2
    assert CHARACTER.inventory.add_item(Items.KNIFE.value)
    assert CHARACTER.inventory.add_item(Items.COIN.value)
    assert not CHARACTER.inventory.add_item(Items.BULLET_MAGAZINE.value)


def test_npc_loot_drops_in_room_loot_if_inventory_full():
    CHARACTER.inventory.max_items = 1
    CHARACTER.inventory.add_item(Items.COIN.value)
    CHARACTER.room = Rooms.LOUNGE.value
    Rooms.KITCHEN.value.loot = Inventory()
    Rooms.KITCHEN.value.npc = NPC(
        "dummy",
        health=1,
        base_damage=3,
        loot=Inventory({
            Items.ARMOR.value: 1
        }))
    execute_commands(commands=[
        f"go {Rooms.KITCHEN.value.name}",
        "attack melee"
    ])
    assert Items.ARMOR.value not in list(CHARACTER.inventory.keys())
    assert Items.ARMOR.value in list(Rooms.KITCHEN.value.loot.keys())


def test_update_respawn_point():
    CHARACTER.room = Rooms.CORRIDOR.value
    CHARACTER.respawn_point = Rooms.BEDROOM.value
    Rooms.FRONT_YARD.value.visited = False
    Rooms.FRONT_YARD.value.locked = False
    execute_commands(commands=[
        f"go {Rooms.FRONT_YARD.value.name}"
    ])
    assert CHARACTER.respawn_point == Rooms.FRONT_YARD.value


def test_buy_item():
    CHARACTER.room = Rooms.GARAGE.value
    CHARACTER.inventory.add_item(Items.COIN.value, 100)
    execute_commands(commands=[
        f"buy {Items.HEALING_POTION.value.name}"
    ])
    assert Items.HEALING_POTION.value in CHARACTER.inventory


def test_buy_multiple_items(items_to_buy: int = 5,):
    CHARACTER.room = Rooms.GARAGE.value
    CHARACTER.inventory.add_item(Items.COIN.value, items_to_buy*100)
    execute_commands(commands=[
        f"buy {Items.HEALING_POTION.value.name} {items_to_buy}"
    ])
    assert CHARACTER.inventory[Items.HEALING_POTION.value] == items_to_buy
    assert CHARACTER.inventory[Items.COIN.value] == items_to_buy*100 - \
        items_to_buy * \
        Rooms.GARAGE.value.items_to_buy[Items.HEALING_POTION.value]
    assert Items.HEALING_POTION.value in CHARACTER.inventory


def test_use_on_pickup():
    CHARACTER.room = Rooms.GARAGE.value
    CHARACTER.inventory.add_item(Items.COIN.value, 100)
    assert CHARACTER.armor == 0
    execute_commands(commands=[
        f"buy {Items.ARMOR.value.name}"
    ])
    assert CHARACTER.armor == 1


def test_fight():
    Rooms.KITCHEN.value.npc = NPC("dummy", health=1, base_damage=3)
    CHARACTER.room = Rooms.LOUNGE.value
    execute_commands(commands=[
        f"go {Rooms.KITCHEN.value.name}",
        "attack melee",
    ])
    assert CHARACTER.room.npc is None


def test_savepoints():
    execute_commands(commands=[
        "import savepoint",
        "create savepoint",
    ])


def test_view_map():
    CHARACTER.inventory.add_item(Items.MAP_HOME.value)
    execute_commands(commands=[
        f"view {Items.MAP_HOME.value.name}"
    ])
