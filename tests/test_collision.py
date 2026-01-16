import sys

sys.path.insert(0, "/media/cipherjon/HDD/Repo/physics-engine/src")

from src.collision.sat import SAT
from src.core.circle import Circle
from src.core.polygon import Polygon
from src.math.vec2 import Vec2


def test_collision_detection():
    """Test collision detection between two rectangles."""
    rect1 = Polygon([Vec2(0, 0), Vec2(2, 0), Vec2(2, 2), Vec2(0, 2)])
    rect2 = Polygon([Vec2(1, 1), Vec2(3, 1), Vec2(3, 3), Vec2(1, 3)])
    assert SAT.detect_collision(rect1, rect2) == True


def test_no_collision():
    """Test no collision between two rectangles."""
    rect1 = Polygon([Vec2(0, 0), Vec2(1, 0), Vec2(1, 1), Vec2(0, 1)])
    rect2 = Polygon([Vec2(2, 2), Vec2(3, 2), Vec2(3, 3), Vec2(2, 3)])
    assert SAT.detect_collision(rect1, rect2) == False


def test_circle_collision():
    """Test collision detection between two circles."""
    circle1 = Circle(Vec2(0, 0), 1)
    circle2 = Circle(Vec2(1, 1), 1)
    assert SAT.detect_collision(circle1, circle2) == True


def test_no_circle_collision():
    """Test no collision between two circles."""
    circle1 = Circle(Vec2(0, 0), 1)
    circle2 = Circle(Vec2(3, 3), 1)
    assert SAT.detect_collision(circle1, circle2) == False


def test_separating_axis_theorem():
    """Test the Separating Axis Theorem (SAT) for collision detection."""
    rect1 = Polygon([Vec2(0, 0), Vec2(2, 0), Vec2(2, 2), Vec2(0, 2)])
    rect2 = Polygon([Vec2(1, 1), Vec2(3, 1), Vec2(3, 3), Vec2(1, 3)])
    axes = SAT._find_axes(rect1.get_vertices())
    assert len(axes) == 4  # A square has 4 edges, hence 4 axes
