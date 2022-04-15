from enum import Enum

from classes.npc import NPC
from classes.room import Room

from world.items import Items


def kitchen():
    pass


def gravestone():
    print("Why is there a gravestone in the front yard?")
    print("Ledgends say that here lies the old guard, the savior from the zombie apocalypse.")


def neighbor():
    from main import CHARACTER

    print("You enter the house of your neighbor and see him coverd in blood lying on the floor")
    print(
        f"Neighbor: \"{CHARACTER}! Good you're still alive. Zombies raided my house.\"")
    print("You: \"Yes my wife also turned into a Zombie. I needed to kill her to survive.\"")
    print("Neighbor: \"I was able to protect this map of the streets from the Zombies. Hopefully it can help you to stay alive and stop the zombie apocalypse. My fight is over, good luck.\"")
    print(
        f"There is nothing you can do to help your neighbor. His injuries are too bad. Type \"view {Items.MAP_STREET.value} to view the map")
    CHARACTER.add_to_inventory(Items.MAP_STREET.value)


class Rooms(Enum):
    # World 1: Creapy House
    BEDROOM: Room = Room(
        name="Bedroom",
        loot={
            Items.MAP_HOME.value: 1
        },
        visited=True)
    KITCHEN: Room = Room(
        name="Kitchen",
        npc=NPC(
            name="Zombie wife",
            health=12,
            base_damage=3,
            loot={
                Items.KNIFE.value: 1,
                Items.COIN.value: 3
            }),
        enter_room_function=kitchen)
    LOUNGE: Room = Room(
        name="Lounge",
        loot={
            Items.LOCKPICKER.value: 1,
            Items.COIN.value: 3
        })
    CORRIDOR: Room = Room(
        name="Corridor",
        loot={
            Items.COIN.value: 5
        })
    LIVING_ROOM: Room = Room(
        name="Living Room",
        lock_message=None,
        loot={
            Items.KEY_HOME.value: 1
        })

    # World 2: The outside world
    FRONT_YARD: Room = Room(
        name="Front yard",
        locked=True,
        lock_message="Because you are always afraid of thieves you lock your front door. But where is the key?")
    GARAGE: Room = Room(
        name="Garage",
        locked=True,
        lock_message="You couldn't find any key for the garage. It must opens differently...",
        loot={
            Items.BOW.value: 1,
            Items.COIN.value: 10,
        })
    GRAVESTONE: Room = Room(
        "Gravestone",
        loot={
            Items.COIN.value: 3
        },
        enter_room_function=gravestone)

    # World 2: The open world
    STREET: Room = Room(
        name="Fence gate",
        npc=NPC(
            name="Zombie",
            health=30,
            base_damage=5,
            loot={
                Items.COIN.value: 3
            }))
    NEIGHBOR: Room = Room(
        name="Neighbor",
        loot={
            Items.MAP_STREET.value: 1
        },
        enter_room_function=neighbor)

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

    # World 1
    [Rooms.FRONT_YARD.value, Rooms.GARAGE.value],
    [Rooms.FRONT_YARD.value, Rooms.GRAVESTONE.value],
    [Rooms.FRONT_YARD.value, Rooms.STREET.value]
]


# Respawn rooms
respawn_rooms: 'list[Room]' = [
    Rooms.BEDROOM.value
]
