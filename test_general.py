from classes.inventory import Inventory
from classes.npc import NPC
from classes.person import MAX_LUCK
from main import CHARACTER, main
from world.items import Items
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
    def test_cant_go_to_locked_room(self):
        CHARACTER.room = Rooms.CORRIDOR.value
        execute_commands(commands=[
            f"go {Rooms.FRONT_YARD.value.name}"
        ])
        assert CHARACTER.room == Rooms.CORRIDOR.value
        assert Rooms.FRONT_YARD.value.locked is True

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
        assert not CHARACTER.inventory.add_item(Items.BULLET_MAGAZINE.value)

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

    def test_buy_item(self):
        CHARACTER.room = Rooms.GARAGE.value
        CHARACTER.inventory.add_item(Items.COIN.value, 100)
        execute_commands(commands=[
            f"buy {Items.HEALING_POTION.value.name}"
        ])
        assert Items.HEALING_POTION.value in CHARACTER.inventory

    def test_buy_multiple_items(self, items_to_buy: int = 5):
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
        CHARACTER.inventory.add_item(Items.GUN.value)
        execute_commands(commands=[
            f"equip {Items.GUN.value.name}"
        ])
        assert CHARACTER.ranged_weapon == Items.GUN.value
        assert len(CHARACTER.inventory) == 0


class TestItems(Test):
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

    def test_use_on_pickup(self):
        CHARACTER.room = Rooms.GARAGE.value
        CHARACTER.inventory.add_item(Items.COIN.value, 100)
        assert CHARACTER.armor == 0
        execute_commands(commands=[
            f"buy {Items.ARMOR.value.name}"
        ])
        assert CHARACTER.armor == 1

    def test_view_map(self):
        CHARACTER.inventory.add_item(Items.MAP_HOME.value)
        execute_commands(commands=[
            f"view {Items.MAP_HOME.value.name}"
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
        CHARACTER.ranged_weapon = Items.GUN.value
        CHARACTER.ranged_weapon.ammunition = 1
        execute_commands(commands=[
            f"go {Rooms.KITCHEN.value.name}",
            "attack ranged",
        ])
        assert CHARACTER.ranged_weapon.ammunition == 0
        assert CHARACTER.room.npc is None
