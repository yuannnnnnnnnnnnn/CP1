"""CSC111 Project 1: Text Adventure Game - Game Entities

Instructions (READ THIS FIRST!)
===============================

This Python module contains the entity classes for Project 1, to be imported and used by
 the `adventure` module.
 Please consult the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2025 CSC111 Teaching Team
"""
from dataclasses import dataclass


@dataclass
class Location:
    """A location in our text adventure game world.

    Instance Attributes:
        - id: the id number of the location
        - name: the name of the location
        - brief_description: brief description of location
        - long_description: full description of the location
        - available_commands: Commands that can be executed at the location
        - available_actions: Actions that you can do when enter a location

    Representation Invariants:
        - self.id
        - self.name != []
        -
    """
    id: int
    name: str
    brief_description: str
    long_description: str
    available_commands: dict[str, int]
    available_actions: dict[str, bool]

    # The only thing you must NOT change is the name of this class: Location.
    # All locations in your game MUST be represented as an instance of this class.

    def __init__(self, location_id, brief_description, long_description, available_commands, items,
                 visited=False, available_actions=None) -> None:
        """Initialize a new location.
        """

        self.id_num = location_id
        self.brief_description = brief_description
        self.long_description = long_description
        self.available_commands = available_commands
        self.items = items
        self.visited = visited
        self.available_actions = available_actions if available_actions is not None else {}


@dataclass
class Item:
    """An item in our text adventure game world.

    Instance Attributes:
        - name: the name of item
        - description: description of action when item is aquired
        - start_position: where the item is found
        - target_position: where the item must be deposited
        - target_points: the amount of points gained when item is aquired

    Representation Invariants:
        - name != ''
        - brief_description != ''
        - long_description != ''
    """

    # NOTES:
    # This is just a suggested starter class for Item.
    # You may change these parameters and the data available for each Item object as you see fit.
    # (The current parameters correspond to the example in the handout).
    #
    # The only thing you must NOT change is the name of this class: Item.
    # All item objects in your game MUST be represented as an instance of this class.

    name: str
    description: str
    start_position: int
    target_position: int
    target_points: int


if __name__ == "__main__":
    pass
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['R1705', 'E9998', 'E9999']
    })
