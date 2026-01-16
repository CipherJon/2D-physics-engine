import math

from ..core.shape import Shape
from ..math.vec2 import Vec2


class Circle(Shape):
    """
    A class to represent a circular shape in a physics engine.
    """

    def __init__(self, center=Vec2.zero(), radius=1.0):
        """
        Initialize a circle with a center and radius.

        Args:
            center (Vec2): The center of the circle.
            radius (float): The radius of the circle.
        """
        self.center = center
        self.radius = float(radius)

    def __str__(self):
        """
        Return a string representation of the circle.
        """
        return f"Circle(center={self.center}, radius={self.radius})"

    def __repr__(self):
        """
        Return a detailed string representation of the circle.
        """
        return f"Circle(center={repr(self.center)}, radius={self.radius})"

    def __eq__(self, other):
        """
        Check if two circles are equal.

        Args:
            other (Circle): The circle to compare with.

        Returns:
            bool: True if the circles are equal, False otherwise.
        """
        if not isinstance(other, Circle):
            return False
        return self.center == other.center and math.isclose(self.radius, other.radius)

    def area(self):
        """
        Calculate the area of the circle.

        Returns:
            float: The area of the circle.
        """
        return math.pi * self.radius**2

    def circumference(self):
        """
        Calculate the circumference of the circle.

        Returns:
            float: The circumference of the circle.
        """
        return 2 * math.pi * self.radius

    def contains_point(self, point):
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

    def translate(self, translation):
        """
        Translate the circle by a vector.

        Args:
            translation (Vec2): The translation vector.
        """
        self.center += translation

    def get_vertices(self):
        """
        Get the vertices of the circle.

        Returns:
            list of Vec2: The vertices of the circle.
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

    def rotate(self, angle, pivot=Vec2.zero()):
        """
        Rotate the circle around a pivot point.

        Args:
            angle (float): The angle to rotate by (in radians).
            pivot (Vec2): The pivot point to rotate around.
        """
        # Translate the circle so that the pivot is at the origin
        translated_center = self.center - pivot
        # Apply rotation
        rotated_center = translated_center.rotate(angle)
        # Translate back
        self.center = rotated_center + pivot
