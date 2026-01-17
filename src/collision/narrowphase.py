"""
Narrowphase collision detection module.
"""

import logging
from typing import List

from src.collision.contact import Contact
from src.collision.sat import SAT
from src.contacts.contact_solver import ContactSolver
from src.core.shape import Shape
from src.math.vec2 import Vec2

# Configure logging
logging.basicConfig(
    level=logging.DEBUG, format="%(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class BodyShapeWrapper(Shape):
    """
    A wrapper class that adjusts shape vertices for body position.
    """

    def __init__(self, body, original_shape):
        super().__init__()
        self.body = body
        self.original_shape = original_shape

    def get_vertices(self) -> List[Vec2]:
        """Get vertices adjusted for body position."""
        vertices = self.original_shape.get_vertices()
        logger.info(
            f"Original vertices for {type(self.original_shape).__name__}: {vertices}"
        )
        logger.info(f"Body position: {self.body.position}")

        if hasattr(self.original_shape, "center"):  # Circle
            # For circles, vertices are calculated relative to circle center
            # Adjust each vertex by body position
            adjusted_vertices = []
            for vertex in vertices:
                adjusted_vertex = vertex + self.body.position
                adjusted_vertices.append(adjusted_vertex)
            logger.info(f"Adjusted circle vertices: {adjusted_vertices}")
            return adjusted_vertices
        else:  # Polygon or other shapes
            # For polygons, adjust each vertex by body position
            adjusted_vertices = []
            for vertex in vertices:
                adjusted_vertex = vertex + self.body.position
                adjusted_vertices.append(adjusted_vertex)
            logger.info(f"Adjusted polygon vertices: {adjusted_vertices}")
            return adjusted_vertices

    # Delegate other methods to the original shape
    def __getattr__(self, name):
        return getattr(self.original_shape, name)


class Narrowphase:
    """
    Performs narrow-phase collision detection between shapes.
    """

    def __init__(self):
        """
        Initialize the narrow-phase collision detector.
        """
        self.sat = SAT()
        self.contact_solver = ContactSolver()

    def detect_collision(self, body1, body2):
        """
        Detect collision between two bodies using the Separating Axis Theorem (SAT).

        Args:
            body1: The first body.
            body2: The second body.

        Returns:
            bool: True if the bodies collide, False otherwise.
        """
        # Create wrapper shapes that account for body positions
        shape1_wrapper = self._create_body_shape_wrapper(body1)
        shape2_wrapper = self._create_body_shape_wrapper(body2)

        collision_detected = self.sat.detect_collision(shape1_wrapper, shape2_wrapper)
        logger.info(f"Collision detected between body1 and body2: {collision_detected}")
        return collision_detected

    def get_collision_manifold(self, body1, body2):
        """
        Get the collision manifold between two bodies.

        Args:
            body1: The first body.
            body2: The second body.

        Returns:
            Manifold: The collision manifold.
        """
        # Create wrapper shapes that account for body positions
        shape1_wrapper = self._create_body_shape_wrapper(body1)
        shape2_wrapper = self._create_body_shape_wrapper(body2)

        manifold = self.sat.get_collision_manifold(shape1_wrapper, shape2_wrapper)
        logger.info(f"Collision manifold: {manifold}")
        return manifold

    def _create_body_shape_wrapper(self, body):
        """
        Create a wrapper shape that accounts for body position.

        Args:
            body: The body to wrap.

        Returns:
            A shape wrapper that includes body position.
        """
        return BodyShapeWrapper(body, body.shape)

    def resolve_collision(self, body1, body2, dt):
        """
        Resolve collision between two bodies using the contact solver.

        Args:
            body1: The first body.
            body2: The second body.
            dt: The time step for the simulation.
        """
        self.contact_solver.clear_contacts()
        if self.detect_collision(body1, body2):
            manifold = self.get_collision_manifold(body1, body2)
            # Apply collision response
            if manifold is not None:
                logger.info("=== COLLISION RESOLUTION ===")
                logger.info(
                    "Body at {} vs Body at {}".format(body1.position, body2.position)
                )
                logger.info(f"Normal: {manifold.normal}, Depth: {manifold.depth:.4f}")

                # Create a contact and add it to the solver
                contact = Contact(
                    body_a=body1,
                    body_b=body2,
                    normal=manifold.normal,
                    penetration=manifold.depth,
                    contact_point=manifold.points[0]
                    if manifold.points
                    else body1.position,
                )
                self.contact_solver.add_contact(contact)

                # Solve the contact
                self.contact_solver.solve(dt)
                logger.info("=== END COLLISION RESOLUTION ===\n")
