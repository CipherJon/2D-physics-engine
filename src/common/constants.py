"""
Constants for the physics engine.

This module provides commonly used constants in the physics engine.
"""

# Mathematical constants
PI = 3.141592653589793
TAU = 6.283185307179586
EPSILON = 1e-6

# Physics constants
GRAVITY = 9.81
GRAVITY_VEC = (0.0, -GRAVITY)

# Simulation constants
DEFAULT_TIME_STEP = 1.0 / 60.0
DEFAULT_VELOCITY_ITERATIONS = 50  # Increased from 8 to 50
DEFAULT_POSITION_ITERATIONS = 20  # Increased from 3 to 20

# Collision constants
DEFAULT_RESTITUTION = 0.5
DEFAULT_FRICTION = 0.5

# Baumgarte stabilization constants (aggressive tuning)
BAUMGARTE = 0.4  # Increased from 0.1 to 0.4
POSITION_SLOP = 0.02  # Allow small penetration before strong correction

# Friction constants
STATIC_FRICTION = 0.6
DYNAMIC_FRICTION = 0.4
