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

    id_num: int
    description: str
    next_command: Optional[str] = None
    next: Optional[Event] = None
    prev: Optional[Event] = None


class EventList:
    """
    A linked list of game events.

    Instance Attributes:
        - first: The first event in the list (or None if the list is empty).
        - last: The last event in the list (or None if the list is empty).
        - current: The current event being processed.

    Representation Invariants:
        - self.first is None == self.last is None
        - (self.last is not None) => (self.last.next is None)
        - (self.current is not None) => (self.first is not None)
    """
    first: Optional[Event]
    last: Optional[Event]
    current: Optional[Event]

    def __init__(self) -> None:
        """Initialize a new empty event list."""

        self.first = None
        self.last = None
        self.current = None

    def display_events(self) -> None:
        """Display all events in chronological order.
        """
        curr = self.first
        while curr:
            print(f"Location: {curr.id_num}, Command: {curr.next_command}")
            curr = curr.next

    def is_empty(self) -> bool:
        """Return whether this event list is empty."""
        return self.first is None

    def add_event(self, event: Event, command: str) -> None:
        """Add the given new event to the end of this event list.
        The given command is the command which was used to reach this new event, or None if this is the first
        event in the game.
        """
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
        if self.first is None:
            return

        if self.first == self.last:
            self.first = None
            self.last = None
            return

        curr = self.first
        while curr.next.next is not None:
            curr = curr.next

        curr.next = None
        curr.next_command = None
        self.last = curr

    def get_id_log(self) -> list[int]:
        """Return a list of all location IDs visited for each event in this list, in sequence."""

        items_so_far = []
        curr = self.first

        while curr is not None:
            items_so_far.append(curr.id_num)
            curr = curr.next

        return items_so_far


# def undo_event(self) -> None:
#     """Undo the last move or inventory-related action."""
#
#     if self.current.prev is None:
#         print("No events have been visited yet.")
#         # come check this again
#
#     if self.current.prev is not None:
#         self.current = self.current.prev
#         self.remove_last_event()
#     else:
#         print("No previous events to undo.")
#
#
# def thisfun(self) -> Optional[bool]:
#     """sdf"""
#     if self.current.next_command in ['go north', 'go south', 'go east', 'go west']:
#         return True
#     elif self.current.next_command in ['check', 'pick up', 'take', 'buy']:
#         return False
#     else:
#         return None


if __name__ == "__main__":
    pass
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['R1705', 'E9998', 'E9999']
    # })
