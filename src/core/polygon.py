import math

from ..math.mat22 import Mat22
from ..math.transform import Transform
from ..math.vec2 import Vec2


class Polygon:
    """
    A class to represent a polygonal shape in a physics engine.
    """

    def __init__(self, vertices, transform=None):
        """
        Initialize a polygon with a list of vertices.

        Args:
            vertices (list of Vec2): The vertices of the polygon.
            transform (Transform): The transformation to apply to the polygon.
        """
        if len(vertices) < 3:
            raise ValueError("A polygon must have at least 3 vertices.")
        self.vertices = vertices
        self.transform = transform if transform is not None else Transform.identity()
        self._normals = None
        self._centroid = None

    def __str__(self):
        """
        Return a string representation of the polygon.
        """
        return f"Polygon(vertices={self.vertices}, transform={self.transform})"

    def __repr__(self):
        """
        Return a detailed string representation of the polygon.
        """
        return (
            f"Polygon(vertices={repr(self.vertices)}, transform={repr(self.transform)})"
        )

    def get_vertices(self):
        """
        Get the vertices of the polygon.

        Returns:
            list of Vec2: The vertices of the polygon.
        """
        return self.vertices

    def get_transformed_vertices(self):
        """
        Get the vertices of the polygon after applying the transformation.

        Returns:
            list of Vec2: The transformed vertices of the polygon.
        """
        return [self.transform.transform_point(v) for v in self.vertices]

    def get_normals(self):
        """
        Get the normals of the polygon edges.

        Returns:
            list of Vec2: The normals of the polygon edges.
        """
        if self._normals is None:
            self._compute_normals()
        return self._normals

    def get_centroid(self):
        """
        Get the centroid of the polygon.

        Returns:
            Vec2: The centroid of the polygon.
        """
        if self._centroid is None:
            self._compute_centroid()
        return self._centroid

    def _compute_normals(self):
        """
        Compute the normals of the polygon edges.
        """
        vertices = self.get_transformed_vertices()
        normals = []
        n = len(vertices)
        for i in range(n):
            v1 = vertices[i]
            v2 = vertices[(i + 1) % n]
            edge = v2 - v1
            normal = Vec2(-edge.y, edge.x).normalize()
            normals.append(normal)
        self._normals = normals

    def _compute_centroid(self):
        """
        Compute the centroid of the polygon.
        """
        vertices = self.get_transformed_vertices()
        n = len(vertices)
        centroid = Vec2.zero()
        for v in vertices:
            centroid += v
        centroid /= n
        self._centroid = centroid

    def get_area(self):
        """
        Compute the area of the polygon.

        Returns:
            float: The area of the polygon.
        """
        vertices = self.get_transformed_vertices()
        n = len(vertices)
        area = 0.0
        for i in range(n):
            v1 = vertices[i]
            v2 = vertices[(i + 1) % n]
            area += v1.x * v2.y - v2.x * v1.y
        return abs(area) / 2.0

    def get_inertia(self, mass):
        """
        Compute the moment of inertia of the polygon.

        Args:
            mass (float): The mass of the polygon.

        Returns:
            float: The moment of inertia of the polygon.
        """
        vertices = self.get_transformed_vertices()
        n = len(vertices)
        inertia = 0.0
        for i in range(n):
            v1 = vertices[i]
            v2 = vertices[(i + 1) % n]
            cross = v1.x * v2.y - v2.x * v1.y
            dot = v1.dot(v1) + v1.dot(v2) + v2.dot(v2)
            inertia += cross * dot
        return mass * abs(inertia) / 12.0

    def contains_point(self, point):
        """
        Check if a point is inside the polygon.

        Args:
            point (Vec2): The point to check.

        Returns:
            bool: True if the point is inside the polygon, False otherwise.
        """
        vertices = self.get_transformed_vertices()
        n = len(vertices)
        inside = False
        for i in range(n):
            v1 = vertices[i]
            v2 = vertices[(i + 1) % n]
            if ((v1.y > point.y) != (v2.y > point.y)) and (
                point.x < (v2.x - v1.x) * (point.y - v1.y) / (v2.y - v1.y) + v1.x
            ):
                inside = not inside
        return inside

    def get_aabb(self):
        """
        Get the axis-aligned bounding box of the polygon.

        Returns:
            tuple: The minimum and maximum vertices of the AABB.
        """
        vertices = self.get_transformed_vertices()
        min_x = min(v.x for v in vertices)
        min_y = min(v.y for v in vertices)
        max_x = max(v.x for v in vertices)
        max_y = max(v.y for v in vertices)
        return (Vec2(min_x, min_y), Vec2(max_x, max_y))

    def translate(self, translation):
        """
        Translate the polygon by a given vector.

        Args:
            translation (Vec2): The translation vector.
        """
        self.transform.position += translation

    def rotate(self, angle):
        """
        Rotate the polygon by a given angle.

        Args:
            angle (float): The angle to rotate by (in radians).
        """
        self.transform.rotation += angle

    def set_transform(self, transform):
        """
        Set the transformation of the polygon.

        Args:
            transform (Transform): The transformation to apply.
        """
        self.transform = transform
        self._normals = None
        self._centroid = None
