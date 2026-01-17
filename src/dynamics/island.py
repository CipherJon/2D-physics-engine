"""
Island class for the physics engine.

This module provides functionality for managing islands of bodies in the physics engine.
"""


class Island:
    """
    A class to represent an island of bodies.

    Attributes:
        bodies (list): A list of bodies in the island.
        joints (list): A list of joints in the island.
        contacts (list): A list of contacts in the island.
    """

    def __init__(self):
        """
        Initialize a new Island.
        """
        self.bodies = []
        self.joints = []
        self.contacts = []

    def add_body(self, body):
        """
        Add a body to the island.

        Args:
            body: The body to add.
        """
        self.bodies.append(body)

    def add_joint(self, joint):
        """
        Add a joint to the island.

        Args:
            joint: The joint to add.
        """
        self.joints.append(joint)

    def add_contact(self, contact):
        """
        Add a contact to the island.

        Args:
            contact: The contact to add.
        """
        self.contacts.append(contact)

    def clear(self):
        """
        Clear all bodies, joints, and contacts from the island.
        """
        self.bodies.clear()
        self.joints.clear()
        self.contacts.clear()

    def solve(self, time_step, velocity_iterations=40, position_iterations=15):
        """
        Solve the island.

        Args:
            time_step (float): The time step for the simulation.
            velocity_iterations (int): The number of velocity iterations.
            position_iterations (int): The number of position iterations.
        """
        for joint in self.joints:
            if hasattr(joint, "pre_solve"):
                joint.pre_solve(time_step)

        for _ in range(velocity_iterations):
            for contact in self.contacts:
                contact.resolve(time_step)

            for joint in self.joints:
                if hasattr(joint, "solve_velocity_constraints"):
                    joint.solve_velocity_constraints(time_step)

            # Add damping to prevent exponential velocity growth
            for body in self.bodies:
                if not body.is_static:
                    body.velocity *= 0.99
                    body.angular_velocity *= 0.98

        for _ in range(position_iterations):
            for joint in self.joints:
                if hasattr(joint, "solve_position_constraints"):
                    joint.solve_position_constraints()

        for joint in self.joints:
            if hasattr(joint, "post_solve"):
                joint.post_solve()
