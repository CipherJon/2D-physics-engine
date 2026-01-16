import sys

sys.path.append("/media/cipherjon/HDD/Repo/physics-engine/src")

from math.vec2 import Vec2

from common.color import Color


class DebugDraw:
    """
    A base class for debugging visualization in a physics engine.
    This class provides methods to draw shapes, lines, and points for debugging purposes.
    """

    def __init__(self):
        """
        Initialize the debug draw object.
        """
        self.draw_flags = {
            "shape": True,
            "joint": True,
            "aabb": False,
            "center_of_mass": False,
            "contact_points": True,
            "contact_normals": True,
        }

    def set_flags(self, flags):
        """
        Set the drawing flags for the debug draw object.

        Args:
            flags (dict): A dictionary of flags to set.
        """
        for key, value in flags.items():
            if key in self.draw_flags:
                self.draw_flags[key] = value

    def get_flags(self):
        """
        Get the current drawing flags.

        Returns:
            dict: The current drawing flags.
        """
        return self.draw_flags

    def draw_point(self, point, color=Color(1.0, 0.0, 0.0), size=5.0):
        """
        Draw a point.

        Args:
            point (Vec2): The point to draw.
            color (Color): The color of the point.
            size (float): The size of the point.
        """
        raise NotImplementedError("This method should be implemented by a subclass.")

    def draw_line(self, start, end, color=Color(1.0, 0.0, 0.0)):
        """
        Draw a line segment.

        Args:
            start (Vec2): The start point of the line.
            end (Vec2): The end point of the line.
            color (Color): The color of the line.
        """
        raise NotImplementedError("This method should be implemented by a subclass.")

    def draw_circle(self, center, radius, color=Color(1.0, 0.0, 0.0)):
        """
        Draw a circle.

        Args:
            center (Vec2): The center of the circle.
            radius (float): The radius of the circle.
            color (Color): The color of the circle.
        """
        raise NotImplementedError("This method should be implemented by a subclass.")

    def draw_polygon(self, vertices, color=Color(1.0, 0.0, 0.0)):
        """
        Draw a polygon.

        Args:
            vertices (list of Vec2): The vertices of the polygon.
            color (Color): The color of the polygon.
        """
        raise NotImplementedError("This method should be implemented by a subclass.")

    def draw_aabb(self, aabb, color=Color(1.0, 0.0, 0.0)):
        """
        Draw an axis-aligned bounding box (AABB).

        Args:
            aabb (tuple): The AABB as a tuple of (min, max) vertices.
            color (Color): The color of the AABB.
        """
        min_vertex, max_vertex = aabb
        vertices = [
            Vec2(min_vertex.x, min_vertex.y),
            Vec2(max_vertex.x, min_vertex.y),
            Vec2(max_vertex.x, max_vertex.y),
            Vec2(min_vertex.x, max_vertex.y),
        ]
        self.draw_polygon(vertices, color)

    def draw_transform(self, transform):
        """
        Draw a transform (position and rotation).

        Args:
            transform (Transform): The transform to draw.
        """
        raise NotImplementedError("This method should be implemented by a subclass.")

    def draw_joint(self, joint):
        """
        Draw a joint.

        Args:
            joint (Joint): The joint to draw.
        """
        raise NotImplementedError("This method should be implemented by a subclass.")

    def draw_contact(self, contact):
        """
        Draw a contact point and normal.

        Args:
            contact (Contact): The contact to draw.
        """
        raise NotImplementedError("This method should be implemented by a subclass.")

    def draw_body(self, body):
        """
        Draw a physics body.

        Args:
            body (Body): The body to draw.
        """
        if self.draw_flags["shape"]:
            if hasattr(body.shape, "get_transformed_vertices"):
                vertices = body.shape.get_transformed_vertices()
                self.draw_polygon(vertices)
            elif hasattr(body.shape, "center"):
                self.draw_circle(body.shape.center, body.shape.radius)

        if self.draw_flags["center_of_mass"]:
            self.draw_point(body.position, Color(0.0, 1.0, 0.0), 5.0)

        if self.draw_flags["aabb"]:
            self.draw_aabb(body.get_aabb())

    def draw_world(self, world):
        """
        Draw the entire simulation world.

        Args:
            world (World): The world to draw.
        """
        for body in world.get_bodies():
            self.draw_body(body)

        if self.draw_flags["joint"]:
            for joint in world.get_joints():
                self.draw_joint(joint)

    def clear(self):
        """
        Clear the drawing surface.
        """
        raise NotImplementedError("This method should be implemented by a subclass.")
