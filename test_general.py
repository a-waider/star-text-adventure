from classes.inventory import Inventory
from classes.item import Item
from classes.npc import NPC
from classes.person import MAX_LUCK
from main import CHARACTER, main
from world.items import Items, antidote
from world.rooms import Rooms


def execute_commands(commands: 'list[str]'):
    main(test_mode=True, user_commands=commands)


def test_savepoints():
    execute_commands(commands=[
        "import savepoint",
        "create savepoint",
    ])


class Test:
    def setup_method(self, _method):
        CHARACTER.inventory.clear()
        CHARACTER.inventory.max_items = 5


class TestMovement(Test):
    def test_unlock_front_door(self):
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

    def test_cant_go_to_locked_room(self):
        CHARACTER.room = Rooms.CORRIDOR.value
        execute_commands(commands=[
            f"go {Rooms.FRONT_YARD.value.name}"
        ])
        assert CHARACTER.room == Rooms.CORRIDOR.value
        assert Rooms.FRONT_YARD.value.locked is True

    def test_unlock_motel_one(self):
        from world.rooms import KILLS_TO_OPEN_MOTEL_ONE

        Rooms.MOTEL_ONE.value.locked = True
        Rooms.NEWMAN_ROW.value.npc = None
        Rooms.MONTANA_AVENUE.value.npc = None
        CHARACTER.room = Rooms.MONTANA_AVENUE.value
        CHARACTER.kills = KILLS_TO_OPEN_MOTEL_ONE
        execute_commands(commands=[
            f"go {Rooms.NEWMAN_ROW.value.name}"
        ])
        assert Rooms.MOTEL_ONE.value.locked is False
        execute_commands(commands=[
            f"go {Rooms.MOTEL_ONE.value.name}"
        ])
        assert CHARACTER.room == Rooms.MOTEL_ONE.value

    def test_update_respawn_point(self):
        CHARACTER.room = Rooms.CORRIDOR.value
        CHARACTER.respawn_point = Rooms.BEDROOM.value
        Rooms.FRONT_YARD.value.visited = False
        Rooms.FRONT_YARD.value.locked = False
        execute_commands(commands=[
            f"go {Rooms.FRONT_YARD.value.name}"
        ])
        assert CHARACTER.respawn_point == Rooms.FRONT_YARD.value


class TestInventory(Test):
    def test_max_inventory(self):
        CHARACTER.inventory.max_items = 2
        assert CHARACTER.inventory.add_item(Items.KNIFE.value)
        assert CHARACTER.inventory.add_item(Items.COIN.value)
        assert not CHARACTER.inventory.add_item(Items.BULLET_CARTRIDGE.value)

    def test_take_item(self, items_to_take: int = 3):
        Rooms.CORRIDOR.value.loot = Inventory({
            Items.COIN.value: items_to_take
        })
        CHARACTER.room = Rooms.CORRIDOR.value
        execute_commands(commands=[
            f"take {Items.COIN.value.name}"
        ])
        assert Items.COIN.value in CHARACTER.inventory
        assert CHARACTER.inventory[Items.COIN.value] == items_to_take

    def test_drop_item(self, items_to_drop: int = 2):
        CHARACTER.inventory.add_item(Items.COIN.value, items_to_drop)
        execute_commands(commands=[
            f"drop {Items.COIN.value.name}"
        ])
        assert Items.COIN.value not in CHARACTER.inventory
        assert Items.COIN.value in CHARACTER.room.loot
        assert CHARACTER.room.loot[Items.COIN.value] == items_to_drop

    def test_buy_item(self, item_to_buy: Item = Items.HEALING_POTION.value):
        CHARACTER.room = Rooms.GARAGE.value
        CHARACTER.inventory.add_item(
            Items.COIN.value, Rooms.GARAGE.value.items_to_buy[item_to_buy])
        execute_commands(commands=[
            f"buy {item_to_buy.name}"
        ])
        assert CHARACTER.inventory[item_to_buy] == 1
        assert Items.COIN.value not in CHARACTER.inventory

    def test_buy_multiple_items(self, item_to_buy: Item = Items.HEALING_POTION.value, amount: int = 5):
        CHARACTER.room = Rooms.GARAGE.value
        CHARACTER.inventory.add_item(
            Items.COIN.value, amount*Rooms.GARAGE.value.items_to_buy[item_to_buy])
        execute_commands(commands=[
            f"buy {item_to_buy.name} {amount}"
        ])
        assert item_to_buy in CHARACTER.inventory
        assert CHARACTER.inventory[item_to_buy] == amount
        assert Items.COIN.value not in CHARACTER.inventory

    def test_sell_item(self, item_to_sell: Item = Items.MAP_HOME.value):
        CHARACTER.room = Rooms.GARAGE.value
        CHARACTER.room.items_to_sell[item_to_sell] = 4
        CHARACTER.inventory.add_item(item_to_sell)
        execute_commands(commands=[
            f"sell {item_to_sell.name}"
        ])
        print(CHARACTER.room.items_to_sell[item_to_sell])
        assert item_to_sell not in CHARACTER.inventory
        assert CHARACTER.inventory[Items.COIN.value] == CHARACTER.room.items_to_sell[item_to_sell]

    def test_equip_melee_weapon(self):
        CHARACTER.melee_weapon = Items.REMOTE.value
        CHARACTER.inventory.add_item(Items.KNIFE.value)
        execute_commands(commands=[
            f"equip {Items.KNIFE.value.name}"
        ])
        assert CHARACTER.melee_weapon == Items.KNIFE.value
        assert Items.KNIFE.value not in CHARACTER.inventory
        assert Items.REMOTE.value in CHARACTER.inventory

    def test_equip_ranged_weapon(self):
        CHARACTER.ranged_weapon = None
        CHARACTER.inventory.add_item(Items.PISTOL.value)
        execute_commands(commands=[
            f"equip {Items.PISTOL.value.name}"
        ])
        assert CHARACTER.ranged_weapon == Items.PISTOL.value
        assert len(CHARACTER.inventory) == 0


