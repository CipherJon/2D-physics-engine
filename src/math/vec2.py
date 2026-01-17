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
        self.x = x
        self.y = y

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
        Multiply a vector by a scalar or another vector (element-wise).

        Args:
            other (Vec2 or float): The scalar or vector to multiply by.

        Returns:
            Vec2: The resulting vector.
        """
        if isinstance(other, Vec2):
            return Vec2(self.x * other.x, self.y * other.y)
        else:
            return Vec2(self.x * other, self.y * other)

    def __rmul__(self, other):
        """
        Multiply a scalar by a vector (reverse multiplication).

        Args:
            other (float): The scalar to multiply by.

        Returns:
            Vec2: The resulting vector.
        """
        return Vec2(other * self.x, other * self.y)

    def __truediv__(self, other):
        """
        Divide a vector by a scalar or another vector (element-wise).

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
        Negate a vector.

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

    def __repr__(self):
        """
        Return a detailed string representation of the vector.

        Returns:
            str: The detailed string representation.
        """
        return f"Vec2(x={self.x}, y={self.y})"

    def __str__(self):
        """
        Return a string representation of the vector.

        Returns:
            str: The string representation.
        """
        return f"Vec2({self.x}, {self.y})"

    def magnitude(self):
        """
        Calculate the magnitude (length) of the vector.

        Returns:
            float: The magnitude of the vector.
        """
        return math.sqrt(self.x**2 + self.y**2)

    def magnitude_squared(self):
        """
        Calculate the squared magnitude of the vector.

        Returns:
            float: The squared magnitude of the vector.
        """
        return self.x**2 + self.y**2

    def normalize(self):
        """
        Normalize the vector to have a magnitude of 1.

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
            float: The cross product.
        """
        return self.x * other.y - self.y * other.x

    @staticmethod
    def cross_scalar(scalar, vec):
        """
        Calculate the cross product of a scalar and a vector in 2D.

        Args:
            scalar (float): The scalar (angular velocity).
            vec (Vec2): The vector (r).

        Returns:
            Vec2: The resulting vector.
        """
        return Vec2(-scalar * vec.y, scalar * vec.x)

    def distance_to(self, other):
        """
        Calculate the distance between two vectors.

        Args:
            other (Vec2): The other vector.

        Returns:
            float: The distance between the vectors.
        """
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def rotate(self, angle):
        """
        Rotate the vector by a given angle.

        Args:
            angle (float): The angle to rotate by, in radians.

        Returns:
            Vec2: The rotated vector.
        """
        cos_theta = math.cos(angle)
        sin_theta = math.sin(angle)
        x = self.x * cos_theta - self.y * sin_theta
        y = self.x * sin_theta + self.y * cos_theta
        # Round to 10 decimal places to avoid floating-point precision issues
        return Vec2(round(x, 10), round(y, 10))

    def project(self, axis):
        """
        Project the vector onto an axis.

        Args:
            axis (Vec2): The axis to project onto.

        Returns:
            float: The projection of the vector onto the axis.
        """
        return self.dot(axis) / axis.magnitude()

    def reflect(self, normal):
        """
        Reflect the vector over a normal.

        Args:
            normal (Vec2): The normal vector.

        Returns:
            Vec2: The reflected vector.
        """
        return self - normal * (2 * self.dot(normal))

    @staticmethod
    def zero():
        """
        Create a zero vector.

        Returns:
            Vec2: The zero vector.
        """
        return Vec2(0, 0)

    @staticmethod
    def one():
        """
        Create a unit vector.

        Returns:
            Vec2: The unit vector.
        """
        return Vec2(1, 1)

    @staticmethod
    def up():
        """
        Create an up vector.

        Returns:
            Vec2: The up vector.
        """
        return Vec2(0, 1)

    @staticmethod
    def down():
        """
        Create a down vector.

        Returns:
            Vec2: The down vector.
        """
        return Vec2(0, -1)

    @staticmethod
    def left():
        """
        Create a left vector.

        Returns:
            Vec2: The left vector.
        """
        return Vec2(-1, 0)

    @staticmethod
    def right():
        """
        Create a right vector.

        Returns:
            Vec2: The right vector.
        """
        return Vec2(1, 0)

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

    @staticmethod
    def unit_x():
        """
        Create a unit vector in the x-direction.

        Returns:
            Vec2: A unit vector in the x-direction.
        """
        return Vec2(1.0, 0.0)

    @staticmethod
    def unit_y():
        """
        Create a unit vector in the y-direction.

        Returns:
            Vec2: A unit vector in the y-direction.
        """
        return Vec2(0.0, 1.0)

    def clamped(self, min_val, max_val):
        """
        Clamp the vector components between min_val and max_val.

        Args:
            min_val (float): The minimum value for clamping.
            max_val (float): The maximum value for clamping.

        Returns:
            Vec2: The clamped vector.
        """
        return Vec2(
            max(min_val, min(max_val, self.x)), max(min_val, min(max_val, self.y))
        )
