"""
Test cases for the stability of the physics engine.
"""

import math
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


def test_energy_conservation():
    """Test that the total energy of the system is conserved."""
    world = World(Vec2(0.0, 0.0))  # No gravity for energy conservation

    # Create a static ground
    ground = Body(
        shape=Polygon([Vec2(-10, -1), Vec2(10, -1), Vec2(10, 0), Vec2(-10, 0)]),
        is_static=True,
    )
    world.add_body(ground)

    # Create a dynamic body
    body = Body(shape=Circle(Vec2(0, 5), 1))
    body.velocity = Vec2(10, 0)  # Initial velocity
    world.add_body(body)

    # Calculate initial energy
    initial_kinetic_energy = 0.5 * body.mass * body.velocity.magnitude_squared()
    initial_potential_energy = 0.0  # No gravity
    initial_total_energy = initial_kinetic_energy + initial_potential_energy

    # Step the simulation
    for _ in range(60):
        world.step(1.0 / 60.0)

    # Calculate final energy
    final_kinetic_energy = 0.5 * body.mass * body.velocity.magnitude_squared()
    final_potential_energy = 0.0  # No gravity
    final_total_energy = final_kinetic_energy + final_potential_energy

    # Verify that energy is conserved (within a small tolerance)
    assert abs(final_total_energy - initial_total_energy) < 0.1


def test_numerical_stability():
    """Test that the simulation remains numerically stable over time."""
    world = World(Vec2(0.0, 10.0))  # Gravity

    # Create a static ground
    ground = Body(
        shape=Polygon([Vec2(-10, -1), Vec2(10, -1), Vec2(10, 0), Vec2(-10, 0)]),
        is_static=True,
    )
    world.add_body(ground)

    # Create a dynamic body
    body = Body(shape=Circle(Vec2(0, 5), 1))
    world.add_body(body)

    # Step the simulation for a long time
    for _ in range(1000):
        world.step(1.0 / 60.0)

    # Verify that the body's position and velocity are finite
    assert math.isfinite(body.position.x) and math.isfinite(body.position.y)
    assert math.isfinite(body.velocity.x) and math.isfinite(body.velocity.y)


def test_long_term_stability():
    """Test that the simulation remains stable over a long period."""
    world = World(Vec2(0.0, 10.0))  # Gravity

    # Create a static ground
    ground = Body(
        shape=Polygon([Vec2(-10, -1), Vec2(10, -1), Vec2(10, 0), Vec2(-10, 0)]),
        is_static=True,
    )
    world.add_body(ground)

    # Create multiple dynamic bodies
    for i in range(10):
        body = Body(shape=Circle(Vec2(i * 2, 10), 1))
        world.add_body(body)

    # Step the simulation for a long time
    for _ in range(1000):
        world.step(1.0 / 60.0)

    # Verify that all bodies' positions and velocities are finite
    for body in world.bodies:
        if not body.is_static:
            assert math.isfinite(body.position.x) and math.isfinite(body.position.y)
            assert math.isfinite(body.velocity.x) and math.isfinite(body.velocity.y)


def test_resting_contact_stability():
    """Test that bodies at rest remain stable."""
    world = World(Vec2(0.0, 1.0))  # Reduced gravity for stability testing

    # Create a static ground
    ground = Body(
        shape=Polygon([Vec2(-10, -1), Vec2(10, -1), Vec2(10, 0), Vec2(-10, 0)]),
        is_static=True,
        restitution=0.0,  # Force no restitution for stability
    )
    world.add_body(ground)

    # Create a dynamic body resting on the ground
    body = Body(
        shape=Circle(Vec2(0, 1), 1),
        position=Vec2(0, 1),  # Explicit position to match circle center
        restitution=0.0,  # Force no restitution
    )
    body.velocity = Vec2(0, 0)  # No initial velocity
    world.add_body(body)

    # Step the simulation
    for _ in range(60):
        world.step(1.0 / 60.0)

    # Verify that the body remains at rest
    assert body.velocity.magnitude() < 0.1  # Should be close to zero


def test_stacking_stability():
    """Test that stacked bodies remain stable."""
    world = World(Vec2(0.0, 10.0))  # Gravity

    # Create a static ground
    ground = Body(
        shape=Polygon([Vec2(-10, -1), Vec2(10, -1), Vec2(10, 0), Vec2(-10, 0)]),
        is_static=True,
        restitution=0.0,  # Force no restitution for stability
    )
    world.add_body(ground)

    # Create stacked bodies
    for i in range(5):
        body = Body(
            shape=Polygon(
                [
                    Vec2(-1, i * 2),
                    Vec2(1, i * 2),
                    Vec2(1, i * 2 + 2),
                    Vec2(-1, i * 2 + 2),
                ]
            ),
            restitution=0.0,  # Force no restitution for stability
        )
        world.add_body(body)

    # Step the simulation
    for _ in range(60):
        world.step(1.0 / 60.0)

    # Verify that the bodies remain stable (no excessive movement)
    for body in world.bodies:
        if not body.is_static:
            assert body.velocity.magnitude() < 1.0  # Should be small
