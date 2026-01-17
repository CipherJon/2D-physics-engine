"""
Debug script to check normal direction in collision detection.
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

def test_normal_direction():
    """Test to verify the normal direction is correct."""
    # Create a world with gravity
    world = World(Vec2(0.0, -10.0))  # Gravity downward

    # Create a static ground at y=-1 to y=0
    ground = Body(
        shape=Polygon([Vec2(-10, -1), Vec2(10, -1), Vec2(10, 0), Vec2(-10, 0)]),
        is_static=True,
    )
    world.add_body(ground)

    # Create a dynamic body above the ground at y=1
    body = Body(shape=Circle(Vec2(0, 1), 1))
    body.position = Vec2(0, 1)  # Set position explicitly
    world.add_body(body)

    print(f"Initial body position: {body.position}")
    print(f"Initial ground position: {ground.position}")

    # Step the simulation once to trigger collision detection
    world.step(1.0 / 60.0)

    print(f"After step body position: {body.position}")
    print(f"After step body velocity: {body.velocity}")

    # Force a collision detection to see the normal
    collision_pairs = [(ground, body)]
    for body1, body2 in collision_pairs:
        manifold = world.narrowphase.get_collision_manifold(body1, body2)
        if manifold:
            print(f"Collision detected!")
            print(f"Normal: {manifold.normal}")
            print(f"Depth: {manifold.depth}")
            print(f"Contact points: {manifold.points}")

            # Check if normal is pointing in the right direction
            # For ground (at y=0) and body (at y=1), normal should be (0, 1) or close to it
            if manifold.normal.y > 0:
                print("✓ Normal is pointing upward (correct)")
            else:
                print("✗ Normal is pointing downward (incorrect)")
        else:
            print("No collision detected")

if __name__ == "__main__":
    test_normal_direction()
