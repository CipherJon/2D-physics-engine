"""
Manifold class for collision detection.
"""

from src.math.vec2 import Vec2


class Manifold:
    """
    Represents a collision manifold between two shapes.
    """

    def __init__(self, normal, depth, points):
        """
        Initialize the collision manifold.

        Args:
            normal (Vec2): The normal vector of the collision.
            depth (float): The depth of the collision.
            points (list of Vec2): The collision points.
        """
        self.normal = normal
        self.depth = depth
        self.points = points

    def __repr__(self):
        """
        Return a string representation of the collision manifold.

        Returns:
            str: A string representation of the collision manifold.
        """
        return (
            f"Manifold(normal={self.normal}, depth={self.depth}, points={self.points})"
        )
