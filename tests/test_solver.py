"""
Test cases for the solver module in the physics engine.
"""

import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent.parent))

import pytest

from src.core.body import Body
from src.core.circle import Circle
from src.core.polygon import Polygon
from src.dynamics.world import World
from src.math.vec2 import Vec2


def test_world_initialization():
    """Test that the world initializes correctly."""
    world = World(Vec2(0.0, 10.0))
    assert world is not None


def test_world_step():
    """Test that the world can step through a simulation."""
    world = World(Vec2(0.0, 10.0))

    # Create two bodies for testing
    body1 = Body(shape=Circle(Vec2(0, 0), 1))
    body2 = Body(shape=Circle(Vec2(2, 2), 1))

    # Add bodies to the world
    world.add_body(body1)
    world.add_body(body2)

    # Step the world
    world.step(1.0 / 60.0)

    # Verify that the world stepped without errors
    assert True


def test_world_collision_resolution():
    """Test that the world resolves collisions correctly."""
    world = World(Vec2(0.0, 10.0))

    # Create two overlapping circles
    body1 = Body(shape=Circle(Vec2(0, 0), 1))
    body2 = Body(shape=Circle(Vec2(1.5, 0), 1))

    # Add bodies to the world
    world.add_body(body1)
    world.add_body(body2)

    # Step the world multiple times to allow collision resolution
    for _ in range(10):
        world.step(1.0 / 60.0)

    # Verify that the bodies have moved apart
    pos1 = body1.position
    pos2 = body2.position
    distance = (pos1 - pos2).magnitude()
    assert distance > 1.5  # Bodies should have moved apart


def test_world_constraint_satisfaction():
    """Test that the world satisfies constraints."""
    world = World(Vec2(0.0, 10.0))

    # Create a static ground
    ground = Body(
        shape=Polygon([Vec2(-10, -1), Vec2(10, -1), Vec2(10, 0), Vec2(-10, 0)]),
        is_static=True,
    )

    # Create a dynamic body above the ground
    body = Body(shape=Circle(Vec2(0, 5), 1))

    # Add bodies to the world
    world.add_body(ground)
    world.add_body(body)

    # Step the world multiple times to let the body fall
    for _ in range(60):
        world.step(1.0 / 60.0)

    # Verify that the body has come to rest on the ground
    assert body.position.y <= 1.0  # Radius of the circle is 1.0


def test_world_performance():
    """Test the performance of the world with many bodies."""
    world = World(Vec2(0.0, 10.0))

    # Create many bodies for performance testing
    for i in range(100):
        body = Body(shape=Circle(Vec2(i * 2, 10), 1))
        world.add_body(body)

    # Step the world and measure performance
    import time

    start_time = time.time()
    world.step(1.0 / 60.0)
    end_time = time.time()

    # Verify that the world steps in a reasonable time
    assert (end_time - start_time) < 1.0  # Should take less than 1 second
