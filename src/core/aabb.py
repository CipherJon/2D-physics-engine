"""
AABB (Axis-Aligned Bounding Box) class for collision detection.
"""

from src.math.vec2 import Vec2


class AABB:
    """
    Represents an axis-aligned bounding box.
    """

    def __init__(self, lower_bound, upper_bound, body=None):
        """
        Initialize the AABB with lower and upper bounds.

        Args:
            lower_bound (Vec2): The lower bound of the AABB.
            upper_bound (Vec2): The upper bound of the AABB.
            body (Body, optional): The body associated with the AABB.
        """
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.body = body

    def __repr__(self):
        """
        Return a string representation of the AABB.

        Returns:
            str: A string representation of the AABB.
        """
        return f"AABB(lower_bound={self.lower_bound}, upper_bound={self.upper_bound})"

    def contains(self, point):
        """
        Check if a point is inside the AABB.

        Args:
            point (Vec2): The point to check.

        Returns:
            bool: True if the point is inside the AABB, False otherwise.
        """
        return (
            self.lower_bound.x <= point.x <= self.upper_bound.x
            and self.lower_bound.y <= point.y <= self.upper_bound.y
        )

    def overlaps(self, other):
        """
        Check if this AABB overlaps with another AABB.

        Args:
            other (AABB): The other AABB to check.

        Returns:
            bool: True if the AABBs overlap, False otherwise.
        """
        return (
            self.lower_bound.x <= other.upper_bound.x
            and self.upper_bound.x >= other.lower_bound.x
            and self.lower_bound.y <= other.upper_bound.y
            and self.upper_bound.y >= other.lower_bound.y
        )
