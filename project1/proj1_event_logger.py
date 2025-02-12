"""CSC111 Project 1: Text Adventure Game - Event Logger

Instructions (READ THIS FIRST!)
===============================

This Python module contains the code for Project 1. Please consult
the project handout for instructions and details.

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
from dataclasses import dataclass
from typing import Optional


@dataclass
class Event:
    """
    A node representing one event in an adventure game.

    Instance Attributes:
    - id_num: Integer id of this event's location
    - description: Long description of this event's location
    - next_command: String command which leads this event to the next event, None if this is the last game event
    - next: Event object representing the next event in the game, or None if this is the last game event
    - prev: Event object representing the previous event in the game, None if this is the first game event
    """

    # NOTES:
    # This is proj1_event_logger (separate from the ex1 file). In this file, you may add new attributes/methods,
    # or modify the names or types of provided attributes/methods, as needed for your game.
    # If you want to create a special type of Event for your game that requires a different
    # set of attributes, you can create new classes using inheritance, as well.

    id_num: int
    description: str
    next_command: Optional[str] = None
    next: Optional[Event] = None
    prev: Optional[Event] = None

    # def __init__(self, id_num, command=None):
    #     """
    #     Initialize an event with a location ID and an optional command.
    #     """
    #     self.id_num = id_num  # Location ID
    #     self.next_command = command  # Command that led to this event
    #     self.next = None  # Pointer to the next event, default is None
    #     self.prev = None


class EventList:
    """
    A linked list of game events.

    Instance Attributes:
        - first: Event Object Representing the first event in EventList
        - last: Even Object Representing the last event in EventList

    Representation Invariants:
        - self.first == self.last
    """
    # idk is representation invariants are right... must change later meow
    first: Optional[Event]
    last: Optional[Event]
    current: Optional[Event]
    is_move_function: bool

    def __init__(self) -> None:
        """Initialize a new empty event list."""

        self.first = None
        self.last = None
        self.current = None
        self.is_move_function = True

    def display_events(self) -> None:
        """Display all events in chronological order.
        """
        curr = self.first
        while curr:
            print(f"Location: {curr.id_num}, Command: {curr.next_command}")
            curr = curr.next

    # TODO: Complete the methods below, based on the given descriptions.
    def is_empty(self) -> bool:
        """Return whether this event list is empty."""
        return self.first is None

    def add_event(self, event: Event, command: str = None) -> None:
        """Add the given new event to the end of this event list.
        The given command is the command which was used to reach this new event, or None if this is the first
        event in the game.
        """
        # Hint: You should update the previous node's <next_command> as needed

        if self.first is None:
            self.first = event
            event.next_command = command
        else:
            curr = self.first
            while curr.next is not None:
                curr = curr.next

            curr.next = event
            event.prev = curr
            curr.next_command = command
        self.current = event

    def remove_last_event(self) -> None:
        """Remove the last event from this event list.
        If the list is empty, do nothing."""

        # Hint: The <next_command> and <next> attributes for the new last event should be updated as needed
        curr = self.first

        if curr is None:
            return

        while curr is not None:
            curr = curr.next

        curr = curr.next

    def get_id_log(self) -> list[int]:
        """Return a list of all location IDs visited for each event in this list, in sequence."""

        items_so_far = []
        curr = self.first

        while curr is not None:
            items_so_far.append(curr.id_num)
            curr = curr.next

        return items_so_far

    def undo_event(self) -> None:
        """Undo the last move or inventory-related action."""

        if self.current is None:
            print("No events have been visited yet.")

        # Check if there's a previous event to go back to
        elif self.current.prev is not None:
            # Check if the last command was one of the move functions (go north, go south, etc.)
            if self.current.next_command in ['go north', 'go south', 'go east', 'go west']:
                self.is_move_function = True  # Mark this as a move event
                # If the last action was a move, go back to the previous event
                self.current = self.current.prev  # Move back

                #         print(f"Undo: Returned to event {self.current.id_num}: {self.current.description}"
            else:
                # add the preconditions
                # self.event_list.current = self.event_list.current.prev
                # print(f"Returned to event {self.event_list.current.id_num}: {self.event_list.current.description}")

                self.is_move_function = False  # It's not a move event
                # If it's an inventory-related action, handle it differently
                # print(f"Undoing inventory action from event {self.current.id_num}: {self.current.description}")

                # Call the game logic to handle inventory-related undo

        else:
            print("No previous events to undo.")  # fix this

    # Note: You may add other methods to this class as needed


if __name__ == "__main__":
    pass
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['R1705', 'E9998', 'E9999']
    # })
