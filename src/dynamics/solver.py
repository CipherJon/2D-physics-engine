"""
Solver class for the physics engine.

This module provides functionality for solving physics constraints in the physics engine.
"""

from .contact_solver import ContactSolver
from .island import Island


class Solver:
    """
    A class to solve physics constraints.

    Attributes:
        islands (list): A list of islands to solve.
        contact_solver (ContactSolver): The contact solver.
    """

    def __init__(self):
        """
        Initialize a new Solver.
        """
        self.islands = []
        self.contact_solver = ContactSolver()

    def add_island(self, island):
        """
        Add an island to the solver.

        Args:
            island (Island): The island to add.
        """
        self.islands.append(island)

    def clear_islands(self):
        """
        Clear all islands from the solver.
        """
        self.islands.clear()

    def solve(self, time_step):
        """
        Solve all islands.

        Args:
            time_step (float): The time step for the simulation.
        """
        for island in self.islands:
            island.solve(time_step)

    def solve_contacts(self):
        """
        Solve all contacts.
        """
        self.contact_solver.solve()
