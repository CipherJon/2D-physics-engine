"""
Utility functions for math operations.

This module provides utility functions for common math operations in the physics engine.
"""

import math

from ..math.vec2 import Vec2


def clamp(value, min_value, max_value):
    """
    Clamp a value between a minimum and maximum value.

    Args:
        value (float): The value to clamp.
        min_value (float): The minimum value.
        max_value (float): The maximum value.

    Returns:
        float: The clamped value.
    """
    return max(min_value, min(value, max_value))


def lerp(a, b, t):
    """
    Linear interpolation between two values.

    Args:
        a (float): The first value.
        b (float): The second value.
        t (float): The interpolation factor.

    Returns:
        float: The interpolated value.
    """
    return a + (b - a) * t


def lerp_vec2(a, b, t):
    """
    Linear interpolation between two vectors.

    Args:
        a (Vec2): The first vector.
        b (Vec2): The second vector.
        t (float): The interpolation factor.

    Returns:
        Vec2: The interpolated vector.
    """
    return Vec2(lerp(a.x, b.x, t), lerp(a.y, b.y, t))


def distance_squared(a, b):
    """
    Calculate the squared distance between two points.

    Args:
        a (Vec2): The first point.
        b (Vec2): The second point.

    Returns:
        float: The squared distance between the two points.
    """
    dx = a.x - b.x
    dy = a.y - b.y
    return dx * dx + dy * dy


def distance(a, b):
    """
    Calculate the distance between two points.

    Args:
        a (Vec2): The first point.
        b (Vec2): The second point.

    Returns:
        float: The distance between the two points.
    """
    return math.sqrt(distance_squared(a, b))


def normalize_angle(angle):
    """
    Normalize an angle to the range [-π, π].

    Args:
        angle (float): The angle to normalize.

    Returns:
        float: The normalized angle.
    """
    while angle > math.pi:
        angle -= 2 * math.pi
    while angle < -math.pi:
        angle += 2 * math.pi
    return angle


def cross(a, b):
    """
    Calculate the cross product of two vectors.

    Args:
        a (Vec2): The first vector.
        b (Vec2): The second vector.

    Returns:
        float: The cross product of the two vectors.
    """
    return a.x * b.y - a.y * b.x


def dot(a, b):
    """
    Calculate the dot product of two vectors.

    Args:
        a (Vec2): The first vector.
        b (Vec2): The second vector.

    Returns:
        float: The dot product of the two vectors.
    """
    return a.x * b.x + a.y * b.y


def project(a, b):
    """
    Project vector a onto vector b.

    Args:
        a (Vec2): The vector to project.
        b (Vec2): The vector to project onto.

    Returns:
        Vec2: The projected vector.
    """
    dot_product = dot(a, b)
    b_length_squared = dot(b, b)
    if b_length_squared == 0:
        return Vec2(0.0, 0.0)
    return b * (dot_product / b_length_squared)


def reflect(vector, normal):
    """
    Reflect a vector over a normal.

    Args:
        vector (Vec2): The vector to reflect.
        normal (Vec2): The normal vector.

    Returns:
        Vec2: The reflected vector.
    """
    dot_product = dot(vector, normal)
    return vector - 2 * dot_product * normal
