import math
from typing import Dict, List, Set

from ..collision.broadphase import Broadphase
from ..collision.narrowphase import Narrowphase
from ..constraints.joint import Joint
from ..core.body import Body
from ..math.vec2 import Vec2


class World:
    """
    A class to represent the simulation world in a physics engine.
    """

    def __init__(self, gravity=Vec2(0.0, -9.81)):
        """
        Initialize the simulation world.

        Args:
            gravity (Vec2): The gravitational acceleration vector.
        """
        self.gravity = gravity
        self.bodies: List[Body] = []
        self.joints: List[Joint] = []
        self.broadphase = Broadphase()
        self.narrowphase = Narrowphase()
        self.time_step = 1.0 / 60.0
        self.velocity_iterations = 8
        self.position_iterations = 3

    def add_body(self, body: Body):
        """
        Add a body to the simulation world.

        Args:
            body (Body): The body to add.
        """
        self.bodies.append(body)
        self.broadphase.add_aabb(body.get_aabb())

    def remove_body(self, body: Body):
        """
        Remove a body from the simulation world.

        Args:
            body (Body): The body to remove.
        """
        if body in self.bodies:
            self.bodies.remove(body)
            self.broadphase.remove_aabb(body.get_aabb())

    def add_joint(self, joint: Joint):
        """
        Add a joint to the simulation world.

        Args:
            joint (Joint): The joint to add.
        """
        self.joints.append(joint)

    def remove_joint(self, joint: Joint):
        """
        Remove a joint from the simulation world.

        Args:
            joint (Joint): The joint to remove.
        """
        if joint in self.joints:
            self.joints.remove(joint)

    def step(self, time_step=None, velocity_iterations=None, position_iterations=None):
        """
        Advance the simulation by one time step.

        Args:
            time_step (float): The time step for the simulation.
            velocity_iterations (int): The number of velocity iterations.
            position_iterations (int): The number of position iterations.
        """
        if time_step is not None:
            self.time_step = time_step
        if velocity_iterations is not None:
            self.velocity_iterations = velocity_iterations
        if position_iterations is not None:
            self.position_iterations = position_iterations

        # Update the broad-phase collision detector
        self.broadphase.update()

        # Get potential colliding pairs
        potential_pairs = self.broadphase.get_potential_pairs()

        # Narrow-phase collision detection
        collision_pairs = []
        for pair in potential_pairs:
            body1_id, body2_id = pair
            body1 = next(body for body in self.bodies if id(body) == body1_id)
            body2 = next(body for body in self.bodies if id(body) == body2_id)
            if self.narrowphase.detect_collision(body1, body2):
                collision_pairs.append((body1, body2))

        # Apply forces (e.g., gravity)
        for body in self.bodies:
            if not body.is_static:
                body.apply_force(self.gravity * body.mass)

        # Integrate velocities
        for body in self.bodies:
            if not body.is_static:
                body.integrate_velocity(self.time_step)

        # Solve constraints (joints)
        for _ in range(self.velocity_iterations):
            for joint in self.joints:
                if hasattr(joint, "pre_solve"):
                    joint.pre_solve(self.time_step)
                joint.solve_velocity_constraints(self.time_step)

        # Solve collisions
        for body1, body2 in collision_pairs:
            self.narrowphase.resolve_collision(body1, body2)

        # Integrate positions
        for body in self.bodies:
            if not body.is_static:
                body.integrate_position(self.time_step)

        # Correct positions (joints)
        for _ in range(self.position_iterations):
            for joint in self.joints:
                joint.solve_position_constraints()

    def clear(self):
        """
        Clear all bodies and joints from the simulation world.
        """
        self.bodies.clear()
        self.joints.clear()
        self.broadphase.clear()

    def get_bodies(self) -> List[Body]:
        """
        Get the list of bodies in the simulation world.

        Returns:
            List[Body]: The list of bodies.
        """
        return self.bodies

    def get_joints(self) -> List[Joint]:
        """
        Get the list of joints in the simulation world.

        Returns:
            List[Joint]: The list of joints.
        """
        return self.joints

    def set_gravity(self, gravity: Vec2):
        """
        Set the gravitational acceleration vector.

        Args:
            gravity (Vec2): The gravitational acceleration vector.
        """
        self.gravity = gravity

    def get_gravity(self) -> Vec2:
        """
        Get the gravitational acceleration vector.

        Returns:
            Vec2: The gravitational acceleration vector.
        """
        return self.gravity

    def set_time_step(self, time_step: float):
        """
        Set the time step for the simulation.

        Args:
            time_step (float): The time step for the simulation.
        """
        self.time_step = time_step

    def get_time_step(self) -> float:
        """
        Get the time step for the simulation.

        Returns:
            float: The time step for the simulation.
        """
        return self.time_step

    def set_velocity_iterations(self, velocity_iterations: int):
        """
        Set the number of velocity iterations for the simulation.

        Args:
            velocity_iterations (int): The number of velocity iterations.
        """
        self.velocity_iterations = velocity_iterations

    def get_velocity_iterations(self) -> int:
        """
        Get the number of velocity iterations for the simulation.

        Returns:
            int: The number of velocity iterations.
        """
        return self.velocity_iterations

    def set_position_iterations(self, position_iterations: int):
        """
        Set the number of position iterations for the simulation.

        Args:
            position_iterations (int): The number of position iterations.
        """
        self.position_iterations = position_iterations

    def get_position_iterations(self) -> int:
        """
        Get the number of position iterations for the simulation.

        Returns:
            int: The number of position iterations.
        """
        return self.position_iterations
