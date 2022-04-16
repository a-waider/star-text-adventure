from enum import Enum

from classes.npc import NPC
from classes.room import Room
from classes.inventory import Inventory

from world.items import Items


def kitchen():
    pass


def gravestone():
    print("Why is there a gravestone in the front yard?")
    print("Ledgends say that here lies the old guard, the savior from the zombie apocalypse.")


def neighbor_joe():
    # pylint: disable=line-too-long

    from main import CHARACTER

    print("You enter the house of your neighbor and see him coverd in blood lying on the floor")
    print(
        f"Neighbor: \"{CHARACTER}! Good you're still alive. Zombies raided my house.\"")
    print("You: \"Yes my wife also turned into a Zombie. I needed to kill her to survive.\"")
    print("Neighbor: \"I was able to protect this map of the streets from the Zombies. Hopefully it can help you to stay alive and stop the zombie apocalypse. My fight is over, good luck.\"")
    print(
        f"There is nothing you can do to help your neighbor. His injuries are too bad. Type \"view {Items.MAP_STREET.value}\" to view the map")
    CHARACTER.add_to_inventory(Items.MAP_STREET.value)


class Rooms(Enum):
    # World 1: Creapy House
    BEDROOM: Room = Room(
        name="Bedroom",
        loot=Inventory({
            Items.MAP_HOME.value: 1
        }),
        visited=True,
        respawn_point=True)
    KITCHEN: Room = Room(
        name="Kitchen",
        npc=NPC(
            name="Zombie wife",
            max_health=12,
            base_damage=3,
            loot=Inventory({
                Items.KNIFE.value: 1,
                Items.COIN.value: 3
            })),
        enter_room_function=kitchen)
    LOUNGE: Room = Room(
        name="Lounge",
        loot=Inventory({
            Items.LOCKPICKER.value: 1,
            Items.COIN.value: 3
        }))
    CORRIDOR: Room = Room(
        name="Corridor",
        loot=Inventory({
            Items.COIN.value: 5
        }))
    LIVING_ROOM: Room = Room(
        name="Living Room",
        lock_message=None,
        loot=Inventory({
            Items.KEY_HOME.value: 1
        }))
    FRONT_YARD: Room = Room(
        name="Front yard",
        locked=True,
        lock_message="Because you are always afraid of thieves you lock your front door. But where is the key?",
        respawn_point=True)
    GARAGE: Room = Room(
        name="Garage",
        locked=True,
        lock_message="You couldn't find any key for the garage. It must opens differently...",
        loot=Inventory({
            Items.BOW.value: 1,
            Items.COIN.value: 10,
        }),
        items_to_buy=Inventory({
            Items.ARMOR.value: 1,
            Items.ARROW.value: 2,
            Items.HEALING_POTION.value: 5,
        }))
    GRAVESTONE: Room = Room(
        "Gravestone",
        loot=Inventory({
            Items.COIN.value: 3
        }),
        enter_room_function=gravestone)

    # World 2: Zombie City
    CANAL_STREET: Room = Room(
        name="Canal street",
        npc=NPC(
            name="Zombie",
            max_health=30,
            base_damage=5,
            loot=Inventory({
                Items.COIN.value: 3
            })))
    NEIGHBOR_JOE: Room = Room(
        name="Neighbor Joe",
        enter_room_function=neighbor_joe)
    CREAPY_NEIGHBOR: Room = Room(
        name="Creapy Neighbor",
        npc=NPC(
            name="Creapy zombie neighbor",
            max_health=40,
            base_damage=6,
            krit_damage=10,
            krit_chance=0.4,
            loot=Inventory({
                Items.COIN.value: 15,
                Items.ARMOR.value: 15,
            })))
    PRINCESS_MAGDALENA_GARDEN: Room = Room(
        name="Princess Magdalena garden",
        npc=NPC(
            name="Zombie tank",
            max_health=60,
            base_damage=10,
            krit_damage=12,
            krit_chance=0.5,
            loot=Inventory({
                Items.COIN.value: 10,
            })))
    MONTANA_AVENUE: Room = Room(
        name="Montana avenue",
        npc=NPC(
            name="Zombie",
            max_health=10,
            base_damage=5,
            loot=Inventory({
                Items.COIN.value: 2
            })))

    @staticmethod
    def to_json() -> list:
        return [room.value.to_json() for room in Rooms]

    @staticmethod
    def get_room_by_name(name: str) -> Room:
        rooms: 'list[Room]' = [
            item.value for item in Rooms]
        for room in rooms:
            if room.name.lower() == name.lower():
                return room
        return None


# Connections between rooms
room_connections: 'list[list[Room]]' = [
    # World 1
    [Rooms.CORRIDOR.value, Rooms.LOUNGE.value],
    [Rooms.LOUNGE.value, Rooms.KITCHEN.value],
    [Rooms.CORRIDOR.value, Rooms.LIVING_ROOM.value],
    [Rooms.CORRIDOR.value, Rooms.BEDROOM.value],
    [Rooms.CORRIDOR.value, Rooms.FRONT_YARD.value],
    [Rooms.FRONT_YARD.value, Rooms.GARAGE.value],
    [Rooms.FRONT_YARD.value, Rooms.GRAVESTONE.value],
    [Rooms.FRONT_YARD.value, Rooms.CANAL_STREET.value],

    # World 2
    [Rooms.CANAL_STREET.value, Rooms.NEIGHBOR_JOE.value],
    [Rooms.CANAL_STREET.value, Rooms.CREAPY_NEIGHBOR.value],
    [Rooms.CANAL_STREET.value, Rooms.PRINCESS_MAGDALENA_GARDEN.value],
    [Rooms.CANAL_STREET.value, Rooms.MONTANA_AVENUE.value]
]


# Respawn rooms
respawn_rooms: 'list[Room]' = [
    Rooms.BEDROOM.value
]
