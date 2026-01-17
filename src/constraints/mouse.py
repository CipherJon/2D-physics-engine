"""
Mouse joint for the physics engine.

This module provides functionality for creating and managing mouse joints,
which are used to simulate mouse interaction with bodies in the physics engine.
"""

from ..core.body import Body
from ..math.vec2 import Vec2
from .joint import Joint


class MouseJoint(Joint):
    """
    A mouse joint to simulate mouse interaction with bodies.

    Attributes:
        body_a (Body): The body connected to the joint.
        body_b (Body): The ground body.
        target (Vec2): The target point for the mouse joint.
        max_force (float): The maximum force that can be applied.
        frequency (float): The frequency of the joint.
        damping_ratio (float): The damping ratio of the joint.
    """

    def __init__(
        self, body_a, body_b, target, max_force=1000.0, frequency=5.0, damping_ratio=0.7
    ):
        """
        Initialize a new MouseJoint.

        Args:
            body_a (Body): The body connected to the joint.
            body_b (Body): The ground body.
            target (Vec2): The target point for the mouse joint.
            max_force (float): The maximum force that can be applied.
            frequency (float): The frequency of the joint.
            damping_ratio (float): The damping ratio of the joint.
        """
        super().__init__(body_a, body_b)
        self.target = target
        self.max_force = max_force
        self.frequency = frequency
        self.damping_ratio = damping_ratio

    def set_target(self, target):
        """
        Set the target point for the mouse joint.

        Args:
            target (Vec2): The target point for the mouse joint.
        """
        self.target = target

    def pre_solve(self, time_step):
        """
        Prepare the joint for solving.

        Args:
            time_step (float): The time step for the simulation.
        """
        pass

    def solve_velocity_constraints(self):
        """
        Solve the velocity constraints for the mouse joint.
        """
        pass

    def solve_position_constraints(self):
        """
        Solve the position constraints for the mouse joint.
        """
        pass

    def get_reaction_force(self, inv_time_step):
        """
        Get the reaction force for the mouse joint.

        Args:
            inv_time_step (float): The inverse time step.

        Returns:
            Vec2: The reaction force.
        """
        return Vec2(0.0, 0.0)

    def get_reaction_torque(self, inv_time_step):
        """
        Get the reaction torque for the mouse joint.

        Args:
            inv_time_step (float): The inverse time step.

        Returns:
            float: The reaction torque.
        """
        return 0.0
