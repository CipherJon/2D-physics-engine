"""
Contact solver for the physics engine.

This module provides functionality for solving contacts between bodies in the physics engine.
"""

from src.common.constants import (
    BAUMGARTE,
    DYNAMIC_FRICTION,
    POSITION_SLOP,
    STATIC_FRICTION,
)


class ContactSolver:
    """
    A contact solver to resolve contacts between bodies.

    Attributes:
        contacts (list): A list of contacts to solve.
        velocity_iterations (int): The number of velocity iterations.
        position_iterations (int): The number of position iterations.
    """

    def __init__(self, velocity_iterations=40, position_iterations=15):
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

    def solve_velocity_constraints(self, dt):
        """
        Solve the velocity constraints for all contacts.

        Args:
            dt (float): The time step.
        """
        for _ in range(self.velocity_iterations):
            impulse_change = 0.0
            for contact in self.contacts:
                old_impulse = contact.normal_impulse
                contact.resolve(dt)
                impulse_change += abs(contact.normal_impulse - old_impulse)
            if impulse_change < 0.001:  # converged
                break

    def solve_position_constraints(self, dt):
        """
        Solve the position constraints for all contacts.

        Args:
            dt (float): The time step.
        """
        for _ in range(self.position_iterations):
            for contact in self.contacts:
                contact.apply_positional_correction(dt)

    def solve(self, dt):
        """
        Solve all contacts.

        Args:
            dt (float): The time step.

        Returns:
            list: List of impulse magnitudes applied
        """
        print(f"ContactSolver.solve called with {len(self.contacts)} contacts")
        impulse_magnitudes = []

        # Solve velocity constraints
        self.solve_velocity_constraints(dt)

        # Solve position constraints
        self.solve_position_constraints(dt)

        # Collect impulse magnitudes
        for contact in self.contacts:
            impulse_magnitudes.append(abs(contact.normal_impulse))

        return impulse_magnitudes
