from enum import Enum

from classes.inventory import Inventory
from classes.npc import NPC
from classes.room import Room
from utilities import print

from world.items import Items

KILLS_TO_OPEN_MOTEL_ONE = 9


def bedroom():
    if not Rooms.BEDROOM.value.visited:
        print([
            f"Let's start by finding out where you can go. \
Type \"where can i go\" and go there with e.g. \"go {Rooms.CORRIDOR.value.name}\"."
        ])


def corridor():
    from main import CHARACTER

    if CHARACTER.kills >= 1:
        Rooms.LIVING_ROOM.value.locked = False

    if not Rooms.CORRIDOR.value.visited:
        print([
            "Take the map to get an overview where you can go."
        ])
        if not CHARACTER.inventory.add_item(Items.MAP_HOME.value):
            CHARACTER.room.loot.add_item(Items.MAP_HOME.value)
            print([
                f"The item still lies in the {Rooms.CORRIDOR.value}. \
You need to drop an item before you can take the map."
            ])
        else:
            print([
                f"Type \"view {Items.MAP_HOME.value.name}\" to view the map."
            ])

    if Items.KEY_HOME.value in CHARACTER.inventory:
        if not Rooms.LIVING_ROOM.value.visited:
            print([
                f"Go to {Rooms.LIVING_ROOM.value} and look for more items."
            ])
        else:
            print([
                f"You can open the door by using the key like this: \"use {Items.KEY_HOME.value.name}\"."
            ])


def lounge():
    from main import CHARACTER

    if not Rooms.LOUNGE.value.visited and len(Rooms.LOUNGE.value.loot) > 0:
        print([
            f"Look around you! Did you notice the items lying around? \
Type \"search room\", \"search\" or \"look\" and take the item with \
e.g. \"take {list(Rooms.LOUNGE.value.loot.keys())[0].name}\".",
            "Maybe there are more items in the other rooms."
        ])
    if Items.KNIFE.value in CHARACTER.inventory:
        print([
            f"You can inspect your weapons with e.g. \"inspect {Items.REMOTE.value.name}\" \
and \"inspect {Items.KNIFE.value.name}\".",
            f"Then to equip a weapon type \"equip {Items.KNIFE.value.name}\"."
        ])


def kitchen():
    if not Rooms.KITCHEN.value.visited:
        print([
            "You just killed your own wife!",
            "You're realizing that either you're still caught in a really bad dream \
or the zombie apocalypse became real.",
            "Either way, you have to get through it and survive as long as you can."
        ])


def front_yard():
    if not Rooms.FRONT_YARD.value.visited:
        print([
            "To get an overview over the other available commands type: \"help\".",
            "You should get along with this menu by your own now."
        ])


def gravestone():
    print([
        "Why is there a gravestone in the front yard?",
        "Ledgends say that here lies the old guard, the savior from the zombie apocalypse.",
        f"According to the ledgend his hideout is {Rooms.MOTEL_ONE.value}."
    ])


def canal_street():
    if not Rooms.CANAL_STREET.value.visited:
        print([
            "You are good friends with your neighbor Joe. Maybe you should check how he's doing."
        ])


def neighbor_joes_house():
    from main import CHARACTER
    if not Rooms.NEIGHBOR_JOES_HOUSE.value.visited:
        print([
            "You enter the house of your neighbor and see him coverd in blood lying on the floor.",
            f"Neighbor: \"{CHARACTER}! Good, you're still alive. Zombies attacked me and raided my house.\"",
            "You: \"Yes my wife also turned into a Zombie. I needed to kill her to survive.\"",
            "Neighbor: \"Oh no. I'm glad you're still at good health. \
I was able to protect this map of the streets from the zombies. \
Hopefully it can help you to stay alive and stop the zombie apocalypse. My fight is over, good luck.\"",
            "There is nothing you can do to help your neighbor. His injuries are too bad.",
            "You stab a knife in his head to stop him from turning into a zombie."
        ])
        CHARACTER.kills += 1
        CHARACTER.inventory.add_item(Items.MAP_STREET_BLURRED.value)
        print([
            "Oh no, the map isn't in good condition. Some parts are not visible."
        ])


def hairy_barber():
    from main import CHARACTER

    if not Rooms.HAIRY_BARBER.value.visited:
        print([
            f"Barber: {CHARACTER}, haven't seen you in a long time. \
But your beard looks really good. Did you betray me??",
            "You: No, no. I would never betray you.",
            "Barber: If you say so.",
            "You: Did you see the zombies running around on the streets?",
            "Barber: Yes, they also tried to get into my store. Probably to get a fresh new haircut. \
*whispering* But I don't think they can pay for it. *whispering*",
            "You: Seems reasonable to me. \
Any chance you have something to reverse the process from truning into a zombie?",
            f"Barber: I'm afraid not, but take my {Items.SCISSORS.value}. It might help you in your next fight.",
        ])
        CHARACTER.inventory.add_item(Items.SCISSORS.value)
        print([
            "You: Thanks, I might just throw it into the next trash bin. ;)",
        ])


