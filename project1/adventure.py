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
        - _locations: a mapping from location id to Location object.
        - _items: a list of Item objects, representing all items in the game.
        - current_location_id: The ID of the player's current location.
        - ongoing: A boolean indicating whether the game is still in progress (True) or has ended (False).
        - inventory: A list of Item objects that the player has collected.
        - score: An integer representing the player's current score, which can be positive or negative.
        - move: An inter representing the number of moves executed.

    Representation Invariants:
        - all(location_id >= 0 for location_id in self._locations)
        - all(isinstance(loc, Location) for loc in self._locations.values())
        - all(isinstance(item, Item) for item in self._items)
        - self.current_location_id in self._locations
        - self.move >= 0
    """
    # Private Instance Attributes (do NOT remove these two attributes):
    #   _locations: a mapping from location id to Location object.
    #                   This represents all the locations in the game.
    #   _items: a list of Item objects, representing all items in the game.

    _locations: dict[int, Location]
    _items: list[Item]
    current_location_id: int
    ongoing: bool
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

    def show_inventory(self) -> None:
        """Lists a list of items the player has in their inventory.
        If the player has not acquired any times, a message will indicate that their inventory is empty.
        """
        if not self.inventory:
            print("Your inventory is empty.")
        else:
            print("Your inventory contains:")
            for item in self.inventory:
                print(f"- {item}")

    def pick_item(self) -> None:
        """Handles the acquirement of an item if 'pick up' action is available.
        If the item has already been retrieved, player will be unable to 'pick' for another item.
        """
        curr_location = self.get_location(self.current_location_id)
        item_dict = {thing.name: thing for thing in self._items}

        if "pick up" not in curr_location.available_actions or not curr_location.available_actions["pick up"]:
            print("There is nothing to retrieve here.")
            return

        if not curr_location.items:
            print("There is nothing to retrieve here.")
            return

        if curr_location.id_num != 10:
            print("There is nothing to retrieve here.")
            return

        item = curr_location.items[0]

        if item in self.inventory:
            print("This item has already been retrieved. Move along~")
            return

        if display_puzzle10():
            self.inventory.append(item)
            self.score += item_dict[item].target_points
            print(f"You picked up {item}. It has been added to your inventory.")
            print(item_dict[item].description)
        else:
            print("You couldn't solve the puzzle.")

    def buy_item(self) -> None:
        """Handles the purchase of an item if the 'buy' action is available.
        The items locations in the locations where the 'buy' options is available can be bought multiple times.
        """
        curr_location = self.get_location(self.current_location_id)
        item_dict = {thing.name: thing for thing in self._items}
        item_name = location.items[0]

        if "buy" in curr_location.available_actions and curr_location.available_actions["buy"]:
            if location.id_num == 20:
                if display_puzzle1():
                    item = curr_location.items[0]
                    self.inventory.append(item)
                    self.score += item_dict[item_name].target_points
                    print(f"You bought {item}. It has been added to your inventory.")
                    print(item_dict[item].description)
                else:
                    print("You couldn't solve the Ramen puzzle.")
            elif location.id_num == 30:
                if display_puzzle2():
                    item = curr_location.items[0]
                    self.inventory.append(item)
                    self.score += item_dict[item_name].target_points
                    print(f"You bought {item}. It has been added to your inventory.")
                    print(item_dict[item].description)
                else:
                    print("You couldn't solve the puzzle.")
            elif location.id_num == 40:
                if display_puzzle40():
                    item = curr_location.items[0]
                    self.inventory.append(item)
                    self.score += item_dict[item_name].target_points
                    print(f"You bought {item}. It has been added to your inventory.")
                    print(item_dict[item].description)
                else:
                    print("You couldn't solve the puzzle.")

    def take_item(self) -> None:
        """Handles the acquirement of an item if the 'take' action is available.
        If the item has already been retrieved, player will be unable to 'take' for another item.
        """
        curr_location = self.get_location(self.current_location_id)
        item_dict = {thing.name: thing for thing in self._items}

        if "take" not in curr_location.available_actions or not curr_location.available_actions["take"]:
            print("There is nothing to take here.")
            return

        if not curr_location.items:
            print("There is nothing to take here.")
            return

        item = curr_location.items[0]

        if item in self.inventory:
            print("This item has already been retrieved. Move along~")
            return

        if display_puzzle60():
            self.inventory.append(item)
            self.score += item_dict[item].target_points
            print(f"You took {item}. It has been added to your inventory.")
            print(item_dict[item].description)
        else:
            print("You couldn't solve the puzzle.")

    def check_item(self) -> None:
        """Handles the acquirement of an item if the 'check' action is available.
        If the item has already been retrieved, player will be unable to 'check' for another item.
        """
        curr_location = self.get_location(self.current_location_id)
        item_dict = {thing.name: thing for thing in self._items}

        if "check" not in curr_location.available_actions or not curr_location.available_actions["check"]:
            print("You can't check anything here.")
            return

        if not curr_location.items:
            print("There is nothing to check here.")
            return

        item = curr_location.items[0]
        if item in self.inventory:
            print("This item has already been retrieved. Move along~")
            return

        if display_puzzle70():
            self.inventory.append(item)
            self.score += item_dict[item].target_points
            print(f"You checked for {item}. It has been added to your inventory.")
            print(item_dict[item].description)
        else:
            print("You couldn't solve the puzzle.")

    def show_score(self) -> None:
        """Displays the current score of the player"""
        print(f"Your current score is: {self.score}")

    def submit_assignment(self) -> None:
        """Allows player to 'submit their project assignment' after collection the three required items.
         When the player inputs this action, if they have all three items in their inventory and have collected 250
         points, they win the game. Otherwise, if they input this action without all three required items
         and/or do not have 250 points, they lose the game.
         """
        if self.score < 250:
            print("Try again! You haven't reached 250 points!")
            self.ongoing = False
            return

        # if self.move > 25:
        #     print("OH NO! You exceeded your maximum number moves!")
        #     self.ongoing = False
        #     return

        required_items = {'Laptop Charger', 'USB Drive', 'Lucky Mug'}
        if not required_items.issubset(self.inventory):
            print("Try again! You didn't collect all three required items!")
            self.ongoing = False
            return

        print("Congratulations! You have won the game!")
        self.ongoing = False

    def undo_item_action(self) -> None:
        """Undoes the most recent item action (check, pick up, take, buy)."""
        item_dict = {thing.name: thing for thing in self._items}
        item_name = location.items[0]
        if item_name in self.inventory:
            item = self.inventory.pop()
            self.score -= item_dict[item_name].target_points
            print(f"Removed {item} from your inventory. Your score is now {self.score}.")
        else:
            print("There aren't any items to remove from inventory.")

    def undo_event(self) -> None:
        """Undoes most recent directional action (go north, go south, go east, go west)."""

        if game_log.current.prev is None:
            print("You have not visited any locations yet, start exploring!")

        if game_log.current.prev is not None:
            game_log.current = game_log.current.prev
            game_log.remove_last_event()
            print("and then this")
        else:
            print("No previous events to undo.")

    def check_action_type(self) -> Optional[bool]:
        """Checks if action is directional (go north, go south, go east, go west) or
        is for an item (check, pick up, take, buy).
        """
        if game_log.current.next_command in ['go north', 'go south', 'go east', 'go west']:
            return True
        elif game_log.current.next_command in ['check', 'pick up', 'take', 'buy']:
            return False
        else:
            return None

    def undo_together(self) -> None:
        """Checks action type (directional or for item) then undoes the action accordingly.
        If the action/command is unable to be undone (look, inventory, score, undo, log), player will be made aware.
         """
        if self.check_action_type():
            self.undo_event()
            game.current_location_id = game_log.current.id_num

        elif self.check_action_type() is None:
            print('This function cannot be undone... sorry :(')
        else:
            self.undo_item_action()


if __name__ == "__main__":
    # import python_ta
    #
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

        game_log.add_event(new_event, choice)

        print(location.brief_description)
        print("What would you like to do? Choose from: look, inventory, score, undo, log, quit")
        print("At this location, you can also:")
        for action in location.available_commands:
            print("-", action)
        if location.id_num == 50:
            if (all(item in game.inventory for item in ['Laptop Charger', 'USB Drive', 'Lucky Mug'])
                    and game.score >= 250):
                print("And you can also:")
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
            print("Eh?! That was an invalid option; try again.")
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
                game.undo_together()
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
            print("OH NO! You have exceeded your maximum move! Maybe pay better attention next time. Try again...")
            game.ongoing = False
        elif game.score < 0:
            print("OH NO! How can you continue, your score is negative... maybe don't get that ramen next time... "
                  "It could totally be a mad omen. Try again!")
            game.ongoing = False
