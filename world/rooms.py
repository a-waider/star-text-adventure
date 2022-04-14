from enum import Enum

from classes.npc import NPC
from classes.room import Room

from world.items import Items


def bedroom():
    pass


def kitchen():
    pass


class Rooms(Enum):
    # World 1: Creapy House
    BEDROOM: Room = Room(
        name="Bedroom",
        loot={
            Items.COIN.value: 5
        },
        visited=True,
        enter_room_function=bedroom)
    KITCHEN: Room = Room(
        name="Kitchen",
        npc=NPC(name="Zombie wife",
                health=12,
                base_damage=100, loot={
                    Items.KNIFE.value: 1
                }),
        enter_room_function=kitchen)
    LOUNGE: Room = Room(
        name="Lounge",
        lock_message=None,
        enter_room_function=None)
    CORRIDOR: Room = Room(
        name="Corridor",
        lock_message=None,
        enter_room_function=None)
    LIVING_ROOM: Room = Room(
        name="Living Room",
        lock_message=None,
        loot={
            Items.KEY_HOME.value: 1
        },
        enter_room_function=None)

    # World 2
    GARDEN: Room = Room(
        name="Garden",
        locked=True,
        lock_message="Because you are always afraid of thieves you lock your front door. But where is the key?",
        enter_room_function=None)

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
    [Rooms.CORRIDOR.value, Rooms.GARDEN.value],
]


# Respawn rooms
respawn_rooms: 'list[Room]' = [
    Rooms.BEDROOM.value
]
