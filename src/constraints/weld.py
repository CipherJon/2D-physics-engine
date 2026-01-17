"""
Weld joint for the physics engine.

This module provides functionality for creating and managing weld joints,
which are used to simulate welded connections between bodies in the physics engine.
"""

from ..core.body import Body
from ..math.vec2 import Vec2
from .joint import Joint


class WeldJoint(Joint):
    """
    A weld joint to simulate welded connections between bodies.

    Attributes:
        body_a (Body): The first body connected to the joint.
        body_b (Body): The second body connected to the joint.
        anchor_a (Vec2): The anchor point on the first body.
        anchor_b (Vec2): The anchor point on the second body.
        reference_angle (float): The reference angle for the joint.
    """

    def __init__(self, body_a, body_b, anchor_a, anchor_b, reference_angle=0.0):
        """
        Initialize a new WeldJoint.

        Args:
            body_a (Body): The first body connected to the joint.
            body_b (Body): The second body connected to the joint.
            anchor_a (Vec2): The anchor point on the first body.
            anchor_b (Vec2): The anchor point on the second body.
            reference_angle (float): The reference angle for the joint.
        """
        super().__init__(body_a, body_b)
        self.anchor_a = anchor_a
        self.anchor_b = anchor_b
        self.reference_angle = reference_angle

    def pre_solve(self, time_step):
        """
        Prepare the joint for solving.

        Args:
            time_step (float): The time step for the simulation.
        """
        pass

    def solve_velocity_constraints(self):
        """
        Solve the velocity constraints for the weld joint.
        """
        pass

    def solve_position_constraints(self):
        """
        Solve the position constraints for the weld joint.
        """
        pass

    def get_reaction_force(self, inv_time_step):
        """
        Get the reaction force for the weld joint.

        Args:
            inv_time_step (float): The inverse time step.

        Returns:
            Vec2: The reaction force.
        """
        return Vec2(0.0, 0.0)

    def get_reaction_torque(self, inv_time_step):
        """
        Get the reaction torque for the weld joint.

        Args:
            inv_time_step (float): The inverse time step.

        Returns:
            float: The reaction torque.
        """
        return 0.0
