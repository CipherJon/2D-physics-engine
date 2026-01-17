"""
Edge class for the physics engine.

This module provides functionality for creating and managing edge shapes,
which are used to represent line segments in the physics engine.
"""

from ..math.vec2 import Vec2
from .shape import Shape


class Edge(Shape):
    """
    A class to represent an edge shape.

    Attributes:
        vertex1 (Vec2): The first vertex of the edge.
        vertex2 (Vec2): The second vertex of the edge.
    """

    def __init__(self, vertex1, vertex2):
        """
        Initialize a new Edge.

        Args:
            vertex1 (Vec2): The first vertex of the edge.
            vertex2 (Vec2): The second vertex of the edge.
        """
        super().__init__()
        self.vertex1 = vertex1
        self.vertex2 = vertex2
        self.type = "edge"

    def compute_mass(self, density):
        """
        Compute the mass of the edge.

        Args:
            density (float): The density of the edge.

        Returns:
            float: The mass of the edge.
        """
        # Edges are considered massless
        return 0.0

    def compute_inertia(self, density):
        """
        Compute the inertia of the edge.

        Args:
            density (float): The density of the edge.

        Returns:
            float: The inertia of the edge.
        """
        # Edges are considered massless
        return 0.0

    def get_center(self):
        """
        Get the center of the edge.

        Returns:
            Vec2: The center of the edge.
        """
        return (self.vertex1 + self.vertex2) * 0.5

    def get_vertices(self):
        """
        Get the vertices of the edge.

        Returns:
            list: A list of the vertices of the edge.
        """
        return [self.vertex1, self.vertex2]

    def get_normals(self):
        """
        Get the normals of the edge.

        Returns:
            list: A list of the normals of the edge.
        """
        edge_vector = self.vertex2 - self.vertex1
        normal = Vec2(-edge_vector.y, edge_vector.x).normalized()
        return [normal]
