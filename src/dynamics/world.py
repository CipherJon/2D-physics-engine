"""
A class to represent the simulation world in a physics engine.
"""

import logging
from collections import deque
from typing import List, Optional

from ..collision.broadphase import Broadphase
from ..collision.contact import Contact
from ..collision.narrowphase import Narrowphase
from ..constraints.joint import Joint
from ..contacts.contact_solver import ContactSolver
from ..core.body import Body
from ..dynamics.island import Island
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
        self.contact_solver = ContactSolver(
            velocity_iterations=40, position_iterations=15
        )
        self.time_step: float = 1.0 / 60.0
        self.velocity_iterations: int = 40
        self.position_iterations: int = 15
        self.step_count: int = 0
        self.active_contacts = {}  # Track persistent contacts across frames
        self.contact_persistence_threshold = (
            0.05  # Distance threshold for contact persistence
        )
        self.islands = []  # List of islands for island-based solving

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

        self.step_count += 1
        logger.info(
            f"\n=== Step {self.step_count} (t={self.time_step * self.step_count:.2f}s) ==="
        )
        logger.info(f"Stepping simulation with time_step={self.time_step}")

        # Diagnostic prints - initial state
        dynamic_bodies = [body for body in self.bodies if not body.is_static]
        if dynamic_bodies:
            body = dynamic_bodies[0]
            logger.info(
                f"Step start | pos.y = {body.position.y:.3f} | vel.y = {body.velocity.y:.3f}"
            )

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

        # Diagnostic: Contact detection results
        logger.info(f"Broadphase found {len(potential_pairs)} potential pairs")
        logger.info(
            f"Narrowphase confirmed {len(collision_pairs)} actual collision pairs"
        )

        # Additional contact diagnostics
        if collision_pairs:
            for i, (body1, body2) in enumerate(collision_pairs):
                logger.info(
                    f"  Collision pair {i}: Body at {body1.position} vs Body at {body2.position}"
                )
        else:
            logger.info(
                "  WARNING: No contacts detected despite potential for collisions!"
            )

        # Apply forces (e.g., gravity)
        for body in self.bodies:
            if not body.is_static and not body.is_sleeping:
                body.apply_force(self.gravity * body.mass)
                logger.debug(
                    f"Applied gravity to body at {body.position}: force={self.gravity * body.mass}"
                )

        # Integrate velocities
        for body in self.bodies:
            if not body.is_static and not body.is_sleeping:
                body.integrate_velocity(self.time_step)

        # Track total impulse for diagnostics
        total_impulse_magnitude = 0.0

        # Solve velocity constraints (contacts + joints)
        for _ in range(self.velocity_iterations):
            # Solve contacts (velocity constraints)
            contact_impulses = self._solve_contacts(collision_pairs, self.time_step)
            for impulse_magnitude in contact_impulses:
                total_impulse_magnitude += abs(impulse_magnitude)

            # Solve joint constraints
            for joint in self.joints:
                if hasattr(joint, "pre_solve"):
                    joint.pre_solve(self.time_step)
                if hasattr(joint, "solve_velocity_constraints"):
                    joint.solve_velocity_constraints(self.time_step)

        # Build islands for island-based solving
        self._build_islands(collision_pairs)

        # Solve all islands
        for island in self.islands:
            island.solve(self.time_step)

        # Integrate positions
        for body in self.bodies:
            if not body.is_static and not body.is_sleeping:
                body.integrate_position(self.time_step)

        # Diagnostic: Solver input
        logger.info(f"Contacts being processed by solver: {len(collision_pairs)}")

        # Diagnostic prints - final state
        if dynamic_bodies:
            body = dynamic_bodies[0]
            logger.info(
                f"Step end | pos.y = {body.position.y:.3f} | vel.y = {body.velocity.y:.3f}"
            )
            logger.info(
                f"Total impulse applied this step: {total_impulse_magnitude:.4f}\n"
            )

        # Correct positions (joints)
        for _ in range(self.position_iterations):
            for joint in self.joints:
                if hasattr(joint, "pre_solve"):
                    joint.pre_solve(self.time_step)
                if hasattr(joint, "solve_position_constraints"):
                    joint.solve_position_constraints()

    def _solve_contacts(self, collision_pairs, dt):
        """
        Solve contacts using the contact solver with persistence.

        Args:
            collision_pairs (list): List of colliding body pairs.
        """
        print(f"_solve_contacts called with {len(collision_pairs)} collision pairs")
        # Clear the contact solver
        self.contact_solver.clear_contacts()

        # Add contacts to the solver with persistence
        for body1, body2 in collision_pairs:
            manifold = self.narrowphase.get_collision_manifold(body1, body2)
            print(f"Manifold for {body1.position} vs {body2.position}: {manifold}")

            if manifold is not None:
                # Check for persistent contacts using order-independent key
                contact_key = frozenset({id(body1), id(body2)})
                if contact_key in self.active_contacts:
                    # Reuse existing contact with accumulated impulses
                    contact = self.active_contacts[contact_key]
                    contact.normal = manifold.normal
                    contact.penetration = manifold.depth
                    contact.contact_point = (
                        manifold.points[0] if manifold.points else body1.position
                    )
                    print(f"REUSING persistent contact: {contact}")
                else:
                    # Create new contact
                    contact = Contact(
                        body_a=body1,
                        body_b=body2,
                        normal=manifold.normal,
                        penetration=manifold.depth,
                        contact_point=manifold.points[0]
                        if manifold.points
                        else body1.position,
                    )
                    print(f"NEW contact: {contact}")
                    # Store the new contact for persistence
                    self.active_contacts[contact_key] = contact

                self.contact_solver.add_contact(contact)
            else:
                print(f"No manifold for {body1.position} vs {body2.position}")
                # Remove from active contacts if no longer colliding
                contact_key = frozenset({id(body1), id(body2)})
                if contact_key in self.active_contacts:
                    del self.active_contacts[contact_key]

        # Clean up old contacts that are no longer colliding
        current_contact_keys = [
            frozenset({id(body1), id(body2)}) for body1, body2 in collision_pairs
        ]
        keys_to_remove = []
        for key in self.active_contacts:
            if key not in current_contact_keys:
                keys_to_remove.append(key)
        for key in keys_to_remove:
            del self.active_contacts[key]

        # Solve the contacts and return impulse magnitudes
        impulse_magnitudes = self.contact_solver.solve(dt)
        return impulse_magnitudes

    def _get_or_create_contact(self, body1, body2, manifold):
        """
        Get or create a contact for the given body pair and manifold.

        Args:
            body1: The first body.
            body2: The second body.
            manifold: The collision manifold.

        Returns:
            Contact: The contact.
        """
        contact_key = frozenset({id(body1), id(body2)})
        if contact_key in self.active_contacts:
            contact = self.active_contacts[contact_key]
            contact.normal = manifold.normal
            contact.penetration = manifold.depth
            contact.contact_point = (
                manifold.points[0] if manifold.points else body1.position
            )
        else:
            contact = Contact(
                body_a=body1,
                body_b=body2,
                normal=manifold.normal,
                penetration=manifold.depth,
                contact_point=manifold.points[0] if manifold.points else body1.position,
            )
            self.active_contacts[contact_key] = contact
        return contact

    def _build_islands(self, collision_pairs):
        """
        Build islands of connected bodies, joints, and contacts.

        Args:
            collision_pairs (list): List of colliding body pairs.
        """
        self.islands = []
        visited = set()

        for body in self.bodies:
            if id(body) in visited:
                continue
            island = Island()
            self._build_island(body, island, visited, collision_pairs)
            self.islands.append(island)

    def _build_island(self, start_body, island, visited, collision_pairs):
        """
        Build an island of connected bodies, joints, and contacts.

        Args:
            start_body: The starting body for the island.
            island: The island to build.
            visited: Set of visited body IDs.
            collision_pairs: List of colliding body pairs.
        """
        queue = deque([start_body])
        visited.add(id(start_body))

        while queue:
            body = queue.popleft()
            island.add_body(body)

            # Add connected joints
            for joint in self.joints:
                if joint.body1 == body or joint.body2 == body:
                    other = joint.body1 if joint.body1 != body else joint.body2
                    island.add_joint(joint)
                    if id(other) not in visited:
                        visited.add(id(other))
                        queue.append(other)

            # Add connected contacts
            for pair in collision_pairs:
                if pair[0] == body or pair[1] == body:
                    manifold = self.narrowphase.get_collision_manifold(pair[0], pair[1])
                    if manifold:
                        contact = self._get_or_create_contact(
                            pair[0], pair[1], manifold
                        )
                        island.add_contact(contact)

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
