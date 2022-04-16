from enum import Enum

from classes.inventory import Inventory
from classes.npc import NPC
from classes.room import Room
from utilities import print

from world.items import Items


def bedroom():
    if not Rooms.BEDROOM.value.visited:
        print([
            f"Let's start by finding out where you can go. Type \"where can i go\" and go there with e.g. \"go {Rooms.CORRIDOR.value.name}\""
        ])


def corridor():
    from main import CHARACTER

    if not Rooms.CORRIDOR.value.visited:
        print([
            "Take the map to get an overview where you can go. Don't expect the map to be complete though."
        ])
        if not CHARACTER.inventory.add_item(Items.MAP_HOME.value):
            CHARACTER.room.loot.add_item(Items.MAP_HOME.value)
            print([
                f"The item still lies in the {Rooms.CORRIDOR.value}. You need to drop an item before you can take the map."
            ])
        else:
            print([
                f"Type \"view {Items.MAP_HOME.value.name}\" to view the map"
            ])

    if Items.KEY_HOME.value in CHARACTER.inventory.keys():
        print([
            f"You can open the door by using the key like this: \"use {Items.KEY_HOME.value.name}\""
        ])


def lounge():
    if len(Rooms.LOUNGE.value.loot) > 0:
        print([
            f"Look around you! Did you notice the items lying around? Type \"search room\", \"search\" or \"look\" and take the item with e.g. \"take {list(Rooms.LOUNGE.value.loot.keys())[0].name}\".",
            "Maybe there are more items in the other rooms."
        ])


def kitchen():
    if not Rooms.KITCHEN.value.visited:
        print([
            "You just killed your own wife!",
            "You're realizing that either you're still caught in a really bad dream or the zombie apocalypse became real.",
            "Either way, you have to get through it and survive as long as you can."
        ])


def front_yard():
    if not Rooms.FRONT_YARD.value.visited:
        print([
            "To get an overview over the other available commands type: \"help\"",
            "You should get along with this menu by your own now."
        ])


def gravestone():
    print([
        "Why is there a gravestone in the front yard?",
        "Ledgends say that here lies the old guard, the savior from the zombie apocalypse."
    ])


def neighbor_joe():
    # pylint: disable=line-too-long

    from main import CHARACTER
    if not Rooms.NEIGHBOR_JOES_HOUSE.value.visited:
        print([
            "You enter the house of your neighbor and see him coverd in blood lying on the floor.",
            f"Neighbor: \"{CHARACTER}! Good, you're still alive. Zombies attacked me and raided my house.\"",
            "You: \"Yes my wife also turned into a Zombie. I needed to kill her to survive.\"",
            "Neighbor: \"Oh no. I'm glad you're still at good health. I was able to protect this map of the streets from the zombies. Hopefully it can help you to stay alive and stop the zombie apocalypse. My fight is over, good luck.\"",
            "There is nothing you can do to help your neighbor. His injuries are too bad.",
            "You stab a knife in his head to stop him from turning into a zombie."
        ])
        CHARACTER.kills += 1
        if not CHARACTER.inventory.add_item(Items.MAP_STREET.value):
            CHARACTER.room.loot.add_item(Items.MAP_STREET.value)
            print([
                "The item still lies in the house. You need to drop an item before you can take the map.",
                f"Then view the map by typing: \"view {Items.MAP_STREET.value.name}\""
            ])
        else:
            print([
                f"Type \"view {Items.MAP_STREET.value.name}\" to view the map"
            ])


class Rooms(Enum):
    # World 1: Creapy House
    BEDROOM: Room = Room(
        name="Bedroom",
        loot=Inventory({
            Items.COIN.value: 4
        }),
        respawn_point=True,
        enter_room_function=bedroom)
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
        }),
        enter_room_function=lounge)
    CORRIDOR: Room = Room(
        name="Corridor",
        enter_room_function=corridor)
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
        lock_message="You couldn't find any key for the garage. It has to open up differently...",
        loot=Inventory({
            Items.GUN.value: 1,
            Items.COIN.value: 10,
        }),
        items_to_buy=Inventory({
            Items.ARMOR.value: 1,
            Items.BULLET_MAGAZINE.value: 2,
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
    NEIGHBOR_JOES_HOUSE: Room = Room(
        name="Neighbor Joe's house",
        enter_room_function=neighbor_joe)
    CREEPY_NEIGHBORS_HOUSE: Room = Room(
        name="Creepy neighbor's house",
        npc=NPC(
            name="Creepy zombie neighbor",
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
    [Rooms.CANAL_STREET.value, Rooms.NEIGHBOR_JOES_HOUSE.value],
    [Rooms.CANAL_STREET.value, Rooms.CREEPY_NEIGHBORS_HOUSE.value],
    [Rooms.CANAL_STREET.value, Rooms.PRINCESS_MAGDALENA_GARDEN.value],
    [Rooms.CANAL_STREET.value, Rooms.MONTANA_AVENUE.value]
]


# Respawn rooms
respawn_rooms: 'list[Room]' = [
    Rooms.BEDROOM.value
]
