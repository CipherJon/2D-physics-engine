"""
Narrowphase collision detection module.
"""

from src.collision.sat import SAT
from src.core.aabb import AABB
from src.math.vec2 import Vec2


class Narrowphase:
    """
    Performs narrow-phase collision detection between shapes.
    """

    def __init__(self):
        """
        Initialize the narrow-phase collision detector.
        """
        self.sat = SAT()

    def detect_collision(self, body1, body2):
        """
        Detect collision between two bodies using the Separating Axis Theorem (SAT).

        Args:
            body1: The first body.
            body2: The second body.

        Returns:
            bool: True if the bodies collide, False otherwise.
        """
        return self.sat.detect_collision(body1.shape, body2.shape)

    def get_collision_manifold(self, shape1, shape2):
        """
        Get the collision manifold between two shapes.

        Args:
            shape1: The first shape.
            shape2: The second shape.

        Returns:
            Manifold: The collision manifold.
        """
        return self.sat.get_collision_manifold(shape1, shape2)

    def resolve_collision(self, body1, body2):
        """
        Resolve collision between two bodies.

        Args:
            body1: The first body.
            body2: The second body.
        """
        if self.detect_collision(body1, body2):
            manifold = self.get_collision_manifold(body1.shape, body2.shape)
            # Apply collision response
            if manifold is not None:
                # Calculate relative velocity
                relative_velocity = body2.velocity - body1.velocity
                # Calculate impulse
                impulse = manifold.normal * manifold.depth
                # Apply impulse to the bodies
                body1.velocity -= impulse * body1.inverse_mass
                body2.velocity += impulse * body2.inverse_mass
