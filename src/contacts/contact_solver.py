"""
Contact solver for the physics engine.

This module provides functionality for solving contacts between bodies in the physics engine.
"""


class ContactSolver:
    """
    A contact solver to resolve contacts between bodies.

    Attributes:
        contacts (list): A list of contacts to solve.
        velocity_iterations (int): The number of velocity iterations.
        position_iterations (int): The number of position iterations.
    """

    def __init__(self, velocity_iterations=8, position_iterations=3):
        """
        Initialize a new ContactSolver.

        Args:
            velocity_iterations (int): The number of velocity iterations.
            position_iterations (int): The number of position iterations.
        """
        self.contacts = []
        self.velocity_iterations = velocity_iterations
        self.position_iterations = position_iterations

    def add_contact(self, contact):
        """
        Add a contact to the solver.

        Args:
            contact (Contact): The contact to add.
        """
        self.contacts.append(contact)

    def clear_contacts(self):
        """
        Clear all contacts from the solver.
        """
        self.contacts.clear()

    def solve_velocity_constraints(self):
        """
        Solve the velocity constraints for all contacts.
        """
        for _ in range(self.velocity_iterations):
            for contact in self.contacts:
                contact.resolve()

    def solve_position_constraints(self, dt):
        """
        Solve the position constraints for all contacts.
        """
        for _ in range(self.position_iterations):
            for contact in self.contacts:
                contact.apply_positional_correction(dt)

    def solve(self, dt):
        """
        Solve all contacts.
        Returns:
            list: List of impulse magnitudes applied
        """
        print(f"ContactSolver.solve called with {len(self.contacts)} contacts")
        impulse_magnitudes = []
        for contact in self.contacts:
            impulse_magnitudes.append(contact.resolve())
        self.solve_position_constraints(dt)
        return impulse_magnitudes
