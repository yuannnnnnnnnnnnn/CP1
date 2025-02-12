"""CSC111 Project 1:
 Text Adventure Game - Game Manager

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
from project1.Puzzle_files.MP_puzzle import display_puzzle70
from project1.Puzzle_files.apt_puzzle import display_puzzle60
from project1.Puzzle_files.new_college_puzzle import display_puzzle1
from project1.Puzzle_files.kungfutea_puzzle import display_puzzle2
from project1.Puzzle_files.robarts_puzzle import display_puzzle10
from project1.Puzzle_files.uoft_bookstore_puzzle import display_puzzle40


class AdventureGame:
    """A text adventure game class storing all location, item and map data.

    Instance Attributes:
        - current_location_id: The ID of the player's current location.
        - ongoing: A boolean indicating whether the game is still in progress (True) or has ended (False).
        - inventory: A list of Item objects that the player has collected.
        - score: An integer representing the player's current score, which can be positive or negative.

    Representation Invariants:
        - all(location_id >= 0 for location_id in self._locations)  # Location IDs must be non-negative
        - all(isinstance(loc, Location) for loc in self._locations.values())
        - all(isinstance(item, Item) for item in self._items)
        - self.current_location_id in self._locations
    """
    # lines 43 - 48 were provided by ChatGPT (DO BE EDITED)

    _locations: dict[int, Location]
    _items: list[Item]
    current_location_id: int  # Suggested attribute, can be removed
    ongoing: bool  # Suggested attribute, can be removed
    inventory: list[Item]
    score: int
    move: int

    def __init__(self, game_data_file: str, initial_location_id: int) -> None:
        """
        Initialize a new text adventure game, based on the data in the given file, setting starting location of game
        at the given initial location ID.
        (note: you are allowed to modify the format of the file as you see fit)

        Preconditions:
        - game_data_file is the filename of a valid game data JSON file
        """

        self._locations, self._items = self._load_game_data(game_data_file)

        self.current_location_id = initial_location_id
        self.ongoing = True
        self.inventory = []
        self.score = 0
        self.move = 0

    @staticmethod
    def _load_game_data(filename: str) -> tuple[dict[int, Location], list[Item]]:
        """Load locations and items from a JSON file with the given filename and
        return a tuple consisting of (1) a dictionary of locations mapping each game location's ID to a Location object,
        and (2) a list of all Item objects."""

        with open(filename, 'r') as f:
            data = json.load(f)  # This loads all the data from the JSON file

        locations = {}
        for loc_data in data.get('locations', []):
            location_obj = Location(loc_data['id'], loc_data['brief_description'], loc_data['long_description'],
                                    loc_data['available_commands'], loc_data['items'],
                                    available_actions=loc_data.get('available_actions', {}))
            locations[loc_data['id']] = location_obj

        items = []
        for item_data in data.get('items', []):
            item_obj = Item(item_data['name'], item_data['description'], item_data['start_position'],
                            item_data['target_position'], item_data['target_points'])
            items.append(item_obj)

        return locations, items

    def get_location(self, loc_id: Optional[int] = None) -> Location:
        """Return Location object associated with the provided location ID.
        If no ID is provided, return the Location object associated with the current location.
        """
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
                print(f"- {item}")

    def pick_item(self):
        """Pick up the item and add it to the inventory."""
        # Check if the 'pick up' action is available at the current location
        curr_location = self.get_location(self.current_location_id)
        self.item_dict = {item.name: item for item in self._items}  # Store items in a dictionary
        item_name = location.items[0]

        if "pick up" in curr_location.available_actions and curr_location.available_actions["pick up"]:
            if curr_location.items:  # Ensure there's an item to pick up
                if curr_location.id_num == 10:
                    item = curr_location.items[0]
                    if item not in self.inventory:
                        if display_puzzle10():

                            self.inventory.append(item)  # Add to inventory
                            self.score += self.item_dict[item_name].target_points
                            print(f"You picked up {item}. It has been added to your inventory.")
                        else:
                            print("You couldn't solve the puzzle.")
                    else:
                        print("This item has already been retrieved. Move along~")
                else:
                    print("There is nothing to retrieve here.")

    def buy_item(self):
        """Handle the purchase of an item if the 'buy' action is available."""
        curr_location = self.get_location(self.current_location_id)
        self.item_dict = {item.name: item for item in self._items}
        item_name = location.items[0]

        if "buy" in curr_location.available_actions and curr_location.available_actions["buy"]:
            if location.id_num == 20:  # Ensure there's an item to buy
                if display_puzzle1():
                    item = curr_location.items[0]  # item = Ramen
                    self.inventory.append(item)  # Add the item to inventory
                    self.score += self.item_dict[item_name].target_points
                    print(f"You bought {item}. It has been added to your inventory.")
                else:
                    print("You couldn't solve the Ramen puzzle.")
            elif location.id_num == 30:
                if display_puzzle2():
                    item = curr_location.items[0]
                    self.inventory.append(item)
                    self.score += self.item_dict[item_name].target_points
                    print(f"You bought {item}. It has been added to your inventory.")
                else:
                    print("You couldn't solve the Bubble Tea puzzle.")
            elif location.id_num == 40:
                if display_puzzle40():
                    item = curr_location.items[0]
                    self.inventory.append(item)
                    self.score += self.item_dict[item_name].target_points
                    print(f"You bought {item}. It has been added to your inventory.")
                else:
                    print("You couldn't solve the Lip Gloss puzzle.")

    def take_item(self):
        """Handle the purchase of an item if the 'buy' action is available."""
        curr_location = self.get_location(self.current_location_id)
        self.item_dict = {item.name: item for item in self._items}
        item_name = location.items[0]

        if "take" in curr_location.available_actions and curr_location.available_actions["take"]:
            item = curr_location.items[0]
            if item not in self.inventory:
                if display_puzzle60():
                    self.inventory.append(item)
                    self.score += self.item_dict[item_name].target_points
                    print(f"You took {item}. It has been added to your inventory.")
                else:
                    print("You couldn't solve the apt puzzle.")
            else:
                print("This item has already been retrieved. Move along~")
        else:
            print("There is nothing to take here.")

    def check_item(self):
        """Handle the purchase of an item if the 'buy' action is available."""
        curr_location = self.get_location(self.current_location_id)
        self.item_dict = {item.name: item for item in self._items}
        item_name = location.items[0]

        if "check" in curr_location.available_actions and curr_location.available_actions["check"]:
            if curr_location.items:
                item = curr_location.items[0]
                if item not in self.inventory:
                    if display_puzzle70():
                        self.inventory.append(item)
                        self.score += self.item_dict[item_name].target_points
                    else:
                        print("You can't solve the puzzles")
                    print(f"You checked {item}. It has been added to your inventory.")
                else:
                    print("This item has already been retrieved. Move along~")
            else:
                print("There is nothing to check here.")

    def show_score(self):
        """Display the current score"""
        print(f"Your current score is: {self.score}")

    def undo_stuff(self):
        """Undo the last command or any action related to the game"""
        self.item_dict = {item.name: item for item in self._items}
        item_name = location.items[0]
        if game_log.is_move_function == False:
            if self.inventory:
                self.item_dict = {item.name: item for item in self._items}
                item = self.inventory.pop()
                self.score += self.item_dict[item_name].target_points
                print(f"Removed {item} from your inventory. Your score is now {self.score}.")
            else:
                print("No items to remove from inventory.")

            print("Undoing a 'check' action. No item removed.")

    def submit_assignment(self):
        """Deposit """
        if self.score >= 250:
            if self.move <= 25:
                if all(item in self.inventory for item in ['Laptop Charger', 'USB Drive', 'Lucky Mug']):
                    print("Congratulations you have won the game")

                else:
                    print("Try again! You didn't collect all three required items!")
            else:
                print("Try again! You exceeded your maximum move!")
        else:
            print("Try again! You haven't reach 250 points!")
        self.ongoing = False


if __name__ == "__main__":
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['R1705', 'E9998', 'E9999']
    # })

    game_log = EventList()  # This is REQUIRED as one of the baseline requirements
    game = AdventureGame('game_data.json', 50)  # load data, setting initial location ID to 1
    menu = ["look", "inventory", "score", "undo", "log", "quit", "buy", "submit assignment", "no",
            "pick up", "check", "take"]  # Regular menu options available at each location
    choice = None

    while game.ongoing:
        location = game.get_location()

        new_event = Event(id_num=location.id_num, description=location.brief_description, next_command=choice,
                          next=None, prev=None)
        game_log.add_event(new_event)

        print(location.brief_description)
        print("What would you like to do? Choose from: look, inventory, score, undo, log, quit")
        print("At this location, you can also:")
        for action in location.available_commands:
            print("-", action)
        if location.id_num == 50:
            if (all(item in game.inventory for item in ['Laptop Charger', 'USB Drive', 'Lucky Mug'])
                    and game.score >= 250):
                print("And you can also:")
                print("what if it's this one")
                if location.available_actions:
                    for moves, available in location.available_actions.items():
                        print("-", moves)
        else:
            print("And you can also:")

            if location.available_actions:
                for moves, available in location.available_actions.items():
                    print("-", moves)

        choice = input("\nEnter action: ").lower().strip()
        while choice not in location.available_commands and choice not in menu:
            print("That was an invalid option; try again.")
            choice = input("\nEnter action: ").lower().strip()

        print("========")
        print("You decided to:", choice)

        if choice in menu:
            if choice == "log":
                game_log.display_events()
            elif choice == "look":
                current_location = game.get_location()
                print(current_location.long_description)
            elif choice == "inventory":
                game.show_inventory()
            elif choice == "score":
                game.show_score()
            elif choice == "undo":
                current_location = game.get_location()
                if game_log.is_move_function == True:
                    game_log.undo_event()
                    game.current_location_id = game_log.current.id_num
                else:
                    print('third goin in')
                    game.undo_stuff()
            elif choice == 'pick up':
                game.pick_item()
            elif choice == 'buy':
                game.buy_item()
            elif choice == 'no':
                pass
            elif choice == "quit":
                game.ongoing = False
                exit()
            elif choice == "take":
                game.take_item()
            elif choice == 'check':
                game.check_item()
            elif choice == 'submit assignment':
                game.submit_assignment()
        else:
            result = location.available_commands[choice]
            game.current_location_id = result
            game.move += 1

        if game.move >= 25:
            print("Try again! You have exceeded your maximum move!")
            game.ongoing = False
            print("update  skdfksjfdsfshmore")
        elif game.score < 0:
            print("Try again! Your score is negative.")
            game.ongoing = False
