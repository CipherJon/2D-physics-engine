import math
from typing import List, Optional

from ..core.shape import Shape
from ..math.vec2 import Vec2


class Circle(Shape):
    """
    A class to represent a circular shape in a physics engine.
    """

    def __init__(self, center: Vec2 = Vec2.zero(), radius: float = 1.0) -> None:
        """
        Initialize a circle with a center and radius.

        Args:
            center (Vec2): The center of the circle. Defaults to Vec2.zero().
            radius (float): The radius of the circle. Defaults to 1.0.
        """
        self.center = center
        self.radius = float(radius)

    def __str__(self) -> str:
        """
        Return a string representation of the circle.

        Returns:
            str: A string representation of the circle.
        """
        return f"Circle(center={self.center}, radius={self.radius})"

    def __repr__(self) -> str:
        """
        Return a detailed string representation of the circle.

        Returns:
            str: A detailed string representation of the circle.
        """
        return f"Circle(center={repr(self.center)}, radius={self.radius})"

    def __eq__(self, other: object) -> bool:
        """
        Check if two circles are equal.

        Args:
            other (object): The object to compare with.

        Returns:
            bool: True if the circles are equal, False otherwise.
        """
        if not isinstance(other, Circle):
            return False
        return self.center == other.center and math.isclose(self.radius, other.radius)

    def area(self) -> float:
        """
        Calculate the area of the circle.

        Returns:
            float: The area of the circle.
        """
        return math.pi * self.radius**2

    def circumference(self) -> float:
        """
        Calculate the circumference of the circle.

        Returns:
            float: The circumference of the circle.
        """
        return 2 * math.pi * self.radius

    def contains_point(self, point: Vec2) -> bool:
        """
        Check if a point is inside the circle.

        Args:
            point (Vec2): The point to check.

        Returns:
            bool: True if the point is inside the circle, False otherwise.
        """
        distance_squared = (point.x - self.center.x) ** 2 + (
            point.y - self.center.y
        ) ** 2
        return distance_squared <= self.radius**2

    def translate(self, translation: Vec2) -> None:
        """
        Translate the circle by a vector.

        Args:
            translation (Vec2): The translation vector.
        """
        self.center += translation

    def get_vertices(self) -> List[Vec2]:
        """
        Get the vertices of the circle.

        Returns:
            List[Vec2]: The vertices of the circle.
        """
        # Approximate the circle with a polygon
        num_vertices = 16
        vertices = []
        for i in range(num_vertices):
            angle = 2 * math.pi * i / num_vertices
            x = self.center.x + self.radius * math.cos(angle)
            y = self.center.y + self.radius * math.sin(angle)
            vertices.append(Vec2(x, y))
        return vertices

    def rotate(self, angle: float, pivot: Vec2 = Vec2.zero()) -> None:
        """
        Rotate the circle around a pivot point.

        Args:
            angle (float): The angle to rotate by (in radians).
            pivot (Vec2): The pivot point to rotate around. Defaults to Vec2.zero().
        """
        # Translate the circle so that the pivot is at the origin
        translated_center = self.center - pivot
        # Apply rotation
        rotated_center = translated_center.rotate(angle)
        # Translate back
        self.center = rotated_center + pivot

    def get_aabb(self, body: Optional["Body"] = None) -> "AABB":
        """
        Get the axis-aligned bounding box for the circle.

        Args:
            body (Optional[Body]): The body associated with the AABB. Defaults to None.

        Returns:
            AABB: The axis-aligned bounding box.
        """
        from src.core.aabb import AABB

        # Calculate the world position of the circle's center
        if body:
            center = body.position + self.center
        else:
            center = self.center

        return AABB(
            Vec2(center.x - self.radius, center.y - self.radius),
            Vec2(center.x + self.radius, center.y + self.radius),
            body,
        )

    def get_inertia(self, mass: float) -> float:
        """
        Calculate the moment of inertia for the circle.

        Args:
            mass (float): The mass of the circle.

        Returns:
            float: The moment of inertia.
        """
        return 0.5 * mass * self.radius**2
