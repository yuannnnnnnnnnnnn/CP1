"""CSC111 Project 1: Text Adventure Game - Game Manager

Instructions (READ THIS FIRST!)
===============================

This Python module contains the code for Project 1. Please consult
the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2025 CSC111 Teaching Team
"""
from __future__ import annotations
import json
from typing import Optional

from game_entities import Location, Item
from proj1_event_logger import Event, EventList


# Note: You may add in other import statements here as needed

# Note: You may add helper functions, classes, etc. below as needed


class AdventureGame:
    """A text adventure game class storing all location, item and map data.

    Instance Attributes:
        - _locations:
        - _items:
        - current_location_id:
        - ongoing:

    Representation Invariants:
        - # TODO add any appropriate representation invariants as needed
    """

    # Private Instance Attributes (do NOT remove these two attributes):
    #   - _locations: a mapping from location id to Location object.
    #                       This represents all the locations in the game.
    #   - _items: a list of Item objects, representing all items in the game.

    _locations: dict[int, Location]
    _items: list[Item]
    current_location_id: int  # Suggested attribute, can be removed
    ongoing: bool  # Suggested attribute, can be removed
    inventory: list[Item]
    score: int

    def __init__(self, game_data_file: str, initial_location_id: int) -> None:
        """
        Initialize a new text adventure game, based on the data in the given file, setting starting location of game
        at the given initial location ID.
        (note: you are allowed to modify the format of the file as you see fit)

        Preconditions:
        - game_data_file is the filename of a valid game data JSON file
        """
        # NOTES:
        # You may add parameters/attributes/methods to this class as you see fit.

        # Requirements:
        # 1. Make sure the Location class is used to represent each location.
        # 2. Make sure the Item class is used to represent each item.

        # Suggested helper method (you can remove and load these differently if you wish to do so):
        self._locations, self._items = self._load_game_data(game_data_file)
        # self._items = []  # eh i don't know if this is right but i made the change

        # Suggested attributes (you can remove and track these differently if you wish to do so):
        self.current_location_id = initial_location_id  # game begins at this location
        self.ongoing = True  # whether the game is ongoing
        self.inventory = []
        self.score = 0

    @staticmethod
    def _load_game_data(filename: str) -> tuple[dict[int, Location], list[Item]]:
        """Load locations and items from a JSON file with the given filename and
        return a tuple consisting of (1) a dictionary of locations mapping each game location's ID to a Location object,
        and (2) a list of all Item objects."""

        with open(filename, 'r') as f:
            data = json.load(f)  # This loads all the data from the JSON file

        locations = {}
        for loc_data in data['locations']:  # Go through each element associated with the 'locations' key in the file
            location_obj = Location(loc_data['id'], loc_data['brief_description'], loc_data['long_description'],
                                    loc_data['available_commands'], loc_data['items'],
                                    available_actions=loc_data.get('available_actions', {}))
            locations[loc_data['id']] = location_obj

        items = []
        for item_data in data['items']:
            item_obj = Item(item_data['name'], item_data['description'], item_data['start_position'],
                            item_data['target_position'], item_data['target_points'])
            items.append(item_obj)
        # TODO: Add Item objects to the items list; your code should be structured similarly to the loop above
        # YOUR CODE BELOW

        return locations, items

    def get_location(self, loc_id: Optional[int] = None) -> Location:
        """Return Location object associated with the provided location ID.
        If no ID is provided, return the Location object associated with the current location.
        """

        # TODO: Complete this method as specified
        # YOUR CODE BELOW
        if loc_id is None:
            return self._locations[self.current_location_id]
        else:
            return self._locations[loc_id]

    def show_inventory(self):
        """Return a list of items you have in your inventory"""
        if not self.inventory:
            print("Your inventory is empty.")
        else:
            print("Your inventory contains:")
            for item in self.inventory:
                print(f"- {item.name}: {item.description}")

    def pick_item(self):
        """Pick up the item and add it to the inventory."""
        # Check if the 'pick up' action is available at the current location
        current_location = self.get_location(self.current_location_id)

        if "pick up" in current_location.available_actions and current_location.available_actions["pick up"]:
            if current_location.items:  # Ensure there's an item to pick up
                item = current_location.items[0]  # Assume only one item per location
                self.inventory.append(item)  # Add to inventory
                self.score += item.target_points
                print(f"You picked up {item}. It has been added to your inventory.")
            else:
                print("There is nothing to pick up here.")
        else:
            print("You chose not to pick up anything.")

    def buy_item(self):
        """Handle the purchase of an item if the 'buy' action is available."""
        # Check if the 'buy' action is available at the current location
        current_location = self.get_location(self.current_location_id)

        if "buy" in current_location.available_actions and current_location.available_actions["buy"]:
            if current_location.items:  # Ensure there's an item to buy
                item = current_location.items[0]  # Assume only one item per location
                self.inventory.append(item)  # Add to inventory
                self.score += item.target_points
                print(f"You bought {item}. It has been added to your inventory.")
            else:
                print("There is nothing to buy here.")
        else:
            print("You chose not to buy anything.")

    def show_score(self):
        """Display the current score"""
        print(f"Your current score is: {self.score}")

