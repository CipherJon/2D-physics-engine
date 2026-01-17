"""
Focused test for collision response.
"""

import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent))

from src.core.body import Body
from src.core.circle import Circle
from src.core.polygon import Polygon
from src.dynamics.world import World
from src.math.vec2 import Vec2


def test_simple_collision_response():
    """Test collision response between a circle and a static ground."""
    world = World(Vec2(0.0, 0.0))  # No gravity for this test

    # Create a static ground
    ground = Body(
        shape=Polygon([Vec2(-10, -1), Vec2(10, -1), Vec2(10, 0), Vec2(-10, 0)]),
        is_static=True,
        restitution=0.0,
    )
    world.add_body(ground)

    # Create a dynamic circle touching the ground
    circle = Body(
        shape=Circle(
            Vec2(0, 1), 1
        ),  # Center at (0, 1), radius 1 - touches ground at y=0
        mass=1.0,
        position=Vec2(0, 1),  # Body position at (0, 1)
        velocity=Vec2(0, -1),  # Moving downward at 1 m/s
        restitution=0.0,
    )
    world.add_body(circle)

    print(f"Initial circle position: {circle.position}")
    print(f"Initial circle velocity: {circle.velocity}")
    print(f"Ground position: {ground.position}")

    # Debug AABBs
    circle_aabb = circle.get_aabb()
    ground_aabb = ground.get_aabb()
    print(f"Circle AABB: {circle_aabb}")
    print(f"Ground AABB: {ground_aabb}")
    print(f"AABBs overlap: {circle_aabb.overlaps(ground_aabb)}")

    # Step the simulation - should collide and stop
    for i in range(10):
        print(f"\n--- Step {i} ---")
        print(f"Before step - circle pos: {circle.position}, vel: {circle.velocity}")

        world.step(1.0 / 60.0)

        print(f"After step - circle pos: {circle.position}, vel: {circle.velocity}")

        # Check if velocity has been constrained
        if circle.velocity.y >= -0.1:  # Should be close to zero or positive (bouncing)
            print("✓ Collision response working!")
            return True

    print("✗ Collision response not working - circle still falling")
    return False


if __name__ == "__main__":
    test_simple_collision_response()
