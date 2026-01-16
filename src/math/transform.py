import math

from .mat22 import Mat22
from .vec2 import Vec2


class Transform:
    """
    A class to represent transformations (translation and rotation) in a physics engine.
    """

    def __init__(self, position=None, rotation=0.0):
        """
        Initialize a transformation with a position and rotation.

        Args:
            position (Vec2): The position of the transformation.
            rotation (float): The rotation angle in radians.
        """
        self.position = position if position is not None else Vec2.zero()
        self.rotation = float(rotation)

    def __str__(self):
        """
        Return a string representation of the transformation.
        """
        return f"Transform(position={self.position}, rotation={self.rotation})"

    def __repr__(self):
        """
        Return a detailed string representation of the transformation.
        """
        return f"Transform(position={repr(self.position)}, rotation={self.rotation})"

    def __eq__(self, other):
        """
        Check if two transformations are equal.

        Args:
            other (Transform): The transformation to compare with.

        Returns:
            bool: True if the transformations are equal, False otherwise.
        """
        if not isinstance(other, Transform):
            return False
        return self.position == other.position and math.isclose(
            self.rotation, other.rotation
        )

    def get_rotation_matrix(self):
        """
        Get the rotation matrix for the transformation.

        Returns:
            Mat22: The rotation matrix.
        """
        return Mat22.from_angle(self.rotation)

    def transform_point(self, point):
        """
        Transform a point using the transformation.

        Args:
            point (Vec2): The point to transform.

        Returns:
            Vec2: The transformed point.
        """
        rotation_matrix = self.get_rotation_matrix()
        rotated_point = rotation_matrix * point
        return rotated_point + self.position

    def inverse_transform_point(self, point):
        """
        Inverse transform a point using the transformation.

        Args:
            point (Vec2): The point to inverse transform.

        Returns:
            Vec2: The inverse transformed point.
        """
        rotation_matrix = self.get_rotation_matrix()
        inverse_rotation_matrix = rotation_matrix.transpose()
        translated_point = point - self.position
        return inverse_rotation_matrix * translated_point

    def transform_vector(self, vector):
        """
        Transform a vector using the rotation of the transformation.

        Args:
            vector (Vec2): The vector to transform.

        Returns:
            Vec2: The transformed vector.
        """
        rotation_matrix = self.get_rotation_matrix()
        return rotation_matrix * vector

    def inverse_transform_vector(self, vector):
        """
        Inverse transform a vector using the rotation of the transformation.

        Args:
            vector (Vec2): The vector to inverse transform.

        Returns:
            Vec2: The inverse transformed vector.
        """
        rotation_matrix = self.get_rotation_matrix()
        inverse_rotation_matrix = rotation_matrix.transpose()
        return inverse_rotation_matrix * vector

    @classmethod
    def identity(cls):
        """
        Create an identity transformation.

        Returns:
            Transform: The identity transformation.
        """
        return cls(Vec2.zero(), 0.0)

    @classmethod
    def from_position(cls, position):
        """
        Create a transformation from a position.

        Args:
            position (Vec2): The position of the transformation.

        Returns:
            Transform: The transformation.
        """
        return cls(position, 0.0)

    @classmethod
    def from_rotation(cls, rotation):
        """
        Create a transformation from a rotation.

        Args:
            rotation (float): The rotation angle in radians.

        Returns:
            Transform: The transformation.
        """
        return cls(Vec2.zero(), rotation)
