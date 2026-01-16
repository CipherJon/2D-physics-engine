import math
from typing import Optional

from ..core.shape import Shape
from ..math.transform import Transform
from ..math.vec2 import Vec2


class Body:
    """
    A class to represent a physics body in a physics engine.
    """

    def __init__(
        self,
        shape: Shape,
        mass: float = 1.0,
        position: Vec2 = Vec2.zero(),
        velocity: Vec2 = Vec2.zero(),
        angular_velocity: float = 0.0,
        orientation: float = 0.0,
        is_static: bool = False,
    ) -> None:
        """
        Initialize a physics body with a shape, mass, position, velocity, and angular velocity.

        Args:
            shape (Shape): The shape of the body.
            mass (float): The mass of the body.
            position (Vec2): The position of the body.
            velocity (Vec2): The velocity of the body.
            angular_velocity (float): The angular velocity of the body.
            is_static (bool): Whether the body is static (immovable).
        """
        self.shape = shape
        self.mass = float(mass)
        self.position = position
        self.velocity = velocity
        self.angular_velocity = float(angular_velocity)
        self.orientation = float(orientation)
        self.is_static = bool(is_static)

        # Calculate derived properties
        self.inverse_mass = 1.0 / self.mass if not self.is_static else 0.0
        self.inertia = (
            self.shape.get_inertia(self.mass) if not self.is_static else float("inf")
        )
        self.inverse_inertia = 1.0 / self.inertia if not self.is_static else 0.0

        # Initialize forces and torques
        self.force = Vec2.zero()
        self.torque = 0.0

        # Initialize transformation
        self.transform = Transform(position, 0.0)

    def __str__(self) -> str:
        """
        Return a string representation of the body.
        """
        return f"Body(shape={self.shape}, mass={self.mass}, position={self.position}, velocity={self.velocity}, angular_velocity={self.angular_velocity})"

    def __repr__(self) -> str:
        """
        Return a detailed string representation of the body.
        """
        return (
            f"Body(shape={repr(self.shape)}, mass={self.mass}, position={repr(self.position)}, "
            f"velocity={repr(self.velocity)}, angular_velocity={self.angular_velocity}, is_static={self.is_static})"
        )

    def apply_force(self, force: Vec2, point: Vec2 = Vec2.zero()) -> None:
        """
        Apply a force to the body at a specific point.

        Args:
            force (Vec2): The force to apply.
            point (Vec2): The point to apply the force at.
        """
        self.force += force
        self.torque += (point - self.position).cross(force)

    def apply_impulse(self, impulse: Vec2, point: Vec2 = Vec2.zero()) -> None:
        """
        Apply an impulse to the body at a specific point.

        Args:
            impulse (Vec2): The impulse to apply.
            point (Vec2): The point to apply the impulse at.
        """
        self.velocity += impulse * self.inverse_mass
        self.angular_velocity += (point - self.position).cross(
            impulse
        ) * self.inverse_inertia

    def update(self, dt: float) -> None:
        """
        Update the body's position and velocity based on the applied forces and torques.

        Args:
            dt (float): The time step.
        """
        if self.is_static:
            return

        # Update velocity and angular velocity
        self.velocity += self.force * self.inverse_mass * dt
        self.angular_velocity += self.torque * self.inverse_inertia * dt

        # Update position and rotation
        self.position += self.velocity * dt
        self.transform.position = self.position
        self.transform.rotation += self.angular_velocity * dt

        # Reset forces and torques
        self.force = Vec2.zero()
        self.torque = 0.0

    def get_kinetic_energy(self) -> float:
        """
        Calculate the kinetic energy of the body.

        Returns:
            float: The kinetic energy of the body.
        """
        linear_energy = 0.5 * self.mass * self.velocity.magnitude_squared()
        rotational_energy = 0.5 * self.inertia * self.angular_velocity**2
        return linear_energy + rotational_energy

    def get_potential_energy(self, gravity: Vec2 = Vec2(0.0, -9.81)) -> float:
        """
        Calculate the potential energy of the body due to gravity.

        Args:
            gravity (Vec2): The gravitational acceleration vector.

        Returns:
            float: The potential energy of the body.
        """
        return self.mass * gravity.y * self.position.y

    def get_total_energy(self, gravity: Vec2 = Vec2(0.0, -9.81)) -> float:
        """
        Calculate the total energy of the body.

        Args:
            gravity (Vec2): The gravitational acceleration vector.

        Returns:
            float: The total energy of the body.
        """
        return self.get_kinetic_energy() + self.get_potential_energy(gravity)

    def get_aabb(self) -> "AABB":
        """
        Get the axis-aligned bounding box of the body.

        Returns:
            AABB: The axis-aligned bounding box.
        """
        return self.shape.get_aabb(body=self)

    def integrate_velocity(self, time_step: float) -> None:
        """
        Integrate the velocity of the body.

        Args:
            time_step (float): The time step for integration.
        """
        if not self.is_static:
            self.position += self.velocity * time_step
            self.orientation += self.angular_velocity * time_step

    def integrate_position(self, time_step: float) -> None:
        """
        Integrate the position of the body.

        Args:
            time_step (float): The time step for integration.
        """
        if not self.is_static:
            self.position += self.velocity * time_step

    def translate(self, translation: Vec2) -> None:
        """
        Translate the body by a given vector.

        Args:
            translation (Vec2): The translation vector.
        """
        self.position += translation
        self.transform.position = self.position

    def rotate(self, angle: float) -> None:
        """
        Rotate the body by a given angle.

        Args:
            angle (float): The angle to rotate by (in radians).
        """
        self.transform.rotation += angle

    def set_transform(self, transform: Transform) -> None:
        """
        Set the transformation of the body.

        Args:
            transform (Transform): The transformation to apply.
        """
        self.transform = transform
        self.position = transform.position
