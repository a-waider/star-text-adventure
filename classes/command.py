from exceptions import CommandFunctionNotDefined
from utilities import print

from classes.room import Room

ALL_ROOMS = "ANY"


class Command:
    def __init__(self,
                 keyword: str,
                 args: 'list[str]' = None,
                 aliases: 'list[str]' = None,
                 attributes: 'list[str]' = None,
                 description: str = None,
                 valid_rooms: 'list[Room]' = ALL_ROOMS,
                 available_in_fight: bool = False,
                 command=lambda: None):
        self.keyword: str = keyword
        self.args: 'list[str]' = args if args is not None else list()
        self.aliases: 'list[str]' = aliases if aliases is not None else list()
        self.attributes: 'list[str]' = attributes if attributes is not None else list(
        )
        self.description: str = description
        self.valid_rooms: 'list[Room]' = valid_rooms
        self.available_in_fight = available_in_fight
        self.command = command

    def __str__(self):
        return self.keyword

    def run_command(self, current_room: Room = None, args: 'list[str]' = None):
        if self.valid_rooms == ALL_ROOMS or current_room in self.valid_rooms:
            if self.command:
                self.command(args)
            else:
                raise CommandFunctionNotDefined
        else:
            print("You can't run this command in this room.")
