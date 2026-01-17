"""
Main module for the physics engine.

This module provides the main functionality for the physics engine.
"""

from .constraints.distance import DistanceJoint
from .constraints.gear import GearJoint
from .constraints.joint import Joint
from .constraints.mouse import MouseJoint
from .constraints.prismatic import PrismaticJoint
from .constraints.pulley import PulleyJoint
from .constraints.revolute import RevoluteJoint
from .constraints.weld import WeldJoint
from .core.body import Body
from .core.circle import Circle
from .core.edge import Edge
from .core.polygon import Polygon
from .core.shape import Shape

# from .dynamics.world import World
from .version import __author__, __copyright__, __license__, __version__

__all__ = [
    "__version__",
    "__author__",
    "__license__",
    "__copyright__",
    "Body",
    "Shape",
    "Circle",
    "Polygon",
    "Edge",
    # "World",
    "Joint",
    "DistanceJoint",
    "RevoluteJoint",
    "PrismaticJoint",
    "PulleyJoint",
    "GearJoint",
    "WeldJoint",
    "MouseJoint",
]
