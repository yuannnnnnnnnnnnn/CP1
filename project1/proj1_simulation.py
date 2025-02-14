"""CSC111 Project 1: Text Adventure Game - Simulator

Instructions (READ THIS FIRST!)
===============================

This Python module contains code for Project 1 that allows a user to simulate an entire
playthrough of the game. Please consult the project handout for instructions and details.

You can copy/paste your code from the ex1_simulation file into this one, and modify it as needed
to work with your game.

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
from proj1_event_logger import Event, EventList
from adventure import AdventureGame
from game_entities import Location


class AdventureGameSimulation:
    """A simulation of an adventure game playthrough.
    """
    # Private Instance Attributes:
    #   - _game: The AdventureGame instance that this simulation uses.
    #   - _events: A collection of the events to process during the simulation.
    _game: AdventureGame
    _events: EventList

    def __init__(self, game_data_file: str, initial_location_id: int, commands: list[str]) -> None:
        """Initialize a new game simulation based on the given game data, that runs through the given commands.

        Preconditions:
        - len(commands) > 0
        - all commands in the given list are valid commands at each associated location in the game
        """
        self._events = EventList()
        self._game = AdventureGame(game_data_file, initial_location_id)

        initial_location = self._game.get_location()
        initial_event = Event(id_num=initial_location.id_num, description=initial_location.brief_description,
                              next_command=None, next=None, prev=None)
        self._events.add_event(initial_event)
        # lines 125 - 128 were provided by ChatGPT

        self.generate_events(commands, initial_location)
        # line 132 was provided by ChatGPT

    def generate_events(self, commands: list[str], current_location: Location) -> None:
        """Generate all events in this simulation.

        Preconditions:
        - len(commands) > 0
        - all commands in the given list are valid commands at each associated location in the game
        """
        previous_event = None

        for command in commands:
            if command in current_location.available_commands:
                next_location_id = current_location.available_commands[command]
                next_location = self._game.get_location(next_location_id)

                new_event = Event(id_num=next_location.id_num, description=next_location.brief_description,
                                  next_command=command, next=None, prev=previous_event)

                if previous_event is not None:
                    previous_event.next = new_event
                    previous_event.next_command = command

                if self._events.is_empty():
                    self._events.first = new_event

                self._events.add_event(new_event)

                previous_event = new_event
                current_location = next_location

    def get_id_log(self) -> list[int]:
        """
        Get back a list of all location IDs in the order that they are visited within a game simulation
        that follows the given commands.

        >>> sim= AdventureGameSimulation('game_data.json', 50, ["go east"])
        >>> sim.get_id_log()
        [50, 60]

        >>> sim = AdventureGameSimulation('game_data.json', 50, ["go east", "go west"])
        >>> sim.get_id_log()
        [50, 60, 50]
        """
        return self._events.get_id_log()

    def run(self) -> None:
        """Run the game simulation and log location descriptions."""
        current_event = self._events.first

        while current_event:
            print(current_event.description)
            if current_event is not self._events.last:
                print("You chose:", current_event.next_command)

            current_event = current_event.next


if __name__ == "__main__":
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['R1705', 'E9998', 'E9999']
    # })

    win_walkthrough = ['go east', 'look', 'take', 'go west', 'go west', 'look', 'buy', 'go west',
                       'go north', 'look', 'pick up', 'go south', 'go south', 'look', 'check',
                       'go east', 'look', 'buy', 'go north', 'go east', 'submit assignment']
    expected_log = [50, 60, 50, 30, 20, 10, 20, 70, 40, 30, 50]
    simulation = AdventureGameSimulation('game_data.json', 50, win_walkthrough)
    assert expected_log == simulation.get_id_log()

    lose_demo = ['go west', 'go west', 'look', 'buy']
    expected_log = [50, 30, 20]
    simulation = AdventureGameSimulation('game_data.json', 50, lose_demo)
    assert expected_log == simulation.get_id_log()

    inventory_demo = ['go west', 'look', 'buy', 'inventory']
    expected_log = [50, 30]
    simulation = AdventureGameSimulation('game_data.json', 50, inventory_demo)
    assert expected_log == simulation.get_id_log()

    scores_demo = ['go east', 'look', 'take', 'score', 'go west', 'go west', 'look', 'buy', 'score']
    expected_log = [50, 60, 50, 30]
    simulation = AdventureGameSimulation('game_data.json', 50, scores_demo)
    assert expected_log == simulation.get_id_log()

    enhancement_puzzle_demo = ['go east', 'look', 'take']
    expected_log = [50, 60]
    simulation = AdventureGameSimulation('game_data.json', 50, enhancement_puzzle_demo)
    assert expected_log == simulation.get_id_log()
