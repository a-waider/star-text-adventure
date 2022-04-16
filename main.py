import os
import signal
import sys

import readchar

from classes.person import Person
from utilities import print
from world.commands import Commands, create_savepoint, import_savepoint
from world.items import Items
from world.rooms import Rooms

DEFAULT_SAVEPOINT_FILENAME = "savepoint.json"
TEST_MODE = [False]

CHARACTER = Person(
    name="",
    room=Rooms.BEDROOM.value)
CHARACTER.melee_weapon = Items.REMOTE.value
CHARACTER.ranged_weapon = None


def handler(signum, frame):
    # pylint: disable=unused-argument

    msg = "\nCtrl-c was pressed. Do you really want to exit? (y)"
    print(msg)
    res = readchar.readchar()
    if res == "y":
        print()
        create_savepoint()
        print("Exiting...")
        sys.exit(0)
    else:
        print("\r")
        print(" " * len(msg))
        print("    \r")


signal.signal(signal.SIGINT, handler)


def main(test_mode: bool = False, user_commands: 'list[str]' = None):
    from main import CHARACTER

    TEST_MODE[0] = test_mode
    if not TEST_MODE[0]:
        if os.path.isfile(DEFAULT_SAVEPOINT_FILENAME):
            import_savepoint()
        else:
            CHARACTER.name = input(
                "To beginn, please enter your character's name: ").strip()
            if CHARACTER.room == Rooms.BEDROOM.value:  # Beginning of story telling
                print([
                    "You wake up in your bed from a nightmare.",
                    "Everything is still so fuzzy so you can't really see your surroundings."
                ])
                CHARACTER.room.enter_room_function()

    while True:
        if TEST_MODE[0]:
            if user_commands:
                user_input = user_commands.pop(0)
                print(f"executing command: {user_input}")
            else:
                break
        else:
            user_input = input("Enter your command: ").strip().lower()
        valid_user_input = False
        for command in Commands:
            try:
                if user_input != "" and (user_input.startswith(command.value.keyword) or [alias for alias in command.value.aliases if user_input.startswith(alias)]):
                    if user_input.startswith(command.value.keyword):
                        args = user_input.replace(
                            command.value.keyword, "", 1).strip().lower().split(" ")
                    else:
                        for alias in command.value.aliases:
                            if user_input.startswith(alias):
                                args = user_input.replace(
                                    alias, "", 1).strip().lower().split(" ")
                                break
                    try:
                        args.remove("")
                    except ValueError:
                        pass
                    valid_user_input = True
                    if not bool(CHARACTER.room.npc) or command.value.available_in_fight:
                        command.value.run_command(
                            current_room=CHARACTER.room, args=args)
                        create_savepoint(background=True)
                    else:
                        print("This command is disabled during fights.")
                    break
            except AttributeError:
                pass
        if not valid_user_input:
            print(
                "This is not a valid command. Try \"help\" for a list of valid commands.")


if __name__ == "__main__":
    main()
