```path/to/physics-engine/src/math/vec2.py#L1-200
import math

class Vec2:
    """
    A 2D vector class for handling vector operations in a physics engine.
    """

    def __init__(self, x=0.0, y=0.0):
        """
        Initialize a 2D vector with x and y components.

        Args:
            x (float): The x-component of the vector.
            y (float): The y-component of the vector.
        """
        self.x = float(x)
        self.y = float(y)

    def __str__(self):
        """
        Return a string representation of the vector.
        """
        return f"Vec2({self.x}, {self.y})"

    def __repr__(self):
        """
        Return a detailed string representation of the vector.
        """
        return f"Vec2(x={self.x}, y={self.y})"

    def __add__(self, other):
        """
        Add two vectors or a vector and a scalar.

        Args:
            other (Vec2 or float): The vector or scalar to add.

        Returns:
            Vec2: The resulting vector.
        """
        if isinstance(other, Vec2):
            return Vec2(self.x + other.x, self.y + other.y)
        else:
            return Vec2(self.x + other, self.y + other)

    def __sub__(self, other):
        """
        Subtract two vectors or a vector and a scalar.

        Args:
            other (Vec2 or float): The vector or scalar to subtract.

        Returns:
            Vec2: The resulting vector.
        """
        if isinstance(other, Vec2):
            return Vec2(self.x - other.x, self.y - other.y)
        else:
            return Vec2(self.x - other, self.y - other)

    def __mul__(self, other):
        """
        Multiply the vector by a scalar or another vector (element-wise).

        Args:
            other (Vec2 or float): The scalar or vector to multiply by.

        Returns:
            Vec2: The resulting vector.
        """
        if isinstance(other, Vec2):
            return Vec2(self.x * other.x, self.y * other.y)
        else:
            return Vec2(self.x * other, self.y * other)

    def __truediv__(self, other):
        """
        Divide the vector by a scalar or another vector (element-wise).

        Args:
            other (Vec2 or float): The scalar or vector to divide by.

        Returns:
            Vec2: The resulting vector.
        """
        if isinstance(other, Vec2):
            return Vec2(self.x / other.x, self.y / other.y)
        else:
            return Vec2(self.x / other, self.y / other)

    def __neg__(self):
        """
        Negate the vector.

        Returns:
            Vec2: The negated vector.
        """
        return Vec2(-self.x, -self.y)

    def __eq__(self, other):
        """
        Check if two vectors are equal.

        Args:
            other (Vec2): The vector to compare with.

        Returns:
            bool: True if the vectors are equal, False otherwise.
        """
        if not isinstance(other, Vec2):
            return False
        return math.isclose(self.x, other.x) and math.isclose(self.y, other.y)

    def magnitude(self):
        """
        Calculate the magnitude (length) of the vector.

        Returns:
            float: The magnitude of the vector.
        """
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def magnitude_squared(self):
        """
        Calculate the squared magnitude of the vector.

        Returns:
            float: The squared magnitude of the vector.
        """
        return self.x ** 2 + self.y ** 2

    def normalize(self):
        """
        Normalize the vector to a unit vector.

        Returns:
            Vec2: The normalized vector.
        """
        mag = self.magnitude()
        if mag == 0:
            return Vec2(0, 0)
        return Vec2(self.x / mag, self.y / mag)

    def dot(self, other):
        """
        Calculate the dot product of two vectors.

        Args:
            other (Vec2): The other vector.

        Returns:
            float: The dot product.
        """
        return self.x * other.x + self.y * other.y

    def cross(self, other):
        """
        Calculate the cross product of two vectors.

        Args:
            other (Vec2): The other vector.

        Returns:
            float: The cross product (scalar for 2D vectors).
        """
        return self.x * other.y - self.y * other.x

    def distance_to(self, other):
        """
        Calculate the distance between this vector and another vector.

        Args:
            other (Vec2): The other vector.

        Returns:
            float: The distance between the vectors.
        """
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def rotate(self, angle):
        """
        Rotate the vector by a given angle (in radians).

        Args:
            angle (float): The angle to rotate by (in radians).

        Returns:
            Vec2: The rotated vector.
        """
        cos_theta = math.cos(angle)
        sin_theta = math.sin(angle)
        x = self.x * cos_theta - self.y * sin_theta
        y = self.x * sin_theta + self.y * cos_theta
        return Vec2(x, y)

    def to_tuple(self):
        """
        Convert the vector to a tuple.

        Returns:
            tuple: The vector as a tuple (x, y).
        """
        return (self.x, self.y)

    @classmethod
    def from_tuple(cls, tuple_data):
        """
        Create a Vec2 from a tuple.

        Args:
            tuple_data (tuple): A tuple (x, y).

        Returns:
            Vec2: The created vector.
        """
        return cls(tuple_data[0], tuple_data[1])

    @classmethod
    def zero(cls):
        """
        Create a zero vector.

        Returns:
            Vec2: A zero vector.
        """
        return cls(0.0, 0.0)

    @classmethod
    def unit_x(cls):
        """
        Create a unit vector in the x-direction.

        Returns:
            Vec2: A unit vector in the x-direction.
        """
        return cls(1.0, 0.0)

    @classmethod
    def unit_y(cls):
        """
        Create a unit vector in the y-direction.

        Returns:
            Vec2: A unit vector in the y-direction.
        """
        return cls(0.0, 1.0)