class TestItems(Test):
    def test_use_on_pickup(self):
        CHARACTER.room = Rooms.GARAGE.value
        CHARACTER.inventory.add_item(Items.COIN.value, 100)
        CHARACTER.armor = 0
        execute_commands(commands=[
            f"buy {Items.ARMOR.value.name}"
        ])
        assert CHARACTER.armor == 1

    def test_holy_scepter(self):
        CHARACTER.room.loot.add_item(Items.HOLY_SCEPTER.value)
        CHARACTER.armor = 0
        execute_commands(commands=[
            f"take {Items.HOLY_SCEPTER.value.name}"
        ])
        assert CHARACTER.armor == 40

    def test_antidote(self):
        CHARACTER.room = Rooms.MONTANA_AVENUE.value
        CHARACTER.room.npc = None
        Rooms.CATHETRAL.value.npc = NPC(name="Dummy")
        CHARACTER.inventory.add_item(Items.ANTIDOTE.value)
        CHARACTER.cures = 0
        execute_commands(commands=[
            f"go {Rooms.CATHETRAL.value.name}",
            f"use {Items.ANTIDOTE.value.name}"
        ])
        assert Rooms.CATHETRAL.value.npc is None
        assert Items.ANTIDOTE.value not in CHARACTER.inventory
        assert CHARACTER.cures == 1

    def test_max_1_antidote_in_inventory(self):
        CHARACTER.room.loot = Inventory({
            Items.ANTIDOTE.value: 1
        })
        CHARACTER.inventory.add_item(Items.ANTIDOTE.value)
        execute_commands(commands=[
            f"take {Items.ANTIDOTE.value.name}"
        ])
        assert CHARACTER.inventory[Items.ANTIDOTE.value] == 1

    def test_view_map(self):
        CHARACTER.inventory.add_item(Items.MAP_STREET_FULL.value)
        execute_commands(commands=[
            f"view {Items.MAP_STREET_FULL.value.name}"
        ])


class TestFighting(Test):
    def test_fight(self):
        Rooms.KITCHEN.value.npc = NPC("dummy", health=1, base_damage=3)
        CHARACTER.room = Rooms.LOUNGE.value
        execute_commands(commands=[
            f"go {Rooms.KITCHEN.value.name}",
            "attack melee",
        ])
        assert CHARACTER.room.npc is None

    def test_npc_loot_drops_in_room_loot_if_inventory_full(self):
        CHARACTER.inventory.max_items = 1
        CHARACTER.inventory.add_item(Items.COIN.value)
        CHARACTER.melee_weapon = Items.KNIFE.value
        CHARACTER.health = CHARACTER.max_health
        CHARACTER.luck = MAX_LUCK+1
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
        assert Items.ARMOR.value not in CHARACTER.inventory
        assert Items.ARMOR.value in Rooms.KITCHEN.value.loot

    def test_ammunition_decrease_after_fight(self):
        Rooms.KITCHEN.value.npc = NPC("dummy", health=1, base_damage=1)
        CHARACTER.health = CHARACTER.max_health
        CHARACTER.luck = MAX_LUCK+1
        CHARACTER.room = Rooms.LOUNGE.value
        CHARACTER.ranged_weapon = Items.PISTOL.value
        CHARACTER.ranged_weapon.ammunition = 1
        execute_commands(commands=[
            f"go {Rooms.KITCHEN.value.name}",
            "attack ranged",
        ])
        assert CHARACTER.ranged_weapon.ammunition == 0
        assert CHARACTER.room.npc is None