if __name__ == "__main__":

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['R1705', 'E9998', 'E9999']
    # })

    game_log = EventList()  # This is REQUIRED as one of the baseline requirements
    game = AdventureGame('game_data.json', 50)  # load data, setting initial location ID to 1
    menu = ["look", "inventory", "score", "undo", "log", "quit"]  # Regular menu options available at each location
    choice = None

    # Note: You may modify the code below as needed; the following starter code is just a suggestion
    while game.ongoing:
        # Note: If the loop body is getting too long, you should split the body up into helper functions
        # for better organization. Part of your marks will be based on how well-organized your code is.

        location = game.get_location()

        # TODO: Add new Event to game log to represent current game location
        if game_log.first is None:
            choice = None
        else:
            choice = game_log.last.next_command

        new_event = Event(id_num=location.id_num, description=location.brief_description, next_command=choice,
                next=None,prev=None)
            #  Note that the <choice> variable should be the command which led to this event
        # YOUR CODE HERE

        # TODO: Depending on whether or not it's been visited before,
        #  print either full description (first time visit) or brief description (every subsequent visit) of location
        # YOUR CODE HERE


        # Display possible actions at this location
        print("What to do? Choose from: look, inventory, score, undo, log, quit")
        print("At this location, you can also:")
        for action in location.available_commands:
            print("-", action)
        print("And you can also:")
        if location.available_actions:  # Ensure it isn't empty or None
            for moves, available in location.available_actions.items():
                print("-", moves)

        # Validate choice
        choice = input("\nEnter action: ").lower().strip()
        while choice not in location.available_commands and choice not in menu:
            print("That was an invalid option; try again.")
            choice = input("\nEnter action: ").lower().strip()

        print("========")
        print("You decided to:", choice)

        if choice in menu:
            # TODO: Handle each menu command as appropriate
            # Note: For the "undo" command, remember to manipulate the game_log event list to keep it up-to-date
            if choice == "log":
                game_log.display_events()
            elif choice == "look":
                current_location = game.get_location()  # Get the current location
                print(current_location.long_description)
            elif choice == "inventory":
                game.show_inventory()
            elif choice == "score":
                game.show_score()
            # elif choice == "undo":
            #     game_log.
            elif choice == "quit":
                break
            # ENTER YOUR CODE BELOW to handle other menu commands (remember to use helper functions as appropriate)
        else:
            # Handle non-menu actions
            result = location.available_commands[choice]
            game.current_location_id = result

            # TODO: Add in code to deal with actions which do not change the location (e.g. taking or using an item)

        #if
            # TODO: Add in code to deal with special locations (e.g. puzzles) as needed for your game
