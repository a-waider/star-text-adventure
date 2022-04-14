from classes.person import Person
from world.commands import commands
from world.items import Items
from world.rooms import Rooms

CHARACTER = Person(
    name="",
    room=Rooms.BEDROOM.value)
CHARACTER.melee_weapon = Items.FIST.value
CHARACTER.ranged_weapon = None


CHARACTER.room = Rooms.LOUNGE.value


def main(test_mode: bool = False, user_commands: 'list[str]' = None):
    # input("Please enter your character's name: ").strip()
    from main import CHARACTER
    CHARACTER.name = "Andy"

    while True:
        if test_mode:
            if user_commands:
                user_input = user_commands.pop(0)
                print(f"executing command: {user_input}")
            else:
                break
        else:
            user_input = input("Enter your command: ").strip()
        valid_user_input = False
        for command in commands:
            if user_input.startswith(command.keyword) or [alias for alias in command.aliases if user_input.startswith(alias)]:
                valid_user_input = True
                if not bool(CHARACTER.room.npc) or command.available_in_fight:
                    args = user_input.replace(
                        command.keyword, "", 1).strip().split(" ")
                    command.run_command(current_room=CHARACTER.room, args=args)
                else:
                    print("This command is disabled during fights")
                break
        if not valid_user_input:
            print(
                "This is not a valid command. Try \"help\" for a list of valid commands.")


if __name__ == "__main__":
    main()
