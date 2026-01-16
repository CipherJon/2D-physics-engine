import math
import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from src.math.vec2 import Vec2


def test_vec2_initialization():
    """Test the initialization of Vec2."""
    v1 = Vec2()
    assert v1.x == 0.0
    assert v1.y == 0.0

    v2 = Vec2(3.0, 4.0)
    assert v2.x == 3.0
    assert v2.y == 4.0


def test_vec2_string_representation():
    """Test the string representation of Vec2."""
    v = Vec2(1.0, 2.0)
    assert str(v) == "Vec2(1.0, 2.0)"
    assert repr(v) == "Vec2(x=1.0, y=2.0)"


def test_vec2_addition():
    """Test the addition of Vec2."""
    v1 = Vec2(1.0, 2.0)
    v2 = Vec2(3.0, 4.0)
    result = v1 + v2
    assert result.x == 4.0
    assert result.y == 6.0

    # Test addition with a scalar
    result_scalar = v1 + 5.0
    assert result_scalar.x == 6.0
    assert result_scalar.y == 7.0


def test_vec2_subtraction():
    """Test the subtraction of Vec2."""
    v1 = Vec2(5.0, 6.0)
    v2 = Vec2(1.0, 2.0)
    result = v1 - v2
    assert result.x == 4.0
    assert result.y == 4.0

    # Test subtraction with a scalar
    result_scalar = v1 - 3.0
    assert result_scalar.x == 2.0
    assert result_scalar.y == 3.0


def test_vec2_multiplication():
    """Test the multiplication of Vec2."""
    v1 = Vec2(2.0, 3.0)
    v2 = Vec2(4.0, 5.0)
    result = v1 * v2
    assert result.x == 8.0
    assert result.y == 15.0

    # Test multiplication with a scalar
    result_scalar = v1 * 3.0
    assert result_scalar.x == 6.0
    assert result_scalar.y == 9.0


def test_vec2_division():
    """Test the division of Vec2."""
    v1 = Vec2(10.0, 20.0)
    v2 = Vec2(2.0, 4.0)
    result = v1 / v2
    assert result.x == 5.0
    assert result.y == 5.0

    # Test division with a scalar
    result_scalar = v1 / 2.0
    assert result_scalar.x == 5.0
    assert result_scalar.y == 10.0


def test_vec2_negation():
    """Test the negation of Vec2."""
    v = Vec2(3.0, 4.0)
    result = -v
    assert result.x == -3.0
    assert result.y == -4.0


def test_vec2_equality():
    """Test the equality of Vec2."""
    v1 = Vec2(1.0, 2.0)
    v2 = Vec2(1.0, 2.0)
    v3 = Vec2(3.0, 4.0)
    assert v1 == v2
    assert not (v1 == v3)


def test_vec2_magnitude():
    """Test the magnitude of Vec2."""
    v = Vec2(3.0, 4.0)
    assert v.magnitude() == 5.0


def test_vec2_magnitude_squared():
    """Test the squared magnitude of Vec2."""
    v = Vec2(3.0, 4.0)
    assert v.magnitude_squared() == 25.0


def test_vec2_normalize():
    """Test the normalization of Vec2."""
    v = Vec2(3.0, 4.0)
    normalized = v.normalize()
    assert math.isclose(normalized.magnitude(), 1.0)


def test_vec2_dot_product():
    """Test the dot product of Vec2."""
    v1 = Vec2(1.0, 2.0)
    v2 = Vec2(3.0, 4.0)
    assert v1.dot(v2) == 11.0


def test_vec2_cross_product():
    """Test the cross product of Vec2."""
    v1 = Vec2(1.0, 2.0)
    v2 = Vec2(3.0, 4.0)
    assert v1.cross(v2) == -2.0


def test_vec2_distance_to():
    """Test the distance between two Vec2."""
    v1 = Vec2(1.0, 2.0)
    v2 = Vec2(4.0, 6.0)
    assert v1.distance_to(v2) == 5.0


def test_vec2_rotate():
    """Test the rotation of Vec2."""
    v = Vec2(1.0, 0.0)
    rotated = v.rotate(math.pi / 2)
    assert math.isclose(rotated.x, 0.0)
    assert math.isclose(rotated.y, 1.0)


def test_vec2_to_tuple():
    """Test the conversion of Vec2 to a tuple."""
    v = Vec2(1.0, 2.0)
    assert v.to_tuple() == (1.0, 2.0)


def test_vec2_from_tuple():
    """Test the creation of Vec2 from a tuple."""
    v = Vec2.from_tuple((3.0, 4.0))
    assert v.x == 3.0
    assert v.y == 4.0


def test_vec2_zero():
    """Test the creation of a zero Vec2."""
    v = Vec2.zero()
    assert v.x == 0.0
    assert v.y == 0.0


def test_vec2_unit_x():
    """Test the creation of a unit Vec2 in the x-direction."""
    v = Vec2.unit_x()
    assert v.x == 1.0
    assert v.y == 0.0


def test_vec2_unit_y():
    """Test the creation of a unit Vec2 in the y-direction."""
    v = Vec2.unit_y()
    assert v.x == 0.0
    assert v.y == 1.0
