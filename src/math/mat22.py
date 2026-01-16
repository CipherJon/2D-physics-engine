import math


class Mat22:
    """
    A 2x2 matrix class for handling matrix operations in a physics engine.
    """

    def __init__(self, cols=None):
        """
        Initialize a 2x2 matrix.

        Args:
            cols (list of lists or list of Vec2): The columns of the matrix.
        """
        if cols is None:
            self.cols = [[1.0, 0.0], [0.0, 1.0]]  # Identity matrix by default
        else:
            self.cols = [
                [float(cols[0][0]), float(cols[0][1])],
                [float(cols[1][0]), float(cols[1][1])],
            ]

    def __str__(self):
        """
        Return a string representation of the matrix.
        """
        return f"Mat22([{self.cols[0][0]}, {self.cols[0][1]}], [{self.cols[1][0]}, {self.cols[1][1]}])"

    def __repr__(self):
        """
        Return a detailed string representation of the matrix.
        """
        return f"Mat22(cols=[[{self.cols[0][0]}, {self.cols[0][1]}], [{self.cols[1][0]}, {self.cols[1][1]}]])"

    def __add__(self, other):
        """
        Add two matrices.

        Args:
            other (Mat22): The matrix to add.

        Returns:
            Mat22: The resulting matrix.
        """
        return Mat22(
            [
                [
                    self.cols[0][0] + other.cols[0][0],
                    self.cols[0][1] + other.cols[0][1],
                ],
                [
                    self.cols[1][0] + other.cols[1][0],
                    self.cols[1][1] + other.cols[1][1],
                ],
            ]
        )

    def __sub__(self, other):
        """
        Subtract two matrices.

        Args:
            other (Mat22): The matrix to subtract.

        Returns:
            Mat22: The resulting matrix.
        """
        return Mat22(
            [
                [
                    self.cols[0][0] - other.cols[0][0],
                    self.cols[0][1] - other.cols[0][1],
                ],
                [
                    self.cols[1][0] - other.cols[1][0],
                    self.cols[1][1] - other.cols[1][1],
                ],
            ]
        )

    def __mul__(self, other):
        """
        Multiply the matrix by another matrix or a scalar.

        Args:
            other (Mat22 or float): The matrix or scalar to multiply by.

        Returns:
            Mat22: The resulting matrix.
        """
        if isinstance(other, Mat22):
            # Matrix multiplication
            return Mat22(
                [
                    [
                        self.cols[0][0] * other.cols[0][0]
                        + self.cols[0][1] * other.cols[1][0],
                        self.cols[0][0] * other.cols[0][1]
                        + self.cols[0][1] * other.cols[1][1],
                    ],
                    [
                        self.cols[1][0] * other.cols[0][0]
                        + self.cols[1][1] * other.cols[1][0],
                        self.cols[1][0] * other.cols[0][1]
                        + self.cols[1][1] * other.cols[1][1],
                    ],
                ]
            )
        else:
            # Scalar multiplication
            return Mat22(
                [
                    [self.cols[0][0] * other, self.cols[0][1] * other],
                    [self.cols[1][0] * other, self.cols[1][1] * other],
                ]
            )

    def __eq__(self, other):
        """
        Check if two matrices are equal.

        Args:
            other (Mat22): The matrix to compare with.

        Returns:
            bool: True if the matrices are equal, False otherwise.
        """
        if not isinstance(other, Mat22):
            return False
        return (
            math.isclose(self.cols[0][0], other.cols[0][0])
            and math.isclose(self.cols[0][1], other.cols[0][1])
            and math.isclose(self.cols[1][0], other.cols[1][0])
            and math.isclose(self.cols[1][1], other.cols[1][1])
        )

    def determinant(self):
        """
        Calculate the determinant of the matrix.

        Returns:
            float: The determinant of the matrix.
        """
        return self.cols[0][0] * self.cols[1][1] - self.cols[0][1] * self.cols[1][0]

    def inverse(self):
        """
        Calculate the inverse of the matrix.

        Returns:
            Mat22: The inverse of the matrix.
        """
        det = self.determinant()
        if det == 0:
            raise ValueError("Matrix is not invertible (determinant is zero).")
        inv_det = 1.0 / det
        return Mat22(
            [
                [self.cols[1][1] * inv_det, -self.cols[0][1] * inv_det],
                [-self.cols[1][0] * inv_det, self.cols[0][0] * inv_det],
            ]
        )

    def transpose(self):
        """
        Calculate the transpose of the matrix.

        Returns:
            Mat22: The transpose of the matrix.
        """
        return Mat22(
            [[self.cols[0][0], self.cols[1][0]], [self.cols[0][1], self.cols[1][1]]]
        )

    def solve(self, b):
        """
        Solve the linear system Ax = b for x.

        Args:
            b (Vec2): The right-hand side vector.

        Returns:
            Vec2: The solution vector x.
        """
        from .vec2 import Vec2

        det = self.determinant()
        if det == 0:
            raise ValueError("Matrix is not invertible (determinant is zero).")
        inv_det = 1.0 / det
        x = Vec2(
            (self.cols[1][1] * b.x - self.cols[0][1] * b.y) * inv_det,
            (-self.cols[1][0] * b.x + self.cols[0][0] * b.y) * inv_det,
        )
        return x

    @classmethod
    def from_angle(cls, angle):
        """
        Create a rotation matrix from an angle (in radians).

        Args:
            angle (float): The angle to rotate by (in radians).

        Returns:
            Mat22: The rotation matrix.
        """
        cos_theta = math.cos(angle)
        sin_theta = math.sin(angle)
        return cls([[cos_theta, -sin_theta], [sin_theta, cos_theta]])

    @classmethod
    def identity(cls):
        """
        Create an identity matrix.

        Returns:
            Mat22: The identity matrix.
        """
        return cls()

    @classmethod
    def zero(cls):
        """
        Create a zero matrix.

        Returns:
            Mat22: The zero matrix.
        """
        return cls([[0.0, 0.0], [0.0, 0.0]])
