"""
Simple test to verify basic physics without collision.
"""

import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent))

from src.core.body import Body
from src.core.circle import Circle
from src.dynamics.world import World
from src.math.vec2 import Vec2


def test_basic_gravity():
    """Test that gravity works without any collision."""
    world = World(Vec2(0.0, 10.0))  # Gravity

    # Create a dynamic body in air
    body = Body(shape=Circle(Vec2(0, 10), 1))
    body.velocity = Vec2(0, 0)  # No initial velocity
    world.add_body(body)

    initial_position = body.position.y
    print(f"Initial position: {initial_position}")

    # Step the simulation for 1 second (60 frames)
    for i in range(60):
        world.step(1.0 / 60.0)
        print(
            f"Step {i}: position={body.position.y:.2f}, velocity={body.velocity.y:.2f}"
        )

    # After 1 second with gravity=10, expected position:
    # y = initial_y + 0.5 * g * t^2 = 10 + 0.5 * 10 * 1^2 = 15
    # Expected velocity: v = g * t = 10 * 1 = 10
    expected_position = 10 + 0.5 * 10 * (1.0) ** 2  # 15.0
    expected_velocity = 10 * 1.0  # 10.0

    print(f"Final position: {body.position.y:.2f} (expected: {expected_position:.2f})")
    print(f"Final velocity: {body.velocity.y:.2f} (expected: {expected_velocity:.2f})")

    # Check if physics is working (should be close to expected values)
    assert abs(body.position.y - expected_position) < 1.0, (
        f"Position mismatch: {body.position.y} vs {expected_position}"
    )
    assert abs(body.velocity.y - expected_velocity) < 1.0, (
        f"Velocity mismatch: {body.velocity.y} vs {expected_velocity}"
    )
    print("✓ Basic gravity test passed!")


if __name__ == "__main__":
    test_basic_gravity()
