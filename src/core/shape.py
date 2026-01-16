from typing import List

from ..math.vec2 import Vec2


class Shape:
    """
    A base class for all shapes in the physics engine.
    """

    def __init__(self) -> None:
        """
        Initialize the shape.
        """
        pass

    def get_vertices(self) -> List[Vec2]:
        """
        Get the vertices of the shape.

        Returns:
            List[Vec2]: The vertices of the shape.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    def get_inertia(self, mass: float) -> float:
        """
        Calculate the moment of inertia for the shape.

        Args:
            mass (float): The mass of the shape.

        Returns:
            float: The moment of inertia.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    def get_aabb(self, body: "Body") -> "AABB":
        """
        Get the axis-aligned bounding box of the shape.

        Args:
            body (Body): The body associated with the shape.

        Returns:
            AABB: The axis-aligned bounding box.
        """
        raise NotImplementedError("Subclasses must implement this method.")
