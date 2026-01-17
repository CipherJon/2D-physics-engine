import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent))

from src.core.body import Body
from src.core.circle import Circle
from src.math.vec2 import Vec2


def test_restitution_attribute():
    """Test that Body has restitution attribute."""
    body = Body(shape=Circle(Vec2(0, 0), 1))
    print(f"Body has restitution: {hasattr(body, 'restitution')}")
    print(f"Body restitution value: {body.restitution}")

    # Test that we can access it
    try:
        e = body.restitution
        print(f"Successfully accessed restitution: {e}")
        return True
    except AttributeError as ex:
        print(f"AttributeError: {ex}")
        return False


if __name__ == "__main__":
    success = test_restitution_attribute()
    if success:
        print("✓ Restitution attribute test PASSED")
    else:
        print("✗ Restitution attribute test FAILED")
