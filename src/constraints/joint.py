"""
Joint constraint module.
"""

from src.core.body import Body
from src.math.vec2 import Vec2


class Joint:
    """
    Represents a joint constraint between two bodies.
    """

    def __init__(self, body1, body2, anchor1, anchor2):
        """
        Initialize the joint.

        Args:
            body1 (Body): The first body.
            body2 (Body): The second body.
            anchor1 (Vec2): The anchor point on the first body.
            anchor2 (Vec2): The anchor point on the second body.
        """
        self.body1 = body1
        self.body2 = body2
        self.anchor1 = anchor1
        self.anchor2 = anchor2

    def apply_impulse(self):
        """
        Apply the impulse to the bodies to satisfy the joint constraint.
        """
        pass

    def solve(self):
        """
        Solve the joint constraint.
        """
        pass

    def solve_velocity_constraints(self, time_step):
        """
        Solve the velocity constraints for the joint.

        Args:
            time_step (float): The time step for the simulation.
        """
        pass

    def solve_position_constraints(self):
        """
        Solve the position constraints for the joint.
        """
        pass

    def pre_solve(self, time_step: float):
        """
        Prepare the joint for solving.

        Args:
            time_step (float): The time step for the simulation.
        """
        pass
