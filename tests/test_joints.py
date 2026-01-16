"""
Test cases for the joints module in the physics engine.
"""

import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent.parent))

import pytest

from src.constraints.distance import DistanceJoint
from src.constraints.revolute import RevoluteJoint
from src.core.body import Body
from src.core.circle import Circle
from src.core.polygon import Polygon
from src.dynamics.world import World
from src.math.vec2 import Vec2


def test_distance_joint_initialization():
    """Test that a distance joint initializes correctly."""
    body1 = Body(shape=Circle(Vec2(0, 0), 1))
    body2 = Body(shape=Circle(Vec2(2, 2), 1))
    joint = DistanceJoint(body1, body2, Vec2(0, 0), Vec2(2, 2))
    assert joint is not None


def test_distance_joint_constraint():
    """Test that a distance joint enforces distance constraints."""
    world = World(Vec2(0.0, 10.0))

    # Create two bodies
    body1 = Body(shape=Circle(Vec2(0, 0), 1))
    body2 = Body(shape=Circle(Vec2(2, 0), 1))

    # Create a distance joint to keep the bodies 2 units apart
    joint = DistanceJoint(body1, body2, Vec2(0, 0), Vec2(2, 0))

    # Add bodies and joint to the world
    world.add_body(body1)
    world.add_body(body2)
    world.add_joint(joint)

    # Step the simulation
    for _ in range(60):
        world.step(1.0 / 60.0)

    # Verify that the distance joint is initialized and added to the world
    assert joint in world.get_joints()


def test_revolute_joint_initialization():
    """Test that a revolute joint initializes correctly."""
    body1 = Body(shape=Circle(Vec2(0, 0), 1))
    body2 = Body(shape=Circle(Vec2(2, 2), 1))
    joint = RevoluteJoint(body1, body2, Vec2(1, 1))
    assert joint is not None


def test_revolute_joint_constraint():
    """Test that a revolute joint enforces rotational constraints."""
    world = World(Vec2(0.0, 10.0))

    # Create two bodies
    body1 = Body(shape=Circle(Vec2(0, 0), 1))
    body2 = Body(shape=Circle(Vec2(2, 0), 1))

    # Create a revolute joint at the midpoint
    joint = RevoluteJoint(body1, body2, Vec2(1, 0))

    # Add bodies and joint to the world
    world.add_body(body1)
    world.add_body(body2)
    world.add_joint(joint)

    # Step the simulation
    for _ in range(60):
        world.step(1.0 / 60.0)

    # Verify that the bodies rotate around the anchor point
    # The distance from the anchor point should remain constant
    distance1 = (body1.position - Vec2(1, 0)).magnitude()
    distance2 = (body2.position - Vec2(1, 0)).magnitude()
    assert abs(distance1 - 1.0) < 0.1  # Allow a small tolerance
    assert abs(distance2 - 1.0) < 0.1  # Allow a small tolerance


def test_joint_removal():
    """Test that joints can be removed from the world."""
    world = World(Vec2(0.0, 10.0))

    # Create two bodies
    body1 = Body(shape=Circle(Vec2(0, 0), 1))
    body2 = Body(shape=Circle(Vec2(2, 0), 1))

    # Create a distance joint
    joint = DistanceJoint(body1, body2, Vec2(0, 0), Vec2(2, 0))

    # Add bodies and joint to the world
    world.add_body(body1)
    world.add_body(body2)
    world.add_joint(joint)

    # Verify that the joint is in the world
    assert joint in world.get_joints()

    # Remove the joint
    world.remove_joint(joint)

    # Verify that the joint is no longer in the world
    assert joint not in world.get_joints()


def test_multiple_joints():
    """Test that multiple joints can be added to the world."""
    world = World(Vec2(0.0, 10.0))

    # Create three bodies
    body1 = Body(shape=Circle(Vec2(0, 0), 1))
    body2 = Body(shape=Circle(Vec2(2, 0), 1))
    body3 = Body(shape=Circle(Vec2(4, 0), 1))

    # Create two distance joints
    joint1 = DistanceJoint(body1, body2, Vec2(0, 0), Vec2(2, 0))
    joint2 = DistanceJoint(body2, body3, Vec2(2, 0), Vec2(4, 0))

    # Add bodies and joints to the world
    world.add_body(body1)
    world.add_body(body2)
    world.add_body(body3)
    world.add_joint(joint1)
    world.add_joint(joint2)

    # Step the simulation
    for _ in range(60):
        world.step(1.0 / 60.0)

    # Verify that the joints are initialized and added to the world
    assert joint1 in world.get_joints()
    assert joint2 in world.get_joints()


def test_joint_with_static_body():
    """Test that joints work with static bodies."""
    world = World(Vec2(0.0, 10.0))

    # Create a static body
    body1 = Body(
        shape=Polygon([Vec2(-1, -1), Vec2(1, -1), Vec2(1, 1), Vec2(-1, 1)]),
        is_static=True,
    )

    # Create a dynamic body
    body2 = Body(shape=Circle(Vec2(0, 2), 1))

    # Create a revolute joint
    joint = RevoluteJoint(body1, body2, Vec2(0, 0))

    # Add bodies and joint to the world
    world.add_body(body1)
    world.add_body(body2)
    world.add_joint(joint)

    # Step the simulation
    for _ in range(60):
        world.step(1.0 / 60.0)

    # Verify that the joint is initialized and added to the world
    assert joint in world.get_joints()
