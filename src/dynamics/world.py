"""
A class to represent the simulation world in a physics engine.
"""

import logging
from typing import List, Optional

from ..collision.broadphase import Broadphase
from ..collision.narrowphase import Narrowphase
from ..constraints.joint import Joint
from ..core.body import Body
from ..math.vec2 import Vec2

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class World:
    """
    A class to represent the simulation world in a physics engine.
    """

    def __init__(self, gravity: Vec2 = Vec2(0.0, -9.81)) -> None:
        """
        Initialize the simulation world.

        Args:
            gravity (Vec2): The gravitational acceleration vector. Defaults to Vec2(0.0, -9.81).
        """
        self.gravity = gravity
        self.bodies: List[Body] = []
        self.joints: List[Joint] = []
        self.broadphase = Broadphase()
        self.narrowphase = Narrowphase()
        self.time_step: float = 1.0 / 60.0
        self.velocity_iterations: int = 8
        self.position_iterations: int = 3

    def add_body(self, body: Body) -> None:
        """
        Add a body to the simulation world.

        Args:
            body (Body): The body to add.

        Raises:
            ValueError: If the body is None.
        """
        if body is None:
            logger.error("Attempted to add a None body to the world.")
            raise ValueError("Body cannot be None.")
        self.bodies.append(body)
        self.broadphase.add_aabb(body.get_aabb())
        logger.info(f"Added body to the world: {body}")

    def remove_body(self, body: Body) -> None:
        """
        Remove a body from the simulation world.

        Args:
            body (Body): The body to remove.

        Raises:
            ValueError: If the body is None or not found in the world.
        """
        if body is None:
            logger.error("Attempted to remove a None body from the world.")
            raise ValueError("Body cannot be None.")
        if body in self.bodies:
            self.bodies.remove(body)
            self.broadphase.remove_aabb(body.get_aabb())
            logger.info(f"Removed body from the world: {body}")
        else:
            logger.warning(f"Attempted to remove a body not found in the world: {body}")

    def add_joint(self, joint: Joint) -> None:
        """
        Add a joint to the simulation world.

        Args:
            joint (Joint): The joint to add.

        Raises:
            ValueError: If the joint is None.
        """
        if joint is None:
            logger.error("Attempted to add a None joint to the world.")
            raise ValueError("Joint cannot be None.")
        self.joints.append(joint)
        logger.info(f"Added joint to the world: {joint}")

    def remove_joint(self, joint: Joint) -> None:
        """
        Remove a joint from the simulation world.

        Args:
            joint (Joint): The joint to remove.

        Raises:
            ValueError: If the joint is None or not found in the world.
        """
        if joint is None:
            logger.error("Attempted to remove a None joint from the world.")
            raise ValueError("Joint cannot be None.")
        if joint in self.joints:
            self.joints.remove(joint)
            logger.info(f"Removed joint from the world: {joint}")
        else:
            logger.warning(
                f"Attempted to remove a joint not found in the world: {joint}"
            )

    def step(
        self,
        time_step: Optional[float] = None,
        velocity_iterations: Optional[int] = None,
        position_iterations: Optional[int] = None,
    ) -> None:
        """
        Advance the simulation by one time step.

        Args:
            time_step (Optional[float]): The time step for the simulation. Defaults to None.
            velocity_iterations (Optional[int]): The number of velocity iterations. Defaults to None.
            position_iterations (Optional[int]): The number of position iterations. Defaults to None.
        """
        if time_step is not None:
            self.time_step = time_step
        if velocity_iterations is not None:
            self.velocity_iterations = velocity_iterations
        if position_iterations is not None:
            self.position_iterations = position_iterations

        logger.info(f"Stepping simulation with time_step={self.time_step}")

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
                if hasattr(joint, "solve_velocity_constraints"):
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
                if hasattr(joint, "solve_position_constraints"):
                    joint.solve_position_constraints()

    def clear(self) -> None:
        """
        Clear all bodies and joints from the simulation world.
        """
        self.bodies.clear()
        self.joints.clear()
        self.broadphase.clear()
        logger.info("Cleared all bodies and joints from the world.")

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

    def set_gravity(self, gravity: Vec2) -> None:
        """
        Set the gravitational acceleration vector.

        Args:
            gravity (Vec2): The gravitational acceleration vector.
        """
        self.gravity = gravity
        logger.info(f"Set gravity to {gravity}.")

    def get_gravity(self) -> Vec2:
        """
        Get the gravitational acceleration vector.

        Returns:
            Vec2: The gravitational acceleration vector.
        """
        return self.gravity

    def set_time_step(self, time_step: float) -> None:
        """
        Set the time step for the simulation.

        Args:
            time_step (float): The time step for the simulation.

        Raises:
            ValueError: If the time step is not positive.
        """
        if time_step <= 0:
            raise ValueError("Time step must be positive.")
        self.time_step = time_step
        logger.info(f"Set time step to {time_step}.")

    def get_time_step(self) -> float:
        """
        Get the time step for the simulation.

        Returns:
            float: The time step for the simulation.
        """
        return self.time_step

    def set_velocity_iterations(self, velocity_iterations: int) -> None:
        """
        Set the number of velocity iterations for the simulation.

        Args:
            velocity_iterations (int): The number of velocity iterations.

        Raises:
            ValueError: If the number of velocity iterations is not positive.
        """
        if velocity_iterations <= 0:
            raise ValueError("Velocity iterations must be positive.")
        self.velocity_iterations = velocity_iterations
        logger.info(f"Set velocity iterations to {velocity_iterations}.")

    def get_velocity_iterations(self) -> int:
        """
        Get the number of velocity iterations for the simulation.

        Returns:
            int: The number of velocity iterations.
        """
        return self.velocity_iterations

    def set_position_iterations(self, position_iterations: int) -> None:
        """
        Set the number of position iterations for the simulation.

        Args:
            position_iterations (int): The number of position iterations.

        Raises:
            ValueError: If the number of position iterations is not positive.
        """
        if position_iterations <= 0:
            raise ValueError("Position iterations must be positive.")
        self.position_iterations = position_iterations
        logger.info(f"Set position iterations to {position_iterations}.")

    def get_position_iterations(self) -> int:
        """
        Get the number of position iterations for the simulation.

        Returns:
            int: The number of position iterations.
        """
        return self.position_iterations
