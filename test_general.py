from classes.npc import NPC
from main import CHARACTER, main
from world.items import Items
from world.rooms import Rooms


def execute_commands(commands: 'list[str]'):
    main(test_mode=True, user_commands=commands)


def test_unlock_front_door():
    Rooms.GARDEN.value.locked = True
    CHARACTER.room = Rooms.CORRIDOR.value
    CHARACTER.inventory[Items.KEY_HOME.value] = 1
    execute_commands(commands=[
        "use key front door"
    ])
    assert Rooms.GARDEN.value.locked is False
    execute_commands(commands=[
        "go garden"
    ])
    assert CHARACTER.room == Rooms.GARDEN.value


def test_cant_go_to_locked_room():
    Rooms.GARDEN.value.locked = True
    CHARACTER.room = Rooms.CORRIDOR.value
    execute_commands(commands=[
        "go garden"
    ])
    assert CHARACTER.room == Rooms.CORRIDOR.value
    assert Rooms.GARDEN.value.locked is True


def test_equip_melee_weapon():
    CHARACTER.melee_weapon = Items.FIST.value
    CHARACTER.inventory[Items.KNIFE.value] = 1
    execute_commands(commands=[
        "equip knife"
    ])
    assert CHARACTER.melee_weapon == Items.KNIFE.value
    assert Items.KNIFE.value not in CHARACTER.inventory.keys()
    assert Items.FIST.value in CHARACTER.inventory.keys()


def test_equip_ranged_weapon():
    CHARACTER.ranged_weapon = None
    CHARACTER.inventory[Items.BOW.value] = 1
    execute_commands(commands=[
        "equip bow"
    ])
    assert CHARACTER.ranged_weapon == Items.BOW.value
    assert len(CHARACTER.inventory) == 0


def test_fight():
    Rooms.KITCHEN.value.npc = NPC("dummy", health=1, base_damage=3)
    CHARACTER.room = Rooms.LOUNGE.value
    execute_commands(commands=[
        "go kitchen",
        "attack melee",
    ])
    assert CHARACTER.room.npc is None


def test_savepoints():
    execute_commands(commands=[
        "import savepoint",
        "create savepoint",
    ])