def newman_row():
    from main import CHARACTER

    if CHARACTER.kills >= KILLS_TO_OPEN_MOTEL_ONE and not Rooms.MOTEL_ONE.value.visited:
        Rooms.MOTEL_ONE.value.locked = False
        print([
            f"The door to to {Rooms.MOTEL_ONE.value} opened."
        ])
    if Rooms.MOTEL_ONE.value.visited:
        Rooms.MOTEL_ONE.value.locked = True


def motel_one():
    from main import CHARACTER

    Rooms.BOSSFIGHT_ARENA.value.locked = False
    if not Rooms.MOTEL_ONE.value.visited:
        print([
            "You found a shelter of some other humans.",
            "The other survivors tell you that they found an antidote against the zombies.",
            "It needs some time to craft the antidote. \
So every time you come back to our shelter, we can provide you with an antidote.",
            "Also take this key to our shelter. You will need it to enter again.",
            "It's a security measure to keep the zombies out."
        ])
        if len(CHARACTER.inventory) >= CHARACTER.inventory.max_items:
            print(
                f"Dropped {list(CHARACTER.inventory.keys())[0]} in {CHARACTER.room}.")
            CHARACTER.inventory.remove_item(
                list(CHARACTER.inventory.keys())[0], CHARACTER.inventory[list(CHARACTER.inventory.keys())[0]])
        CHARACTER.inventory.add_item(Items.KEY_MOTEL_ONE.value)
        Rooms.MOTEL_ONE.value.lock_message = f"Use the appropriate key to open the door to {Rooms.MOTEL_ONE.value}."
    if not Items.ANTIDOTE.value in Rooms.MOTEL_ONE.value.loot:
        Rooms.MOTEL_ONE.value.loot.add_item(Items.ANTIDOTE.value)


