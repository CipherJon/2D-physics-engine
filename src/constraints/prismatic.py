"""
Prismatic joint for the physics engine.

This module provides functionality for creating and managing prismatic joints,
which allow relative translation along a specified axis.
"""

from ..core.body import Body
from ..math.vec2 import Vec2
from .joint import Joint


class PrismaticJoint(Joint):
    """
    A prismatic joint to allow relative translation along a specified axis.

    Attributes:
        body_a (Body): The first body connected to the joint.
        body_b (Body): The second body connected to the joint.
        anchor_a (Vec2): The anchor point on the first body.
        anchor_b (Vec2): The anchor point on the second body.
        axis (Vec2): The axis of translation.
        lower_translation (float): The lower translation limit.
        upper_translation (float): The upper translation limit.
        enable_limit (bool): Whether to enable the translation limits.
    """

    def __init__(
        self,
        body_a,
        body_b,
        anchor_a,
        anchor_b,
        axis,
        lower_translation=-float("inf"),
        upper_translation=float("inf"),
        enable_limit=False,
    ):
        """
        Initialize a new PrismaticJoint.

        Args:
            body_a (Body): The first body connected to the joint.
            body_b (Body): The second body connected to the joint.
            anchor_a (Vec2): The anchor point on the first body.
            anchor_b (Vec2): The anchor point on the second body.
            axis (Vec2): The axis of translation.
            lower_translation (float): The lower translation limit.
            upper_translation (float): The upper translation limit.
            enable_limit (bool): Whether to enable the translation limits.
        """
        super().__init__(body_a, body_b)
        self.anchor_a = anchor_a
        self.anchor_b = anchor_b
        self.axis = axis
        self.lower_translation = lower_translation
        self.upper_translation = upper_translation
        self.enable_limit = enable_limit

    def pre_solve(self, time_step):
        """
        Prepare the joint for solving.

        Args:
            time_step (float): The time step for the simulation.
        """
        pass

    def solve_velocity_constraints(self):
        """
        Solve the velocity constraints for the prismatic joint.
        """
        pass

    def solve_position_constraints(self):
        """
        Solve the position constraints for the prismatic joint.
        """
        pass

    def get_reaction_force(self, inv_time_step):
        """
        Get the reaction force for the prismatic joint.

        Args:
            inv_time_step (float): The inverse time step.

        Returns:
            Vec2: The reaction force.
        """
        return Vec2(0.0, 0.0)

    def get_reaction_torque(self, inv_time_step):
        """
        Get the reaction torque for the prismatic joint.

        Args:
            inv_time_step (float): The inverse time step.

        Returns:
            float: The reaction torque.
        """
        return 0.0
