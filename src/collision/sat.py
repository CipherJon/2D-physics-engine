import logging

from ..core.shape import Shape
from ..math.vec2 import Vec2

# Configure logging
logging.basicConfig(
    level=logging.DEBUG, format="%(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class SAT:
    """
    Separating Axis Theorem (SAT) for collision detection between convex polygons.
    """

    # Position tolerance constants
    PENETRATION_TOLERANCE = 0.01  # Allow tiny penetrations to be treated as contact
    SEPARATION_TOLERANCE = 0.005  # Allow tiny gaps to be treated as contact

    @staticmethod
    def detect_collision(shape1, shape2):
        """
        Detect collision between two shapes using the Separating Axis Theorem.

        Args:
            shape1 (Shape): The first shape.
            shape2 (Shape): The second shape.

        Returns:
            bool: True if the shapes are colliding, False otherwise.
        """
        if not isinstance(shape1, Shape) or not isinstance(shape2, Shape):
            raise ValueError("Both shapes must be instances of Shape.")

        # Get the vertices of both shapes
        vertices1 = shape1.get_vertices()
        vertices2 = shape2.get_vertices()

        # Combine the vertices to find all potential axes
        all_vertices = vertices1 + vertices2

        # Find the axes to test
        axes = SAT._find_axes(all_vertices)

        # Test each axis for separation
        for axis in axes:
            if SAT._is_separating_axis(vertices1, vertices2, axis):
                logger.info(f"Separating axis found: {axis}")
                return False

        logger.info("No separating axis found, collision detected")
        return True

    @staticmethod
    def _find_axes(vertices):
        """
        Find the axes to test for separation.

        Args:
            vertices (list of Vec2): The vertices of the shapes.

        Returns:
            list of Vec2: The axes to test.
        """
        axes = []
        for i in range(len(vertices)):
            # Get the current vertex and the next vertex
            current = vertices[i]
            next_vertex = vertices[(i + 1) % len(vertices)]

            # Calculate the edge vector
            edge = next_vertex - current

            # Calculate the normal vector (perpendicular to the edge)
            normal = Vec2(-edge.y, edge.x)
            normal = normal.normalize()

            # Add the normal to the list of axes
            axes.append(normal)

        return axes

    @staticmethod
    def _is_separating_axis(vertices1, vertices2, axis):
        """
        Check if the given axis is a separating axis.

        Args:
            vertices1 (list of Vec2): The vertices of the first shape.
            vertices2 (list of Vec2): The vertices of the second shape.
            axis (Vec2): The axis to test.

        Returns:
            bool: True if the axis is a separating axis, False otherwise.
        """
        # Project the vertices of both shapes onto the axis
        min1, max1 = SAT._project_vertices(vertices1, axis)
        min2, max2 = SAT._project_vertices(vertices2, axis)

        # Check for overlap
        if max1 < min2 or max2 < min1:
            logger.info(
                f"Separating axis found: {axis} (max1={max1}, min2={min2}, max2={max2}, min1={min1})"
            )
            return True

        logger.info(
            f"No separating axis found: {axis} (max1={max1}, min2={min2}, max2={max2}, min1={min1})"
        )
        return False

    @staticmethod
    def _project_vertices(vertices, axis):
        """
        Project the vertices onto the given axis.

        Args:
            vertices (list of Vec2): The vertices to project.
            axis (Vec2): The axis to project onto.

        Returns:
            tuple: The minimum and maximum projections.
        """
        min_proj = float("inf")
        max_proj = -float("inf")

        for vertex in vertices:
            # Calculate the projection of the vertex onto the axis
            proj = vertex.dot(axis)

            # Update the minimum and maximum projections
            if proj < min_proj:
                min_proj = proj
            if proj > max_proj:
                max_proj = proj

        return min_proj, max_proj

    @staticmethod
    def find_minimum_translation_vector(shape1, shape2):
        """
        Find the Minimum Translation Vector (MTV) to resolve a collision.

        Args:
            shape1 (Shape): The first shape.
            shape2 (Shape): The second shape.

        Returns:
            Vec2: The Minimum Translation Vector.
        """
        if not isinstance(shape1, Shape) or not isinstance(shape2, Shape):
            raise ValueError("Both shapes must be instances of Shape.")

        # Get the vertices of both shapes
        vertices1 = shape1.get_vertices()
        vertices2 = shape2.get_vertices()

        # Combine the vertices to find all potential axes
        all_vertices = vertices1 + vertices2

        # Find the axes to test
        axes = SAT._find_axes(all_vertices)

        # Initialize the minimum overlap and the MTV
        min_overlap = float("inf")
        mtv = Vec2.zero()

        # Test each axis for the minimum overlap
        for axis in axes:
            # Project the vertices of both shapes onto the axis
            min1, max1 = SAT._project_vertices(vertices1, axis)
            min2, max2 = SAT._project_vertices(vertices2, axis)

            # Calculate the overlap
            overlap = min(max1, max2) - max(min1, min2)

            # Log the overlap for debugging
            logger.info(f"Overlap on axis {axis}: {overlap}")

            # If there is no overlap, the shapes are not colliding
            # Use position tolerance to handle tiny gaps or penetrations
            if overlap < -SAT.SEPARATION_TOLERANCE:
                logger.info("Separating axis found, no collision")
                return Vec2.zero()

            # If the overlap is smaller than the current minimum, update the MTV
            if overlap < min_overlap:
                min_overlap = overlap
                mtv = axis * overlap

        logger.info(f"Final MTV: {mtv}")
        return mtv

    @staticmethod
    def get_collision_manifold(shape1, shape2):
        """
        Get the collision manifold between two shapes.

        Args:
            shape1 (Shape): The first shape.
            shape2 (Shape): The second shape.

        Returns:
            Manifold: The collision manifold.
        """
        if not isinstance(shape1, Shape) or not isinstance(shape2, Shape):
            raise ValueError("Both shapes must be instances of Shape.")

        # Get the vertices of both shapes
        vertices1 = shape1.get_vertices()
        vertices2 = shape2.get_vertices()

        # Find the Minimum Translation Vector (MTV)
        mtv = SAT.find_minimum_translation_vector(shape1, shape2)

        # If there is no collision, return None
        # But treat zero MTV (just touching) as a collision for physics stability
        if mtv == Vec2.zero():
            # Check if shapes are just touching by testing a few axes
            # Find an axis where shapes are closest
            test_axes = SAT._find_axes(
                vertices1[:4] + vertices2[:4]
            )  # Use first few vertices
            for axis in test_axes:
                min1, max1 = SAT._project_vertices(vertices1, axis)
                min2, max2 = SAT._project_vertices(vertices2, axis)
                overlap = min(max1, max2) - max(min1, min2)
                if abs(overlap) < SAT.PENETRATION_TOLERANCE:
                    # Shapes are just touching, create a small penetration
                    mtv = axis * SAT.PENETRATION_TOLERANCE
                    break
            if mtv == Vec2.zero():
                return None

        # Apply position tolerance to treat tiny gaps or penetrations as contacts
        if mtv.magnitude() < SAT.PENETRATION_TOLERANCE:
            mtv = mtv.normalize() * SAT.PENETRATION_TOLERANCE

        # Find the collision normal
        normal = mtv.normalize()

        # Find the collision depth
        depth = mtv.magnitude()

        # Find the collision points
        collision_points = []
        for vertex in vertices1:
            if SAT._is_point_in_shape(vertex, vertices2):
                collision_points.append(vertex)
        for vertex in vertices2:
            if SAT._is_point_in_shape(vertex, vertices1):
                collision_points.append(vertex)

        # Create and return the collision manifold
        from src.collision.manifold import Manifold

        return Manifold(normal, depth, collision_points)

    @staticmethod
    def _is_point_in_shape(point, vertices):
        """
        Check if a point is inside a shape.

        Args:
            point (Vec2): The point to check.
            vertices (list of Vec2): The vertices of the shape.

        Returns:
            bool: True if the point is inside the shape, False otherwise.
        """
        # Implement point-in-polygon algorithm
        inside = False
        n = len(vertices)
        for i in range(n):
            j = (i + 1) % n
            if ((vertices[i].y > point.y) != (vertices[j].y > point.y)) and (
                point.x
                < (vertices[j].x - vertices[i].x)
                * (point.y - vertices[i].y)
                / (vertices[j].y - vertices[i].y)
                + vertices[i].x
            ):
                inside = not inside
        return inside