def bossfight_arena():
    from world.rooms import Rooms
    from main import CHARACTER

    print([
        f"You defeated {Rooms.BOSSFIGHT_ARENA.value.npc}. \
The whole world thanks you for your commitment in the fight against the zombie apocalypse.",
        "You will be a honored member of the city for life.",
        "Thanks for playing my game. © Andras Waider",
        "Here are your final stats:",
        f"{CHARACTER.stats()}"
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
                Items.LOCKPICKER.value: 1,
                Items.KNIFE.value: 1
            })),
        enter_room_function=kitchen)
    LOUNGE: Room = Room(
        name="Lounge",
        loot=Inventory({
            Items.COIN.value: 3
        }),
        enter_room_function=lounge)
    CORRIDOR: Room = Room(
        name="Corridor",
        enter_room_function=corridor)
    LIVING_ROOM: Room = Room(
        name="Living Room",
        locked=True,
        lock_message="You must make your first kill to enter this room.",
        loot=Inventory({
            Items.KEY_HOME.value: 1,
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
            Items.PISTOL.value: 1,
            Items.COIN.value: 10,
        }),
        items_to_buy=Inventory({
            Items.ARMOR.value: 1,
            Items.BULLET_CARTRIDGE.value: 2,
            Items.HEALING_POTION.value: 5,
        }),
        items_to_sell=Inventory({
            Items.MAP_HOME: 7
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
            base_damage=8,
            loot=Inventory({
                Items.COIN.value: 3
            })),
        enter_room_function=canal_street)
    NEIGHBOR_JOES_HOUSE: Room = Room(
        name="Neighbor Joe's house",
        enter_room_function=neighbor_joes_house)
    CREEPY_NEIGHBORS_HOUSE: Room = Room(
        name="Creepy neighbor's house",
        npc=NPC(
            name="Creepy zombie neighbor",
            max_health=40,
            base_damage=6,
            krit_damage=10,
            krit_chance=0.4,
            loot=Inventory({
                Items.COIN.value: 4,
                Items.ARMOR.value: 8,
            })))
    PRINCESS_MAGDALENA_GARDEN: Room = Room(
        name="Princess Magdalena garden",
        locked=True,
        lock_message="You must first find the full map.",
        npc=NPC(
            name="Armored zombie",
            max_health=100,
            armor=50,
            base_damage=25,
            krit_damage=37,
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
                Items.COIN.value: 5,
                Items.ARMOR.value: 6
            })))
    REWE_TO_GO: Room = Room(
        name="REWE to go",
        loot=Inventory({
            Items.COIN.value: 12,
            Items.ARMOR.value: 5,
        }),
        locked=True,
        lock_message="You must first find the full map.",
        items_to_buy=Inventory({
            Items.APPLE.value: 2,
            Items.BANANA.value: 4,
            Items.EGGPLANT.value: 7,
            Items.PRETZEL.value: 3
        }),
        items_to_sell=Inventory({
            Items.APPLE.value: 1,
            Items.BANANA.value: 3,
            Items.EGGPLANT.value: 4,
            Items.PRETZEL.value: 2
        }))
    CATHETRAL: Room = Room(
        name="Cathetral",
        npc=NPC(
            name="Priest",
            max_health=90,
            armor=10,
            base_damage=13,
            krit_damage=20,
            krit_chance=0.75,
            loot=Inventory({
                Items.COIN.value: 9
            })),
        loot=Inventory({
            Items.MAP_STREET_FULL.value: 1,
            Items.BULLET_CARTRIDGE.value: 2
        }))
    CATACOMB: Room = Room(
        name="Catacomb",
        locked=True,
        lock_message="You must first find the full map.",
        npc=NPC(
            name="Monk",
            max_health=60,
            base_damage=10,
            krit_damage=15,
            krit_chance=0.4,
            loot=Inventory({
                Items.ARMOR.value: 5
            })),
        loot=Inventory({
            Items.AK_47.value: 1,
        }))
    SACRISTY: Room = Room(
        name="Sacristy",
        locked=True,
        lock_message="You must first find the full map.",
        loot=Inventory({
            Items.HOLY_SCEPTER.value: 1,
            Items.COIN.value: 7
        }))
    HAIRY_BARBER: Room = Room(
        name="Hairy barber",
        locked=True,
        lock_message="The door to the Hairy barber store is still locked. But you can't find a key anywhere.",
        loot=Inventory({
            Items.COIN.value: 2
        }),
        items_to_sell=Inventory({
            Items.PISTOL.value: 15
        }),
        enter_room_function=hairy_barber)
    BATHROOM: Room = Room(
        name="Bathroom",
        loot=Inventory({
            Items.COIN.value: 3
        }),
        respawn_point=True)
    WILSON_GROVE: Room = Room(
        name="Wilson grove",
        locked=True,
        lock_message="You must first find the full map.",
        npc=NPC(
            name="Zombie",
            max_health=50,
            base_damage=13,
            krit_damage=17,
            krit_chance=0.8,
            loot=Inventory({
                Items.COIN.value: 8

            })),
        loot=Inventory({
            Items.BULLET_CARTRIDGE.value: 5
        }))
    NEWMAN_ROW: Room = Room(
        name="Newman row",
        npc=NPC(
            name="Zombie",
            base_damage=25,
            krit_damage=28,
            krit_chance=0.9,
            loot=Inventory({
                Items.ARMOR.value: 8
            })),
        enter_room_function=newman_row)
    MOTEL_ONE: Room = Room(
        name="Motel ONE",
        locked=True,
        lock_message=f"You need to kill {KILLS_TO_OPEN_MOTEL_ONE} zombies to enter motel ONE.",
        enter_room_function=motel_one)
    BOSSFIGHT_ARENA: Room = Room(
        name="Bossfight arena",
        locked=True,
        lock_message="You must first find the other survivors.",
        npc=NPC(
            name="Zombie boss",
            max_health=150,
            base_damage=50,
            krit_damage=65,
            krit_chance=0.7,
            armor=60),
        enter_room_function=bossfight_arena)

    @ staticmethod
    def to_json() -> list:
        return [room.value.to_json() for room in Rooms]

    @ staticmethod
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
    [Rooms.PRINCESS_MAGDALENA_GARDEN.value, Rooms.WILSON_GROVE.value],
    [Rooms.CANAL_STREET.value, Rooms.MONTANA_AVENUE.value],
    [Rooms.CANAL_STREET.value, Rooms.WILSON_GROVE.value],
    [Rooms.MONTANA_AVENUE.value, Rooms.REWE_TO_GO.value],
    [Rooms.MONTANA_AVENUE.value, Rooms.CATHETRAL.value],
    [Rooms.CATHETRAL.value, Rooms.CATACOMB.value],
    [Rooms.CATHETRAL.value, Rooms.SACRISTY.value],
    [Rooms.MONTANA_AVENUE.value, Rooms.HAIRY_BARBER.value],
    [Rooms.HAIRY_BARBER.value, Rooms.BATHROOM.value],
    [Rooms.HAIRY_BARBER.value, Rooms.NEWMAN_ROW.value],
    [Rooms.MONTANA_AVENUE.value, Rooms.NEWMAN_ROW.value],
    [Rooms.NEWMAN_ROW.value, Rooms.MOTEL_ONE.value],
    [Rooms.WILSON_GROVE.value, Rooms.NEWMAN_ROW.value],
    [Rooms.PRINCESS_MAGDALENA_GARDEN.value, Rooms.BOSSFIGHT_ARENA.value],
]
