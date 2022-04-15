from termcolor import colored
from utilities import text_print

from classes.item import Item
from classes.npc import NPC


class Room:
    def __init__(self,
                 name: str,
                 npc: NPC = None,
                 loot: 'dict[Item,int]' = None,
                 visited: bool = False,
                 locked: bool = False,
                 lock_message: str = None,
                 enter_room_function=lambda: None,
                 items_to_buy: 'dict[Item,int]' = None):
        self.name = name
        self.connected_rooms = list()
        self.npc: NPC = npc
        self.loot: 'dict[Item,int]' = loot if loot is not None else dict()
        self.visited: bool = visited
        self.enter_room_function = enter_room_function
        self.locked: bool = locked
        self.lock_message: str = lock_message
        self.items_to_buy: 'dict[Item,int]' = items_to_buy if items_to_buy is not None else dict(
        )

    def __str__(self) -> str:
        return colored(self.name, "blue")

    def to_json(self) -> dict:
        from world.items import Items

        # pylint: disable=duplicate-code

        return {
            "name": self.name,
            "npc": self.npc.to_json() if self.npc else None,
            "loot": Items.dict_to_json(self.loot),
            "visited": self.visited,
            "locked": self.locked,
            "lock_message": self.lock_message
        }

    def enter_room(self):
        if self.locked and self.lock_message:
            text_print(f"{self.lock_message}\n")
            return
        if self.npc:
            print(f"----- {self.npc} -----")
            print(self.npc.fighting_stats())
            print("-----")
            return
        if self.enter_room_function:
            self.enter_room_function()
        text_print(f"You are now in {self}.\n")
        if self.items_to_buy:
            print(self.buy_menu())

    def buy_menu(self) -> str:
        ret = f"""----- {self} shop -----\n{'Item':15}{'Price':10}"""
        for item, price in self.items_to_buy.items():
            ret += f"\n{str(item):15}{price:10}"
        return ret + "\n-----"

    def get_connected_rooms(self) -> 'list[Room]':
        from world.rooms import room_connections

        connected_rooms: 'set[Room]' = set()
        for room_connection in room_connections:
            if self in room_connection:
                if self == room_connection[0]:
                    connected_rooms.add(room_connection[1])
                elif self == room_connection[1]:
                    connected_rooms.add(room_connection[0])

        return connected_rooms
