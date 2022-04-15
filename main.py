import os
from classes.person import Person
from world.commands import commands, import_savepoint
from world.items import Items
from world.rooms import Rooms

DEFAULT_SAVEPOINT_FILENAME = "savepoint.json"

CHARACTER = Person(
    name="",
    room=Rooms.BEDROOM.value)
CHARACTER.melee_weapon = Items.FIST.value
CHARACTER.ranged_weapon = None


def main(test_mode: bool = False, user_commands: 'list[str]' = None):
    from main import CHARACTER

    if not test_mode:
        if os.path.isfile(DEFAULT_SAVEPOINT_FILENAME):
            import_savepoint()
        else:
            CHARACTER.name = input(
                "To beginn, please enter your character's name: ").strip()
            if CHARACTER.room == Rooms.BEDROOM.value:  # Beginning of story telling
                print("You wake up in your bed from a nightmare. Everything is still so fuzzy so you can't really see your surroundings. ")
                print("To get an overview over the available commands type: \"help\"")

    while True:
        if test_mode:
            if user_commands:
                user_input = user_commands.pop(0)
                print(f"executing command: {user_input}")
            else:
                break
        else:
            user_input = input("Enter your command: ").strip().lower()
        valid_user_input = False
        for command in commands:
            if user_input.startswith(command.keyword) or [alias for alias in command.aliases if user_input.startswith(alias)]:
                valid_user_input = True
                if not bool(CHARACTER.room.npc) or command.available_in_fight:
                    args = user_input.replace(
                        command.keyword, "", 1).strip().lower().split(" ")
                    command.run_command(current_room=CHARACTER.room, args=args)
                else:
                    print("This command is disabled during fights")
                break
        if not valid_user_input:
            print(
                "This is not a valid command. Try \"help\" for a list of valid commands.")


if __name__ == "__main__":
    main()
