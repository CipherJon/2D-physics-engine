"""
Integrator class for numerical integration.

This module provides functionality for numerical integration in the physics engine.
"""

from ..math.vec2 import Vec2


class Integrator:
    """
    A class to perform numerical integration for the physics engine.

    Attributes:
        gravity (Vec2): The gravity vector.
        damping (float): The damping factor.
    """

    def __init__(self, gravity=Vec2(0.0, -9.81), damping=0.99):
        """
        Initialize a new Integrator.

        Args:
            gravity (Vec2): The gravity vector.
            damping (float): The damping factor.
        """
        self.gravity = gravity
        self.damping = damping

    def integrate_velocity(self, body, time_step):
        """
        Integrate the velocity of a body.

        Args:
            body: The body to integrate.
            time_step (float): The time step for the integration.
        """
        body.velocity += (self.gravity + body.inv_mass * body.force) * time_step
        body.velocity *= self.damping
        body.angular_velocity += body.inv_inertia * body.torque * time_step
        body.angular_velocity *= self.damping

    def integrate_position(self, body, time_step):
        """
        Integrate the position of a body.

        Args:
            body: The body to integrate.
            time_step (float): The time step for the integration.
        """
        body.position += body.velocity * time_step
        body.rotation += body.angular_velocity * time_step

    def integrate(self, body, time_step):
        """
        Integrate the velocity and position of a body.

        Args:
            body: The body to integrate.
            time_step (float): The time step for the integration.
        """
        self.integrate_velocity(body, time_step)
        self.integrate_position(body, time_step)
